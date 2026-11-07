"""
Motor de la Batalla en vivo.

El profe proyecta una pregunta, los alumnos contestan desde su dispositivo y gana quien acierta más rápido.
No hay una conexión abierta con cada dispositivo: cada uno pregunta cada segundo «¿cambió algo?» enviando la
versión que tiene (su «ficha»), y el servidor solo le manda la pantalla completa cuando sí cambió.

Esa señal (qué batalla tiene la clase y en qué versión va) vive en Redis cuando hay REDIS_URL, así las consultas
de cada segundo no tocan la base de datos. Si no hay Redis, o si Redis falla, la señal se lee de la base de datos
y todo funciona igual (solo un poco más de trabajo para el servidor).

Los cambios de pantalla usan la versión como candado: si el profe da doble clic en «Siguiente» o tiene el
proyector abierto en dos pestañas, solo cuenta el primero.
"""
import logging
import random
import time
from datetime import timedelta

from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError, transaction
from django.db.models import Count, F, Q
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone

from . import gamificacion as juego
from .models import Batalla, JugadorBatalla, Mision, Pregunta, PreguntaBatalla, RespuestaBatalla

log = logging.getLogger(__name__)

PREPARACION = 3        # «¡Prepárate! 3, 2, 1» antes de poder contestar
GRACIA = 1.5           # segundos extra para las respuestas que vienen en camino por la red de la escuela
AUTO_REVELAR = 4       # si el proyector no revela la respuesta (pestaña cerrada), se revela sola tras este tiempo
MINUTOS_PODIO = 15     # tras terminar, los alumnos que jugaron todavía pueden ver sus resultados
MAX_OPCIONES = 6
PUNTOS_MAX = 1000      # contestar al instante
PUNTOS_MIN = 500       # contestar bien en el último segundo
BONO_RACHA = 100       # por cada acierto seguido (desde el segundo)…
BONO_RACHA_MAX = 300   # …hasta este tope

TIEMPOS = [(10, '⚡', 'Relámpago'), (20, '⏱️', 'Normal'), (30, '🐢', 'Con calma'), (60, '🧠', 'Para pensar')]
CANTIDADES = [5, 10, 15, 20]
PREMIOS = {
    # clave: (emoji, nombre, 1.º, 2.º, 3.º, por participar, XP por acierto)
    'practica': ('🧪', 'Práctica', 0, 0, 0, 0, 0),
    'normal': ('🪙', 'Normal', 30, 20, 10, 5, 10),
    'grande': ('💰', 'Gran premio', 60, 40, 20, 10, 15),
}
LETRAS = 'ABCDEF'

TTL_SENAL = 20             # segundos que Redis guarda la señal antes de volver a leerla de la base de datos
TTL_ACTIVIDAD = 6 * 3600


# ========================
# REDIS (con respaldo en la base de datos)
# ========================
class _Cache:
    """Usa la caché solo si la comparten todos los procesos del servidor (Redis).

    Una caché en memoria de cada proceso daría versiones distintas según qué proceso conteste, así que en ese caso
    no se usa. Si Redis falla, se aparta 30 segundos para no hacer esperar a nadie.
    """
    PAUSA = 30

    def __init__(self):
        self._apagada_hasta = 0.0

    @property
    def disponible(self):
        backend = settings.CACHES.get('default', {}).get('BACKEND', '')
        return 'redis' in backend.lower() and time.monotonic() >= self._apagada_hasta

    def _fallo(self, error):
        self._apagada_hasta = time.monotonic() + self.PAUSA
        log.warning('Redis no respondió (%s); la Batalla en vivo usa la base de datos por %s s.', error, self.PAUSA)

    def get(self, clave):
        if not self.disponible:
            return None
        try:
            return cache.get(clave)
        except Exception as error:  # noqa: BLE001 — cualquier falla de Redis se trata igual
            self._fallo(error)
            return None

    def set(self, clave, valor, ttl):
        if not self.disponible:
            return
        try:
            cache.set(clave, valor, ttl)
        except Exception as error:  # noqa: BLE001
            self._fallo(error)

    def delete(self, clave):
        if not self.disponible:
            return
        try:
            cache.delete(clave)
        except Exception as error:  # noqa: BLE001
            self._fallo(error)

    def incr(self, clave, ttl):
        if not self.disponible:
            return
        try:
            try:
                cache.incr(clave)
            except ValueError:  # la clave no existía todavía
                cache.set(clave, 1, ttl)
        except Exception as error:  # noqa: BLE001
            self._fallo(error)


