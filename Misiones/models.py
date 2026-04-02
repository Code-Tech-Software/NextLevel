from django.db import models, transaction


# ========================
# CLASES
# ========================
class Clase(models.Model):
    nombre = models.CharField(max_length=50)
    grado = models.CharField(max_length=20)
    grupo = models.CharField(max_length=10)
    anio = models.IntegerField()

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
    pin = models.CharField(max_length=4,default="0000")
    xp_total = models.IntegerField(default=0)
    monedas = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# ========================
# NIVELES
# ========================
class Nivel(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="niveles")
    nombre = models.CharField(max_length=100)
    orden = models.IntegerField()
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
    )
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
    def __str__(self):
        return self.nombre

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

    def __str__(self):
        return f"{self.alumno} - {self.mision}"

    @property
    def calificacion_escala_10(self):
        return self.puntuacion / 10.0

    @property
    def monedas_obtenidas(self):
        return int((self.puntuacion / 100.0) * self.mision.monedas_recompensa)


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
# TIENDA Y RECOMPENSAS
# ========================
class ArticuloTienda(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    costo_monedas = models.IntegerField()
    imagen = models.ImageField(upload_to="tienda/", blank=True, null=True)

    # Si es algo físico o un permiso (ej. "Elegir la música de hoy"), el profe debe validarlo.
    # Si es solo digital (ej. "Avatar de Robot"), no requiere validación.
    requiere_validacion = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.costo_monedas} monedas"


class CompraAlumno(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="compras")
    articulo = models.ForeignKey(ArticuloTienda, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    # Si el artículo requiere validación, el profesor lo marcará como usado cuando se lo entregue al alumno
    entregado_usado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.alumno.nombre} compró {self.articulo.nombre}"