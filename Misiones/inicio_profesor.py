"""Datos del inicio del panel del profesor.

La clase que toca ahora, los alumnos que necesitan atención, las entregas que vencen pronto y las metas del grupo.
Todo sale de consultas agrupadas (nunca una por clase ni una por alumno) para que el inicio siga cargando rápido
aunque crezcan las clases.
"""
from datetime import timedelta
from statistics import median

from django.db.models import Count, F, Min, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.utils import timezone

from . import gamificacion as juego
from .models import Alumno, Batalla, Clase, MetaGrupo, Mision, Movimiento, ProgresoMision

Inscripcion = Alumno.clases.through

DIAS_AUSENTE = 10      # sin entrar a la plataforma desde hace tantos días
DIAS_NUEVO = 7         # a los recién dados de alta todavía no se les marca como ausentes
MINIMO_GRUPO = 3       # para comparar el avance, el grupo debe llevar al menos tantas misiones (en la mediana)
MINIMO_ALUMNOS = 3     # y tener al menos tantos alumnos
MAX_ATENCION = 30
DIAS_SEMANA = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']


def _semana(hoy):
    """Primer día de «esta semana» (hoy y los 6 días anteriores)."""
    return hoy - timedelta(days=6)


def horario_de_hoy(clase, ahora):
    """Si hoy le toca clase a este grupo: {'inicio', 'fin', 'estado'} con estado 'ahora', 'despues' o 'termino'."""
    if not clase.tiene_horario or ahora.weekday() not in clase.dias_horario:
        return None
    hora = ahora.time()
    if hora < clase.horario_inicio:
        estado = 'despues'
    elif hora < clase.horario_fin:
        estado = 'ahora'
    else:
        estado = 'termino'
    return {'inicio': clase.horario_inicio, 'fin': clase.horario_fin, 'estado': estado}


def clases_del_inicio(ahora):
    """Todas las clases con sus cifras (tarjetas de «Mis clases») y, aparte, las activas en el orden del lanzador:
    primero la que está en clase ahora, luego las que tienen clase más tarde hoy y después las demás."""
    hoy = ahora.date()
    clases = list(Clase.objects.annotate(
        total_alumnos=Count('alumnos', filter=Q(alumnos__activo=True), distinct=True),
        total_misiones=Count('misiones', filter=Q(misiones__activa=True), distinct=True),
        total_mundos=Count('mundos', distinct=True),
    ).order_by('-activa', 'anio', 'grado', 'grupo'))

    pendientes = dict(ProgresoMision.objects.filter(estado='pendiente')
                      .values_list('mision__clase').annotate(n=Count('id')))
    hechas = dict(ProgresoMision.objects.filter(
        estado='aprobado', mision__activa=True, alumno__activo=True, alumno__clases=F('mision__clase'),
    ).values_list('mision__clase').annotate(n=Count('id')))
    activos = dict(Inscripcion.objects.filter(
        alumno__activo=True, alumno__es_prueba=False, alumno__ultima_actividad__gte=_semana(hoy),
    ).values_list('clase_id').annotate(n=Count('alumno_id')))
    batallas = {}
    for batalla in Batalla.objects.abiertas().order_by('-creada'):
        batallas.setdefault(batalla.clase_id, batalla)

    for clase in clases:
        clase.misiones_pendientes = pendientes.get(clase.id, 0)
        posibles = clase.total_alumnos * clase.total_misiones
        clase.avance = min(100, int(hechas.get(clase.id, 0) * 100 / posibles)) if posibles else 0
        clase.activos_semana = activos.get(clase.id, 0)
        clase.hoy = horario_de_hoy(clase, ahora)
        clase.batalla = batallas.get(clase.id)

    activas = [c for c in clases if c.activa]
    ahora_mismo = [c for c in activas if c.hoy and c.hoy['estado'] == 'ahora']
    mas_tarde = sorted((c for c in activas if c.hoy and c.hoy['estado'] == 'despues'), key=lambda c: c.hoy['inicio'])
    primero = ahora_mismo + mas_tarde
    lanzador = primero + [c for c in activas if c not in primero]
    sugerida = primero[0] if primero else None
    return clases, lanzador, sugerida


