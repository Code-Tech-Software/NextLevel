"""
Motor de gamificación de Next-Level.

Toda la economía (XP, monedas, niveles, logros, misiones del día, cofres y tienda)
pasa por aquí para que cada recompensa quede registrada en el historial y genere
sus notificaciones.
"""
import random
from collections import OrderedDict, defaultdict
from datetime import timedelta

from django.db import transaction
from django.db.models import Count, F, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.utils import timezone

from .models import (
    Alumno, ArticuloTienda, CofreAbierto, CompraAlumno, Logro, LogroAlumno, Mision, MisionDiaria,
    Movimiento, Notificacion, ProgresoDiario, ProgresoMision, PuntosEquipo, RegistroConducta, calcular_nivel, xp_para_nivel, RANGOS,
)

DIARIAS_POR_DIA = 3

TIPO_INFO = {
    'arduino': {'icono': 'bi-cpu-fill', 'emoji': '🤖', 'color': '#0ea5e9'},
    'cuestionario': {'icono': 'bi-patch-question-fill', 'emoji': '🧠', 'color': '#8b5cf6'},
    'link': {'icono': 'bi-link-45deg', 'emoji': '🔗', 'color': '#06b6d4'},
    'video': {'icono': 'bi-play-btn-fill', 'emoji': '🎬', 'color': '#ef4444'},
    'evidencia': {'icono': 'bi-camera-fill', 'emoji': '📸', 'color': '#f59e0b'},
    'texto': {'icono': 'bi-pencil-fill', 'emoji': '✍️', 'color': '#ec4899'},
    'presencial': {'icono': 'bi-people-fill', 'emoji': '🙋', 'color': '#10b981'},
}

TEMA_INFO = {
    'bosque': {'emoji': '🌳', 'decos': ['🌲', '🍄', '🌼', '🦋', '🐿️', '🌿']},
    'oceano': {'emoji': '🌊', 'decos': ['🐠', '🐙', '🐚', '🐳', '🦀', '🐬']},
    'desierto': {'emoji': '🏜️', 'decos': ['🌵', '🐪', '☀️', '🦂', '🏺', '🌴']},
    'volcan': {'emoji': '🌋', 'decos': ['🔥', '💎', '🐉', '☄️', '🦖', '🌶️']},
    'hielo': {'emoji': '❄️', 'decos': ['⛄', '🐧', '🏔️', '❄️', '🎿', '⛸️']},
    'espacio': {'emoji': '🚀', 'decos': ['🌎', '⭐', '🛸', '🌙', '👽', '☄️']},
    'ciudad': {'emoji': '🌆', 'decos': ['🏙️', '🤖', '🚦', '💡', '🛰️', '🎮']},
    'dulces': {'emoji': '🍭', 'decos': ['🍬', '🧁', '🍩', '🍫', '🍦', '🍪']},
}


# ========================
# NOTIFICACIONES E HISTORIAL
# ========================
def notificar(alumno, tipo, titulo, mensaje='', icono='🔔', celebrar=False):
    return Notificacion.objects.create(
        alumno=alumno, tipo=tipo, titulo=titulo[:120], mensaje=mensaje[:255], icono=icono, celebrar=celebrar
    )


def otorgar(alumno, xp=0, monedas=0, tipo='ajuste', descripcion='', clase=None):
    """Suma (o resta) XP y monedas, lo registra en el historial y revisa subidas de nivel y logros."""
    if not xp and not monedas:
        return

    with transaction.atomic():
        fresco = Alumno.objects.select_for_update().get(pk=alumno.pk)
        nivel_antes = fresco.nivel
        rango_antes = fresco.rango['nombre']
        fresco.xp_total += xp
        fresco.monedas += monedas
        fresco.save(update_fields=['xp_total', 'monedas'])
        Movimiento.objects.create(alumno=fresco, clase=clase, tipo=tipo, descripcion=descripcion[:200],
                                  monedas=monedas, xp=xp)

        nivel_despues = fresco.nivel
        if nivel_despues > nivel_antes:
            bono_total = 0
            for nuevo_nivel in range(nivel_antes + 1, nivel_despues + 1):
                bono = 10 * nuevo_nivel
                bono_total += bono
                Movimiento.objects.create(
                    alumno=fresco, tipo='nivel', descripcion=f'¡Subiste a nivel {nuevo_nivel}!', monedas=bono
                )
            fresco.monedas += bono_total
            fresco.save(update_fields=['monedas'])

            rango = fresco.rango
            mensaje = f'Ganaste {bono_total} monedas de premio.'
            if rango['nombre'] != rango_antes:
                mensaje = f'¡Ahora eres {rango["nombre"]}! ' + mensaje
            notificar(fresco, 'nivel', f'¡Subiste a nivel {nivel_despues}!', mensaje, rango['emoji'], celebrar=True)

    alumno.xp_total = fresco.xp_total
    alumno.monedas = fresco.monedas

    if xp > 0:
        registrar_evento(alumno, 'xp', xp, clase)
        sumar_puntos_equipo(alumno, xp, descripcion, clase)
    verificar_logros(alumno)


