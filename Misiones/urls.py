from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from . import views_clase as aula
from . import views_profesor as profe

urlpatterns = [
    # ===== Alumnos =====
    path('seleccionar-clase/', views.seleccionar_clase, name='seleccionar_clase'),
    path('clase/<int:clase_id>/', views.lista_alumnos, name='lista_alumnos'),
    path('clase/<int:clase_id>/alumno/<int:alumno_id>/ingresar/', views.ingresar_pin, name='ingresar_pin'),
    path('clase/<int:clase_id>/dashboard/', views.dashboard_alumno, name='dashboard_alumno'),
    path('clase/<int:clase_id>/mundo/<int:mundo_id>/', views.ver_mundo, name='ver_mundo'),
    path('clase/<int:clase_id>/mision/<int:mision_id>/', views.ver_mision, name='ver_mision'),
    path('clase/<int:clase_id>/mision/<int:mision_id>/completar/', views.marcar_completada, name='marcar_completada'),
    path('clase/<int:clase_id>/cofre/<int:nivel_id>/', views.abrir_cofre, name='abrir_cofre'),
    path('clase/<int:clase_id>/diaria/<int:diaria_id>/reclamar/', views.reclamar_diaria, name='reclamar_diaria'),
    path('clase/<int:clase_id>/notificaciones/leer/', views.leer_notificaciones, name='leer_notificaciones'),
    path('clase/<int:clase_id>/tienda/', views.tienda_alumno, name='tienda_alumno'),
    path('clase/<int:clase_id>/tienda/comprar/<int:articulo_id>/', views.comprar_articulo, name='comprar_articulo'),
    path('clase/<int:clase_id>/progreso/', views.mi_progreso, name='mi_progreso'),
    path('clase/<int:clase_id>/avatar/<int:compra_id>/', views.equipar_avatar, name='equipar_avatar'),
    path('clase/<int:clase_id>/ranking/', views.ranking, name='ranking'),
    path('salir/', views.salir_alumno, name='salir_alumno'),

    # ===== Acceso del profesor =====
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # ===== Panel del profesor =====
    path('profesor/dashboard/', profe.dashboard_profesor, name='dashboard_profesor'),

    path('profesor/clases/', profe.clases_lista, name='clases_lista'),
    path('forja/clase/nueva/', profe.alta_clase, name='alta_clase'),
    path('profesor/clases/<int:pk>/editar/', profe.alta_clase, name='editar_clase'),
    path('profesor/clases/<int:clase_id>/', profe.clase_detalle, name='clase_detalle'),
    path('profesor/clases/<int:clase_id>/proyector/', profe.proyector, name='proyector'),

    path('profesor/mundos/nuevo/', profe.mundo_form, name='alta_mundo'),
    path('profesor/mundos/<int:pk>/editar/', profe.mundo_form, name='editar_mundo'),
    path('forja/nivel/nuevo/', profe.alta_nivel, name='alta_nivel'),
    path('profesor/niveles/<int:pk>/editar/', profe.alta_nivel, name='editar_nivel'),
    path('forja/mision/nueva/', profe.alta_mision, name='alta_mision'),
    path('profesor/misiones/<int:pk>/editar/', profe.alta_mision, name='editar_mision'),
    path('profesor/misiones/<int:pk>/duplicar/', profe.duplicar_mision, name='duplicar_mision'),
    path('profesor/misiones/<int:mision_id>/calificar/', profe.calificar_mision, name='calificar_mision'),

    path('profesor/revisiones/', profe.revisiones, name='revisiones'),
    path('clase/<int:clase_id>/panel-profesor/', profe.panel_profesor, name='panel_profesor'),
    path('progreso/<int:progreso_id>/aprobar/', profe.aprobar_mision, name='aprobar_mision'),
    path('progreso/<int:progreso_id>/rechazar/', profe.rechazar_mision, name='rechazar_mision'),
    path('profesor/calificaciones/', profe.calificaciones_inicio, name='calificaciones'),
    path('clase/<int:clase_id>/matriz/', profe.matriz_calificaciones, name='matriz_calificaciones'),
    path('clase/<int:clase_id>/matriz/exportar-excel/', profe.exportar_matriz_excel, name='exportar_matriz_excel'),

    path('profesor/alumnos/', profe.alumnos_lista, name='alumnos_lista'),
    path('forja/alumno/nuevo/', profe.alta_alumno, name='alta_alumno'),
    path('profesor/alumnos/masivo/', profe.alta_masiva, name='alta_masiva'),
    path('profesor/alumnos/credenciales/', profe.credenciales, name='credenciales'),
    path('profesor/alumnos/<int:pk>/', profe.alumno_detalle, name='alumno_detalle'),
    path('profesor/alumnos/<int:pk>/editar/', profe.alta_alumno, name='editar_alumno'),
    path('profesor/alumnos/<int:pk>/ajuste/', profe.alumno_ajuste, name='alumno_ajuste'),

    path('profesor/tienda/', profe.tienda_admin, name='tienda_admin'),
    path('forja/tienda/nuevo/', profe.alta_articulo, name='alta_articulo'),
    path('profesor/tienda/<int:pk>/editar/', profe.alta_articulo, name='editar_articulo'),
    path('profesor/tienda/<int:pk>/stock/', profe.ajustar_stock, name='ajustar_stock'),
    path('profesor/pedidos/', profe.pedidos, name='pedidos'),
    path('profesor/tienda/entregar/<int:compra_id>/', profe.entregar_articulo_tienda, name='entregar_articulo_tienda'),
    path('profesor/tienda/cancelar/<int:compra_id>/', profe.cancelar_compra, name='cancelar_compra'),

    path('economia-alumnos/', profe.gestionar_monedas, name='gestionar_monedas'),
    path('api/actualizar-monedas/', profe.api_actualizar_monedas, name='api_actualizar_monedas'),
    path('api/monedas-masivo/', profe.api_monedas_masivo, name='api_monedas_masivo'),
    path('profesor/actividad/', profe.actividad, name='actividad'),

    path('profesor/diarias/', profe.diarias_lista, name='diarias_lista'),
    path('profesor/diarias/nueva/', profe.diaria_form, name='alta_diaria'),
    path('profesor/diarias/<int:pk>/editar/', profe.diaria_form, name='editar_diaria'),
    path('profesor/logros/', profe.logros_lista, name='logros_lista'),
    path('profesor/logros/nuevo/', profe.logro_form, name='alta_logro'),
    path('profesor/logros/<int:pk>/editar/', profe.logro_form, name='editar_logro'),
    path('profesor/logros/otorgar/', profe.otorgar_logro, name='otorgar_logro'),

    # ===== Modo clase, equipos y metas =====
    path('profesor/modo-clase/', aula.modo_clase, name='modo_clase_inicio'),
    path('profesor/modo-clase/<int:clase_id>/', aula.modo_clase, name='modo_clase'),
    path('api/modo-clase/conducta/', aula.api_conducta, name='api_conducta'),
    path('api/modo-clase/deshacer/', aula.api_deshacer_conducta, name='api_deshacer_conducta'),
    path('api/modo-clase/puntos-equipo/', aula.api_puntos_equipo, name='api_puntos_equipo'),
    path('api/modo-clase/meta/', aula.api_meta_manual, name='api_meta_manual'),
    path('profesor/comportamientos/', aula.comportamientos_lista, name='comportamientos_lista'),
    path('profesor/comportamientos/nuevo/', aula.comportamiento_form, name='alta_comportamiento'),
    path('profesor/comportamientos/<int:pk>/editar/', aula.comportamiento_form, name='editar_comportamiento'),
    path('profesor/equipos/', aula.equipos_clase, name='equipos_lista'),
    path('profesor/equipos/clase/<int:clase_id>/', aula.equipos_clase, name='equipos_clase'),
    path('profesor/equipos/nuevo/', aula.equipo_form, name='alta_equipo'),
    path('profesor/equipos/<int:pk>/editar/', aula.equipo_form, name='editar_equipo'),
    path('profesor/equipos/clase/<int:clase_id>/casas/', aula.crear_casas, name='crear_casas'),
    path('profesor/equipos/clase/<int:clase_id>/repartir/', aula.repartir_equipos, name='repartir_equipos'),
    path('profesor/equipos/clase/<int:clase_id>/reiniciar/', aula.reiniciar_equipos, name='reiniciar_equipos'),
    path('api/equipos/asignar/', aula.api_asignar_equipo, name='api_asignar_equipo'),
    path('profesor/metas/', aula.metas_lista, name='metas_lista'),
    path('profesor/metas/nueva/', aula.meta_form, name='alta_meta'),
    path('profesor/metas/<int:pk>/editar/', aula.meta_form, name='editar_meta'),
    path('profesor/metas/<int:pk>/reiniciar/', aula.reiniciar_meta, name='reiniciar_meta'),

    path('profesor/eliminar/<str:modelo>/<int:pk>/', profe.eliminar, name='eliminar'),
    path('profesor/alternar/<str:modelo>/<int:pk>/', profe.alternar_activo, name='alternar_activo'),
    path('ajax/cargar-niveles/', profe.cargar_niveles, name='ajax_cargar_niveles'),
]
