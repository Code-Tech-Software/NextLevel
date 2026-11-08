"""Batalla en vivo: el profe la crea y la proyecta; los alumnos la juegan desde su dispositivo.

La lógica del juego (puntos, cambios de pantalla, premios y la señal en Redis) vive en `batallas.py`.
"""
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from . import batallas as motor
from .forms import BatallaForm
from .models import Batalla, Clase, JugadorBatalla, RespuestaBatalla
from .views import _es_ajax, alumno_en_sesion
from .views_profesor import _es_modal, _formulario, _siguiente

VISTA_PREVIA = '👀 Estás en la vista de alumno: así lo ven tus alumnos, pero el profe no juega.'
SESION_TERMINADA = 'Tu sesión terminó. Vuelve a entrar con tu PIN.'


def _entero(valor, por_defecto=None):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return por_defecto


# ========================
# PROFESOR
# ========================
@login_required
def batallas_lista(request):
    clases = list(Clase.objects.order_by('-activa', 'grado', 'grupo'))
    clase = next((c for c in clases if str(c.id) == request.GET.get('clase', '')), None)
    batallas = Batalla.objects.select_related('clase').annotate(
        n_jugadores=Count('jugadores', filter=Q(jugadores__contestadas__gt=0), distinct=True),
        n_preguntas=Count('preguntas', distinct=True),
    )
    if clase:
        batallas = batallas.filter(clase=clase)
    abiertas = [b for b in batallas.filter(estado__in=['sala', 'pregunta', 'resultado']) if b.abierta]
    pagina = Paginator(batallas.filter(estado='final').order_by('-terminada', '-id'), 15).get_page(request.GET.get('pagina'))

    ids = [b.id for b in pagina]
    totales = {f['batalla']: f for f in JugadorBatalla.objects.filter(batalla_id__in=ids).values('batalla')
               .annotate(aciertos=Sum('aciertos'), contestadas=Sum('contestadas'))}
    ganadores = {}
    for jugador in JugadorBatalla.objects.filter(batalla_id__in=ids, posicion=1).select_related('alumno', 'equipo'):
        ganadores.setdefault(jugador.batalla_id, []).append(jugador)
    for batalla in pagina:
        fila = totales.get(batalla.id) or {}
        batalla.pct = round(fila['aciertos'] * 100 / fila['contestadas']) if fila.get('contestadas') else None
        batalla.ganadores = ganadores.get(batalla.id, [])

    return render(request, 'Profesor/batallas.html', {
        'clases': clases, 'clase': clase, 'abiertas': abiertas, 'pagina': pagina, 'seccion': 'batallas',
        'hay_preguntas': Clase.objects.filter(misiones__preguntas__isnull=False).exists(),
    })


@login_required
def batalla_nueva(request):
    origen = request.POST.get('clase') or request.GET.get('clase')
    clase = Clase.objects.filter(pk=origen).first() if str(origen or '').isdigit() else None
    if not clase:
        clase = (Clase.objects.filter(misiones__preguntas__isnull=False).distinct().order_by('-activa', 'grado', 'grupo').first()
                 or Clase.objects.order_by('-activa', 'grado', 'grupo').first())
    mundos = motor.misiones_con_preguntas(clase) if clase else []
    form = BatallaForm(request.POST or None, mundos=mundos, initial={
        'clase': clase, 'cantidad': 10, 'segundos': 20, 'premios': 'normal', 'modo': 'individual', 'mezclar': True,
    })
    if request.method == 'POST' and form.is_valid():
        datos = form.cleaned_data
        try:
            batalla = motor.crear_batalla(
                datos['clase'], datos['misiones'], cantidad=datos['cantidad'], segundos=datos['segundos'],
                mezclar=datos['mezclar'], por_equipos=datos['modo'] == 'equipos', premios=datos['premios'],
                titulo=datos['titulo'].strip(),
            )
        except ValueError as error:
            form.add_error('misiones', str(error))
        else:
            # Sin mensaje emergente: el proyector ya explica cómo entrar y la ventana taparía la sala de espera
            destino = reverse('batalla_proyector', args=[batalla.id])
            if _es_modal(request):
                return JsonResponse({'ok': True, 'redirect': destino, 'navegar': True})
            return redirect(destino)

    elegidas = {int(m) for m in form['misiones'].value() or [] if str(m).isdigit()}
    return _formulario(request, 'Profesor/batalla_form.html', {
        'form': form, 'clase': clase, 'mundos': mundos, 'elegidas': elegidas,
        'clases': Clase.objects.order_by('-activa', 'grado', 'grupo'),
        'abierta': Batalla.objects.abiertas().filter(clase=clase).first() if clase else None,
        'tiene_equipos': bool(clase and clase.equipos.exists()),
        'tiempos': motor.TIEMPOS, 'premios': motor.PREMIOS, 'cantidades': motor.CANTIDADES,
        'seccion': 'batallas',
    })