# ========================
# RACHA DIARIA
# ========================
def actualizar_racha(alumno):
    """Cuenta los días seguidos que el alumno entra. Devuelve True la primera visita del día."""
    hoy = timezone.localdate()
    if alumno.ultima_actividad == hoy:
        return False

    if alumno.ultima_actividad == hoy - timedelta(days=1):
        alumno.racha_actual += 1
    else:
        alumno.racha_actual = 1
    alumno.racha_maxima = max(alumno.racha_maxima, alumno.racha_actual)
    alumno.ultima_actividad = hoy
    alumno.save(update_fields=['racha_actual', 'racha_maxima', 'ultima_actividad'])

    if alumno.racha_actual > 1 and alumno.racha_actual % 5 == 0:
        notificar(alumno, 'sistema', f'¡Racha de {alumno.racha_actual} días!',
                  'Sigue entrando todos los días para mantener el fuego encendido.', '🔥', celebrar=True)
    verificar_logros(alumno)
    return True


# ========================
# MISIONES DEL DÍA
# ========================
def seleccionar_diarias(clase, fecha=None):
    """Las misiones del día cambian a diario, pero son las mismas para toda la clase."""
    fecha = fecha or timezone.localdate()
    pool = list(
        MisionDiaria.objects.filter(activa=True).filter(Q(clase=clase) | Q(clase__isnull=True)).order_by('id')
    )
    if len(pool) <= DIARIAS_POR_DIA:
        return pool

    fijas = [m for m in pool if m.objetivo == 'login'][:1]
    resto = [m for m in pool if m not in fijas]
    rnd = random.Random(fecha.toordinal())
    elegidas = fijas + rnd.sample(resto, DIARIAS_POR_DIA - len(fijas))
    return sorted(elegidas, key=lambda m: (m.objetivo != 'login', m.id))


def misiones_del_dia(alumno, clase):
    hoy = timezone.localdate()
    diarias = seleccionar_diarias(clase, hoy)
    progresos = {
        p.mision_id: p for p in ProgresoDiario.objects.filter(alumno=alumno, fecha=hoy, mision__in=diarias)
    }
    resultado = []
    for diaria in diarias:
        progreso = progresos.get(diaria.id)
        valor = progreso.progreso if progreso else 0
        resultado.append({
            'mision': diaria,
            'valor': valor,
            'pct': min(100, int(valor * 100 / diaria.meta)) if diaria.meta else 100,
            'completada': valor >= diaria.meta,
            'reclamada': bool(progreso and progreso.reclamada),
        })
    return resultado


def registrar_evento(alumno, objetivo, cantidad=1, clase=None):
    hoy = timezone.localdate()
    clases = [clase] if clase else list(alumno.clases.all())
    candidatas = {}
    for c in clases:
        for diaria in seleccionar_diarias(c, hoy):
            if diaria.objetivo == objetivo:
                candidatas[diaria.id] = diaria

    for diaria in candidatas.values():
        progreso, _ = ProgresoDiario.objects.get_or_create(alumno=alumno, mision=diaria, fecha=hoy)
        if progreso.progreso < diaria.meta:
            progreso.progreso = min(diaria.meta, progreso.progreso + cantidad)
            progreso.save(update_fields=['progreso'])


def reclamar_diaria(alumno, diaria_id, clase):
    """Devuelve la MisionDiaria reclamada o None si no se puede reclamar."""
    hoy = timezone.localdate()
    diaria = next((d for d in seleccionar_diarias(clase, hoy) if d.id == diaria_id), None)
    if not diaria:
        return None

    with transaction.atomic():
        progreso = ProgresoDiario.objects.select_for_update().filter(alumno=alumno, mision=diaria, fecha=hoy).first()
        if not progreso or progreso.reclamada or progreso.progreso < diaria.meta:
            return None
        progreso.reclamada = True
        progreso.save(update_fields=['reclamada'])

    otorgar(alumno, xp=diaria.recompensa_xp, monedas=diaria.recompensa_monedas, tipo='diaria',
            descripcion=f'Misión del día: {diaria.titulo}', clase=clase)
    return diaria


