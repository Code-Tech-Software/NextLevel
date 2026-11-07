from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone


# ========================
# CONSTANTES DE JUEGO
# ========================
# Rangos del jugador según su nivel (nivel mínimo, nombre, emoji, color)
RANGOS = [
    (1, 'Novato', '🥚', 'bronce'),
    (3, 'Aprendiz', '🐣', 'bronce'),
    (5, 'Explorador', '🧭', 'plata'),
    (8, 'Inventor', '💡', 'plata'),
    (12, 'Ingeniero', '⚙️', 'oro'),
    (16, 'Maestro', '🧙', 'diamante'),
    (20, 'Leyenda', '👑', 'leyenda'),
]


def xp_para_nivel(nivel):
    """XP acumulada necesaria para llegar a `nivel`. Cada nivel pide 50 XP más que el anterior."""
    k = max(nivel - 1, 0)
    return 100 * k + 25 * k * (k - 1)


def calcular_nivel(xp):
    nivel = 1
    while xp >= xp_para_nivel(nivel + 1):
        nivel += 1
    return nivel


# ========================
# CLASES
# ========================
class Clase(models.Model):
    COLORES = [
        ('indigo', 'Índigo'),
        ('esmeralda', 'Esmeralda'),
        ('coral', 'Coral'),
        ('ambar', 'Ámbar'),
        ('cielo', 'Cielo'),
        ('uva', 'Uva'),
        ('rosa', 'Rosa'),
    ]
    nombre = models.CharField(max_length=50)
    grado = models.CharField(max_length=20)
    grupo = models.CharField(max_length=10)
    anio = models.IntegerField()
    descripcion = models.TextField(blank=True, default='')
    icono = models.CharField(max_length=10, default='🚀', help_text='Un emoji que represente la clase')
    ACCESOS = [
        ('abierto', 'Abierta siempre'),
        ('horario', 'Solo en horario de clase'),
        ('cerrado', 'Cerrada'),
    ]
    DIAS = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']

    color = models.CharField(max_length=20, choices=COLORES, default='indigo')
    activa = models.BooleanField(default=True, help_text='Las clases inactivas no aparecen en el lobby')
    # Cerrada (o fuera de horario) los alumnos entran con su PIN pero solo ven la información de su cuenta
    acceso = models.CharField(max_length=10, choices=ACCESOS, default='abierto')
    horario_dias = models.CharField(max_length=20, blank=True, default='',
                                    help_text='Días con clase: 0 = lunes … 6 = domingo, separados por comas')
    horario_inicio = models.TimeField(null=True, blank=True)
    horario_fin = models.TimeField(null=True, blank=True)
    # Secciones que el profe puede cerrar a un grupo sin cerrarle la plataforma (el mapa y las misiones siguen abiertos)
    tienda_abierta = models.BooleanField(default=True, help_text='Cerrada, sus alumnos no pueden comprar')
    arcade_abierto = models.BooleanField(default=True, help_text='Cerrado, sus alumnos no pueden jugar en el Arcade')

    SECCIONES = {
        'tienda': {'campo': 'tienda_abierta', 'nombre': 'Tienda', 'el': 'La', 'emoji': '🛒', 'icono': 'bi-shop',
                   'abierta': 'abierta', 'cerrada': 'cerrada',
                   'si_abre': 'Sus alumnos pueden comprar premios con sus monedas.',
                   'si_cierra': 'Sus alumnos no pueden comprar; sus monedas y su mochila se quedan guardadas.'},
        'arcade': {'campo': 'arcade_abierto', 'nombre': 'Arcade', 'el': 'El', 'emoji': '🕹️', 'icono': 'bi-controller',
                   'abierta': 'abierto', 'cerrada': 'cerrado',
                   'si_abre': 'Sus alumnos pueden jugar y ganar monedas extra.',
                   'si_cierra': 'Sus alumnos no pueden jugar ahí; los juegos de las misiones del mapa sí siguen.'},
    }

    def __str__(self):
        return f"{self.grado} {self.grupo} - {self.nombre}"

    def seccion_abierta(self, seccion):
        return getattr(self, self.SECCIONES[seccion]['campo'])

    @property
    def secciones(self):
        """La Tienda y el Arcade con su estado en este grupo (para los interruptores del panel)."""
        lista = []
        for clave, info in self.SECCIONES.items():
            abierta = getattr(self, info['campo'])
            lista.append({**info, 'clave': clave, 'abierta_ahora': abierta,
                          'estado': info['abierta'] if abierta else info['cerrada'],
                          'texto': info['si_abre'] if abierta else info['si_cierra']})
        return lista

    @property
    def secciones_cerradas(self):
        return [s for s in self.secciones if not s['abierta_ahora']]

    # --- Acceso de los alumnos ---
    @property
    def dias_horario(self):
        return sorted({int(d) for d in self.horario_dias.split(',') if d.strip().isdigit() and int(d) <= 6})

    @property
    def tiene_horario(self):
        return bool(self.dias_horario and self.horario_inicio and self.horario_fin
                    and self.horario_inicio < self.horario_fin)

    @property
    def texto_horario(self):
        if not self.tiene_horario:
            return ''
        dias = ', '.join(self.DIAS[d] for d in self.dias_horario)
        return f"{dias} · {self.horario_inicio:%H:%M} a {self.horario_fin:%H:%M}"

    def acceso_abierto(self, momento=None):
        if self.acceso == 'abierto':
            return True
        if self.acceso == 'cerrado' or not self.tiene_horario:
            return False
        ahora = timezone.localtime(momento)
        return ahora.weekday() in self.dias_horario and self.horario_inicio <= ahora.time() < self.horario_fin

    def proxima_apertura(self, momento=None):
        """Cuándo vuelve a abrir según el horario (None si está cerrada a mano o no tiene horario)."""
        if self.acceso != 'horario' or not self.tiene_horario:
            return None
        ahora = timezone.localtime(momento)
        for dias in range(8):
            fecha = ahora.date() + timedelta(days=dias)
            if fecha.weekday() in self.dias_horario:
                inicio = timezone.make_aware(datetime.combine(fecha, self.horario_inicio))
                if inicio > ahora:
                    return inicio
        return None

    def dia_de_clase_anterior(self, fecha):
        """El último día con clase antes de `fecha` (para que la racha cuente días de clase, no de calendario)."""
        if self.acceso != 'horario' or not self.dias_horario:
            return fecha - timedelta(days=1)
        for dias in range(1, 8):
            anterior = fecha - timedelta(days=dias)
            if anterior.weekday() in self.dias_horario:
                return anterior
        return fecha - timedelta(days=1)


