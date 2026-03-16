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
    )
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="misiones")
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, related_name="misiones")
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_MISION)
    imagen = models.ImageField(upload_to="misiones/", blank=True, null=True)
    codigo = models.TextField(blank=True, null=True)
    link_formulario = models.URLField(blank=True, null=True)
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