# ========================
# ESTADÍSTICAS Y LOGROS
# ========================
def mundos_completados(alumno):
    aprobadas = set(
        ProgresoMision.objects.filter(alumno=alumno, estado='aprobado').values_list('mision_id', flat=True)
    )
    por_mundo = defaultdict(set)
    misiones = Mision.objects.filter(
        activa=True, clase__in=alumno.clases.all(), nivel__mundo__isnull=False
    ).values_list('id', 'nivel__mundo_id')
    for mision_id, mundo_id in misiones:
        por_mundo[mundo_id].add(mision_id)
    return sum(1 for ids in por_mundo.values() if ids and ids <= aprobadas)


def estadisticas_alumno(alumno):
    aprobados = ProgresoMision.objects.filter(alumno=alumno, estado='aprobado')
    compras = CompraAlumno.objects.filter(alumno=alumno).exclude(estado='cancelado')
    gastado = compras.aggregate(total=Coalesce(Sum('costo_pagado'), Value(0)))['total']
    estrellas = sum(p.estrellas for p in aprobados)
    return {
        'misiones': aprobados.count(),
        'xp': alumno.xp_total,
        'monedas': alumno.monedas + gastado,
        'racha': alumno.racha_maxima,
        'perfectos': aprobados.filter(mision__tipo='cuestionario', puntuacion__gte=100).count(),
        'compras': compras.count(),
        'mundos': mundos_completados(alumno),
        'nivel': alumno.nivel,
        'diarias': ProgresoDiario.objects.filter(alumno=alumno, reclamada=True).count(),
        'jefes': aprobados.filter(mision__es_jefe=True).count(),
        'estrellas': estrellas,
        'logros': LogroAlumno.objects.filter(alumno=alumno).count(),
    }


def otorgar_logro(alumno, logro):
    registro, creado = LogroAlumno.objects.get_or_create(alumno=alumno, logro=logro)
    if not creado:
        return False

    premio = []
    if logro.recompensa_monedas:
        premio.append(f'+{logro.recompensa_monedas} monedas')
    if logro.recompensa_xp:
        premio.append(f'+{logro.recompensa_xp} XP')
    mensaje = logro.descripcion + (f' · {" y ".join(premio)}' if premio else '')
    notificar(alumno, 'logro', f'Logro desbloqueado: {logro.nombre}', mensaje, logro.icono, celebrar=True)

    if logro.recompensa_monedas or logro.recompensa_xp:
        otorgar(alumno, xp=logro.recompensa_xp, monedas=logro.recompensa_monedas, tipo='logro',
                descripcion=f'Logro: {logro.nombre}')
    return True


def verificar_logros(alumno):
    desbloqueados = LogroAlumno.objects.filter(alumno=alumno).values_list('logro_id', flat=True)
    pendientes = list(
        Logro.objects.filter(activo=True).exclude(condicion='manual').exclude(id__in=list(desbloqueados))
    )
    if not pendientes:
        return

    stats = estadisticas_alumno(alumno)
    for logro in pendientes:
        if stats.get(logro.condicion, 0) >= logro.valor:
            otorgar_logro(alumno, logro)


def alumnos_que_cumplen(condicion, valor):
    """Ids de los alumnos activos que ya cumplen la condición de un logro (consultas agrupadas)."""
    activos = Alumno.objects.filter(activo=True)
    try:
        valor = max(int(valor), 0)
    except (TypeError, ValueError):
        valor = 0
    if condicion == 'manual':
        return []
    if valor == 0:
        return list(activos.values_list('id', flat=True))
    if condicion == 'xp':
        return list(activos.filter(xp_total__gte=valor).values_list('id', flat=True))
    if condicion == 'nivel':
        return list(activos.filter(xp_total__gte=xp_para_nivel(valor)).values_list('id', flat=True))
    if condicion == 'racha':
        return list(activos.filter(racha_maxima__gte=valor).values_list('id', flat=True))
    if condicion == 'monedas':
        return list(activos.annotate(
            gastado=Coalesce(Sum('compras__costo_pagado', filter=~Q(compras__estado='cancelado')), Value(0)),
        ).annotate(total=F('monedas') + F('gastado')).filter(total__gte=valor).values_list('id', flat=True))
    if condicion == 'mundos':
        return [alumno.id for alumno in activos if mundos_completados(alumno) >= valor]

    aprobados = ProgresoMision.objects.filter(estado='aprobado', alumno__activo=True)
    origenes = {
        'misiones': aprobados,
        'perfectos': aprobados.filter(mision__tipo='cuestionario', puntuacion__gte=100),
        'jefes': aprobados.filter(mision__es_jefe=True),
        'compras': CompraAlumno.objects.filter(alumno__activo=True).exclude(estado='cancelado'),
        'diarias': ProgresoDiario.objects.filter(alumno__activo=True, reclamada=True),
    }
    if condicion not in origenes:
        return []
    return list(origenes[condicion].values('alumno_id').annotate(total=Count('id'))
                .filter(total__gte=valor).values_list('alumno_id', flat=True))


