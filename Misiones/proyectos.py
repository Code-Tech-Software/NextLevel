"""«Mis proyectos»: los archivos de las prácticas de cada alumno (Scratch, Arduino, mBlock, Word…), guardados en su
cuenta para abrirlos en cualquier computadora con su PIN.

Los límites están pensados para el plan gratis de Cloudinary: acepta archivos «raw» de hasta 10 MB y trae unos 25
créditos al mes que se reparten entre lo guardado y lo descargado (también las fotos de evidencias y los avatares).
Cada proyecto conserva sus últimas versiones por si el alumno se equivoca; al guardar una más se borra la más vieja.
"""
import logging
import secrets

from django.db import transaction
from django.db.models import Count, Max, Prefetch, Sum
from django.http import FileResponse
from django.utils import timezone
from django.utils.text import slugify

from .almacen import borrar_archivo
from .models import Alumno, ProyectoAlumno, VersionProyecto

registro = logging.getLogger(__name__)

TAMANO_MAX = 10_000_000           # por archivo: lo más que acepta Cloudinary gratis en archivos «raw»
ESPACIO_POR_ALUMNO = 50_000_000   # todo lo que guarda cada alumno, con sus versiones
MAX_PROYECTOS = 30
VERSIONES_GUARDADAS = 5

# (clave, emoji, nombre, extensiones). Solo se aceptan estas: nada de programas (.exe) ni archivos raros.
TIPOS = [
    ('scratch', '🐱', 'Scratch', ('sb3', 'sb2', 'sb')),
    ('mblock', '🤖', 'mBlock', ('mblock',)),
    ('arduino', '⚡', 'Arduino', ('ino',)),
    ('microbit', '📟', 'micro:bit', ('hex',)),
    ('python', '🐍', 'Python', ('py',)),
    ('web', '🌐', 'Página web', ('html', 'htm', 'css', 'js')),
    ('3d', '🧊', 'Modelo 3D', ('stl', 'obj')),
    ('documento', '📄', 'Documento', ('doc', 'docx', 'odt', 'rtf', 'txt')),
    ('presentacion', '📊', 'Presentación', ('ppt', 'pptx', 'odp')),
    ('hoja', '📗', 'Hoja de cálculo', ('xls', 'xlsx', 'ods', 'csv')),
    ('pdf', '📕', 'PDF', ('pdf',)),
    ('imagen', '🖼️', 'Imagen', ('png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp')),
    ('zip', '🗜️', 'Carpeta comprimida', ('zip',)),
]
POR_EXTENSION = {ext: {'clave': clave, 'emoji': emoji, 'nombre': nombre}
                 for clave, emoji, nombre, extensiones in TIPOS for ext in extensiones}
ACEPTA = ','.join(f'.{ext}' for ext in POR_EXTENSION)   # para el <input type="file" accept="…">
OTRO = {'clave': 'otro', 'emoji': '📦', 'nombre': 'Archivo'}
# El plan gratis de Cloudinary no deja descargar estos hasta activar «Allow delivery of PDF and ZIP files»
BLOQUEADOS_EN_CLOUDINARY_GRATIS = {'pdf', 'zip'}


class NoSePudoGuardar(Exception):
    """El archivo no se guardó; el mensaje es para el alumno."""


def extension(nombre):
    return nombre.rsplit('.', 1)[-1].lower() if '.' in (nombre or '') else ''


def tipo_de(nombre):
    return POR_EXTENSION.get(extension(nombre), OTRO)


def peso(num_bytes):
    """1234567 → '1.2 MB' (como lo ve el alumno)."""
    num_bytes = num_bytes or 0
    if not num_bytes:
        return '0 MB'   # la carpeta vacía: «0 bytes» confunde
    if num_bytes < 1000:
        return f'{num_bytes} bytes' if num_bytes != 1 else '1 byte'
    if num_bytes < 1_000_000:
        return f'{max(1, round(num_bytes / 1000))} KB'
    mb = num_bytes / 1_000_000
    return f'{mb:.1f}'.rstrip('0').rstrip('.') + ' MB'


def nombre_seguro(nombre_archivo):
    """«Semáforo Final (2).sb3» → «semaforo-final-2.sb3»: sin acentos ni espacios, para guardarlo en la nube."""
    ext = extension(nombre_archivo)
    base = nombre_archivo[:-(len(ext) + 1)] if ext else nombre_archivo
    base = slugify(base)[:60].strip('-_') or 'proyecto'
    return f'{base}.{ext}' if ext else base


def nombre_sugerido(nombre_archivo):
    """«semaforo_final.sb3» → «Semaforo final»: el nombre del proyecto si el alumno no escribe otro."""
    ext = extension(nombre_archivo)
    base = nombre_archivo[:-(len(ext) + 1)] if ext else nombre_archivo
    base = ' '.join(base.replace('_', ' ').split()).strip()[:80]
    return (base[:1].upper() + base[1:]) if base else 'Mi proyecto'