memoria = _Cache()


def _clave_senal(clase_id):
    return f'batalla:clase:{clase_id}'


def _clave_actividad(batalla_id):
    return f'batalla:{batalla_id}:actividad'


def _senal_de(batalla):
    if not batalla:
        return {'id': 0}
    fin = batalla.fin_pregunta if batalla.estado == 'pregunta' else None
    return {'id': batalla.id, 'v': batalla.version, 'estado': batalla.estado, 'titulo': batalla.titulo,
            'fin': fin.timestamp() if fin else None}


def _batalla_de_la_clase(clase_id):
    """La batalla abierta de la clase o, si no hay, la que terminó hace poco (para ver el podio)."""
    ahora = timezone.now()
    return Batalla.objects.filter(clase_id=clase_id).filter(
        Q(creada__gte=ahora - timedelta(hours=Batalla.HORAS_VIGENCIA), estado__in=['sala', 'pregunta', 'resultado'])
        | Q(estado='final', terminada__gte=ahora - timedelta(minutes=MINUTOS_PODIO))
    ).order_by('-creada', '-id').first()


def senal(clase_id, fresca=False):
    """Qué batalla tiene la clase y en qué versión va. {'id': 0} si no hay ninguna.

    `fresca` la lee de la base de datos (para las acciones que guardan algo) y de paso actualiza Redis.
    """
    datos = None if fresca else memoria.get(_clave_senal(clase_id))
    if datos is None:
        datos = _senal_de(_batalla_de_la_clase(clase_id))
        memoria.set(_clave_senal(clase_id), datos, TTL_SENAL)
    return datos


def ficha(datos):
    """Lo que el dispositivo guarda para preguntar «¿cambió algo?»."""
    return f"{datos['id']}.{datos['v']}" if datos.get('id') else '0'


def en_juego(datos):
    return bool(datos.get('id')) and datos.get('estado') != 'final'


def _publicar(clase_id):
    """Avisa a los dispositivos de un cambio en cuanto se guarda en la base de datos."""
    def avisar():
        memoria.set(_clave_senal(clase_id), _senal_de(_batalla_de_la_clase(clase_id)), TTL_SENAL)
    transaction.on_commit(avisar)


def actividad(batalla_id):
    """Cuántos se han unido o contestado (solo con Redis): el proyector lo usa para no pedir de más."""
    return memoria.get(_clave_actividad(batalla_id))


def _hubo_actividad(batalla_id):
    memoria.incr(_clave_actividad(batalla_id), TTL_ACTIVIDAD)


@receiver(post_delete, sender=Batalla)
def _batalla_borrada(sender, instance, **kwargs):
    _publicar(instance.clase_id)


# ========================
# PREGUNTAS DISPONIBLES
# ========================
def _opciones_validas(pregunta):
    opciones = [{'texto': o.texto.strip(), 'correcta': o.es_correcta} for o in pregunta.opciones.all() if o.texto.strip()]
    correctas = sum(1 for o in opciones if o['correcta'])
    if not 2 <= len(opciones) <= MAX_OPCIONES or not 0 < correctas < len(opciones):
        return None
    return opciones