def entregar_logro_a_quienes_cumplen(logro):
    """Al crear o editar un logro automático, se entrega a quienes ya cumplen la condición."""
    if not logro.activo or logro.condicion == 'manual':
        return 0
    ya_tienen = set(LogroAlumno.objects.filter(logro=logro).values_list('alumno_id', flat=True))
    nuevos = 0
    for alumno in Alumno.objects.filter(id__in=alumnos_que_cumplen(logro.condicion, logro.valor)).exclude(id__in=ya_tienen):
        if otorgar_logro(alumno, logro):
            nuevos += 1
    return nuevos


def progreso_logros(alumno):
    """Lista de logros con su avance para la vitrina de trofeos."""
    stats = estadisticas_alumno(alumno)
    obtenidos = {la.logro_id: la for la in LogroAlumno.objects.filter(alumno=alumno)}
    lista = []
    for logro in Logro.objects.filter(activo=True):
        valor = stats.get(logro.condicion, 0) if logro.condicion != 'manual' else 0
        lista.append({
            'logro': logro,
            'obtenido': obtenidos.get(logro.id),
            'valor': min(valor, logro.valor),
            'pct': min(100, int(valor * 100 / logro.valor)) if logro.valor else 0,
        })
    lista.sort(key=lambda x: (x['obtenido'] is None, x['logro'].orden))
    return lista, stats


# ========================
# RUTA DEL MAPA (mundos → niveles → misiones)
# ========================
def construir_ruta(alumno, clase):
    """
    Arma el mapa del alumno. LA REGLA DE ORO se mantiene: si una misión no está
    aprobada, todas las que siguen quedan bloqueadas.
    """
    misiones = list(Mision.objects.filter(clase=clase, activa=True).select_related('nivel', 'nivel__mundo'))
    misiones.sort(key=lambda m: (
        m.nivel.mundo.orden if m.nivel.mundo else 10 ** 6,
        m.nivel.mundo_id or 0,
        m.nivel.orden, m.nivel_id, m.orden, m.id,
    ))
    progresos = {p.mision_id: p for p in ProgresoMision.objects.filter(alumno=alumno, mision__clase=clase)}
    cofres = {c.nivel_id: c for c in CofreAbierto.objects.filter(alumno=alumno, nivel__clase=clase)}

    mundos = OrderedDict()
    for mundo in clase.mundos.all():
        mundos[mundo.id] = {'mundo': mundo, 'niveles': OrderedDict()}

    desbloqueada = True
    actual = None
    total = aprobadas_total = 0
    for mision in misiones:
        nivel = mision.nivel
        clave_mundo = nivel.mundo_id or 0
        if clave_mundo not in mundos:
            mundos[clave_mundo] = {'mundo': None, 'niveles': OrderedDict()}
        niveles = mundos[clave_mundo]['niveles']
        if nivel.id not in niveles:
            niveles[nivel.id] = {'nivel': nivel, 'misiones': []}

        progreso = progresos.get(mision.id)
        estado = progreso.estado if progreso else 'nuevo'
        item = {
            'mision': mision,
            'progreso': progreso,
            'estado': estado,
            'desbloqueada': desbloqueada,
            'estrellas': progreso.estrellas if progreso else 0,
            'actual': False,
            'info': TIPO_INFO.get(mision.tipo, TIPO_INFO['link']),
        }
        if desbloqueada and estado != 'aprobado' and actual is None:
            item['actual'] = True
            actual = item
        if estado != 'aprobado':
            desbloqueada = False
        else:
            aprobadas_total += 1
        total += 1
        niveles[nivel.id]['misiones'].append(item)

    lista_mundos = []
    for numero, datos in enumerate(mundos.values(), start=1):
        niveles = list(datos['niveles'].values())
        items = [item for nivel in niveles for item in nivel['misiones']]
        for indice, item in enumerate(items):
            item['indice'] = indice
        aprobadas = sum(1 for item in items if item['estado'] == 'aprobado')
        for nivel in niveles:
            completo = all(item['estado'] == 'aprobado' for item in nivel['misiones'])
            cofre = cofres.get(nivel['nivel'].id)
            nivel['completo'] = completo
            nivel['cofre_abierto'] = cofre
            nivel['cofre_disponible'] = completo and cofre is None

        if not items:
            estado = 'vacio'
        elif aprobadas == len(items):
            estado = 'completado'
        elif items[0]['desbloqueada']:
            estado = 'actual'
        else:
            estado = 'bloqueado'

        mundo = datos['mundo']
        tema = mundo.tema if mundo else 'bosque'
        lista_mundos.append({
            'numero': numero,
            'mundo': mundo,
            'nombre': mundo.nombre if mundo else 'Zona extra',
            'tema': tema,
            'tema_info': TEMA_INFO.get(tema, TEMA_INFO['bosque']),
            'niveles': niveles,
            'total': len(items),
            'aprobadas': aprobadas,
            'pct': int(aprobadas * 100 / len(items)) if items else 0,
            'estrellas': sum(item['estrellas'] for item in items),
            'estrellas_max': 3 * len(items),
            'estado': estado,
            'tiene_actual': any(item['actual'] for item in items),
            'cofres_disponibles': sum(1 for n in niveles if n['cofre_disponible']),
        })

    return {
        'mundos': lista_mundos,
        'actual': actual,
        'total': total,
        'aprobadas': aprobadas_total,
        'pct': int(aprobadas_total * 100 / total) if total else 0,
        'estrellas': sum(m['estrellas'] for m in lista_mundos),
        'cofres_disponibles': sum(m['cofres_disponibles'] for m in lista_mundos),
    }


