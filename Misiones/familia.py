"""Portal para la familia: lo que ven los papás con el enlace privado de su hijo.

Es de solo lectura y solo muestra datos del propio alumno: nunca nombres ni datos de sus compañeros, ni su PIN.
"""
import secrets
from datetime import timedelta

from django.conf import settings
from django.db.models import Avg
from django.urls import reverse
from django.utils import timezone

from . import gamificacion as juego
from .models import Aviso, Mision, ProgresoMision, RegistroConducta

DIAS_CONDUCTA = 30


def generar_enlace(alumno):
    """Crea (o cambia) su enlace: el anterior deja de funcionar."""
    alumno.familia_token = secrets.token_urlsafe(18)
    alumno.save(update_fields=['familia_token'])
    return alumno.familia_token


def quitar_enlace(alumno):
    alumno.familia_token = None
    alumno.save(update_fields=['familia_token'])


def url_enlace(request, alumno):
    """La dirección completa para compartir. En línea siempre con https (el enlace es como una contraseña)."""
    if not alumno.familia_token:
        return ''
    url = request.build_absolute_uri(reverse('portal_familia', args=[alumno.familia_token]))
    if not settings.DEBUG and url.startswith('http://'):
        url = 'https://' + url[len('http://'):]
    return url


def resumen(alumno, hoy):
    clases = list(alumno.clases.filter(activa=True).order_by('grado', 'grupo', 'nombre'))
    por_clase = [{'clase': clase, 'ruta': juego.construir_ruta(alumno, clase)} for clase in clases]
    total = sum(c['ruta']['total'] for c in por_clase)
    hechas = sum(c['ruta']['aprobadas'] for c in por_clase)

    progresos = ProgresoMision.objects.filter(alumno=alumno, mision__clase__in=clases, mision__activa=True) \
        .select_related('mision', 'mision__clase')
    promedio = progresos.filter(estado='aprobado').aggregate(p=Avg('puntuacion'))['p']
    entregadas = set(progresos.filter(estado__in=('pendiente', 'aprobado')).values_list('mision_id', flat=True))
    vencen = [m for m in Mision.objects.filter(
        clase__in=clases, activa=True, fecha_limite__gte=hoy, fecha_limite__lte=hoy + timedelta(days=14),
    ).select_related('clase').order_by('fecha_limite', 'id') if m.id not in entregadas][:6]
    for mision in vencen:
        mision.dias = (mision.fecha_limite - hoy).days

    conducta = RegistroConducta.objects.filter(alumno=alumno, clase__in=clases,
                                               fecha__gte=timezone.now() - timedelta(days=DIAS_CONDUCTA))
    return {
        'por_clase': por_clase,
        'total': total,
        'hechas': hechas,
        'pct': int(hechas * 100 / total) if total else 0,
        'estrellas': sum(c['ruta']['estrellas'] for c in por_clase),
        'promedio': promedio / 10 if promedio is not None else None,
        'recientes': list(progresos.filter(estado='aprobado').order_by('-fecha_revision', '-id')[:6]),
        'por_corregir': list(progresos.filter(estado='rechazado').order_by('-fecha_revision', '-id')[:5]),
        'en_revision': progresos.filter(estado='pendiente').count(),
        'vencen': vencen,
        'conducta_bien': conducta.filter(monedas__gte=0).count(),
        'conducta_mejorar': conducta.filter(monedas__lt=0).count(),
        'conducta_recientes': list(conducta.order_by('-fecha')[:6]),
        'dias_conducta': DIAS_CONDUCTA,
        'logros': list(alumno.logros.select_related('logro').order_by('-fecha')[:12]),
        'avisos': list(Aviso.objects.vigentes(hoy).filter(clases__in=clases).distinct()[:5]),
    }