def misiones_con_preguntas(clase):
    """Mundos → misiones de la clase con cuántas de sus preguntas sirven para la batalla (en el orden del mapa)."""
    preguntas = Pregunta.objects.filter(mision__clase=clase).prefetch_related('opciones')
    utiles = {}
    for pregunta in preguntas:
        if _opciones_validas(pregunta):
            utiles[pregunta.mision_id] = utiles.get(pregunta.mision_id, 0) + 1
    misiones = Mision.objects.filter(id__in=utiles).select_related('nivel', 'nivel__mundo').order_by(
        'nivel__mundo__orden', 'nivel__mundo_id', 'nivel__orden', 'nivel_id', 'orden', 'id')
    mundos = []
    for mision in misiones:
        mundo = mision.nivel.mundo
        clave = mundo.id if mundo else 0
        if not mundos or mundos[-1]['id'] != clave:
            mundos.append({'id': clave, 'nombre': mundo.nombre if mundo else 'Sin mundo',
                           'emoji': juego.TEMA_INFO.get(mundo.tema, {}).get('emoji', '🌍') if mundo else '🌍',
                           'misiones': [], 'preguntas': 0})
        mundos[-1]['misiones'].append({'id': mision.id, 'nombre': mision.nombre, 'nivel': mision.nivel.nombre,
                                       'preguntas': utiles[mision.id], 'activa': mision.activa,
                                       'jefe': mision.es_jefe})
        mundos[-1]['preguntas'] += utiles[mision.id]
    return mundos


def _titulo_automatico(misiones):
    if len(misiones) == 1:
        return misiones[0].nombre
    mundos = {m.nivel.mundo_id for m in misiones}
    if len(mundos) == 1 and misiones[0].nivel.mundo:
        return f'Repaso: {misiones[0].nivel.mundo.nombre}'
    return 'Gran repaso'


# ========================
# CREAR
# ========================
def crear_batalla(clase, mision_ids, cantidad=10, segundos=20, mezclar=True, por_equipos=False, premios='normal',
                  titulo=''):
    """Copia las preguntas elegidas y abre la sala de espera. Si la clase tenía otra batalla abierta, la termina."""
    misiones = list(Mision.objects.filter(clase=clase, id__in=mision_ids).select_related('nivel', 'nivel__mundo')
                    .order_by('nivel__mundo__orden', 'nivel__mundo_id', 'nivel__orden', 'nivel_id', 'orden', 'id'))
    lista = []
    for mision in misiones:
        for pregunta in mision.preguntas.prefetch_related('opciones').order_by('orden', 'id'):
            opciones = _opciones_validas(pregunta)
            if opciones:
                lista.append((mision, pregunta.texto.strip(), opciones))
    if not lista:
        raise ValueError('Esas misiones no tienen preguntas de opción múltiple.')
    if mezclar:
        random.shuffle(lista)
    if cantidad:
        lista = lista[:cantidad]

    for abierta in Batalla.objects.abiertas().filter(clase=clase):
        terminar(abierta)

    _, _, p1, p2, p3, participar, xp = PREMIOS.get(premios, PREMIOS['normal'])
    with transaction.atomic():
        batalla = Batalla.objects.create(
            clase=clase, titulo=(titulo or _titulo_automatico(misiones))[:120], segundos=segundos,
            por_equipos=por_equipos and clase.equipos.exists(), premio_1=p1, premio_2=p2, premio_3=p3,
            premio_participar=participar, xp_por_acierto=xp,
        )
        PreguntaBatalla.objects.bulk_create([
            PreguntaBatalla(batalla=batalla, orden=i, texto=texto, mision=mision,
                            opciones=random.sample(opciones, len(opciones)) if mezclar else opciones)
            for i, (mision, texto, opciones) in enumerate(lista)
        ])
    _publicar(clase.id)
    return batalla


def repetir(batalla):
    """La misma batalla otra vez, con las preguntas y opciones en otro orden."""
    preguntas = list(batalla.preguntas.all())
    random.shuffle(preguntas)
    for abierta in Batalla.objects.abiertas().filter(clase=batalla.clase):
        terminar(abierta)
    with transaction.atomic():
        nueva = Batalla.objects.create(
            clase=batalla.clase, titulo=batalla.titulo, segundos=batalla.segundos, por_equipos=batalla.por_equipos,
            premio_1=batalla.premio_1, premio_2=batalla.premio_2, premio_3=batalla.premio_3,
            premio_participar=batalla.premio_participar, xp_por_acierto=batalla.xp_por_acierto,
        )
        PreguntaBatalla.objects.bulk_create([
            PreguntaBatalla(batalla=nueva, orden=i, texto=p.texto, mision_id=p.mision_id,
                            opciones=random.sample(p.opciones, len(p.opciones)))
            for i, p in enumerate(preguntas)
        ])
    _publicar(nueva.clase_id)
    return nueva