def buscar_en_ruta(ruta, mision_id):
    for mundo in ruta['mundos']:
        for nivel in mundo['niveles']:
            for item in nivel['misiones']:
                if item['mision'].id == mision_id:
                    return mundo, nivel, item
    return None, None, None


def abrir_cofre(alumno, nivel):
    """Abre el cofre de un nivel completado. Devuelve las monedas obtenidas o None."""
    ids = list(nivel.misiones.filter(activa=True).values_list('id', flat=True))
    if not ids:
        return None
    aprobadas = ProgresoMision.objects.filter(alumno=alumno, mision_id__in=ids, estado='aprobado').count()
    if aprobadas < len(ids):
        return None

    base = max(nivel.recompensa_cofre, 1)
    monedas = random.randint(max(1, int(base * 0.6)), int(base * 1.5) + 1)
    with transaction.atomic():
        _, creado = CofreAbierto.objects.get_or_create(alumno=alumno, nivel=nivel, defaults={'monedas': monedas})
    if not creado:
        return None
    otorgar(alumno, monedas=monedas, tipo='cofre', descripcion=f'Cofre de {nivel.nombre}', clase=nivel.clase)
    return monedas


# ========================
# CALIFICACIONES
# ========================
def calificar(progreso, puntuacion, comentario=None, avisar=True):
    """
    Aprueba una misión con una calificación de 0 a 100.
    La primera aprobación entrega XP completa y monedas proporcionales; si se vuelve
    a calificar, solo se ajusta la diferencia de monedas.
    """
    puntuacion = max(0, min(100, int(puntuacion)))
    mision = progreso.mision
    alumno = progreso.alumno
    ya_aprobado = progreso.pk is not None and progreso.estado == 'aprobado'
    monedas_antes = progreso.monedas_obtenidas if ya_aprobado else 0

    progreso.estado = 'aprobado'
    progreso.revisado = True
    progreso.puntuacion = puntuacion
    progreso.fecha_revision = timezone.now()
    if comentario is not None:
        progreso.comentario_profesor = comentario
    progreso.save()

    monedas = int((puntuacion / 100.0) * mision.monedas_recompensa)
    if not ya_aprobado:
        otorgar(alumno, xp=mision.xp_recompensa, monedas=monedas, tipo='mision',
                descripcion=f'Misión: {mision.nombre}', clase=mision.clase)
        if avisar:
            estrellas = '⭐' * progreso.estrellas
            notificar(alumno, 'aprobada', f'¡Misión aprobada! {estrellas}',
                      f'"{mision.nombre}" · Calificación {puntuacion / 10:.1f} · +{monedas} monedas',
                      '🏆', celebrar=True)
    elif monedas != monedas_antes:
        otorgar(alumno, monedas=monedas - monedas_antes, tipo='ajuste',
                descripcion=f'Recalificación: {mision.nombre}', clase=mision.clase)
    if not ya_aprobado:
        revisar_metas(mision.clase)
    return monedas


