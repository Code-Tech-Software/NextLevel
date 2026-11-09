"""Bandeja de revisiones del profe: qué entregas esperan calificación y cómo se mandan a la página.

La página califica sin recargar (y la «revisión rápida» muestra una entrega a la vez), así que cada entrega viaja
también como JSON con lo necesario para pintarla.
"""
from django.db.models import Count
from django.urls import reverse
from django.utils.timesince import timesince

from .gamificacion import TIPO_INFO
from .models import ProgresoMision
from .templatetags.nextlevel import avatar_url, imagen_web

VISTAS = ('llegada', 'mision')

# Frases de un toque: para felicitar al aprobar y para explicar qué corregir al devolver
COMENTARIOS_APROBAR = ['¡Excelente trabajo! 🌟', '¡Muy bien hecho!', 'Buen trabajo, sigue así 💪', '¡Qué creativo! 🎨']
MOTIVOS_DEVOLVER = [
    'La foto no se ve bien: tómala de nuevo con más luz 📸',
    'Falta la evidencia de tu trabajo',
    'Revisa las conexiones del circuito 🔌',
    'Está incompleto: termina todos los pasos',
    'Lee otra vez las instrucciones y vuelve a intentarlo',
]


def entregas_pendientes(clase_id=None, tipo=None, vista='llegada'):
    entregas = ProgresoMision.objects.filter(estado='pendiente').select_related(
        'alumno', 'mision', 'mision__clase', 'mision__nivel', 'mision__nivel__mundo')
    if clase_id and str(clase_id).isdigit():
        entregas = entregas.filter(mision__clase_id=clase_id)
    if tipo:
        entregas = entregas.filter(mision__tipo=tipo)
    if vista == 'mision':
        # Todas las entregas de una misión juntas, en el orden del mapa: se califican con el mismo criterio en mente
        return entregas.order_by('mision__clase__grado', 'mision__clase__grupo', 'mision__clase_id',
                                 'mision__nivel__mundo__orden', 'mision__nivel__orden', 'mision__orden', 'mision_id',
                                 'fecha', 'id')
    return entregas.order_by('fecha', 'id')


def pendientes_por_clase():
    return dict(ProgresoMision.objects.filter(estado='pendiente').values_list('mision__clase').annotate(n=Count('id')))


def ruta_de(mision):
    nivel = mision.nivel
    return f'{nivel.mundo.nombre} › {nivel.nombre}' if nivel.mundo_id else nivel.nombre


def _hace(fecha):
    texto = timesince(fecha, depth=1)
    return 'unos segundos' if texto.startswith('0 ') or texto.startswith('0 ') else texto


def entrega_json(entrega):
    mision, alumno = entrega.mision, entrega.alumno
    info = TIPO_INFO.get(mision.tipo, TIPO_INFO['link'])
    return {
        'id': entrega.id,
        'alumno': {'id': alumno.id, 'nombre': alumno.nombre, 'apellido': alumno.apellido,
                   'avatar': avatar_url(alumno), 'url': reverse('alumno_detalle', args=[alumno.id])},
        'clase': {'id': mision.clase_id, 'nombre': mision.clase.nombre},
        'mision': {'id': mision.id, 'nombre': mision.nombre, 'tipo': mision.get_tipo_display(), 'emoji': info['emoji'],
                   'color': info['color'], 'ruta': ruta_de(mision), 'monedas': mision.monedas_recompensa,
                   'xp': mision.xp_recompensa},
        'evidencia': imagen_web(entrega.evidencia, 'grande'),
        'evidencia_mini': imagen_web(entrega.evidencia, 'mini'),
        'texto': entrega.respuesta_texto,
        'intentos': entrega.intentos,
        # Al reenviar, lo que el profe le había pedido corregir
        'comentario_anterior': entrega.comentario_profesor if entrega.intentos > 1 else '',
        'hace': _hace(entrega.fecha),
        'aprobar': reverse('aprobar_mision', args=[entrega.id]),
        'rechazar': reverse('rechazar_mision', args=[entrega.id]),
    }


def revisada_json(progreso):
    """Una entrega recién revisada, para la lista «Revisadas recientemente»."""
    return {
        'alumno': progreso.alumno.nombre,
        'avatar': avatar_url(progreso.alumno),
        'mision': progreso.mision.nombre,
        'estado': progreso.estado,
        'calificacion': f'{progreso.puntuacion / 10:.1f}',
    }


def ya_revisada(progreso):
    if progreso.estado == 'aprobado':
        return (f'La entrega de {progreso.alumno.nombre} ya estaba aprobada con {progreso.puntuacion / 10:.1f} '
                f'(quizá desde otro dispositivo).')
    return f'La entrega de {progreso.alumno.nombre} ya se había devuelto para corregir.'