def limpiar_nombre(nombre):
    return ' '.join((nombre or '').split())[:80]


# ---------- Espacio ----------
def espacio_usado(alumno):
    return VersionProyecto.objects.filter(proyecto__alumno=alumno).aggregate(t=Sum('tamano'))['t'] or 0


def resumen_espacio(alumno):
    usado = espacio_usado(alumno)
    total = ProyectoAlumno.objects.filter(alumno=alumno).count()
    pct = min(100, int(usado * 100 / ESPACIO_POR_ALUMNO))
    return {
        'usado': usado, 'maximo': ESPACIO_POR_ALUMNO, 'libre': max(0, ESPACIO_POR_ALUMNO - usado), 'pct': pct,
        'proyectos': total, 'max_proyectos': MAX_PROYECTOS, 'casi_lleno': pct >= 85 or total >= MAX_PROYECTOS - 2,
        'usado_texto': peso(usado), 'maximo_texto': peso(ESPACIO_POR_ALUMNO),
    }


def _preparar(proyecto):
    """Datos listos para la página: su última versión, las anteriores, el tipo y cuánto pesa en total."""
    versiones = list(proyecto.versiones.all())   # ya vienen en orden (la más nueva primero)
    proyecto.ultima = versiones[0] if versiones else None
    proyecto.anteriores = versiones[1:]
    proyecto.tipo = tipo_de(proyecto.ultima.nombre_archivo if proyecto.ultima else '')
    proyecto.peso_total = sum(v.tamano for v in versiones)
    return proyecto


def lista_de(alumno):
    proyectos = ProyectoAlumno.objects.filter(alumno=alumno).select_related('clase').prefetch_related(
        Prefetch('versiones', queryset=VersionProyecto.objects.order_by('-fecha', '-id')))
    return [_preparar(p) for p in proyectos if p.versiones.all()]


def _revisar_espacio(alumno, tamano, proyecto):
    """Lanza NoSePudoGuardar si el archivo ya no cabe. Cuenta lo que se libera al quitar la versión más vieja."""
    if proyecto is None and ProyectoAlumno.objects.filter(alumno=alumno).count() >= MAX_PROYECTOS:
        raise NoSePudoGuardar(f'Ya tienes {MAX_PROYECTOS} proyectos, el máximo. Borra los que ya no uses o guarda '
                              f'este como versión nueva de uno que ya tengas.')
    liberado = 0
    if proyecto is not None:
        tamanos = list(proyecto.versiones.order_by('-fecha', '-id').values_list('tamano', flat=True))
        liberado = sum(tamanos[VERSIONES_GUARDADAS - 1:])
    usado = espacio_usado(alumno)
    if usado - liberado + tamano > ESPACIO_POR_ALUMNO:
        libre = max(0, ESPACIO_POR_ALUMNO - usado + liberado)
        raise NoSePudoGuardar(f'Ya no te cabe: este archivo pesa {peso(tamano)} y te quedan {peso(libre)} libres. '
                              f'Borra versiones viejas o proyectos que ya no uses.')


def validar(archivo):
    """El mensaje de por qué no se puede guardar este archivo (None si está bien)."""
    if not archivo:
        return '📂 Primero elige el archivo de tu proyecto.'
    ext = extension(archivo.name)
    if ext not in POR_EXTENSION:
        if not ext:
            return 'Ese archivo no tiene extensión (como .sb3 o .ino). Guárdalo desde su programa y vuelve a intentar.'
        return (f'Los archivos .{ext} no se pueden guardar aquí. Sirven los de Scratch, mBlock, Arduino, micro:bit, '
                f'Python, Word, PowerPoint, Excel, PDF, fotos y .zip.')
    if not archivo.size:
        return 'Ese archivo está vacío. Ábrelo en su programa, guárdalo otra vez y vuelve a intentar.'
    if archivo.size > TAMANO_MAX:
        return f'Tu archivo pesa {peso(archivo.size)} y lo más que se puede guardar es {peso(TAMANO_MAX)} por archivo.'
    return None


