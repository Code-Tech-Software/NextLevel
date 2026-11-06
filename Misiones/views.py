"""Vistas del lado del alumno (la experiencia gamificada)."""
import time
from datetime import timedelta
from functools import wraps

from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from . import gamificacion as juego
from .minijuegos import datos_juego
from .models import (
    Alumno, ArticuloTienda, Clase, CompraAlumno, Mision, Nivel, OpcionRespuesta, ProgresoMision,
    RespuestaAlumno,
)

MAX_INTENTOS_PIN = 5
BLOQUEO_PIN_SEGUNDOS = 60
TAMANO_MAX_EVIDENCIA = 8 * 1024 * 1024


def home_redirect(request):
    return HttpResponseRedirect('/seleccionar-clase/')


MENSAJE_VISTA_PREVIA = '👀 Estás en la vista de alumno: puedes verlo y probarlo todo, pero aquí no se guarda nada.'


def alumno_en_sesion(request, clase):
    """El alumno que entró con su PIN o, si el profe abrió la «vista de alumno» de esta clase, el alumno de prueba."""
    alumno_id = request.session.get('alumno_id')
    if not alumno_id:
        return None
    if request.session.get('vista_alumno') == clase.id and request.user.is_authenticated:
        return Alumno.todos.filter(id=alumno_id, es_prueba=True).first()
    return Alumno.objects.filter(id=alumno_id, activo=True, clases=clase).first()


def permite_vista_previa(vista):
    """Marca las acciones POST que la vista de alumno sí puede usar (las simula sin guardar)."""
    vista.permite_vista_previa = True
    return vista


def alumno_requerido(vista):
    """Inyecta (alumno, clase) y regresa a la selección de jugador si no hay sesión válida.

    Si el profe cerró la clase (o está fuera de su horario), el alumno solo puede ver la pantalla de su cuenta.
    En la vista de alumno del profe todo está abierto, pero las acciones que guardan algo no se hacen.
    """

    @wraps(vista)
    def envoltura(request, clase_id, *args, **kwargs):
        clase = get_object_or_404(Clase, id=clase_id)
        alumno = alumno_en_sesion(request, clase)
        if not alumno:
            if _es_ajax(request):
                return JsonResponse({'ok': False, 'mensaje': 'Tu sesión terminó.'}, status=403)
            return redirect('lista_alumnos', clase_id=clase.id)
        if alumno.es_prueba:
            if request.method == 'POST' and not getattr(vista, 'permite_vista_previa', False):
                if _es_ajax(request):
                    return JsonResponse({'ok': False, 'mensaje': MENSAJE_VISTA_PREVIA}, status=403)
                messages.info(request, MENSAJE_VISTA_PREVIA)
                return redirect(_volver(request, reverse('dashboard_alumno', args=[clase.id])))
            return vista(request, alumno, clase, *args, **kwargs)
        if not clase.acceso_abierto():
            if _es_ajax(request):
                return JsonResponse({'ok': False, 'mensaje': '🔒 La plataforma está cerrada por ahora.'}, status=403)
            return redirect('cuenta_cerrada', clase_id=clase.id)
        juego.actualizar_racha(alumno, clase)
        return vista(request, alumno, clase, *args, **kwargs)

    return envoltura


def _es_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def _volver(request, por_defecto):
    """La página de donde vino la petición (si es de este sitio)."""
    for destino in (request.POST.get('next'), request.headers.get('referer')):
        if destino and url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()},
                                                       require_https=request.is_secure()):
            return destino
    return por_defecto


# ========================
# LOBBY Y ACCESO
# ========================
def seleccionar_clase(request):
    clases = Clase.objects.filter(activa=True).annotate(
        total_alumnos=Count('alumnos', filter=Q(alumnos__activo=True), distinct=True),
        total_mundos=Count('mundos', distinct=True),
    ).order_by('anio', 'grado', 'grupo')
    return render(request, 'Alumnos/seleccionar_clase.html', {'clases': clases})


