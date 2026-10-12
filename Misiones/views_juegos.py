"""Minijuegos: el Arcade del alumno, las partidas y la biblioteca de juegos del profe."""
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Max, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from . import minijuegos
from .forms import JuegoForm, campos_clasifica
from .models import Juego, Mision, Nivel, PartidaJuego
from .views import alumno_requerido
from .views_profesor import _acomodar, _formulario, _guardado

ICONOS_JUEGO = ['🎮', '☄️', '⌨️', '🚀', '👾', '🕹️', '🛸', '🌠', '🔤', '🧠', '⚡', '🏆', '🤖', '💻', '🎯', '🔥']


# ========================
# ALUMNO: ARCADE Y PARTIDAS
# ========================
@alumno_requerido
def arcade(request, alumno, clase):
    return render(request, 'Alumnos/arcade.html', {
        'alumno': alumno,
        'clase': clase,
        'maquinas': minijuegos.estado_arcade(alumno, clase),
        'seccion': 'arcade',
    })


@alumno_requerido
def arcade_juego(request, alumno, clase, juego_id):
    juego = get_object_or_404(minijuegos.juegos_arcade(clase), id=juego_id)
    if minijuegos.bloqueado_en_arcade(alumno, clase, juego):
        messages.warning(request, '🔒 Completa primero su misión en el mapa para jugarlo en el Arcade.')
        return redirect('arcade', clase_id=clase.id)
    propias = PartidaJuego.objects.filter(alumno=alumno, juego=juego, terminada=True)
    return render(request, 'Alumnos/arcade_juego.html', {
        'alumno': alumno,
        'clase': clase,
        'juego': juego,
        'datos': minijuegos.datos_juego(juego),
        'info': minijuegos.PLANTILLAS_INFO[juego.plantilla],
        'record': propias.aggregate(m=Max('puntaje'))['m'],
        'partidas': propias.count(),
        'semana': minijuegos.ranking_juego(juego, clase, desde=minijuegos.inicio_semana()),
        'siempre': minijuegos.ranking_juego(juego, clase),
        'premio_hoy': bool(juego.monedas_arcade) and not minijuegos._premio_cobrado_hoy(alumno, juego),
        'seccion': 'arcade',
    })


@require_POST
@alumno_requerido
def iniciar_partida(request, alumno, clase, juego_id):
    juego = get_object_or_404(Juego, id=juego_id, activo=True)
    mision = None
    if request.POST.get('mision'):
        mision = get_object_or_404(Mision, id=request.POST['mision'], clase=clase, tipo='juego', juego=juego, activa=True)
        if not minijuegos.mision_jugable(alumno, clase, mision):
            return JsonResponse({'ok': False, 'mensaje': '🔒 Esta misión aún está bloqueada.'}, status=403)
    else:
        if not minijuegos.juegos_arcade(clase).filter(pk=juego.pk).exists() \
                or minijuegos.bloqueado_en_arcade(alumno, clase, juego):
            return JsonResponse({'ok': False, 'mensaje': '🔒 Este juego no está disponible en tu Arcade.'}, status=403)
    partida = PartidaJuego.objects.create(juego=juego, alumno=alumno, clase=clase, mision=mision)
    return JsonResponse({'ok': True, 'partida': partida.id})


@require_POST
@alumno_requerido
def terminar_partida(request, alumno, clase, partida_id):
    partida = get_object_or_404(PartidaJuego, id=partida_id, alumno=alumno, clase=clase)
    try:
        datos = json.loads(request.body or '{}')
    except ValueError:
        datos = {}
    resumen = minijuegos.terminar_partida(partida, datos if isinstance(datos, dict) else {})
    if resumen is None:
        return JsonResponse({'ok': False, 'mensaje': 'Esta partida ya no es válida. ¡Juega otra!'}, status=400)
    return JsonResponse({'ok': True, **resumen})


# ========================
# PROFE: BIBLIOTECA DE JUEGOS
# ========================
@login_required
def juegos_lista(request):
    juegos = list(Juego.objects.select_related('clase').annotate(
        total_partidas=Count('partidas', filter=Q(partidas__terminada=True), distinct=True),
        jugadores=Count('partidas__alumno', filter=Q(partidas__terminada=True), distinct=True),
        total_misiones=Count('misiones', distinct=True),
    ).order_by('-creado', '-id'))
    for juego in juegos:
        juego.info = minijuegos.PLANTILLAS_INFO[juego.plantilla]
        juego.meta_texto = minijuegos.descripcion_meta(juego)
        juego.mejor = PartidaJuego.objects.filter(juego=juego, terminada=True).select_related('alumno').order_by(
            '-puntaje', 'inicio').first()
        juego.lista_misiones = list(juego.misiones.select_related('clase', 'nivel'))
        juego.datos = minijuegos.datos_juego(juego)
        juego.datos_id = f'juego-data-{juego.id}'
    return render(request, 'Profesor/juegos.html', {
        'juegos': juegos,
        'plantillas': minijuegos.PLANTILLAS_INFO,
        'seccion': 'juegos',
    })