# ========================
# CAMBIOS DE PANTALLA (los hace el profe desde el proyector)
# ========================
def _cambiar(batalla, version, **campos):
    """Cambia de pantalla solo si la batalla sigue en la versión que vio quien lo pide. True si se hizo."""
    hechos = Batalla.objects.filter(pk=batalla.pk, version=version).update(version=F('version') + 1, **campos)
    batalla.refresh_from_db()
    if hechos:
        _publicar(batalla.clase_id)
    return bool(hechos)


def siguiente(batalla, version):
    """De la sala (o del resultado) a la siguiente pregunta; después de la última, al podio."""
    if batalla.estado not in ('sala', 'resultado'):
        return False
    if batalla.indice + 1 >= batalla.preguntas.count():
        return terminar(batalla, version)
    return _cambiar(batalla, version, estado='pregunta', indice=batalla.indice + 1,
                    inicio_pregunta=timezone.now() + timedelta(seconds=PREPARACION))


def revelar(batalla, version):
    """Muestra la respuesta correcta. Quien no contestó pierde su racha."""
    if batalla.estado != 'pregunta':
        return False
    if not _cambiar(batalla, version, estado='resultado'):
        return False
    contestaron = RespuestaBatalla.objects.filter(pregunta__batalla=batalla, pregunta__orden=batalla.indice)
    batalla.jugadores.exclude(id__in=contestaron.values('jugador_id')).update(racha=0)
    return True


def revelar_si_vencida(datos):
    """Respaldo por si el proyector se cerró a media pregunta: la respuesta se revela sola."""
    if datos.get('estado') != 'pregunta' or not datos.get('fin'):
        return False
    if time.time() < datos['fin'] + AUTO_REVELAR:
        return False
    batalla = Batalla.objects.filter(pk=datos['id']).first()
    return bool(batalla) and revelar(batalla, datos['v'])


def terminar(batalla, version=None):
    """Pasa al podio y reparte los premios (una sola vez)."""
    if batalla.estado == 'final':
        return False
    if not _cambiar(batalla, batalla.version if version is None else version, estado='final',
                    terminada=timezone.now()):
        return False
    entregar_premios(batalla)
    return True


def quitar_jugador(batalla, jugador_id):
    """El profe saca a alguien de la sala (se equivocó de nombre o no está en clase)."""
    borrados, _ = batalla.jugadores.filter(pk=jugador_id).delete()
    if borrados:
        _hubo_actividad(batalla.id)
    return bool(borrados)


# ========================
# ALUMNOS: UNIRSE Y CONTESTAR
# ========================
def unir(batalla, alumno):
    """Se puede entrar en la sala de espera o ya empezada (las preguntas que se perdió no cuentan)."""
    if batalla.estado == 'final' or alumno.es_prueba:
        return None
    equipo = juego.equipo_de(alumno, batalla.clase) if batalla.por_equipos else None
    jugador, creado = JugadorBatalla.objects.get_or_create(batalla=batalla, alumno=alumno,
                                                           defaults={'equipo': equipo})
    if creado:
        _hubo_actividad(batalla.id)
    return jugador


def puntos_por_acierto(milisegundos, segundos, racha_previa):
    """Entre 1000 (al instante) y 500 (al final), más el bono por aciertos seguidos."""
    total = segundos * 1000
    rapidez = 1 - min(max(milisegundos, 0), total) / total
    bono = min(racha_previa * BONO_RACHA, BONO_RACHA_MAX)
    return round(PUNTOS_MIN + (PUNTOS_MAX - PUNTOS_MIN) * rapidez) + bono


