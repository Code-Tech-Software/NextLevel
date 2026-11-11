"""Cumpleaños de los alumnos.

Solo se guardan el día y el mes. Quien cumple en sábado o domingo también se celebra el lunes, para que nadie se
quede sin su festejo en clase. El 29 de febrero se celebra el 28 en los años que no son bisiestos.
"""
import calendar
from datetime import date

from django.db.models import Q

from . import gamificacion as juego
from .models import Alumno


def fecha_en(alumno, anio):
    """Su cumpleaños en ese año (None si no lo tiene capturado o la fecha no existe)."""
    if not alumno.tiene_cumple:
        return None
    dia, mes = alumno.cumple_dia, alumno.cumple_mes
    if mes == 2 and dia == 29 and not calendar.isleap(anio):
        dia = 28
    try:
        return date(anio, mes, dia)
    except ValueError:
        return None


def celebra_hoy(alumno, hoy):
    fecha = fecha_en(alumno, hoy.year)
    if not fecha:
        return False
    dias = (hoy - fecha).days
    return dias == 0 or (hoy.weekday() == 0 and dias in (1, 2))   # el lunes, si cayó en fin de semana


def proximo(alumno, hoy):
    """(días que faltan, fecha) de su próximo festejo; 0 si se celebra hoy. None si no tiene cumpleaños."""
    fecha = fecha_en(alumno, hoy.year)
    if not fecha:
        return None
    if celebra_hoy(alumno, hoy):
        return 0, fecha
    if fecha < hoy:
        fecha = fecha_en(alumno, hoy.year + 1)
    return (fecha - hoy).days, fecha


def cercanos(alumnos, hoy, dias=7):
    """Los que cumplen hoy o en los próximos `dias`, del más cercano al más lejano."""
    lista = []
    for alumno in alumnos:
        datos = proximo(alumno, hoy)
        if datos and datos[0] <= dias:
            lista.append({'alumno': alumno, 'faltan': datos[0], 'fecha': datos[1]})
    lista.sort(key=lambda c: (c['faltan'], c['alumno'].nombre, c['alumno'].apellido))
    return lista


def companeros_que_cumplen(clase, hoy, sin=None):
    """Compañeros de la clase que celebran hoy (para felicitarlos)."""
    alumnos = clase.alumnos.filter(activo=True, cumple_mes__isnull=False, cumple_dia__isnull=False)
    if sin is not None:
        alumnos = alumnos.exclude(pk=sin.pk)
    return [a for a in alumnos if celebra_hoy(a, hoy)]


def felicitar(alumno, hoy):
    """El aviso de «¡Feliz cumpleaños!», una sola vez por año. Devuelve True si se lo mandó ahora."""
    if alumno.es_prueba or not celebra_hoy(alumno, hoy):
        return False
    # Solo una petición gana aunque entre desde dos dispositivos a la vez
    marcado = Alumno.todos.filter(pk=alumno.pk).filter(
        Q(cumple_felicitado__isnull=True) | Q(cumple_felicitado__lt=hoy.year)
    ).update(cumple_felicitado=hoy.year)
    if not marcado:
        return False
    alumno.cumple_felicitado = hoy.year
    juego.notificar(alumno, 'sistema', f'¡Feliz cumpleaños, {alumno.nombre}! 🎂'[:120],
                    'Tu profe y todo Next-Level te desean un día increíble. 🎉', '🎂', celebrar=True)
    return True