def rechazar(progreso, comentario=''):
    progreso.estado = 'rechazado'
    progreso.revisado = True
    progreso.comentario_profesor = comentario
    progreso.fecha_revision = timezone.now()
    progreso.save()
    mensaje = comentario or 'Revisa tu trabajo y vuelve a enviarlo.'
    notificar(progreso.alumno, 'rechazada', f'"{progreso.mision.nombre}" necesita correcciones',
              mensaje, '🔧', celebrar=True)


# ========================
# TIENDA
# ========================
def comprar(alumno, articulo):
    """Devuelve (ok, mensaje)."""
    with transaction.atomic():
        art = ArticuloTienda.objects.select_for_update().get(pk=articulo.pk)
        al = Alumno.objects.select_for_update().get(pk=alumno.pk)

        if not art.activo:
            return False, 'Este artículo ya no está disponible.'
        if art.agotado:
            return False, f'¡"{art.nombre}" se agotó! Pídele al profe que traiga más.'
        if al.nivel < art.nivel_requerido:
            return False, f'Necesitas ser nivel {art.nivel_requerido} para comprar esto.'
        if art.limite_por_alumno:
            ya = CompraAlumno.objects.filter(alumno=al, articulo=art).exclude(estado='cancelado').count()
            if ya >= art.limite_por_alumno:
                return False, f'Ya alcanzaste el límite de {art.limite_por_alumno} para este artículo.'
        if al.monedas < art.costo_monedas:
            return False, '¡Oh no! No tienes suficientes monedas para este artículo.'

        if art.stock is not None:
            art.stock -= 1
            art.save(update_fields=['stock'])
        if art.tipo == 'avatar' and art.imagen:
            al.avatar = art.imagen
            al.save(update_fields=['avatar'])

        CompraAlumno.objects.create(
            alumno=al, articulo=art, costo_pagado=art.costo_monedas,
            estado='pendiente' if art.requiere_validacion else 'entregado',
            fecha_entrega=None if art.requiere_validacion else timezone.now(),
        )
        otorgar(al, monedas=-art.costo_monedas, tipo='compra', descripcion=f'Compra: {art.nombre}')

    alumno.monedas = al.monedas
    alumno.avatar = al.avatar
    if art.tipo == 'avatar':
        return True, f'¡Nuevo avatar equipado! Te ves increíble 😎'
    if art.requiere_validacion:
        return True, f'¡Compraste "{art.nombre}"! El profe te lo entregará pronto 🎁'
    return True, f'¡Compraste "{art.nombre}" con éxito! 🎉'


def entregar_compra(compra):
    if compra.estado != 'pendiente':
        return False
    compra.estado = 'entregado'
    compra.fecha_entrega = timezone.now()
    compra.save(update_fields=['estado', 'fecha_entrega'])
    notificar(compra.alumno, 'tienda', '¡Tu premio fue entregado!', f'Disfruta tu "{compra.articulo.nombre}".', '🎁')
    return True


def cancelar_compra(compra):
    """Cancela una compra pendiente: devuelve las monedas y regresa la pieza al stock."""
    with transaction.atomic():
        compra = CompraAlumno.objects.select_for_update().select_related('articulo', 'alumno').get(pk=compra.pk)
        if compra.estado != 'pendiente':
            return False
        compra.estado = 'cancelado'
        compra.save(update_fields=['estado'])
        articulo = ArticuloTienda.objects.select_for_update().get(pk=compra.articulo_id)
        if articulo.stock is not None:
            articulo.stock += 1
            articulo.save(update_fields=['stock'])
        otorgar(compra.alumno, monedas=compra.costo_pagado, tipo='reembolso',
                descripcion=f'Reembolso: {articulo.nombre}')
    notificar(compra.alumno, 'tienda', 'Compra cancelada',
              f'Te devolvimos {compra.costo_pagado} monedas de "{articulo.nombre}".', '↩️')
    return True


def ajustar_monedas(alumno, cantidad, motivo=''):
    """Ajuste manual del profesor; nunca deja al alumno en negativo. Devuelve el cambio real."""
    alumno.refresh_from_db(fields=['monedas'])
    delta = max(cantidad, -alumno.monedas)
    if delta == 0:
        return 0
    otorgar(alumno, monedas=delta, tipo='ajuste', descripcion=motivo or 'Ajuste del profesor')
    if delta > 0:
        notificar(alumno, 'monedas', f'¡El profe te dio +{delta} monedas!', motivo, '🎁')
    return delta