def responder(batalla, alumno, indice, opcion):
    """Guarda la respuesta. Devuelve (True, None) o (False, mensaje para el alumno).

    El alumno no sabe si acertó hasta que el profe revela la respuesta: así nadie se copia viendo la pantalla
    del de al lado.
    """
    ahora = timezone.now()
    if batalla.estado != 'pregunta' or batalla.indice != indice or not batalla.inicio_pregunta:
        return False, 'Esa pregunta ya se cerró.'
    if ahora < batalla.inicio_pregunta - timedelta(seconds=0.3):
        return False, '¡Espera a que aparezcan las respuestas!'
    if ahora > batalla.fin_pregunta + timedelta(seconds=GRACIA):
        return False, '⏰ Se acabó el tiempo.'
    pregunta = batalla.preguntas.filter(orden=indice).first()
    if not pregunta or not 0 <= opcion < len(pregunta.opciones):
        return False, 'Esa respuesta no existe.'
    milisegundos = max(0, min(int((ahora - batalla.inicio_pregunta).total_seconds() * 1000), batalla.segundos * 1000))
    correcta = opcion in pregunta.correctas

    try:
        with transaction.atomic():
            jugador = JugadorBatalla.objects.select_for_update().filter(batalla=batalla, alumno=alumno).first()
            if not jugador:
                return False, 'Primero únete a la batalla.'
            if RespuestaBatalla.objects.filter(pregunta=pregunta, jugador=jugador).exists():
                return False, 'Ya contestaste esta pregunta.'
            puntos = puntos_por_acierto(milisegundos, batalla.segundos, jugador.racha) if correcta else 0
            RespuestaBatalla.objects.create(pregunta=pregunta, jugador=jugador, opcion=opcion, correcta=correcta,
                                            puntos=puntos, milisegundos=milisegundos)
            jugador.contestadas += 1
            jugador.puntos += puntos
            if correcta:
                jugador.aciertos += 1
                jugador.racha += 1
                jugador.milisegundos += milisegundos
            else:
                jugador.racha = 0
            jugador.save(update_fields=['contestadas', 'puntos', 'aciertos', 'racha', 'milisegundos'])
    except IntegrityError:
        return False, 'Ya contestaste esta pregunta.'
    _hubo_actividad(batalla.id)
    return True, None


# ========================
# POSICIONES Y PREMIOS
# ========================
def orden_jugador(jugador):
    return (-jugador.puntos, -jugador.aciertos, jugador.milisegundos, jugador.unido, jugador.id)


def ranking_equipos(jugadores):
    """Equipos ordenados por el promedio de puntos de sus integrantes (así un equipo grande no gana por ser grande)."""
    grupos = {}
    for jugador in jugadores:
        if jugador.equipo_id:
            grupos.setdefault(jugador.equipo_id, []).append(jugador)
    equipos = []
    for miembros in grupos.values():
        equipo = miembros[0].equipo
        promedio = round(sum(j.puntos for j in miembros) / len(miembros))
        equipos.append({'id': equipo.id, 'nombre': equipo.nombre, 'emoji': equipo.emoji, 'color': equipo.color,
                        'promedio': promedio, 'aciertos': sum(j.aciertos for j in miembros),
                        'miembros': sorted(miembros, key=orden_jugador)})
    equipos.sort(key=lambda e: (-e['promedio'], -e['aciertos'], e['id']))
    for posicion, equipo in enumerate(equipos, start=1):
        equipo['posicion'] = posicion
    return equipos


def _posiciones(batalla, jugadores):
    """Lugar final de cada jugador que contestó algo. En equipos cuenta el lugar de su equipo."""
    participaron = [j for j in jugadores if j.contestadas]
    if batalla.por_equipos:
        return {j.id: e['posicion'] for e in ranking_equipos(participaron) for j in e['miembros']}
    return {j.id: posicion for posicion, j in enumerate(sorted(participaron, key=orden_jugador), start=1)}


def ordinal(posicion):
    return {1: '1.er', 2: '2.º', 3: '3.er'}.get(posicion, f'{posicion}.º')