# ========================
# ALUMNOS
# ========================
class AlumnoManager(models.Manager):
    """Los alumnos reales. El alumno de prueba (la «vista de alumno» del profe) no aparece en listas,
    rankings, estadísticas ni credenciales; para encontrarlo se usa Alumno.todos."""

    def get_queryset(self):
        return super().get_queryset().filter(es_prueba=False)


class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    clases = models.ManyToManyField(Clase, related_name='alumnos')
    avatar = models.ImageField(upload_to="avatares/", blank=True, null=True)
    pin = models.CharField(max_length=4, default="0000")
    xp_total = models.IntegerField(default=0)
    monedas = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    racha_actual = models.IntegerField(default=0)
    racha_maxima = models.IntegerField(default=0)
    ultima_actividad = models.DateField(null=True, blank=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    # El profe recorre la plataforma con este alumno: no pertenece a ninguna clase y nunca guarda progreso
    es_prueba = models.BooleanField(default=False, editable=False)

    objects = AlumnoManager()
    todos = models.Manager()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    @classmethod
    def de_prueba(cls):
        """El alumno con el que el profe entra a la «vista de alumno» (se crea la primera vez)."""
        alumno = cls.todos.filter(es_prueba=True).order_by('id').first()
        if not alumno:
            alumno = cls.todos.create(nombre='Profe', apellido='(vista de alumno)', pin='', activo=False,
                                      es_prueba=True)
        return alumno

    # --- Nivel del jugador (derivado de la XP) ---
    @property
    def nivel(self):
        return calcular_nivel(self.xp_total)

    @property
    def xp_nivel_actual(self):
        """XP ganada dentro del nivel actual."""
        return self.xp_total - xp_para_nivel(self.nivel)

    @property
    def xp_siguiente_nivel(self):
        """XP que pide el nivel actual para subir al siguiente."""
        return xp_para_nivel(self.nivel + 1) - xp_para_nivel(self.nivel)

    @property
    def xp_faltante(self):
        return xp_para_nivel(self.nivel + 1) - self.xp_total

    @property
    def progreso_nivel(self):
        return int(self.xp_nivel_actual * 100 / self.xp_siguiente_nivel)

    @property
    def rango(self):
        actual = RANGOS[0]
        for rango in RANGOS:
            if self.nivel >= rango[0]:
                actual = rango
        return {'nombre': actual[1], 'emoji': actual[2], 'color': actual[3]}


# ========================
# MUNDOS
# ========================
class Mundo(models.Model):
    TEMAS = [
        ('bosque', '🌳 Bosque Encantado'),
        ('oceano', '🌊 Océano Profundo'),
        ('desierto', '🏜️ Desierto Dorado'),
        ('volcan', '🌋 Volcán de Fuego'),
        ('hielo', '❄️ Reino de Hielo'),
        ('espacio', '🚀 Espacio Exterior'),
        ('ciudad', '🌆 Ciudad Neón'),
        ('dulces', '🍭 Tierra de Dulces'),
        ('abismo', '🦑 Abismo Profundo'),
        ('marte', '🛰️ Planeta Rojo'),
        ('tormenta', '⛈️ Tormenta Eléctrica'),
        ('futuro', '🔮 Laboratorio del Futuro'),
        ('cyber', '🛡️ Cuartel Ciber'),
    ]
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="mundos")
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')
    tema = models.CharField(max_length=20, choices=TEMAS, default='bosque')
    orden = models.IntegerField(default=1)

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return f"{self.clase} - {self.nombre}"