def guardar(alumno, archivo, clase=None, proyecto=None, nombre=''):
    """Guarda el archivo como proyecto nuevo (o como versión nueva de `proyecto`). Regresa (proyecto, nuevo)."""
    error = validar(archivo)
    if error:
        raise NoSePudoGuardar(error)
    nombre_original = (archivo.name.replace('\\', '/').rsplit('/', 1)[-1] or 'proyecto')[-150:]
    _revisar_espacio(alumno, archivo.size, proyecto)

    # Primero se sube (puede tardar), sin tener nada bloqueado en la base de datos
    almacen = VersionProyecto._meta.get_field('archivo').storage
    ruta = f'proyectos/{alumno.id}/{secrets.token_urlsafe(12)}/{nombre_seguro(nombre_original)}'
    try:
        guardado = almacen.save(ruta, archivo, max_length=255)
    except Exception:  # noqa: BLE001 — Cloudinary caído, sin créditos, etc.: que el alumno lo sepa y lo intente otra vez
        registro.exception('No se pudo subir el proyecto de %s a su almacenamiento', alumno.pk)
        raise NoSePudoGuardar('No se pudo guardar tu archivo por un problema de conexión. Espera un momento e '
                              'inténtalo otra vez.')

    try:
        with transaction.atomic():
            # Si mandó dos archivos al mismo tiempo, el segundo espera y vuelve a revisar el espacio
            Alumno.todos.select_for_update().filter(pk=alumno.pk).first()
            if proyecto is not None:
                proyecto = ProyectoAlumno.objects.filter(pk=proyecto.pk, alumno=alumno).first()
                if proyecto is None:
                    raise NoSePudoGuardar('Ese proyecto ya no existe. Guárdalo como proyecto nuevo.')
            _revisar_espacio(alumno, archivo.size, proyecto)
            nuevo = proyecto is None
            ahora = timezone.now()
            if nuevo:
                proyecto = ProyectoAlumno.objects.create(
                    alumno=alumno, clase=clase, nombre=limpiar_nombre(nombre) or nombre_sugerido(nombre_original),
                    creado=ahora, actualizado=ahora)
            else:
                proyecto.actualizado = ahora
                proyecto.save(update_fields=['actualizado'])
            VersionProyecto.objects.create(proyecto=proyecto, archivo=guardado, nombre_archivo=nombre_original,
                                           tamano=archivo.size, fecha=ahora)
            # Solo las últimas versiones (los archivos de las que salen se borran al terminar)
            for vieja in proyecto.versiones.order_by('-fecha', '-id')[VERSIONES_GUARDADAS:]:
                vieja.delete()
    except BaseException:
        borrar_archivo(guardado)
        raise
    return proyecto, nuevo


def renombrar(proyecto, nombre):
    nombre = limpiar_nombre(nombre)
    if not nombre:
        raise NoSePudoGuardar('Escribe el nuevo nombre de tu proyecto.')
    proyecto.nombre = nombre
    proyecto.save(update_fields=['nombre'])
    return proyecto


def borrar_version(version):
    """Borra una versión. Si era la única, se va todo el proyecto. Regresa True si se borró el proyecto."""
    proyecto = version.proyecto
    with transaction.atomic():
        if proyecto.versiones.count() <= 1:
            proyecto.delete()
            return True
        version.delete()
        proyecto.actualizado = proyecto.versiones.aggregate(f=Max('fecha'))['f'] or proyecto.actualizado
        proyecto.save(update_fields=['actualizado'])
    return False


def respuesta_descarga(version):
    """El archivo para descargar, con su nombre original. Puede lanzar almacen.ArchivoNoDisponible u otra falla."""
    archivo = version.archivo.storage.open(version.archivo.name, 'rb')
    respuesta = FileResponse(archivo, as_attachment=True, filename=version.nombre_archivo,
                             content_type='application/octet-stream')   # siempre se descarga, nunca se abre aquí
    largo = getattr(archivo, 'largo', None)
    if largo and not respuesta.has_header('Content-Length'):
        respuesta['Content-Length'] = str(largo)
    respuesta['Cache-Control'] = 'private, no-store'
    return respuesta


# ---------- Para el profe ----------
def resumen_grupo(clase, hoy=None):
    """Cada alumno del grupo con sus proyectos, cuánto ocupa y si guardó algo hoy (consultas agrupadas)."""
    hoy = hoy or timezone.localdate()
    alumnos = list(clase.alumnos.filter(activo=True).order_by('nombre', 'apellido'))
    por_alumno = {a.id: [] for a in alumnos}
    proyectos = ProyectoAlumno.objects.filter(alumno__in=alumnos).select_related('clase').prefetch_related(
        Prefetch('versiones', queryset=VersionProyecto.objects.order_by('-fecha', '-id')))
    for proyecto in proyectos:
        if proyecto.versiones.all():
            por_alumno[proyecto.alumno_id].append(_preparar(proyecto))
    for alumno in alumnos:
        alumno.lista_proyectos = por_alumno[alumno.id]
        alumno.espacio = sum(p.peso_total for p in alumno.lista_proyectos)
        alumno.espacio_pct = min(100, int(alumno.espacio * 100 / ESPACIO_POR_ALUMNO))
        alumno.ultimo_guardado = max((p.actualizado for p in alumno.lista_proyectos), default=None)
        alumno.guardo_hoy = bool(alumno.ultimo_guardado and timezone.localdate(alumno.ultimo_guardado) == hoy)
    return alumnos


def total_guardado():
    datos = VersionProyecto.objects.aggregate(t=Sum('tamano'), n=Count('id'))
    return {'bytes': datos['t'] or 0, 'texto': peso(datos['t'] or 0), 'archivos': datos['n']}
