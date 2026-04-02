from django.urls import path
from . import views

urlpatterns = [
    path('seleccionar-clase/', views.seleccionar_clase, name='seleccionar_clase'),
    path('clase/<int:clase_id>/', views.lista_alumnos, name='lista_alumnos'),
    path('clase/<int:clase_id>/alumno/<int:alumno_id>/ingresar/', views.ingresar_pin, name='ingresar_pin'),
    path('clase/<int:clase_id>/dashboard/', views.dashboard_alumno, name='dashboard_alumno'),
    path('clase/<int:clase_id>/mision/<int:mision_id>/', views.ver_mision, name='ver_mision'),
    path('clase/<int:clase_id>/mision/<int:mision_id>/completar/', views.marcar_completada, name='marcar_completada'),
    path('salir/', views.salir_alumno, name='salir_alumno'),
    path('clase/<int:clase_id>/panel-profesor/', views.panel_profesor, name='panel_profesor'),
    path('progreso/<int:progreso_id>/aprobar/', views.aprobar_mision, name='aprobar_mision'),
    path('progreso/<int:progreso_id>/rechazar/', views.rechazar_mision, name='rechazar_mision'),
    # ... Tienda ...
    path('clase/<int:clase_id>/tienda/', views.tienda_alumno, name='tienda_alumno'),
    path('clase/<int:clase_id>/tienda/comprar/<int:articulo_id>/', views.comprar_articulo, name='comprar_articulo'),

    path('profesor/dashboard/', views.dashboard_profesor, name='dashboard_profesor'),
    path('profesor/tienda/entregar/<int:compra_id>/', views.entregar_articulo_tienda, name='entregar_articulo_tienda'),

    path('clase/<int:clase_id>/matriz/', views.matriz_calificaciones, name='matriz_calificaciones'),

    path('clase/<int:clase_id>/progreso/', views.mi_progreso, name='mi_progreso'),
]