def _comparar(actual, anterior):
    """Cifra de esta semana contra la anterior: {'actual', 'anterior', 'pct', 'sube'} (pct None si antes fue 0)."""
    if not anterior:
        return {'actual': actual, 'anterior': anterior, 'pct': None, 'sube': actual > 0}
    pct = round((actual - anterior) * 100 / anterior)
    return {'actual': actual, 'anterior': anterior, 'pct': abs(pct), 'sube': pct >= 0}


def indicadores(ahora):
    hoy = ahora.date()
    hace_7, hace_14 = ahora - timedelta(days=7), ahora - timedelta(days=14)
    xp = Movimiento.objects.filter(xp__gt=0, fecha__gte=hace_14).aggregate(
        actual=Coalesce(Sum('xp', filter=Q(fecha__gte=hace_7)), Value(0)),
        anterior=Coalesce(Sum('xp', filter=Q(fecha__lt=hace_7)), Value(0)),
    )
    aprobadas = ProgresoMision.objects.filter(estado='aprobado', fecha_revision__gte=hace_14).aggregate(
        actual=Count('id', filter=Q(fecha_revision__gte=hace_7)),
        anterior=Count('id', filter=Q(fecha_revision__lt=hace_7)),
    )
    revisiones = ProgresoMision.objects.filter(estado='pendiente').aggregate(total=Count('id'), antigua=Min('fecha'))
    alumnos = Alumno.objects.filter(activo=True).aggregate(
        total=Count('id'), activos=Count('id', filter=Q(ultima_actividad__gte=_semana(hoy))),
    )
    antigua = revisiones['antigua']
    return {
        'revisiones': revisiones['total'],
        'revision_dias': (hoy - timezone.localtime(antigua).date()).days if antigua else None,
        'alumnos': alumnos['total'],
        'activos': alumnos['activos'],
        'sin_entrar': alumnos['total'] - alumnos['activos'],
        'participacion': int(alumnos['activos'] * 100 / alumnos['total']) if alumnos['total'] else 0,
        'xp': _comparar(xp['actual'], xp['anterior']),
        'aprobadas': _comparar(aprobadas['actual'], aprobadas['anterior']),
    }


def _plural(n, uno, varios):
    return f'{n} {uno if n == 1 else varios}'


def alumnos_con_atencion(hoy):
    """Alumnos de las clases activas que van atrasados, que no entran desde hace días o que tienen misiones por
    corregir. Cada uno con sus motivos, del más urgente al menos urgente."""
    filas = list(Inscripcion.objects.filter(
        clase__activa=True, alumno__activo=True, alumno__es_prueba=False,
    ).values_list('alumno_id', 'clase_id', 'clase__nombre'))
    if not filas:
        return []
    aprobadas = {
        (alumno, clase): n for alumno, clase, n in ProgresoMision.objects.filter(
            estado='aprobado', mision__activa=True, mision__clase__activa=True, alumno__activo=True,
        ).values_list('alumno_id', 'mision__clase_id').annotate(n=Count('id'))
    }
    por_corregir = dict(ProgresoMision.objects.filter(
        estado='rechazado', mision__activa=True, mision__clase__activa=True, alumno__activo=True,
    ).values_list('alumno_id').annotate(n=Count('id')))

    por_clase, nombre_clase, clase_de = {}, {}, {}
    for alumno_id, clase_id, nombre in filas:
        por_clase.setdefault(clase_id, []).append(alumno_id)
        nombre_clase[clase_id] = nombre
        clase_de.setdefault(alumno_id, clase_id)

    # Atrasados: llevan la mitad (o menos) de las misiones que lleva la mayoría de su grupo
    atrasos = {}
    for clase_id, ids in por_clase.items():
        if len(ids) < MINIMO_ALUMNOS:
            continue
        mediana = median(aprobadas.get((a, clase_id), 0) for a in ids)
        if mediana < MINIMO_GRUPO:
            continue
        for alumno_id in ids:
            suyas = aprobadas.get((alumno_id, clase_id), 0)
            proporcion = suyas / mediana
            if proporcion <= .5 and proporcion < atrasos.get(alumno_id, {}).get('proporcion', 1):
                atrasos[alumno_id] = {'proporcion': proporcion, 'suyas': suyas, 'grupo': round(mediana),
                                      'clase_id': clase_id}

    alumnos = Alumno.objects.filter(id__in={a for a, _, _ in filas}).only(
        'id', 'nombre', 'apellido', 'avatar', 'ultima_actividad', 'fecha_registro')
    lista = []
    for alumno in alumnos:
        motivos, peso = [], 0
        atraso = atrasos.get(alumno.id)
        if atraso:
            motivos.append({'tipo': 'atraso', 'icono': 'bi-hourglass-split',
                            'texto': f"{_plural(atraso['suyas'], 'misión', 'misiones')} · su grupo lleva {atraso['grupo']}"})
            peso += 3
        if alumno.ultima_actividad:
            dias = (hoy - alumno.ultima_actividad).days
            if dias >= DIAS_AUSENTE:
                motivos.append({'tipo': 'ausente', 'icono': 'bi-moon-stars', 'texto': f'No entra desde hace {dias} días'})
                peso += 3 if dias >= 21 else 2
        elif (hoy - timezone.localtime(alumno.fecha_registro).date()).days >= DIAS_NUEVO:
            motivos.append({'tipo': 'ausente', 'icono': 'bi-moon-stars', 'texto': 'Nunca ha entrado'})
            peso += 2
        corregir = por_corregir.get(alumno.id, 0)
        if corregir:
            motivos.append({'tipo': 'corregir', 'icono': 'bi-arrow-repeat',
                            'texto': _plural(corregir, 'misión por corregir', 'misiones por corregir')})
            peso += 1 + min(corregir, 2)
        if motivos:
            clase_id = atraso['clase_id'] if atraso else clase_de[alumno.id]
            lista.append({'alumno': alumno, 'clase': nombre_clase[clase_id], 'clase_id': clase_id,
                          'motivos': motivos, 'peso': peso})
    lista.sort(key=lambda f: (-f['peso'], f['alumno'].nombre, f['alumno'].apellido))
    return lista[:MAX_ATENCION]


