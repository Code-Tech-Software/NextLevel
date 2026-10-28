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
    color = models.CharField(max_length=20, choices=COLORES, default='indigo')
    activa = models.BooleanField(default=True, help_text='Las clases inactivas no aparecen en el lobby')

    def __str__(self):
        return f"{self.grado} {self.grupo} - {self.nombre}"


# ========================
# ALUMNOS
# ========================
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

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

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