# ========================
# RANKING
# ========================
def ranking_clase(clase, periodo='total'):
    alumnos = clase.alumnos.filter(activo=True)
    if periodo == 'semana':
        desde = timezone.now() - timedelta(days=7)
        alumnos = alumnos.annotate(
            puntos=Coalesce(Sum('movimientos__xp', filter=Q(movimientos__fecha__gte=desde)), Value(0))
        ).order_by('-puntos', '-xp_total', 'nombre')
    else:
        alumnos = alumnos.order_by('-xp_total', 'nombre')
    lista = list(alumnos)
    for posicion, alumno in enumerate(lista, start=1):
        alumno.posicion = posicion
        if periodo != 'semana':
            alumno.puntos = alumno.xp_total
    return lista


def info_rangos():
    return [{'nivel': r[0], 'nombre': r[1], 'emoji': r[2], 'color': r[3]} for r in RANGOS]


# ========================
# EQUIPOS / CASAS
# ========================
def equipo_de(alumno, clase):
    return alumno.equipos.filter(clase=clase).first()


def sumar_puntos_equipo(alumno, puntos, motivo, clase=None):
    """La XP que gana un integrante también suma para su equipo."""
    equipos = alumno.equipos.filter(clase=clase) if clase else alumno.equipos.all()
    for equipo in equipos:
        PuntosEquipo.objects.create(equipo=equipo, alumno=alumno, puntos=puntos,
                                    motivo=f'{alumno.nombre}: {motivo}'[:200])


def dar_puntos_equipo(equipo, puntos, motivo=''):
    return PuntosEquipo.objects.create(equipo=equipo, puntos=puntos, motivo=(motivo or 'Puntos del profesor')[:200])


def ranking_equipos(clase):
    equipos = list(clase.equipos.annotate(total=Coalesce(Sum('puntos__puntos'), Value(0))).prefetch_related('miembros'))
    equipos.sort(key=lambda e: (-e.total, e.orden, e.id))
    maximo = max([e.total for e in equipos] + [1])
    for posicion, equipo in enumerate(equipos, start=1):
        equipo.posicion = posicion
        equipo.pct = int(max(equipo.total, 0) * 100 / maximo) if maximo > 0 else 0
        equipo.lista_miembros = [m for m in equipo.miembros.all() if m.activo]
    return equipos


def asignar_equipo(alumno, clase, equipo=None):
    """Un alumno pertenece a un solo equipo por clase."""
    for actual in alumno.equipos.filter(clase=clase):
        actual.miembros.remove(alumno)
    if equipo:
        equipo.miembros.add(alumno)


def repartir_equipos(clase):
    """Reparte a los alumnos activos al azar en equipos del mismo tamaño."""
    equipos = list(clase.equipos.all())
    if not equipos:
        return 0
    alumnos = list(clase.alumnos.filter(activo=True))
    random.shuffle(alumnos)
    for equipo in equipos:
        equipo.miembros.clear()
    for indice, alumno in enumerate(alumnos):
        equipos[indice % len(equipos)].miembros.add(alumno)
    return len(alumnos)


# ========================
# MODO CLASE: COMPORTAMIENTOS
# ========================
def registrar_conducta(alumno, clase, comportamiento):
    """Aplica un botón del modo clase. Los negativos solo restan monedas y nunca dejan saldo negativo."""
    alumno.refresh_from_db(fields=['monedas'])
    monedas = max(comportamiento.monedas, -alumno.monedas)
    xp = comportamiento.xp if comportamiento.positivo else 0
    registro = RegistroConducta.objects.create(
        alumno=alumno, clase=clase, comportamiento=comportamiento, nombre=comportamiento.nombre,
        icono=comportamiento.icono, monedas=monedas, xp=xp,
    )
    otorgar(alumno, xp=xp, monedas=monedas, tipo='conducta',
            descripcion=f'{comportamiento.icono} {comportamiento.nombre}', clase=clase)
    if comportamiento.positivo:
        partes = [f'+{monedas} monedas'] if monedas else []
        if xp:
            partes.append(f'+{xp} XP')
        notificar(alumno, 'monedas', f'¡{comportamiento.nombre}!', ' · '.join(partes) or '¡Bien hecho!',
                  comportamiento.icono)
    else:
        notificar(alumno, 'sistema', f'Recuerda: {comportamiento.nombre}',
                  f'{monedas} monedas. ¡Tú puedes mejorar!' if monedas else '¡Tú puedes mejorar!',
                  comportamiento.icono)
    return registro