# ========================
# NIVELES
# ========================
class Nivel(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="niveles")
    mundo = models.ForeignKey(Mundo, on_delete=models.CASCADE, related_name="niveles", null=True, blank=True)
    nombre = models.CharField(max_length=100)
    orden = models.IntegerField()
    recompensa_cofre = models.IntegerField(
        default=20, help_text='Monedas base del cofre que se abre al completar todas las misiones del nivel'
    )

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return f"{self.clase} - {self.nombre}"


# ========================
# MISIONES
# ========================
class Mision(models.Model):
    TIPO_MISION = (
        ("arduino", "Arduino"),
        ("cuestionario", "Cuestionario"),
        ("link", "Link"),
        ("video", "Video"),
        ("evidencia", "Evidencia con foto"),
        ("texto", "Respuesta escrita"),
        ("presencial", "Actividad en clase"),
        ("juego", "Minijuego"),
    )
    # Tipos que se califican solos al enviarse (no pasan por revisión del profesor)
    TIPOS_AUTOMATICOS = ('cuestionario', 'video', 'juego')

    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="misiones")
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, related_name="misiones")
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_MISION)
    imagen = models.ImageField(upload_to="misiones/", blank=True, null=True)
    codigo = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    xp_recompensa = models.IntegerField(default=50)
    monedas_recompensa = models.IntegerField(default=10)
    orden = models.IntegerField(default=1)
    es_jefe = models.BooleanField(default=False, help_text='Batalla final: se ve especial en el mapa')
    activa = models.BooleanField(default=True, help_text='Las misiones inactivas no aparecen a los alumnos')
    fecha_limite = models.DateField(null=True, blank=True)
    juego = models.ForeignKey('Juego', on_delete=models.SET_NULL, null=True, blank=True, related_name='misiones',
                              help_text='Solo para misiones de tipo minijuego')

    def __str__(self):
        return self.nombre

    @property
    def es_automatica(self):
        return self.tipo in self.TIPOS_AUTOMATICOS


# ========================
# PROGRESO MISION
# ========================
class ProgresoMision(models.Model):
    ESTADO = (
        ("pendiente", "Pendiente"),
        ("aprobado", "Aprobado"),
        ("rechazado", "Rechazado"),
    )
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    mision = models.ForeignKey(Mision, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO, default="pendiente")
    puntuacion = models.IntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    revisado = models.BooleanField(default=False)
    evidencia = models.ImageField(upload_to="evidencias/", blank=True, null=True)
    respuesta_texto = models.TextField(blank=True, default='')
    comentario_profesor = models.TextField(blank=True, default='')
    fecha_revision = models.DateTimeField(null=True, blank=True)
    intentos = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.alumno} - {self.mision}"

    @property
    def calificacion_escala_10(self):
        return self.puntuacion / 10.0

    @property
    def monedas_obtenidas(self):
        return int((self.puntuacion / 100.0) * self.mision.monedas_recompensa)

    @property
    def estrellas(self):
        if self.estado != 'aprobado':
            return 0
        if self.puntuacion >= 90:
            return 3
        if self.puntuacion >= 70:
            return 2
        return 1