def lista_alumnos(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    alumnos = clase.alumnos.filter(activo=True).order_by('apellido', 'nombre')
    return render(request, 'Alumnos/lista_alumnos.html', {
        'clase': clase,
        'alumnos': alumnos,
        'pin_error': request.session.pop('pin_error', None),
        # El QR de la credencial abre directo la tarjeta del alumno
        'jugador': int(request.GET['jugador']) if request.GET.get('jugador', '').isdigit() else None,
    })


@require_POST
def ingresar_pin(request, clase_id, alumno_id):
    clase = get_object_or_404(Clase, id=clase_id)
    alumno = get_object_or_404(Alumno, id=alumno_id, activo=True, clases=clase)

    clave = f'pin_fallos_{alumno.id}'
    fallos, desde = request.session.get(clave, [0, 0])
    if fallos >= MAX_INTENTOS_PIN and time.time() - desde < BLOQUEO_PIN_SEGUNDOS:
        espera = int(BLOQUEO_PIN_SEGUNDOS - (time.time() - desde))
        messages.error(request, f'Demasiados intentos. Espera {espera} segundos e inténtalo otra vez.')
        return redirect('lista_alumnos', clase_id=clase.id)

    if alumno.pin == request.POST.get('pin', '').strip():
        request.session.pop(clave, None)
        request.session['alumno_id'] = alumno.id
        request.session['clase_id'] = clase.id
        if not clase.acceso_abierto():
            # Con la clase cerrada no cuenta como visita: ni racha ni misión del día
            return redirect('cuenta_cerrada', clase_id=clase.id)
        juego.actualizar_racha(alumno, clase)
        juego.registrar_evento(alumno, 'login', clase=clase)
        return redirect('dashboard_alumno', clase_id=clase.id)

    if time.time() - desde >= BLOQUEO_PIN_SEGUNDOS:
        fallos = 0
    request.session[clave] = [fallos + 1, time.time()]
    request.session['pin_error'] = alumno.id
    return redirect('lista_alumnos', clase_id=clase.id)


def cuenta_cerrada(request, clase_id):
    """Lo único que ve el alumno mientras la clase está cerrada: el resumen de su cuenta, sin poder jugar."""
    clase = get_object_or_404(Clase, id=clase_id)
    alumno = alumno_en_sesion(request, clase)
    if not alumno:
        return redirect('lista_alumnos', clase_id=clase.id)
    # En la vista de alumno el profe puede ver esta pantalla aunque la clase esté abierta
    if clase.acceso_abierto() and not alumno.es_prueba:
        return redirect('dashboard_alumno', clase_id=clase.id)

    misiones = list(Mision.objects.filter(clase=clase, activa=True).select_related('nivel'))
    aprobadas = set(ProgresoMision.objects.filter(alumno=alumno, mision__clase=clase, mision__activa=True,
                                                  estado='aprobado').values_list('mision_id', flat=True))
    mundos = []
    for mundo in clase.mundos.all():
        ids = [m.id for m in misiones if m.nivel.mundo_id == mundo.id]
        if ids:
            hechas = sum(1 for i in ids if i in aprobadas)
            mundos.append({'mundo': mundo, 'tema': juego.TEMA_INFO.get(mundo.tema), 'hechas': hechas,
                           'total': len(ids), 'pct': round(hechas * 100 / len(ids))})

    return render(request, 'Alumnos/cuenta_cerrada.html', {
        'alumno': alumno,
        'clase': clase,
        'rango': alumno.rango,
        'aprobadas': len(aprobadas),
        'total_misiones': len(misiones),
        'mundos': mundos,
        'en_revision': ProgresoMision.objects.filter(alumno=alumno, mision__clase=clase, estado='pendiente').count(),
        'premios_pendientes': alumno.compras.filter(estado='pendiente').select_related('articulo')[:5],
        'logros': alumno.logros.select_related('logro')[:8],
        'total_logros': alumno.logros.count(),
        'equipo': juego.equipo_de(alumno, clase),
        'proxima': clase.proxima_apertura(),
    })


def salir_alumno(request):
    clase_id = request.session.pop('clase_id', None)
    request.session.pop('alumno_id', None)
    vista = request.session.pop('vista_alumno', None)
    regreso = request.session.pop('vista_alumno_regreso', None)
    if vista and request.user.is_authenticated:
        # El profe termina la vista de alumno y vuelve a su panel
        return redirect(regreso or reverse('clase_detalle', args=[vista]))
    if clase_id:
        return redirect('lista_alumnos', clase_id=clase_id)
    return redirect('seleccionar_clase')


# ========================
# MAPA
# ========================
def _segundos_para_medianoche():
    ahora = timezone.localtime()
    manana = (ahora + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return int((manana - ahora).total_seconds())


@alumno_requerido
def dashboard_alumno(request, alumno, clase):
    juego.registrar_evento(alumno, 'login', clase=clase)
    ruta = juego.construir_ruta(alumno, clase)
    ranking = juego.ranking_clase(clase, 'semana')
    mi_posicion = next((a.posicion for a in ranking if a.id == alumno.id), None)

    equipos = juego.ranking_equipos(clase)
    mi_equipo = next((e for e in equipos if any(m.id == alumno.id for m in e.lista_miembros)), None)
    return render(request, 'Alumnos/dashboard.html', {
        'alumno': alumno,
        'clase': clase,
        'ruta': ruta,
        'equipos': equipos,
        'mi_equipo': mi_equipo,
        'metas': juego.metas_visibles(clase),
        'diarias': juego.misiones_del_dia(alumno, clase),
        'segundos_reinicio': _segundos_para_medianoche(),
        'podio': ranking[:3],
        'mi_posicion': mi_posicion,
        'total_jugadores': len(ranking),
        'logros_recientes': alumno.logros.select_related('logro')[:4],
        'avance': juego.avance_del_grupo(clase) if alumno.es_prueba else None,
        'seccion': 'mapa',
    })


@alumno_requerido
def ver_mundo(request, alumno, clase, mundo_id):
    ruta = juego.construir_ruta(alumno, clase)
    mundo = next((m for m in ruta['mundos'] if (m['mundo'].id if m['mundo'] else 0) == mundo_id), None)
    if not mundo:
        messages.info(request, 'Ese mundo no existe todavía.')
        return redirect('dashboard_alumno', clase_id=clase.id)

    indice = ruta['mundos'].index(mundo)
    return render(request, 'Alumnos/mundo.html', {
        'alumno': alumno,
        'clase': clase,
        'datos': mundo,
        'anterior': ruta['mundos'][indice - 1] if indice > 0 else None,
        'siguiente': ruta['mundos'][indice + 1] if indice + 1 < len(ruta['mundos']) else None,
        'avance': juego.avance_del_grupo(clase) if alumno.es_prueba else None,
        'seccion': 'mapa',
    })


@alumno_requerido
def ver_mision(request, alumno, clase, mision_id):
    mision = get_object_or_404(Mision.objects.select_related('nivel', 'nivel__mundo'), id=mision_id, clase=clase)
    ruta = juego.construir_ruta(alumno, clase)
    mundo, nivel, item = juego.buscar_en_ruta(ruta, mision.id)
    if not item and alumno.es_prueba:
        # Misión oculta: el profe puede ver cómo quedará antes de publicarla
        mundo = next((m for m in ruta['mundos'] if m['mundo'] and m['mundo'].id == mision.nivel.mundo_id), None)
        item = {'progreso': None, 'estado': 'nuevo', 'desbloqueada': True}
    if not item or (not item['desbloqueada'] and item['estado'] != 'aprobado'):
        messages.warning(request, '🔒 Esta misión aún está bloqueada. ¡Completa las anteriores primero!')
        return redirect('dashboard_alumno', clase_id=clase.id)

    progreso = item['progreso']
    preguntas = mision.preguntas.prefetch_related('opciones') if mision.tipo == 'cuestionario' else None
    respuestas = {}
    if progreso and mision.tipo == 'cuestionario':
        respuestas = {
            r.pregunta_id: r for r in progreso.respuestas_detalladas.select_related('opcion_seleccionada')
        }

    return render(request, 'Alumnos/mision_detalle.html', {
        'alumno': alumno,
        'clase': clase,
        'mision': mision,
        'progreso': progreso,
        'preguntas': preguntas,
        'respuestas': respuestas,
        'mundo': mundo,
        'info': juego.TIPO_INFO.get(mision.tipo),
        'juego_datos': datos_juego(mision.juego) if mision.tipo == 'juego' and mision.juego and mision.juego.activo else None,
        'resultado': request.session.pop('resultado_mision', None),
        'avance': _avance_de_mision(clase, mision) if alumno.es_prueba else None,
        'seccion': 'mapa',
    })


def _avance_de_mision(clase, mision):
    """Quién completó la misión y quién va en ella, para el panel que ve el profe en la vista de alumno."""
    grupo = juego.avance_del_grupo(clase)
    datos = grupo['misiones'].get(mision.id)
    if datos is None:
        # Misión oculta: nadie «va» en ella, pero puede haber alumnos que ya la hicieron
        datos = {'aqui': [], 'completaron': [
            {'alumno': p.alumno, 'progreso': p}
            for p in ProgresoMision.objects.filter(mision=mision, estado='aprobado', alumno__activo=True,
                                                   alumno__clases=clase).select_related('alumno')]}
    pendientes = [d for d in datos['aqui'] if d['estado'] == 'pendiente']
    por_corregir = [d for d in datos['aqui'] if d['estado'] == 'rechazado']
    empezando = [d for d in datos['aqui'] if d['estado'] not in ('pendiente', 'rechazado')]
    hechos = len(datos['completaron'])
    return {
        'total': grupo['total'], 'completaron': datos['completaron'], 'pendientes': pendientes,
        'por_corregir': por_corregir, 'empezando': empezando,
        'no_llegan': max(grupo['total'] - hechos - len(datos['aqui']), 0),
        'pct': int(hechos * 100 / grupo['total']) if grupo['total'] else 0,
    }


@require_POST
@alumno_requerido
@permite_vista_previa
def marcar_completada(request, alumno, clase, mision_id):
    if alumno.es_prueba:
        return _simular_mision(request, clase, get_object_or_404(Mision, id=mision_id, clase=clase))
    mision = get_object_or_404(Mision, id=mision_id, clase=clase, activa=True)
    ruta = juego.construir_ruta(alumno, clase)
    _, _, item = juego.buscar_en_ruta(ruta, mision.id)
    if not item or not item['desbloqueada']:
        messages.warning(request, '🔒 Esta misión aún está bloqueada.')
        return redirect('dashboard_alumno', clase_id=clase.id)

    progreso = item['progreso']
    if progreso and progreso.estado == 'aprobado':
        messages.info(request, '¡Ya completaste esta misión!')
        return redirect('ver_mision', clase_id=clase.id, mision_id=mision.id)
    if progreso and progreso.estado == 'pendiente' and not mision.es_automatica:
        messages.info(request, 'Tu trabajo ya está en revisión. ¡Paciencia, aventurero!')
        return redirect('ver_mision', clase_id=clase.id, mision_id=mision.id)

    if mision.tipo == 'presencial':
        messages.info(request, 'Esta misión se completa en clase. ¡El profe la marcará cuando la termines!')
        return redirect('ver_mision', clase_id=clase.id, mision_id=mision.id)
    if mision.tipo == 'juego':
        messages.info(request, '🎮 Esta misión se completa jugando. ¡Presiona «Jugar»!')
        return redirect('ver_mision', clase_id=clase.id, mision_id=mision.id)

    if mision.tipo == 'cuestionario':
        return _resolver_cuestionario(request, alumno, clase, mision, progreso)
    if mision.tipo == 'video':
        progreso = progreso or ProgresoMision(alumno=alumno, mision=mision)
        monedas = juego.calificar(progreso, 100, avisar=False)
        juego.registrar_evento(alumno, 'misiones', clase=clase)
        request.session['resultado_mision'] = {
            'estrellas': 3, 'monedas': monedas, 'xp': mision.xp_recompensa, 'calificacion': '10.0',
        }
        return redirect('ver_mision', clase_id=clase.id, mision_id=mision.id)

    # Misiones que revisa el profesor
    evidencia = request.FILES.get('evidencia')
    texto = request.POST.get('respuesta_texto', '').strip()
    if evidencia:
        if not (evidencia.content_type or '').startswith('image/'):
            messages.error(request, 'La evidencia debe ser una foto o imagen.')
            return redirect('ver_mision', clase_id=clase.id, mision_id=mision.id)
        if evidencia.size > TAMANO_MAX_EVIDENCIA:
            messages.error(request, 'La foto es muy pesada (máximo 8 MB).')
            return redirect('ver_mision', clase_id=clase.id, mision_id=mision.id)
    if mision.tipo == 'evidencia' and not evidencia:
        messages.error(request, '📸 Esta misión necesita una foto de tu trabajo.')
        return redirect('ver_mision', clase_id=clase.id, mision_id=mision.id)
    if mision.tipo == 'texto' and not texto:
        messages.error(request, '✍️ Escribe tu respuesta antes de enviar.')
        return redirect('ver_mision', clase_id=clase.id, mision_id=mision.id)

    if progreso:
        progreso.intentos += 1
    else:
        progreso = ProgresoMision(alumno=alumno, mision=mision)
    progreso.estado = 'pendiente'
    progreso.revisado = False
    progreso.respuesta_texto = texto
    if evidencia:
        progreso.evidencia = evidencia
    progreso.save()

    juego.registrar_evento(alumno, 'misiones', clase=clase)
    juego.registrar_evento(alumno, 'evidencias', clase=clase)
    messages.success(request, f'¡Excelente! "{mision.nombre}" fue enviada a revisión. 🚀')
    return redirect('dashboard_alumno', clase_id=clase.id)


def _simular_mision(request, clase, mision):
    """Vista de alumno: el profe ve lo que le saldría a un alumno, sin guardar progreso ni mandar nada a revisión."""
    volver = redirect('ver_mision', clase_id=clase.id, mision_id=mision.id)
    if mision.tipo == 'cuestionario':
        respuestas, obtenidos, totales = [], 0, 0
        for pregunta in mision.preguntas.prefetch_related('opciones'):
            opciones = list(pregunta.opciones.all())
            elegida = next((o for o in opciones if str(o.id) == request.POST.get(f'pregunta_{pregunta.id}')), None)
            correcta = next((o for o in opciones if o.es_correcta), None)
            totales += pregunta.puntos
            if elegida and elegida.es_correcta:
                obtenidos += pregunta.puntos
            respuestas.append({
                'pregunta': pregunta.texto,
                'respondio': elegida.texto if elegida else '',
                'bien': bool(elegida and elegida.es_correcta),
                'correcta': correcta.texto if correcta else '',
            })
        porcentaje = int(obtenidos * 100 / totales) if totales else 0
    elif mision.tipo == 'video':
        porcentaje, respuestas = 100, []
    else:
        # Las misiones que revisa el profe (foto, texto, enlace), las del salón y los minijuegos
        messages.info(request, '👀 Vista de alumno: así se ve esta misión. No se envió nada a Revisiones.')
        return volver

    request.session['resultado_mision'] = {
        'estrellas': 3 if porcentaje >= 90 else 2 if porcentaje >= 70 else 1,
        'monedas': int(porcentaje / 100 * mision.monedas_recompensa),
        'xp': mision.xp_recompensa,
        'calificacion': f'{porcentaje / 10:.1f}',
        'prueba': True,
        'respuestas': respuestas,
    }
    return volver


def _resolver_cuestionario(request, alumno, clase, mision, progreso):
    preguntas = list(mision.preguntas.prefetch_related('opciones'))
    puntos_totales = sum(p.puntos for p in preguntas)

    progreso = progreso or ProgresoMision(alumno=alumno, mision=mision)
    if progreso.pk:
        progreso.intentos += 1
        RespuestaAlumno.objects.filter(progreso=progreso).delete()
    progreso.save()

    obtenidos = 0
    for pregunta in preguntas:
        opcion_id = request.POST.get(f'pregunta_{pregunta.id}')
        opcion = next((o for o in pregunta.opciones.all() if str(o.id) == opcion_id), None)
        if not opcion:
            continue
        RespuestaAlumno.objects.create(progreso=progreso, pregunta=pregunta, opcion_seleccionada=opcion)
        if opcion.es_correcta:
            obtenidos += pregunta.puntos

    porcentaje = int(obtenidos * 100 / puntos_totales) if puntos_totales else 0
    monedas = juego.calificar(progreso, porcentaje, avisar=False)

    juego.registrar_evento(alumno, 'misiones', clase=clase)
    juego.registrar_evento(alumno, 'cuestionarios', clase=clase)
    if porcentaje >= 100:
        juego.registrar_evento(alumno, 'perfecto', clase=clase)
        juego.verificar_logros(alumno)

    request.session['resultado_mision'] = {
        'estrellas': progreso.estrellas,
        'monedas': monedas,
        'xp': mision.xp_recompensa,
        'calificacion': f'{porcentaje / 10:.1f}',
    }
    return redirect('ver_mision', clase_id=clase.id, mision_id=mision.id)


@require_POST
@alumno_requerido
def abrir_cofre(request, alumno, clase, nivel_id):
    nivel = get_object_or_404(Nivel, id=nivel_id, clase=clase)
    monedas = juego.abrir_cofre(alumno, nivel)
    if monedas is None:
        respuesta = {'ok': False, 'mensaje': 'Este cofre todavía no se puede abrir.'}
    else:
        respuesta = {'ok': True, 'monedas': monedas, 'total': alumno.monedas, 'xp': alumno.xp_total}
    if _es_ajax(request):
        return JsonResponse(respuesta)
    if respuesta['ok']:
        messages.success(request, f'¡Abriste el cofre y encontraste {monedas} monedas! 💰')
    return redirect(request.POST.get('next') or reverse('dashboard_alumno', args=[clase.id]))


@require_POST
@alumno_requerido
def reclamar_diaria(request, alumno, clase, diaria_id):
    diaria = juego.reclamar_diaria(alumno, diaria_id, clase)
    if diaria:
        respuesta = {
            'ok': True, 'titulo': diaria.titulo, 'monedas': diaria.recompensa_monedas, 'xp': diaria.recompensa_xp,
            'total': alumno.monedas, 'xp_total': alumno.xp_total,
        }
    else:
        respuesta = {'ok': False, 'mensaje': 'Esta misión del día aún no está lista.'}
    if _es_ajax(request):
        return JsonResponse(respuesta)
    if diaria:
        messages.success(request, f'¡Recompensa reclamada! +{diaria.recompensa_monedas} monedas')
    return redirect('dashboard_alumno', clase_id=clase.id)


@require_POST
@alumno_requerido
@permite_vista_previa
def leer_notificaciones(request, alumno, clase):
    ids = request.POST.getlist('ids')
    notificaciones = alumno.notificaciones.filter(leida=False)
    if ids:
        notificaciones = notificaciones.filter(id__in=[i for i in ids if i.isdigit()])
    notificaciones.update(leida=True)
    return JsonResponse({'ok': True})


# ========================
# TIENDA
# ========================
@alumno_requerido
def tienda_alumno(request, alumno, clase):
    juego.registrar_evento(alumno, 'tienda', clase=clase)
    articulos = list(ArticuloTienda.objects.filter(activo=True).order_by('-destacado', 'costo_monedas'))
    compradas = dict(
        CompraAlumno.objects.filter(alumno=alumno).exclude(estado='cancelado')
        .values_list('articulo_id').annotate(total=Count('id'))
    )
    for articulo in articulos:
        articulo.compradas = compradas.get(articulo.id, 0)
        articulo.limite_alcanzado = bool(
            articulo.limite_por_alumno and articulo.compradas >= articulo.limite_por_alumno
        )
        articulo.nivel_bloqueado = alumno.nivel < articulo.nivel_requerido
        articulo.faltan = max(0, articulo.costo_monedas - alumno.monedas)
        articulo.puede_comprar = not (
            articulo.agotado or articulo.limite_alcanzado or articulo.nivel_bloqueado or articulo.faltan
        )

    return render(request, 'Alumnos/tienda.html', {
        'alumno': alumno,
        'clase': clase,
        'articulos': articulos,
        'destacados': [a for a in articulos if a.destacado][:3],
        'mis_compras': alumno.compras.select_related('articulo').order_by('-fecha_compra')[:30],
        'por_entregar': alumno.compras.filter(estado='pendiente').count(),
        'seccion': 'tienda',
    })


@require_POST
@alumno_requerido
def comprar_articulo(request, alumno, clase, articulo_id):
    articulo = get_object_or_404(ArticuloTienda, id=articulo_id)
    ok, mensaje = juego.comprar(alumno, articulo)
    (messages.success if ok else messages.error)(request, mensaje)
    return redirect('tienda_alumno', clase_id=clase.id)


# ========================
# PERFIL, LOGROS Y RANKING
# ========================
@alumno_requerido
def mi_progreso(request, alumno, clase):
    logros, stats = juego.progreso_logros(alumno)
    progresos = ProgresoMision.objects.filter(alumno=alumno, mision__clase=clase).select_related(
        'mision', 'mision__nivel', 'mision__nivel__mundo'
    ).order_by('mision__nivel__mundo__orden', 'mision__nivel__orden', 'mision__orden')
    avatares = (
        alumno.compras.filter(articulo__tipo='avatar').exclude(estado='cancelado').exclude(articulo__imagen='')
        .select_related('articulo').order_by('-fecha_compra')
    )
    vistos, avatares_unicos = set(), []
    for compra in avatares:
        if compra.articulo_id not in vistos:
            vistos.add(compra.articulo_id)
            avatares_unicos.append(compra)

    return render(request, 'Alumnos/mi_progreso.html', {
        'alumno': alumno,
        'clase': clase,
        'stats': stats,
        'logros': logros,
        'logros_obtenidos': sum(1 for l in logros if l['obtenido']),
        'progresos': progresos,
        'movimientos': alumno.movimientos.all()[:40],
        'avatares': avatares_unicos,
        'rangos': juego.info_rangos(),
        'mi_equipo': juego.equipo_de(alumno, clase),
        'seccion': 'perfil',
    })


@require_POST
@alumno_requerido
def equipar_avatar(request, alumno, clase, compra_id):
    if compra_id == 0:
        alumno.avatar = None
        alumno.save(update_fields=['avatar'])
        messages.success(request, '¡Volviste a tu robot clásico! 🤖')
    else:
        compra = get_object_or_404(CompraAlumno, id=compra_id, alumno=alumno, articulo__tipo='avatar')
        if compra.estado == 'cancelado' or not compra.articulo.imagen:
            messages.error(request, 'No puedes usar ese avatar.')
        else:
            alumno.avatar = compra.articulo.imagen
            alumno.save(update_fields=['avatar'])
            messages.success(request, f'¡Avatar "{compra.articulo.nombre}" equipado! 😎')
    return redirect('mi_progreso', clase_id=clase.id)


@alumno_requerido
def ranking(request, alumno, clase):
    periodo = request.GET.get('periodo') if request.GET.get('periodo') in ('total', 'equipos') else 'semana'
    lista = juego.ranking_clase(clase, 'total' if periodo == 'total' else 'semana')
    equipos = juego.ranking_equipos(clase)
    return render(request, 'Alumnos/ranking.html', {
        'alumno': alumno,
        'clase': clase,
        'periodo': periodo,
        'equipos': equipos,
        'mi_equipo': next((e for e in equipos if any(m.id == alumno.id for m in e.lista_miembros)), None),
        'podio': lista[:3],
        'resto': lista[3:],
        'mi_posicion': next((a for a in lista if a.id == alumno.id), None),
        'seccion': 'ranking',
    })
