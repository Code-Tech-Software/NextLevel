from django.contrib import admin

from Misiones.models import (
    Alumno, ArticuloTienda, Clase, CofreAbierto, CompraAlumno, Comportamiento, Equipo, Logro, LogroAlumno, MetaGrupo,
    Mision, MisionDiaria, Movimiento, Mundo, Nivel, Notificacion, OpcionRespuesta, Pregunta, ProgresoDiario,
    ProgresoMision, PuntosEquipo, RegistroConducta,
)

admin.site.register(Clase)
admin.site.register(Mundo)
admin.site.register(Nivel)
admin.site.register(CofreAbierto)
admin.site.register(MisionDiaria)
admin.site.register(ProgresoDiario)
admin.site.register(LogroAlumno)
admin.site.register(Comportamiento)
admin.site.register(RegistroConducta)
admin.site.register(Equipo)
admin.site.register(PuntosEquipo)
admin.site.register(MetaGrupo)


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'xp_total', 'monedas', 'racha_actual', 'activo')
    list_filter = ('activo', 'clases')
    search_fields = ('nombre', 'apellido')


@admin.register(Mision)
class MisionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'clase', 'nivel', 'tipo', 'orden', 'es_jefe', 'activa')
    list_filter = ('clase', 'tipo', 'activa')


@admin.register(ProgresoMision)
class ProgresoMisionAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'mision', 'estado', 'puntuacion', 'fecha')
    list_filter = ('estado',)


@admin.register(ArticuloTienda)
class ArticuloTiendaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'costo_monedas', 'stock', 'activo')
    list_filter = ('tipo', 'activo')


@admin.register(CompraAlumno)
class CompraAlumnoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'articulo', 'estado', 'costo_pagado', 'fecha_compra')
    list_filter = ('estado',)


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'tipo', 'descripcion', 'monedas', 'xp', 'fecha')
    list_filter = ('tipo',)


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'titulo', 'tipo', 'leida', 'fecha')
    list_filter = ('tipo', 'leida')


@admin.register(Logro)
class LogroAdmin(admin.ModelAdmin):
    list_display = ('icono', 'nombre', 'condicion', 'valor', 'rareza', 'activo')


class OpcionRespuestaInline(admin.TabularInline):
    model = OpcionRespuesta
    extra = 4  # Te mostrará 4 campos vacíos por defecto para las opciones (ej. A, B, C, D)


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'mision', 'orden', 'puntos')
    list_filter = ('mision',)
    inlines = [OpcionRespuestaInline]