@login_required
def juego_form(request, pk=None):
    juego = get_object_or_404(Juego, pk=pk) if pk else None
    inicial = {}
    if not juego:
        plantilla = request.GET.get('plantilla') if request.GET.get('plantilla') in minijuegos.PLANTILLAS_INFO else 'meteoros'
        inicial = {'plantilla': plantilla, 'icono': minijuegos.PLANTILLAS_INFO[plantilla]['emoji'],
                   'palabras': '\n'.join(minijuegos.TEMAS_PALABRAS['computadora'][2]),
                   **campos_clasifica(minijuegos.configuracion_clasifica({'tema': 'seguridad'}))}
        inicial['tema_clasifica'] = 'seguridad'
        inicial['atajos'] = list(minijuegos.GRUPOS_ATAJOS['texto'][2])
        inicial['palabras_mensaje'] = '\n'.join(minijuegos.TEMAS_PALABRAS['robotica'][2][:8])
    form = JuegoForm(request.POST or None, instance=juego, initial=inicial)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            guardado = form.save()
            mensaje = f'Juego «{guardado.nombre}» guardado.'
            if form.cleaned_data.get('agregar_mapa'):
                nivel = Nivel.objects.select_related('clase').get(pk=form.cleaned_data['nivel_mapa'])
                mision = Mision.objects.create(
                    clase=nivel.clase, nivel=nivel, tipo='juego', juego=guardado, nombre=guardado.nombre,
                    descripcion=guardado.descripcion or minijuegos.PLANTILLAS_INFO[guardado.plantilla]['como'],
                    xp_recompensa=form.cleaned_data.get('xp_mapa') or 0,
                    monedas_recompensa=form.cleaned_data.get('monedas_mapa') or 0, orden=9999,
                )
                _acomodar(mision, Mision.objects.filter(nivel=nivel), 'final')
                mensaje += f' También quedó como misión en «{nivel.nombre}».'
        return _guardado(request, mensaje, reverse('juegos_lista'))
    return _formulario(request, 'Profesor/juego_form.html', {
        'form': form,
        'juego': juego,
        'plantillas': minijuegos.PLANTILLAS_INFO,
        'temas': {clave: {'emoji': e, 'nombre': n, 'palabras': p} for clave, (e, n, p) in minijuegos.TEMAS_PALABRAS.items()},
        'conjuntos': minijuegos.CONJUNTOS_TECLAS,
        'temas_clasifica': {clave: {'emoji': e, 'nombre': n, 'categorias': [
            {'nombre': c, 'emoji': ce, 'tarjetas': t} for c, ce, t in grupos]}
            for clave, (e, n, grupos) in minijuegos.TEMAS_CLASIFICA.items()},
        'dificultades': minijuegos.DIFICULTADES_ROBOT,
        'catalogo_atajos': {k: {'tecla': t, 'nombre': n, 'emoji': e, 'situaciones': sit}
                            for k, (t, n, e, sit) in minijuegos.ATAJOS.items()},
        'grupos_atajos': {k: {'emoji': e, 'nombre': n, 'atajos': a} for k, (e, n, a) in minijuegos.GRUPOS_ATAJOS.items()},
        'cifrados': minijuegos.CIFRADOS,
        'dificultades_rutas': minijuegos.DIFICULTADES_RUTAS,
        'dificultades_formato': minijuegos.DIFICULTADES_FORMATO,
        'frases_formato': minijuegos.FRASES_FORMATO,
        'velocidades': minijuegos.VELOCIDADES,
        'iconos': ICONOS_JUEGO,
        'misiones': list(juego.misiones.select_related('clase', 'nivel', 'nivel__mundo')) if juego else [],
        'seccion': 'juegos',
    })


@require_POST
@login_required
def alternar_arcade(request, pk):
    juego = get_object_or_404(Juego, pk=pk)
    juego.en_arcade = not juego.en_arcade
    juego.save(update_fields=['en_arcade'])
    return JsonResponse({'ok': True, 'activo': juego.en_arcade})
