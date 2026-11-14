"""«Mis proyectos»: el alumno guarda los archivos de sus prácticas en su cuenta y el profe los ve por grupo."""
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from . import gamificacion as juego
from . import proyectos
from .almacen import ArchivoNoDisponible
from .models import Clase, ProyectoAlumno, VersionProyecto
from .views import _es_ajax, _volver, alumno_requerido
from .views_profesor import _siguiente

registro = logging.getLogger(__name__)

CERRADO = '🔒 Tu profe cerró «Mis proyectos» por ahora: no puedes subir archivos, pero sí descargar los que ya tienes.'


def _no_se_pudo_descargar(request, version, error):
    """Mensaje claro cuando el archivo no llega (y la pista para el profe en los registros de Railway)."""
    if isinstance(error, ArchivoNoDisponible) and error.estado in (401, 403) \
            and version.extension in proyectos.BLOQUEADOS_EN_CLOUDINARY_GRATIS:
        registro.warning('Cloudinary no entrega archivos .%s: activa «Allow delivery of PDF and ZIP files» en '
                         'Settings › Security de Cloudinary', version.extension)
        return (f'Los archivos .{version.extension} todavía no se pueden descargar: falta activar un permiso en el '
                f'almacenamiento de la plataforma. Avísale a tu profe.')
    registro.warning('No se pudo descargar la versión %s de un proyecto', version.pk, exc_info=error)
    return 'No se pudo descargar el archivo en este momento. Espera un poquito e inténtalo otra vez.'


# ========================
# ALUMNO
# ========================
@alumno_requerido
def mis_proyectos(request, alumno, clase):
    return render(request, 'Alumnos/proyectos.html', {
        'alumno': alumno,
        'clase': clase,
        'proyectos': proyectos.lista_de(alumno),
        'espacio': proyectos.resumen_espacio(alumno),
        'abierto': clase.proyectos_abierto,
        'tipos': proyectos.TIPOS,
        'acepta': proyectos.ACEPTA,
        'iconos': {ext: info['emoji'] for ext, info in proyectos.POR_EXTENSION.items()},
        'tamano_max': proyectos.TAMANO_MAX,
        'tamano_max_texto': proyectos.peso(proyectos.TAMANO_MAX),
        'versiones_max': proyectos.VERSIONES_GUARDADAS,
        'seccion': 'proyectos',
    })


def _responder(request, clase, ok, mensaje, ancla=''):
    """Con fetch (la subida con barra de progreso) responde JSON; sin JavaScript, vuelve a la página con su mensaje."""
    destino = reverse('mis_proyectos', args=[clase.id]) + ancla
    if _es_ajax(request):
        if ok:
            messages.success(request, mensaje)   # se muestra al llegar a la página
        return JsonResponse({'ok': ok, 'mensaje': mensaje, 'redirect': destino}, status=200 if ok else 400)
    (messages.success if ok else messages.error)(request, mensaje)
    return redirect(destino)


@require_POST
@alumno_requerido
def guardar_proyecto(request, alumno, clase):
    if not clase.proyectos_abierto:
        return _responder(request, clase, False, CERRADO)
    proyecto = None
    if request.POST.get('proyecto', '').isdigit():
        proyecto = ProyectoAlumno.objects.filter(pk=request.POST['proyecto'], alumno=alumno).first()
        if proyecto is None:
            return _responder(request, clase, False, 'Ese proyecto ya no existe. Guárdalo como proyecto nuevo.')
    try:
        proyecto, nuevo = proyectos.guardar(alumno, request.FILES.get('archivo'), clase=clase, proyecto=proyecto,
                                            nombre=request.POST.get('nombre', ''))
    except proyectos.NoSePudoGuardar as error:
        return _responder(request, clase, False, str(error))
    if nuevo:
        mensaje = f'💾 ¡Listo! «{proyecto.nombre}» quedó guardado. Ya lo puedes abrir desde cualquier compu.'
    else:
        mensaje = f'💾 ¡Listo! Guardaste una versión nueva de «{proyecto.nombre}».'
    return _responder(request, clase, True, mensaje, ancla=f'#proyecto-{proyecto.id}')


@require_POST
@alumno_requerido
def renombrar_proyecto(request, alumno, clase, proyecto_id):
    proyecto = get_object_or_404(ProyectoAlumno, pk=proyecto_id, alumno=alumno)
    try:
        proyectos.renombrar(proyecto, request.POST.get('nombre', ''))
    except proyectos.NoSePudoGuardar as error:
        return _responder(request, clase, False, str(error))
    return _responder(request, clase, True, f'✏️ Ahora tu proyecto se llama «{proyecto.nombre}».',
                      ancla=f'#proyecto-{proyecto.id}')