def entregar_premios(batalla):
    """Guarda el lugar de cada quien y le da sus monedas y XP con `otorgar` (quedan en su historial)."""
    with transaction.atomic():
        fresca = Batalla.objects.select_for_update().get(pk=batalla.pk)
        if fresca.premios_entregados:
            return
        jugadores = list(fresca.jugadores.select_related('alumno', 'equipo'))
        posiciones = _posiciones(fresca, jugadores)
        for jugador in jugadores:
            jugador.posicion = posiciones.get(jugador.id)
            jugador.monedas = 0
            jugador.xp = 0
            if jugador.contestadas:
                podio = fresca.premios_podio[jugador.posicion - 1] if jugador.posicion and jugador.posicion <= 3 else 0
                jugador.monedas = podio + fresca.premio_participar
                jugador.xp = jugador.aciertos * fresca.xp_por_acierto
        JugadorBatalla.objects.bulk_update(jugadores, ['posicion', 'monedas', 'xp'])

        equipo_txt = 'Tu equipo quedó' if fresca.por_equipos else 'Quedaste'
        total = fresca.preguntas.count()
        for jugador in jugadores:
            alumno = jugador.alumno
            if not jugador.contestadas or alumno.es_prueba:
                continue
            lugar = jugador.posicion
            descripcion = f'Batalla en vivo: {fresca.titulo}' + (f' · {ordinal(lugar)} lugar' if lugar else '')
            if jugador.monedas or jugador.xp:
                juego.otorgar(alumno, xp=jugador.xp, monedas=jugador.monedas, tipo='batalla',
                              descripcion=descripcion, clase=fresca.clase)
            else:
                juego.verificar_logros(alumno)  # «Juega N batallas» cuenta aunque sea de práctica
            premio = ' y '.join(p for p in [f'+{jugador.monedas} monedas' if jugador.monedas else '',
                                            f'+{jugador.xp} XP' if jugador.xp else ''] if p)
            detalle = f'{jugador.aciertos} de {total} aciertos · {jugador.puntos:,} puntos'
            if lugar and lugar <= 3:
                juego.notificar(alumno, 'batalla', f'¡{equipo_txt} en {ordinal(lugar)} lugar en la batalla!',
                                f'{fresca.titulo}: {detalle}.' + (f' Ganaste {premio}.' if premio else ''),
                                ['🥇', '🥈', '🥉'][lugar - 1], celebrar=True)
            elif premio:
                juego.notificar(alumno, 'batalla', f'Batalla en vivo: {premio}', f'{fresca.titulo}: {detalle}.', '⚔️')

        Batalla.objects.filter(pk=fresca.pk).update(premios_entregados=True, version=F('version') + 1)
    batalla.refresh_from_db()
    _publicar(batalla.clase_id)


# ========================
# LO QUE VE CADA PANTALLA
# ========================
def _avatar(alumno):
    from .templatetags.nextlevel import avatar_url  # aquí para no importar las plantillas al cargar el motor
    return avatar_url(alumno)


def _ms_hasta(momento):
    return int((momento - timezone.now()).total_seconds() * 1000) if momento else 0


def _reloj(batalla):
    if batalla.estado != 'pregunta' or not batalla.inicio_pregunta:
        return {}
    return {'inicio_ms': max(_ms_hasta(batalla.inicio_pregunta), 0), 'restante_ms': max(_ms_hasta(batalla.fin_pregunta), 0)}


def _jugador_dict(jugador, extra=None):
    alumno = jugador.alumno
    datos = {'id': jugador.id, 'nombre': alumno.nombre, 'apellido': alumno.apellido[:1] + '.' if alumno.apellido else '',
             'avatar': _avatar(alumno), 'puntos': jugador.puntos, 'aciertos': jugador.aciertos,
             'equipo': jugador.equipo.emoji if jugador.equipo else ''}
    datos.update(extra or {})
    return datos