@login_required
def batalla_proyector(request, pk):
    batalla = get_object_or_404(Batalla.objects.select_related('clase'), pk=pk)
    return render(request, 'Profesor/batalla_proyector.html', {
        'batalla': batalla, 'clase': batalla.clase, 'estado': motor.estado_profesor(batalla),
        'url_entrar': request.build_absolute_uri(reverse('lista_alumnos', args=[batalla.clase_id])),
        'url_control': request.build_absolute_uri(reverse('batalla_control', args=[batalla.id])),
        'sitio': request.get_host(),
    })


@login_required
def batalla_control(request, pk):
    """El control remoto en el celular del profe: maneja la batalla mientras camina por el salón."""
    batalla = get_object_or_404(Batalla.objects.select_related('clase'), pk=pk)
    return render(request, 'Profesor/batalla_control.html', {
        'batalla': batalla, 'clase': batalla.clase, 'estado': motor.estado_profesor(batalla),
    })


@never_cache
@login_required
def batalla_estado(request, pk):
    batalla = get_object_or_404(Batalla, pk=pk)
    ficha = request.GET.get('ficha')
    # Con Redis se sabe sin calcular nada si alguien se unió o contestó desde la última consulta
    if ficha and motor.memoria.disponible and ficha == f'{batalla.version}.{motor.actividad(batalla.id) or 0}':
        return JsonResponse({'cambio': False})
    return JsonResponse({'cambio': True, 'estado': motor.estado_profesor(batalla)})


@require_POST
@login_required
def batalla_accion(request, pk):
    batalla = get_object_or_404(Batalla, pk=pk)
    accion = request.POST.get('accion')
    version = _entero(request.POST.get('v'), batalla.version)
    if accion in ('empezar', 'siguiente'):
        motor.siguiente(batalla, version)
    elif accion == 'revelar':
        motor.revelar(batalla, version)
    elif accion == 'terminar':
        motor.terminar(batalla, version)
    elif accion == 'quitar':
        motor.quitar_jugador(batalla, _entero(request.POST.get('jugador'), 0))
    else:
        return JsonResponse({'ok': False, 'mensaje': 'Acción desconocida.'}, status=400)
    batalla.refresh_from_db()
    if not _es_ajax(request):  # el botón «Terminar» de la lista es un formulario normal
        if accion == 'terminar':
            messages.success(request, f'«{batalla.titulo}» terminó y se repartieron los premios.')
        return redirect(_siguiente(request, reverse('batallas_lista')))
    return JsonResponse({'ok': True, 'estado': motor.estado_profesor(batalla)})


@require_POST
@login_required
def batalla_repetir(request, pk):
    nueva = motor.repetir(get_object_or_404(Batalla, pk=pk))
    # Desde el celular se sigue en el control; el proyector se pasa solo a la nueva batalla
    return redirect('batalla_control' if request.POST.get('desde') == 'control' else 'batalla_proyector', pk=nueva.pk)


@login_required
def batalla_resumen(request, pk):
    batalla = get_object_or_404(Batalla.objects.select_related('clase'), pk=pk)
    jugadores = sorted(batalla.jugadores.select_related('alumno', 'equipo'), key=motor.orden_jugador)
    preguntas = list(batalla.preguntas.order_by('orden'))
    marcas = {(j, o): c for j, o, c in RespuestaBatalla.objects.filter(pregunta__batalla=batalla)
              .values_list('jugador_id', 'pregunta__orden', 'correcta')}
    for jugador in jugadores:
        jugador.marcas = [marcas.get((jugador.id, p.orden)) for p in preguntas]
        jugador.pct = round(jugador.aciertos * 100 / jugador.contestadas) if jugador.contestadas else None
    resumen = motor.resumen_preguntas(batalla)

    # Misiones para repasar: las que tuvieron preguntas con menos de 60 % de aciertos
    repasar = {}
    for fila in resumen:
        if fila['pct'] < 60 and fila['mision_id']:
            repasar.setdefault(fila['mision_id'], {'nombre': fila['mision'], 'preguntas': 0})['preguntas'] += 1
    participaron = [j for j in jugadores if j.contestadas]
    respuestas = sum(j.contestadas for j in participaron)
    return render(request, 'Profesor/batalla_resumen.html', {
        'batalla': batalla, 'clase': batalla.clase, 'jugadores': jugadores, 'preguntas': preguntas,
        'resumen': resumen, 'repasar': list(repasar.values()), 'participaron': len(participaron),
        'pct': round(sum(j.aciertos for j in participaron) * 100 / respuestas) if respuestas else None,
        'equipos': motor.ranking_equipos(participaron) if batalla.por_equipos else [],
        'seccion': 'batallas',
    })