# ========================
# PREGUNTAS DEL CUESTIONARIO
# ========================
class Pregunta(models.Model):
    mision = models.ForeignKey(Mision, on_delete=models.CASCADE, related_name="preguntas")
    texto = models.TextField(help_text="Escribe la pregunta aquí")
    orden = models.IntegerField(default=1)
    puntos = models.IntegerField(default=10, help_text="Puntos que otorga esta pregunta")

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.mision.nombre} - {self.texto[:50]}"


# ========================
# OPCIONES DE RESPUESTA
# ========================
class OpcionRespuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name="opciones")
    texto = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto


# ========================
# RESPUESTAS DEL ALUMNO
# ========================
class RespuestaAlumno(models.Model):
    progreso = models.ForeignKey(ProgresoMision, on_delete=models.CASCADE, related_name="respuestas_detalladas")
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_seleccionada = models.ForeignKey(OpcionRespuesta, on_delete=models.CASCADE, null=True, blank=True)
    respuesta_texto = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.progreso.alumno} - {self.pregunta}"


# ========================
# COFRES DE NIVEL
# ========================
class CofreAbierto(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="cofres")
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, related_name="cofres")
    monedas = models.IntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('alumno', 'nivel')

    def __str__(self):
        return f"{self.alumno} abrió el cofre de {self.nivel}"


# ========================
# TIENDA Y RECOMPENSAS
# ========================
class ArticuloTienda(models.Model):
    TIPO_CHOICES = [
        ('avatar', 'Avatar para el perfil'),
        ('permiso', 'Permiso / Privilegio en clase'),
        ('fisico', 'Recompensa Física'),
        ('otro', 'Otro Digital'),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    costo_monedas = models.IntegerField()
    imagen = models.ImageField(upload_to="tienda/", blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='fisico')
    requiere_validacion = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(
        null=True, blank=True, help_text='Piezas disponibles. Déjalo vacío si es ilimitado (ej. artículos digitales)'
    )
    limite_por_alumno = models.PositiveIntegerField(
        null=True, blank=True, help_text='Máximo de veces que un mismo alumno puede comprarlo. Vacío = sin límite'
    )
    nivel_requerido = models.PositiveIntegerField(default=1, help_text='Nivel de jugador mínimo para comprarlo')
    activo = models.BooleanField(default=True, help_text='Los artículos inactivos no se muestran en la tienda')
    destacado = models.BooleanField(default=False, help_text='Aparece en la vitrina principal de la tienda')
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre} - {self.costo_monedas} monedas"

    @property
    def stock_ilimitado(self):
        return self.stock is None

    @property
    def agotado(self):
        return self.stock is not None and self.stock <= 0

    @property
    def stock_bajo(self):
        return self.stock is not None and 0 < self.stock <= 3


class CompraAlumno(models.Model):
    ESTADOS = [
        ('pendiente', 'Por entregar'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="compras")
    articulo = models.ForeignKey(ArticuloTienda, on_delete=models.CASCADE, related_name="compras")
    fecha_compra = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    costo_pagado = models.IntegerField(default=0)
    fecha_entrega = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.alumno.nombre} compró {self.articulo.nombre}"


# ========================
# HISTORIAL DE MOVIMIENTOS (monedas y XP)
# ========================
class Movimiento(models.Model):
    TIPOS = [
        ('mision', 'Misión'),
        ('cofre', 'Cofre'),
        ('diaria', 'Misión diaria'),
        ('logro', 'Logro'),
        ('nivel', 'Subida de nivel'),
        ('compra', 'Compra'),
        ('reembolso', 'Reembolso'),
        ('ajuste', 'Ajuste del profesor'),
        ('conducta', 'Comportamiento'),
        ('meta', 'Meta del grupo'),
        ('juego', 'Minijuego del Arcade'),
    ]
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="movimientos")
    clase = models.ForeignKey(Clase, on_delete=models.SET_NULL, null=True, blank=True, related_name="movimientos")
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.CharField(max_length=200)
    monedas = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.alumno} · {self.descripcion}"