@require_POST
@alumno_requerido
def borrar_proyecto(request, alumno, clase, proyecto_id):
    proyecto = get_object_or_404(ProyectoAlumno, pk=proyecto_id, alumno=alumno)
    nombre = proyecto.nombre
    proyecto.delete()
    return _responder(request, clase, True, f'🗑️ Borraste «{nombre}» con todas sus versiones.')


@require_POST
@alumno_requerido
def borrar_version(request, alumno, clase, version_id):
    version = get_object_or_404(VersionProyecto.objects.select_related('proyecto'), pk=version_id,
                                proyecto__alumno=alumno)
    nombre = version.proyecto.nombre
    if proyectos.borrar_version(version):
        return _responder(request, clase, True, f'🗑️ Borraste «{nombre}».')
    return _responder(request, clase, True, f'🗑️ Borraste una versión vieja de «{nombre}».',
                      ancla=f'#proyecto-{version.proyecto_id}')


@alumno_requerido
def descargar_version(request, alumno, clase, version_id):
    version = get_object_or_404(VersionProyecto.objects.select_related('proyecto'), pk=version_id,
                                proyecto__alumno=alumno)
    try:
        return proyectos.respuesta_descarga(version)
    except Exception as error:  # noqa: BLE001 — Cloudinary sin conexión o sin permiso para ese tipo de archivo
        messages.error(request, _no_se_pudo_descargar(request, version, error))
        return redirect(reverse('mis_proyectos', args=[clase.id]) + f'#proyecto-{version.proyecto_id}')


# ========================
# PROFESOR
# ========================
@login_required
def proyectos_grupo(request, clase_id=None):
    """Los proyectos que guardó cada alumno de un grupo: para revisarlos, descargarlos y ver quién guardó hoy."""
    if clase_id is None:
        clase = Clase.objects.filter(activa=True).order_by('grado', 'grupo').first() or Clase.objects.first()
        return redirect('proyectos_grupo', clase_id=clase.id) if clase else redirect('clases_lista')
    clase = get_object_or_404(Clase, id=clase_id)
    alumnos = proyectos.resumen_grupo(clase)
    con_proyectos = [a for a in alumnos if a.lista_proyectos]
    return render(request, 'Profesor/proyectos.html', {
        'clase': clase,
        'clases': Clase.objects.filter(activa=True).order_by('grado', 'grupo', 'nombre'),
        'alumnos': alumnos,
        'con_proyectos': len(con_proyectos),
        'guardaron_hoy': sum(1 for a in alumnos if a.guardo_hoy),
        'espacio_grupo': proyectos.peso(sum(a.espacio for a in alumnos)),
        'total': proyectos.total_guardado(),
        'espacio_alumno': proyectos.peso(proyectos.ESPACIO_POR_ALUMNO),
        'tamano_max': proyectos.peso(proyectos.TAMANO_MAX),
        'versiones_max': proyectos.VERSIONES_GUARDADAS,
        'max_proyectos': proyectos.MAX_PROYECTOS,
        'seccion': 'proyectos',
    })


@login_required
def descargar_version_profe(request, version_id):
    version = get_object_or_404(VersionProyecto.objects.select_related('proyecto'), pk=version_id)
    try:
        return proyectos.respuesta_descarga(version)
    except Exception as error:  # noqa: BLE001
        mensaje = _no_se_pudo_descargar(request, version, error)
        if version.extension in proyectos.BLOQUEADOS_EN_CLOUDINARY_GRATIS and 'permiso' in mensaje:
            mensaje = (f'Cloudinary no deja descargar archivos .{version.extension} en el plan gratis hasta que lo '
                       f'actives: en Cloudinary entra a Settings › Security y marca «Allow delivery of PDF and ZIP files».')
        messages.error(request, mensaje)
        return HttpResponseRedirect(_volver(request, reverse('alumno_detalle', args=[version.proyecto.alumno_id])))


@require_POST
@login_required
def borrar_proyecto_profe(request, proyecto_id):
    proyecto = get_object_or_404(ProyectoAlumno.objects.select_related('alumno'), pk=proyecto_id)
    alumno, nombre = proyecto.alumno, proyecto.nombre
    proyecto.delete()
    juego.notificar(alumno, 'sistema', f'Tu profe borró tu proyecto «{nombre}»',
                    'Si lo necesitas, pregúntale por qué y vuelve a guardarlo.', '🗑️')
    messages.success(request, f'Se borró «{nombre}» de {alumno.nombre}, con todas sus versiones.')
    return redirect(_siguiente(request, reverse('alumno_detalle', args=[alumno.id])))
