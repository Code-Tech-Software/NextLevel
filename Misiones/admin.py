from django.contrib import admin

from Misiones.models import *

admin.site.register(Clase)
admin.site.register(Alumno)
admin.site.register(Nivel)
admin.site.register(Mision)
admin.site.register(ProgresoMision)
admin.site.register(ArticuloTienda)

class OpcionRespuestaInline(admin.TabularInline):
    model = OpcionRespuesta
    extra = 4 # Te mostrará 4 campos vacíos por defecto para las opciones (ej. A, B, C, D)

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'mision', 'orden', 'puntos')
    list_filter = ('mision',)
    inlines = [OpcionRespuestaInline]