# ========================
# NOTIFICACIONES DEL ALUMNO
# ========================
class Notificacion(models.Model):
    TIPOS = [
        ('aprobada', 'Misión aprobada'),
        ('rechazada', 'Misión rechazada'),
        ('logro', 'Logro desbloqueado'),
        ('nivel', 'Subida de nivel'),
        ('cofre', 'Cofre'),
        ('diaria', 'Misión diaria'),
        ('tienda', 'Tienda'),
        ('monedas', 'Monedas'),
        ('sistema', 'Sistema'),
    ]
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="notificaciones")
    tipo = models.CharField(max_length=20, choices=TIPOS, default='sistema')
    titulo = models.CharField(max_length=120)
    mensaje = models.CharField(max_length=255, blank=True, default='')
    icono = models.CharField(max_length=10, default='🔔')
    celebrar = models.BooleanField(default=False, help_text='Se muestra como ventana de celebración')
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.alumno} · {self.titulo}"


# ========================
# LOGROS / INSIGNIAS
# ========================
class Logro(models.Model):
    CONDICIONES = [
        ('misiones', 'Misiones completadas'),
        ('xp', 'XP total'),
        ('monedas', 'Monedas ganadas en total'),
        ('racha', 'Días seguidos de racha'),
        ('perfectos', 'Cuestionarios con 10'),
        ('compras', 'Compras en la tienda'),
        ('mundos', 'Mundos completados'),
        ('nivel', 'Nivel de jugador'),
        ('diarias', 'Misiones diarias completadas'),
        ('jefes', 'Jefes derrotados'),
        ('juegos', 'Partidas de minijuegos'),
        ('ppm', 'Récord de palabras por minuto'),
        ('manual', 'Lo otorga el profesor'),
    ]
    RAREZAS = [
        ('comun', 'Común'),
        ('raro', 'Raro'),
        ('epico', 'Épico'),
        ('legendario', 'Legendario'),
    ]
    nombre = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=200)
    icono = models.CharField(max_length=10, default='🏅')
    condicion = models.CharField(max_length=20, choices=CONDICIONES, default='misiones')
    valor = models.IntegerField(default=1, help_text='Cantidad necesaria para desbloquearlo')
    rareza = models.CharField(max_length=20, choices=RAREZAS, default='comun')
    recompensa_monedas = models.IntegerField(default=0)
    recompensa_xp = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=1)

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return f"{self.icono} {self.nombre}"


class LogroAlumno(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="logros")
    logro = models.ForeignKey(Logro, on_delete=models.CASCADE, related_name="alumnos")
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('alumno', 'logro')
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.alumno} · {self.logro}"


class LogroRetirado(models.Model):
    """Logro automático que el profe le quitó a un alumno: el sistema no se lo vuelve a dar solo."""
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="logros_retirados")
    logro = models.ForeignKey(Logro, on_delete=models.CASCADE, related_name="retirados")
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('alumno', 'logro')

    def __str__(self):
        return f"{self.alumno} · sin {self.logro}"


# ========================
# MISIONES DEL DÍA
# ========================
class MisionDiaria(models.Model):
    OBJETIVOS = [
        ('login', 'Entrar a la plataforma'),
        ('misiones', 'Completar misiones'),
        ('cuestionarios', 'Completar cuestionarios'),
        ('perfecto', 'Sacar 10 en un cuestionario'),
        ('xp', 'Ganar XP'),
        ('evidencias', 'Enviar trabajos para revisión'),
        ('tienda', 'Visitar la tienda'),
        ('juegos', 'Jugar minijuegos'),
    ]
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True, default='')
    icono = models.CharField(max_length=10, default='⭐')
    objetivo = models.CharField(max_length=20, choices=OBJETIVOS)
    meta = models.PositiveIntegerField(default=1, help_text='Cuántas veces hay que lograr el objetivo en el día')
    recompensa_monedas = models.IntegerField(default=10)
    recompensa_xp = models.IntegerField(default=10)
    clase = models.ForeignKey(
        Clase, on_delete=models.CASCADE, null=True, blank=True, related_name='misiones_diarias',
        help_text='Déjalo vacío para que aplique a todas las clases'
    )
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.titulo