def _ranking_vivo(batalla, jugadores, pregunta=None):
    """Top con flechas: cuántos lugares subió cada quien con la última pregunta."""
    actuales = sorted(jugadores, key=orden_jugador)
    if pregunta is None:
        return [_jugador_dict(j, {'posicion': i}) for i, j in enumerate(actuales, start=1)]
    ganados = dict(pregunta.respuestas.values_list('jugador_id', 'puntos'))
    antes = sorted(jugadores, key=lambda j: (-(j.puntos - ganados.get(j.id, 0)), j.unido, j.id))
    lugar_antes = {j.id: i for i, j in enumerate(antes, start=1)}
    primera = pregunta.orden == 0   # antes de la primera todos iban empatados en 0: no hay quien «suba»
    return [_jugador_dict(j, {'posicion': i, 'sube': 0 if primera else lugar_antes[j.id] - i, 'gano': ganados.get(j.id, 0)})
            for i, j in enumerate(actuales, start=1)]


def _equipos_dict(jugadores):
    return [{k: v for k, v in e.items() if k != 'miembros'} | {'miembros': len(e['miembros'])}
            for e in ranking_equipos(jugadores)]


def estado_profesor(batalla):
    """Todo lo que pinta el proyector."""
    jugadores = list(batalla.jugadores.select_related('alumno', 'equipo'))
    total = batalla.preguntas.count()
    datos = {
        'ficha': f'{batalla.version}.{actividad(batalla.id) or 0}', 'v': batalla.version, 'id': batalla.id,
        'estado': batalla.estado, 'titulo': batalla.titulo, 'indice': batalla.indice, 'total': total,
        'segundos': batalla.segundos, 'por_equipos': batalla.por_equipos, 'premios_entregados': batalla.premios_entregados,
        'con_premios': batalla.con_premios, 'premios': batalla.premios_podio, 'premio_participar': batalla.premio_participar,
        'total_jugadores': len(jugadores), **_reloj(batalla),
    }
    pregunta = batalla.preguntas.filter(orden=batalla.indice).first() if batalla.indice >= 0 else None
    if batalla.estado == 'sala':
        datos['jugadores'] = [_jugador_dict(j) for j in sorted(jugadores, key=lambda j: (j.unido, j.id))]
    if pregunta and batalla.estado in ('pregunta', 'resultado'):
        votos = dict(pregunta.respuestas.values_list('opcion').annotate(n=Count('id')))
        revelada = batalla.estado == 'resultado'
        datos['pregunta'] = {
            'texto': pregunta.texto, 'mision': pregunta.mision.nombre if pregunta.mision else '',
            'opciones': [{'letra': LETRAS[i], 'texto': o['texto'],
                          **({'correcta': bool(o.get('correcta')), 'votos': votos.get(i, 0)} if revelada else {})}
                         for i, o in enumerate(pregunta.opciones)],
        }
        datos['respondieron'] = sum(votos.values())
        contestaron = set(pregunta.respuestas.values_list('jugador_id', flat=True))
        datos['faltan'] = [j.alumno.nombre for j in jugadores if j.id not in contestaron][:12]
    if batalla.estado == 'resultado':
        datos['ranking'] = _ranking_vivo(batalla, jugadores, pregunta)[:5]
        datos['aciertos_pregunta'] = pregunta.respuestas.filter(correcta=True).count() if pregunta else 0
    if batalla.por_equipos and batalla.estado in ('resultado', 'final'):
        datos['equipos'] = _equipos_dict([j for j in jugadores if j.contestadas])
    if batalla.estado == 'final':
        participaron = [j for j in jugadores if j.contestadas]
        datos['ranking'] = _ranking_vivo(batalla, participaron)[:10]
        datos['podio'] = [_jugador_dict(j, {'posicion': j.posicion, 'monedas': j.monedas})
                          for j in sorted(participaron, key=orden_jugador)[:3]]
        datos['resumen'] = resumen_preguntas(batalla)[:3]
        datos['participaron'] = len(participaron)
    return datos


