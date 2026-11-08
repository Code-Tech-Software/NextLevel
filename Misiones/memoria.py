"""
Caché compartida (Redis) con respaldo en la base de datos.

La usan la Batalla en vivo (la señal de cada clase) y las sesiones (quién es cada alumno y el profe). La base de
datos sigue siendo la fuente de verdad: Redis solo evita leerla una y otra vez.

- Solo se usa si la comparten todos los procesos del servidor (Redis). Una caché en memoria de cada proceso daría
  datos distintos según qué proceso conteste, así que en ese caso es como si no hubiera caché.
- Si Redis falla, se aparta 30 segundos para no hacer esperar a nadie y todo se lee de la base de datos.
- Lo que cambió mientras Redis no estaba se borra de Redis en cuanto vuelve: así nadie lee datos viejos (por ejemplo
  una sesión que se cerró durante la falla).
"""
import logging
import threading
import time

from django.conf import settings
from django.core.cache import caches

log = logging.getLogger(__name__)


class Memoria:
    PAUSA = 30                 # segundos que se aparta Redis después de una falla
    MAX_PENDIENTES = 10000     # tope de claves por borrar al volver Redis (el resto caduca sola)

    def __init__(self, alias='default'):
        self.alias = alias
        self._apagada_hasta = 0.0
        self._pendientes = set()
        self._candado = threading.Lock()

    # ---------- ¿Se puede usar? ----------
    @property
    def compartida(self):
        backend = settings.CACHES.get(self.alias, {}).get('BACKEND', '')
        return 'redis' in backend.lower()

    @property
    def disponible(self):
        return self.compartida and time.monotonic() >= self._apagada_hasta

    def _fallo(self, error):
        self._apagada_hasta = time.monotonic() + self.PAUSA
        log.warning('Redis no respondió (%s); se usa la base de datos durante %s s.', error, self.PAUSA)

    # ---------- Lo que cambió sin Redis ----------
    def _apuntar(self, clave):
        if not self.compartida:
            return
        with self._candado:
            if len(self._pendientes) < self.MAX_PENDIENTES:
                self._pendientes.add(clave)

    def _ponerse_al_dia(self, cache):
        if not self._pendientes:
            return
        with self._candado:
            claves, self._pendientes = list(self._pendientes), set()
        try:
            cache.delete_many(claves)
        except Exception:
            with self._candado:
                self._pendientes.update(claves)
            raise

    def _usar(self, operacion, cambia=None, por_defecto=None):
        """Hace la operación en Redis; si no se puede, devuelve `por_defecto` y apunta la clave que cambió."""
        if not self.disponible:
            if cambia:
                self._apuntar(cambia)
            return por_defecto
        cache = caches[self.alias]
        try:
            self._ponerse_al_dia(cache)
            return operacion(cache)
        except Exception as error:  # noqa: BLE001 — cualquier falla de Redis se trata igual
            self._fallo(error)
            if cambia:
                self._apuntar(cambia)
            return por_defecto

    # ---------- Operaciones ----------
    def get(self, clave):
        return self._usar(lambda c: c.get(clave))

    def set(self, clave, valor, ttl):
        self._usar(lambda c: c.set(clave, valor, ttl), cambia=clave)

    def delete(self, clave):
        self._usar(lambda c: c.delete(clave), cambia=clave)

    def incr(self, clave, ttl):
        def sumar(cache):
            try:
                cache.incr(clave)
            except ValueError:  # la clave no existía todavía
                cache.set(clave, 1, ttl)
        self._usar(sumar, cambia=clave)


memoria = Memoria()