class ProgresoDiario(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="progresos_diarios")
    mision = models.ForeignKey(MisionDiaria, on_delete=models.CASCADE, related_name="progresos")
    fecha = models.DateField()
    progreso = models.IntegerField(default=0)
    reclamada = models.BooleanField(default=False)

    class Meta:
        unique_together = ('alumno', 'mision', 'fecha')

    def __str__(self):
        return f"{self.alumno} · {self.mision} · {self.fecha}"

    @property
    def completada(self):
        return self.progreso >= self.mision.meta


# ========================
# MODO CLASE: COMPORTAMIENTOS
# ========================
class Comportamiento(models.Model):
    """Botones del modo clase (ej. 🙋 Participación +5). Negativos = solo restan monedas."""
    nombre = models.CharField(max_length=60)
    icono = models.CharField(max_length=10, default='⭐')
    monedas = models.IntegerField(default=5, help_text='Usa un número negativo para restar (ej. -3)')
    xp = models.PositiveIntegerField(default=0, help_text='Solo para comportamientos positivos')
    orden = models.IntegerField(default=1)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return f"{self.icono} {self.nombre}"

    @property
    def positivo(self):
        return self.monedas >= 0


class RegistroConducta(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="conductas")
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="conductas")
    comportamiento = models.ForeignKey(Comportamiento, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=60)
    icono = models.CharField(max_length=10, default='⭐')
    monedas = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.alumno} · {self.nombre}"

    @property
    def positivo(self):
        return self.monedas >= 0


# ========================
# EQUIPOS / CASAS
# ========================
class Equipo(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="equipos")
    nombre = models.CharField(max_length=60)
    emoji = models.CharField(max_length=10, default='🛡️')
    color = models.CharField(max_length=20, choices=Clase.COLORES, default='indigo')
    miembros = models.ManyToManyField(Alumno, related_name="equipos", blank=True)
    orden = models.IntegerField(default=1)

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return f"{self.emoji} {self.nombre}"


class PuntosEquipo(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name="puntos")
    alumno = models.ForeignKey(Alumno, on_delete=models.SET_NULL, null=True, blank=True)
    puntos = models.IntegerField()
    motivo = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.equipo} {self.puntos:+d}"


# ========================
# METAS DEL GRUPO
# ========================
class MetaGrupo(models.Model):
    TIPOS = [
        ('misiones', 'Misiones completadas entre todos'),
        ('xp', 'XP ganada entre todos'),
        ('conducta', 'Comportamientos positivos'),
        ('manual', 'Avance manual (tú lo marcas)'),
    ]
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="metas")
    titulo = models.CharField(max_length=100, help_text='Ej. ¡Viernes de película!')
    descripcion = models.CharField(max_length=200, blank=True, default='')
    icono = models.CharField(max_length=10, default='🎯')
    tipo = models.CharField(max_length=20, choices=TIPOS, default='misiones')
    objetivo = models.PositiveIntegerField(default=30, help_text='Cantidad que el grupo debe alcanzar')
    progreso_manual = models.PositiveIntegerField(default=0)
    recompensa = models.CharField(max_length=120, blank=True, default='', help_text='Ej. 🍿 Película el viernes')
    monedas_recompensa = models.PositiveIntegerField(default=0, help_text='Monedas para cada alumno al cumplirla (opcional)')
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_limite = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    completada_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-activa', '-fecha_inicio']

    def __str__(self):
        return f"{self.icono} {self.titulo}"


# ========================
# MINIJUEGOS
# ========================
class Juego(models.Model):
    """Un minijuego configurado por el profe. Se puede usar como misión del mapa, en el Arcade o en ambos."""
    PLANTILLAS = [
        ('meteoros', 'Mecanografía de meteoros'),
        ('teclado', 'Teclado misterioso'),
        ('clasifica', 'Detective digital'),
        ('robot', 'Robot programador'),
        ('atajos', 'Atajos ninja'),
        ('mensaje', 'Mensaje secreto'),
        ('rutas', 'Explorador de rutas'),
        ('formato', 'Copia el formato'),
    ]
    DESBLOQUEOS = [
        ('libre', 'Siempre disponible'),
        ('mision', 'Al completar su misión del mapa'),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True, default='')
    icono = models.CharField(max_length=10, default='🎮')
    plantilla = models.CharField(max_length=20, choices=PLANTILLAS, default='meteoros')
    configuracion = models.JSONField(default=dict, blank=True)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, null=True, blank=True, related_name='juegos',
                              help_text='Vacío = aparece en el Arcade de todas las clases')
    en_arcade = models.BooleanField(default=True)
    desbloqueo = models.CharField(max_length=10, choices=DESBLOQUEOS, default='libre')
    monedas_arcade = models.PositiveIntegerField(
        default=5, help_text='Monedas por la primera partida del día con al menos una estrella'
    )
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado', '-id']

    def __str__(self):
        return f"{self.icono} {self.nombre}"


