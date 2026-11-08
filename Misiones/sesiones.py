"""
Sesiones en Redis con respaldo en la base de datos (SESSION_ENGINE = 'Misiones.sesiones').

Cada página, y cada consulta de la Batalla en vivo (una por segundo y por alumno), necesita saber quién es el alumno
o el profe. Con esto se lee de Redis y no de la base de datos.

La base de datos sigue guardando todas las sesiones, como antes: si Redis no está o falla, se leen de ahí y nadie
tiene que volver a entrar. Por eso, a diferencia del «cached_db» de Django, una falla de Redis nunca rompe una página.
"""
from asgiref.sync import sync_to_async
from django.contrib.sessions.backends.db import SessionStore as SesionEnBase

from .memoria import memoria

PREFIJO = 'sesion:'
TTL_MAX = 3600   # se vuelve a leer de la base de datos al menos cada hora (por si algo quedó viejo en Redis)


class SessionStore(SesionEnBase):

    def _clave(self, session_key=None):
        return PREFIJO + (session_key or self._get_or_create_session_key())

    def _ttl(self, **kwargs):
        return max(1, min(self.get_expiry_age(**kwargs), TTL_MAX))

    def load(self):
        datos = memoria.get(self._clave())
        if datos is None:
            sesion = self._get_session_from_db()   # si caducó o no existe, Django le quita la clave
            if not sesion:
                return {}
            datos = self.decode(sesion.session_data)
            memoria.set(self._clave(), datos, self._ttl(expiry=sesion.expire_date))
        return datos

    def save(self, must_create=False):
        super().save(must_create)
        memoria.set(self._clave(), self._session, self._ttl())

    def delete(self, session_key=None):
        session_key = session_key or self.session_key
        super().delete(session_key)
        if session_key:
            memoria.delete(PREFIJO + session_key)

    # Django solo usa estas en vistas asíncronas (aquí no hay), pero deben pasar por Redis igual que las otras
    async def aload(self):
        return await sync_to_async(self.load)()

    async def asave(self, must_create=False):
        await sync_to_async(self.save)(must_create)

    async def adelete(self, session_key=None):
        await sync_to_async(self.delete)(session_key)