# ========================
# ALUMNO
# ========================
def _alumno_de_batalla(vista):
    """Como alumno_requerido, pero la batalla se puede jugar aunque la clase esté cerrada: abrirla es decisión del
    profe. La vista de alumno del profe solo mira."""

    @wraps(vista)
    def envoltura(request, clase_id, *args, **kwargs):
        clase = get_object_or_404(Clase, id=clase_id)
        alumno = alumno_en_sesion(request, clase)
        if not alumno:
            if _es_ajax(request) or request.method == 'POST':
                return JsonResponse({'ok': False, 'salir': True, 'mensaje': SESION_TERMINADA}, status=403)
            return redirect('lista_alumnos', clase_id=clase.id)
        if alumno.es_prueba and request.method == 'POST':
            return JsonResponse({'ok': False, 'mensaje': VISTA_PREVIA}, status=403)
        return vista(request, alumno, clase, *args, **kwargs)

    return envoltura


@never_cache
@_alumno_de_batalla
def batalla_alumno(request, alumno, clase):
    datos = motor.senal(clase.id, fresca=True)
    if not datos.get('id') and not clase.acceso_abierto() and not alumno.es_prueba:
        return redirect('cuenta_cerrada', clase_id=clase.id)
    return render(request, 'Alumnos/batalla.html', {
        'alumno': alumno, 'clase': clase, 'estado': motor.estado_alumno(datos, alumno),
    })


@never_cache
def batalla_alumno_estado(request, clase_id):
    """La consulta de cada segundo. Lo normal es contestar «sin cambios» sin tocar la base de datos (con Redis)."""
    sesion = request.session
    if not sesion.get('alumno_id') or clase_id not in (sesion.get('clase_id'), sesion.get('vista_alumno')):
        return JsonResponse({'ok': False, 'salir': True, 'mensaje': SESION_TERMINADA}, status=403)
    datos = motor.senal(clase_id)
    if motor.revelar_si_vencida(datos):
        datos = motor.senal(clase_id, fresca=True)
    if request.GET.get('senal'):
        # Las demás páginas del alumno solo quieren saber si hay batalla para mostrar el aviso
        return JsonResponse({'en_juego': motor.en_juego(datos), 'titulo': datos.get('titulo', '')})
    if request.GET.get('ficha') == motor.ficha(datos):
        return JsonResponse({'cambio': False})
    clase = get_object_or_404(Clase, id=clase_id)
    alumno = alumno_en_sesion(request, clase)
    if not alumno:
        return JsonResponse({'ok': False, 'salir': True, 'mensaje': SESION_TERMINADA}, status=403)
    return JsonResponse({'cambio': True, 'estado': motor.estado_alumno(datos, alumno)})


def _batalla_en_juego(clase):
    datos = motor.senal(clase.id, fresca=True)
    batalla = Batalla.objects.filter(pk=datos['id']).first() if motor.en_juego(datos) else None
    return datos, batalla


@require_POST
@_alumno_de_batalla
def batalla_unirse(request, alumno, clase):
    datos, batalla = _batalla_en_juego(clase)
    if not batalla:
        return JsonResponse({'ok': False, 'mensaje': 'Ya no hay una batalla abierta.',
                             'estado': motor.estado_alumno(datos, alumno)})
    motor.unir(batalla, alumno)
    return JsonResponse({'ok': True, 'estado': motor.estado_alumno(datos, alumno)})


@require_POST
@_alumno_de_batalla
def batalla_responder(request, alumno, clase):
    datos, batalla = _batalla_en_juego(clase)
    indice, opcion = _entero(request.POST.get('indice')), _entero(request.POST.get('opcion'))
    if indice is None or opcion is None:
        return JsonResponse({'ok': False, 'mensaje': 'Respuesta incompleta.'}, status=400)
    if not batalla:
        return JsonResponse({'ok': False, 'mensaje': 'La batalla ya terminó.', 'estado': motor.estado_alumno(datos, alumno)})
    ok, mensaje = motor.responder(batalla, alumno, indice, opcion)
    return JsonResponse({'ok': ok, 'mensaje': mensaje, 'estado': motor.estado_alumno(datos, alumno)})