class PartidaJuego(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='partidas')
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='partidas')
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='partidas')
    mision = models.ForeignKey(Mision, on_delete=models.SET_NULL, null=True, blank=True, related_name='partidas')
    inicio = models.DateTimeField(default=timezone.now)
    terminada = models.BooleanField(default=False)
    puntaje = models.PositiveIntegerField(default=0)
    calificacion = models.PositiveSmallIntegerField(default=0, help_text='0 a 100')
    estrellas = models.PositiveSmallIntegerField(default=0)
    aciertos = models.PositiveIntegerField(default=0)
    errores = models.PositiveIntegerField(default=0)
    precision = models.PositiveSmallIntegerField(default=0, help_text='Porcentaje de teclas correctas')
    ppm = models.PositiveSmallIntegerField(default=0, help_text='Palabras por minuto')
    duracion = models.PositiveIntegerField(default=0, help_text='Segundos jugados')
    monedas = models.IntegerField(default=0)

    class Meta:
        ordering = ['-inicio']

    def __str__(self):
        return f"{self.alumno} · {self.juego} · {self.puntaje}"


# ========================
# LLAVERO DE APPS (accesos a plataformas de terceros)
# ========================
class AppExterna(models.Model):
    """Una app o plataforma de terceros que se usa en clase (Pinion, Tinkercad, MakeCode…).

    Cada etiqueta en blanco significa que esa app no usa ese dato: p. ej. MakeCode no pide usuario, y en Tinkercad el
    código de clase es el mismo para todo el grupo pero el apodo es de cada alumno.
    """
    nombre = models.CharField(max_length=80)
    icono = models.CharField(max_length=10, default='🔑')
    url = models.URLField(blank=True, default='', help_text='Dónde se entra a la app')
    instrucciones = models.TextField(blank=True, default='', help_text='Cómo entrar, paso a paso')
    etiqueta_codigo = models.CharField(max_length=40, blank=True, default='',
                                       help_text='Dato que comparte toda la clase, p. ej. «Código de clase»')
    etiqueta_usuario = models.CharField(max_length=40, blank=True, default='Usuario')
    etiqueta_contrasena = models.CharField(max_length=40, blank=True, default='Contraseña')
    clases = models.ManyToManyField(Clase, through='AppClase', related_name='apps_externas', blank=True)
    activa = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre', 'id']
        verbose_name = 'app de clase'
        verbose_name_plural = 'apps de clase'

    def __str__(self):
        return f"{self.icono} {self.nombre}"

    @property
    def es_personal(self):
        """¿Cada alumno tiene su propio usuario o contraseña?"""
        return bool(self.etiqueta_usuario or self.etiqueta_contrasena)


class AppClase(models.Model):
    """Una app usada en una clase, con el dato que comparte todo el grupo (código de clase) y una nota."""
    app = models.ForeignKey(AppExterna, on_delete=models.CASCADE, related_name='en_clases')
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='apps_de_clase')
    codigo = models.CharField(max_length=120, blank=True, default='')
    nota = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        unique_together = [('app', 'clase')]

    def __str__(self):
        return f"{self.app} · {self.clase}"


class AccesoAlumno(models.Model):
    """El usuario y la contraseña de un alumno en una app de terceros. Solo los ven el alumno y el profe."""
    app = models.ForeignKey(AppExterna, on_delete=models.CASCADE, related_name='accesos')
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='accesos_apps')
    usuario = models.CharField(max_length=150, blank=True, default='')
    contrasena = models.CharField(max_length=150, blank=True, default='')
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('app', 'alumno')]

    def __str__(self):
        return f"{self.alumno} · {self.app}"
