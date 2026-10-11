"""Modo clase (comportamientos con un toque), equipos/casas y metas del grupo."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from . import gamificacion as juego
from .forms import ComportamientoForm, EquipoForm, MetaGrupoForm
from .models import Alumno, Clase, Comportamiento, Equipo, MetaGrupo, PuntosEquipo, RegistroConducta
from .views_profesor import _formulario, _guardado

CASAS_CLASICAS = [
    ('Leones', '🦁', 'ambar'),
    ('Dragones', '🐉', 'coral'),
    ('Águilas', '🦅', 'cielo'),
    ('Lobos', '🐺', 'uva'),
]


def _primera_clase():
    return Clase.objects.filter(activa=True).order_by('grado', 'grupo').first() or Clase.objects.first()


def _ids(request, campo):
    return [int(v) for v in request.POST.getlist(campo) if str(v).isdigit()]


def _estado_clase(clase, alumnos_ids=()):
    """Datos que el modo clase necesita para refrescarse sin recargar la página."""
    alumnos = {
        a.id: {'monedas': a.monedas, 'nivel': a.nivel}
        for a in Alumno.objects.filter(id__in=alumnos_ids)
    }
    equipos = {e.id: e.total for e in juego.ranking_equipos(clase)}
    metas = [
        {'id': m.id, 'valor': m.valor, 'objetivo': m.objetivo, 'pct': m.pct, 'completada': bool(m.completada_en)}
        for m in juego.metas_visibles(clase)
    ]
    return {'alumnos': alumnos, 'equipos': equipos, 'metas': metas}


# ========================
# MODO CLASE
# ========================
@login_required
def modo_clase(request, clase_id=None):
    if clase_id is None:
        clase = _primera_clase()
        return redirect('modo_clase', clase_id=clase.id) if clase else redirect('clases_lista')
    clase = get_object_or_404(Clase, id=clase_id)

    equipos = juego.ranking_equipos(clase)
    equipo_de = {m.id: e for e in equipos for m in e.lista_miembros}
    hoy = timezone.localdate()
    conteos = {
        fila['alumno_id']: fila for fila in RegistroConducta.objects.filter(clase=clase, fecha__date=hoy)
        .values('alumno_id').annotate(pos=Count('id', filter=Q(monedas__gte=0)), neg=Count('id', filter=Q(monedas__lt=0)))
    }
    alumnos = list(clase.alumnos.filter(activo=True).order_by('nombre', 'apellido'))
    for alumno in alumnos:
        alumno.equipo = equipo_de.get(alumno.id)
        alumno.hoy_pos = conteos.get(alumno.id, {}).get('pos', 0)
        alumno.hoy_neg = conteos.get(alumno.id, {}).get('neg', 0)

    comportamientos = list(Comportamiento.objects.filter(activo=True))
    return render(request, 'Profesor/modo_clase.html', {
        'clase': clase,
        'clases': Clase.objects.filter(activa=True).order_by('grado', 'grupo'),
        'alumnos': alumnos,
        'equipos': equipos,
        'positivos': [c for c in comportamientos if c.positivo],
        'negativos': [c for c in comportamientos if not c.positivo],
        'metas': juego.metas_visibles(clase),
        'recientes': RegistroConducta.objects.filter(clase=clase, fecha__date=hoy).select_related('alumno')[:10],
        'seccion': 'modo_clase',
    })


@require_POST
@login_required
def api_conducta(request):
    clase = get_object_or_404(Clase, id=request.POST.get('clase'))
    comportamiento = get_object_or_404(Comportamiento, id=request.POST.get('comportamiento'))
    alumnos = clase.alumnos.filter(activo=True, id__in=_ids(request, 'alumnos'))
    registros = [juego.registrar_conducta(alumno, clase, comportamiento) for alumno in alumnos]
    juego.revisar_metas(clase)
    return JsonResponse({
        'ok': True,
        'registros': [r.id for r in registros],
        'aplicados': {r.alumno_id: {'monedas': r.monedas, 'xp': r.xp} for r in registros},
        'comportamiento': {'nombre': comportamiento.nombre, 'icono': comportamiento.icono,
                           'positivo': comportamiento.positivo},
        **_estado_clase(clase, [r.alumno_id for r in registros]),
    })


@require_POST
@login_required
def api_deshacer_conducta(request):
    clase = get_object_or_404(Clase, id=request.POST.get('clase'))
    registros = list(RegistroConducta.objects.filter(clase=clase, id__in=_ids(request, 'registros')).select_related('alumno'))
    alumnos_ids = [r.alumno_id for r in registros]
    for registro in registros:
        juego.deshacer_conducta(registro)
    return JsonResponse({'ok': True, 'deshechos': len(registros), **_estado_clase(clase, alumnos_ids)})


@require_POST
@login_required
def api_puntos_equipo(request):
    equipo = get_object_or_404(Equipo, id=request.POST.get('equipo'))
    try:
        puntos = int(request.POST.get('puntos', 0))
    except ValueError:
        return JsonResponse({'ok': False, 'mensaje': 'Puntos inválidos'}, status=400)
    if puntos:
        juego.dar_puntos_equipo(equipo, puntos, request.POST.get('motivo', '').strip())
    return JsonResponse({'ok': True, **_estado_clase(equipo.clase)})


@require_POST
@login_required
def api_meta_manual(request):
    meta = get_object_or_404(MetaGrupo, id=request.POST.get('meta'), tipo='manual')
    try:
        delta = int(request.POST.get('delta', 1))
    except ValueError:
        delta = 1
    meta.progreso_manual = max(0, meta.progreso_manual + delta)
    meta.save(update_fields=['progreso_manual'])
    juego.revisar_metas(meta.clase)
    return JsonResponse({'ok': True, **_estado_clase(meta.clase)})


# ========================
# COMPORTAMIENTOS (botones del modo clase)
# ========================
@login_required
def comportamientos_lista(request):
    return render(request, 'Profesor/comportamientos.html', {
        'comportamientos': Comportamiento.objects.annotate(usos=Count('registroconducta')),
        'seccion': 'modo_clase',
    })


@login_required
def comportamiento_form(request, pk=None):
    comportamiento = get_object_or_404(Comportamiento, pk=pk) if pk else None
    inicial = {} if comportamiento else {
        'orden': (Comportamiento.objects.aggregate(m=Max('orden'))['m'] or 0) + 1, 'monedas': 5, 'activo': True,
    }
    form = ComportamientoForm(request.POST or None, instance=comportamiento, initial=inicial)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return _guardado(request, 'Botón guardado.', reverse('comportamientos_lista'))
    return _formulario(request, 'Profesor/form_generico.html', {
        'form': form,
        'titulo': 'Editar botón' if pk else 'Nuevo botón del modo clase',
        'subtitulo': 'Los positivos dan monedas y XP. Los negativos solo restan monedas (usa un número negativo).',
        'icono': 'bi-hand-index-thumb',
        'volver': reverse('comportamientos_lista'),
        'seccion': 'modo_clase',
    })


# ========================
# EQUIPOS / CASAS
# ========================
@login_required
def equipos_clase(request, clase_id=None):
    if clase_id is None:
        clase = _primera_clase()
        return redirect('equipos_clase', clase_id=clase.id) if clase else redirect('clases_lista')
    clase = get_object_or_404(Clase, id=clase_id)
    equipos = juego.ranking_equipos(clase)
    equipo_de = {m.id: e for e in equipos for m in e.lista_miembros}
    alumnos = list(clase.alumnos.filter(activo=True).order_by('apellido', 'nombre'))
    for alumno in alumnos:
        alumno.equipo = equipo_de.get(alumno.id)
    return render(request, 'Profesor/equipos.html', {
        'clase': clase,
        'clases': Clase.objects.order_by('grado', 'grupo'),
        'equipos': equipos,
        'alumnos': alumnos,
        'sin_equipo': sum(1 for a in alumnos if not a.equipo),
        'historial': PuntosEquipo.objects.filter(equipo__clase=clase).select_related('equipo')[:12],
        'seccion': 'equipos',
    })


@login_required
def equipo_form(request, pk=None):
    equipo = get_object_or_404(Equipo, pk=pk) if pk else None
    inicial = {}
    if not equipo and request.GET.get('clase', '').isdigit():
        clase = Clase.objects.filter(pk=request.GET['clase']).first()
        if clase:
            inicial = {'clase': clase, 'orden': clase.equipos.count() + 1}
    form = EquipoForm(request.POST or None, instance=equipo, initial=inicial)
    if request.method == 'POST' and form.is_valid():
        equipo = form.save()
        return _guardado(request, f'Equipo "{equipo.nombre}" guardado.', reverse('equipos_clase', args=[equipo.clase_id]))
    return _formulario(request, 'Profesor/form_generico.html', {
        'form': form,
        'titulo': 'Editar equipo' if pk else 'Nuevo equipo',
        'subtitulo': 'Los equipos suman la XP de sus integrantes y los puntos que tú les des.',
        'icono': 'bi-shield',
        'volver': reverse('equipos_lista'),
        'seccion': 'equipos',
    })


@require_POST
@login_required
def crear_casas(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    if not clase.equipos.exists():
        for orden, (nombre, emoji, color) in enumerate(CASAS_CLASICAS, start=1):
            Equipo.objects.create(clase=clase, nombre=nombre, emoji=emoji, color=color, orden=orden)
        repartidos = juego.repartir_equipos(clase)
        messages.success(request, f'¡Se crearon 4 casas y se repartieron {repartidos} alumnos al azar!')
    return redirect('equipos_clase', clase_id=clase.id)


@require_POST
@login_required
def repartir_equipos(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    repartidos = juego.repartir_equipos(clase)
    messages.success(request, f'Se repartieron {repartidos} alumnos al azar en equipos equilibrados.')
    return redirect('equipos_clase', clase_id=clase.id)


@require_POST
@login_required
def reiniciar_equipos(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    PuntosEquipo.objects.filter(equipo__clase=clase).delete()
    messages.success(request, '¡Nueva temporada! Los puntos de todos los equipos volvieron a cero.')
    return redirect('equipos_clase', clase_id=clase.id)


@require_POST
@login_required
def api_asignar_equipo(request):
    clase = get_object_or_404(Clase, id=request.POST.get('clase'))
    alumno = get_object_or_404(Alumno, id=request.POST.get('alumno'), clases=clase)
    equipo_id = request.POST.get('equipo')
    equipo = get_object_or_404(Equipo, id=equipo_id, clase=clase) if equipo_id else None
    juego.asignar_equipo(alumno, clase, equipo)
    return JsonResponse({'ok': True})


# ========================
# METAS DEL GRUPO
# ========================
@login_required
def metas_lista(request):
    metas = list(MetaGrupo.objects.select_related('clase'))
    hoy = timezone.localdate()
    for meta in metas:
        meta.valor = juego.progreso_meta(meta)
        meta.pct = min(100, int(meta.valor * 100 / meta.objetivo)) if meta.objetivo else 100
        meta.dias_restantes = (meta.fecha_limite - hoy).days if meta.fecha_limite else None
    return render(request, 'Profesor/metas.html', {
        'metas': metas,
        'clases': Clase.objects.filter(activa=True).order_by('grado', 'grupo'),
        'seccion': 'metas',
    })


@login_required
def meta_form(request, pk=None):
    meta = get_object_or_404(MetaGrupo, pk=pk) if pk else None
    inicial = {}
    if not meta:
        inicial = {'icono': '🎯', 'activa': True, 'objetivo': 30, 'recompensa': '🍿 Película el viernes'}
        if request.GET.get('clase', '').isdigit():
            inicial['clase'] = request.GET['clase']
    form = MetaGrupoForm(request.POST or None, instance=meta, initial=inicial)
    if request.method == 'POST' and form.is_valid():
        meta = form.save()
        juego.revisar_metas(meta.clase)
        return _guardado(request, f'Meta "{meta.titulo}" guardada.', reverse('metas_lista'))
    return _formulario(request, 'Profesor/form_generico.html', {
        'form': form,
        'titulo': 'Editar meta del grupo' if pk else 'Nueva meta del grupo',
        'subtitulo': 'Un reto para toda la clase: cuando entre todos lleguen al objetivo, todos celebran.',
        'icono': 'bi-bullseye',
        'volver': reverse('metas_lista'),
        'seccion': 'metas',
    })


@require_POST
@login_required
def reiniciar_meta(request, pk):
    meta = get_object_or_404(MetaGrupo, pk=pk)
    meta.fecha_inicio = timezone.now()
    meta.completada_en = None
    meta.progreso_manual = 0
    meta.activa = True
    meta.save(update_fields=['fecha_inicio', 'completada_en', 'progreso_manual', 'activa'])
    messages.success(request, f'La meta "{meta.titulo}" empezó de nuevo desde cero.')
    return redirect('metas_lista')