def deshacer_conducta(registro):
    alumno = registro.alumno
    otorgar(alumno, xp=-registro.xp, monedas=-registro.monedas, tipo='conducta',
            descripcion=f'Se deshizo: {registro.nombre}', clase=registro.clase)
    if registro.xp:
        for equipo in alumno.equipos.filter(clase=registro.clase):
            PuntosEquipo.objects.create(equipo=equipo, alumno=alumno, puntos=-registro.xp,
                                        motivo=f'Se deshizo: {registro.nombre}')
    alumno.notificaciones.filter(fecha__gte=registro.fecha, titulo__contains=registro.nombre).delete()
    registro.delete()


# ========================
# METAS DEL GRUPO
# ========================
def progreso_meta(meta):
    clase = meta.clase
    if meta.tipo == 'manual':
        return meta.progreso_manual
    if meta.tipo == 'misiones':
        return ProgresoMision.objects.filter(
            mision__clase=clase, estado='aprobado', fecha_revision__gte=meta.fecha_inicio,
            alumno__clases=clase, alumno__activo=True,
        ).count()
    if meta.tipo == 'xp':
        return Movimiento.objects.filter(
            alumno__clases=clase, alumno__activo=True, xp__gt=0, fecha__gte=meta.fecha_inicio,
        ).filter(Q(clase=clase) | Q(clase__isnull=True)).aggregate(t=Coalesce(Sum('xp'), Value(0)))['t']
    if meta.tipo == 'conducta':
        return RegistroConducta.objects.filter(clase=clase, monedas__gte=0, fecha__gte=meta.fecha_inicio).count()
    return 0


def completar_meta(meta):
    meta.completada_en = timezone.now()
    meta.save(update_fields=['completada_en'])
    mensaje = meta.recompensa or '¡Trabajo en equipo increíble!'
    if meta.monedas_recompensa:
        mensaje += f' · +{meta.monedas_recompensa} monedas para todos'
    for alumno in meta.clase.alumnos.filter(activo=True):
        if meta.monedas_recompensa:
            otorgar(alumno, monedas=meta.monedas_recompensa, tipo='meta',
                    descripcion=f'Meta del grupo: {meta.titulo}', clase=meta.clase)
        notificar(alumno, 'sistema', f'¡Meta del grupo cumplida: {meta.titulo}!', mensaje, meta.icono, celebrar=True)


def revisar_metas(clase):
    for meta in clase.metas.filter(activa=True, completada_en__isnull=True):
        if progreso_meta(meta) >= meta.objetivo:
            completar_meta(meta)


def metas_visibles(clase, dias=7):
    """Metas activas y las cumplidas recientemente, con su avance calculado."""
    desde = timezone.now() - timedelta(days=dias)
    metas = list(clase.metas.filter(activa=True).filter(Q(completada_en__isnull=True) | Q(completada_en__gte=desde)))
    hoy = timezone.localdate()
    for meta in metas:
        meta.valor = progreso_meta(meta)
        if meta.completada_en is None and meta.valor >= meta.objetivo:
            completar_meta(meta)
        meta.pct = min(100, int(meta.valor * 100 / meta.objetivo)) if meta.objetivo else 100
        meta.faltan = max(0, meta.objetivo - meta.valor)
        meta.dias_restantes = (meta.fecha_limite - hoy).days if meta.fecha_limite else None
    return metas


__all__ = [
    'TIPO_INFO', 'TEMA_INFO', 'notificar', 'otorgar', 'actualizar_racha', 'seleccionar_diarias',
    'misiones_del_dia', 'registrar_evento', 'reclamar_diaria', 'estadisticas_alumno', 'verificar_logros',
    'otorgar_logro', 'progreso_logros', 'construir_ruta', 'buscar_en_ruta', 'abrir_cofre', 'calificar',
    'rechazar', 'comprar', 'entregar_compra', 'cancelar_compra', 'ajustar_monedas', 'ranking_clase',
    'calcular_nivel', 'info_rangos', 'equipo_de', 'sumar_puntos_equipo', 'dar_puntos_equipo', 'ranking_equipos',
    'asignar_equipo', 'repartir_equipos', 'registrar_conducta', 'deshacer_conducta', 'progreso_meta',
    'completar_meta', 'revisar_metas', 'metas_visibles', 'alumnos_que_cumplen',
    'entregar_logro_a_quienes_cumplen',
]