def resumen_preguntas(batalla):
    """Cada pregunta con su porcentaje de aciertos, de la más difícil a la más fácil (para saber qué repasar)."""
    filas = []
    for pregunta in batalla.preguntas.select_related('mision').annotate(
            total=Count('respuestas'), bien=Count('respuestas', filter=Q(respuestas__correcta=True))):
        if not pregunta.total:
            continue
        votos = dict(pregunta.respuestas.values_list('opcion').annotate(n=Count('id')))
        erradas = [(n, i) for i, n in votos.items() if i not in pregunta.correctas]
        confusion = max(erradas)[1] if erradas else None
        filas.append({
            'orden': pregunta.orden + 1, 'texto': pregunta.texto, 'mision': pregunta.mision.nombre if pregunta.mision else '',
            'mision_id': pregunta.mision_id, 'pct': round(pregunta.bien * 100 / pregunta.total), 'total': pregunta.total,
            'correcta': ', '.join(pregunta.opciones[i]['texto'] for i in pregunta.correctas),
            'confusion': pregunta.opciones[confusion]['texto'] if confusion is not None else '',
        })
    filas.sort(key=lambda f: (f['pct'], f['orden']))
    return filas


def estado_alumno(datos_senal, alumno):
    """Lo que ve el alumno en su dispositivo. Nunca incluye la respuesta correcta antes de revelarla."""
    base = {'ficha': ficha(datos_senal), 'vista_previa': alumno.es_prueba}
    batalla = Batalla.objects.filter(pk=datos_senal.get('id')).select_related('clase').first() if datos_senal.get('id') else None
    jugador = batalla.jugadores.select_related('equipo').filter(alumno=alumno).first() if batalla else None
    if not batalla or (batalla.estado == 'final' and not jugador):
        return {**base, 'estado': 'nada'}

    total = batalla.preguntas.count()
    datos = {**base, 'estado': batalla.estado, 'titulo': batalla.titulo, 'indice': batalla.indice, 'total': total,
             'segundos': batalla.segundos, 'unido': bool(jugador), 'por_equipos': batalla.por_equipos,
             'jugadores': batalla.jugadores.count(), **_reloj(batalla)}
    if jugador:
        datos['equipo'] = {'nombre': jugador.equipo.nombre, 'emoji': jugador.equipo.emoji} if jugador.equipo else None
        datos['puntos'] = jugador.puntos
        datos['racha'] = jugador.racha
        datos['lugar'] = batalla.jugadores.filter(
            Q(puntos__gt=jugador.puntos) | Q(puntos=jugador.puntos, aciertos__gt=jugador.aciertos)).count() + 1

    pregunta = batalla.preguntas.filter(orden=batalla.indice).first() if batalla.indice >= 0 else None
    if pregunta and batalla.estado in ('pregunta', 'resultado'):
        respuesta = pregunta.respuestas.filter(jugador=jugador).first() if jugador else None
        datos['pregunta'] = {'texto': pregunta.texto,
                             'opciones': [{'letra': LETRAS[i], 'texto': o['texto']} for i, o in enumerate(pregunta.opciones)]}
        datos['mi_respuesta'] = respuesta.opcion if respuesta else None
        if batalla.estado == 'resultado':
            datos['correctas'] = pregunta.correctas
            datos['resultado'] = {'acerte': bool(respuesta and respuesta.correcta),
                                  'contesto': bool(respuesta), 'puntos': respuesta.puntos if respuesta else 0}

    if batalla.estado == 'final' and jugador:
        datos['final'] = {'listo': batalla.premios_entregados, 'posicion': jugador.posicion, 'puntos': jugador.puntos,
                          'aciertos': jugador.aciertos, 'contestadas': jugador.contestadas,
                          'monedas': jugador.monedas, 'xp': jugador.xp, 'ordinal': ordinal(jugador.posicion) if jugador.posicion else ''}
        if batalla.premios_entregados:
            ganadores = sorted([j for j in batalla.jugadores.select_related('alumno', 'equipo') if j.contestadas], key=orden_jugador)
            datos['podio'] = [_jugador_dict(j, {'posicion': j.posicion}) for j in ganadores[:3]]
            if batalla.por_equipos:
                datos['equipos'] = _equipos_dict(ganadores)[:3]
    return datos