def _cuando_vence(dias, fecha):
    if dias < 0:
        return 'Venció ayer' if dias == -1 else f'Venció hace {-dias} días'
    if dias == 0:
        return 'Vence hoy'
    if dias == 1:
        return 'Vence mañana'
    if dias >= 7:
        return 'Vence en una semana'
    return f'Vence el {DIAS_SEMANA[fecha.weekday()]}'


def entregas_que_vencen(hoy):
    """Misiones con fecha límite cercana (de hace 3 días a 7 días adelante) y cuántos de su grupo ya entregaron."""
    misiones = list(Mision.objects.filter(
        activa=True, clase__activa=True,
        fecha_limite__gte=hoy - timedelta(days=3), fecha_limite__lte=hoy + timedelta(days=7),
    ).select_related('clase').order_by('fecha_limite', 'id')[:6])
    if not misiones:
        return []
    entregaron = dict(ProgresoMision.objects.filter(
        mision__in=misiones, alumno__activo=True, alumno__clases=F('mision__clase'),
    ).values_list('mision_id').annotate(n=Count('alumno_id', distinct=True)))
    totales = dict(Inscripcion.objects.filter(
        clase_id__in={m.clase_id for m in misiones}, alumno__activo=True, alumno__es_prueba=False,
    ).values_list('clase_id').annotate(n=Count('alumno_id')))
    for mision in misiones:
        mision.entregaron = entregaron.get(mision.id, 0)
        mision.total = totales.get(mision.clase_id, 0)
        mision.faltan = max(0, mision.total - mision.entregaron)
        mision.pct = int(mision.entregaron * 100 / mision.total) if mision.total else 0
        mision.dias = (mision.fecha_limite - hoy).days
        mision.cuando = _cuando_vence(mision.dias, mision.fecha_limite)
    return misiones


def metas_en_curso(hoy):
    """Metas del grupo activas y sin cumplir, con su avance (sin cumplirlas aquí: eso pasa al ganar puntos)."""
    metas = list(MetaGrupo.objects.filter(activa=True, completada_en__isnull=True, clase__activa=True)
                 .select_related('clase').order_by(F('fecha_limite').asc(nulls_last=True), '-fecha_inicio')[:4])
    for meta in metas:
        meta.valor = juego.progreso_meta(meta)
        meta.pct = min(100, int(meta.valor * 100 / meta.objetivo)) if meta.objetivo else 100
        meta.faltan = max(0, meta.objetivo - meta.valor)
        meta.dias = (meta.fecha_limite - hoy).days if meta.fecha_limite else None
    return metas
