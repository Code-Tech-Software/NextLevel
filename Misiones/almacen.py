"""Dónde se guardan los archivos de «Mis proyectos» (Scratch, Arduino, Word…).

En Railway van a Cloudinary como archivos «raw» (no imagen), en el almacenamiento «proyectos» de settings.STORAGES.
Si ese almacenamiento no existe (las pruebas y los ajustes locales), se usa el de siempre (`default`).
"""
import logging

import cloudinary.uploader
import requests
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.core.files import File
from django.core.files.storage import InvalidStorageError, Storage, default_storage, storages
from django.utils.deconstruct import deconstructible

registro = logging.getLogger(__name__)


class ArchivoNoDisponible(Exception):
    """Cloudinary no entregó el archivo (por ejemplo, PDF o ZIP sin permiso de descarga en el plan gratis)."""

    def __init__(self, estado):
        super().__init__(f'Cloudinary respondió {estado}')
        self.estado = estado


def almacen_proyectos():
    try:
        return storages['proyectos']
    except InvalidStorageError:
        return default_storage


@deconstructible(path='Misiones.almacen.AlmacenProyectos')
class AlmacenProyectos(Storage):
    """Pasa cada operación al almacenamiento «proyectos» del momento. Así las pruebas lo cambian por uno en memoria
    con `override_settings(STORAGES=…)` y nunca suben nada a Cloudinary."""

    @property
    def real(self):
        return almacen_proyectos()

    def _open(self, name, mode='rb'):
        return self.real.open(name, mode)

    def _save(self, name, content):
        return self.real.save(name, content)

    def save(self, name, content, max_length=None):
        return self.real.save(name, content, max_length=max_length)

    def delete(self, name):
        return self.real.delete(name)

    def exists(self, name):
        return self.real.exists(name)

    def url(self, name):
        return self.real.url(name)

    def size(self, name):
        return self.real.size(name)

    def path(self, name):
        return self.real.path(name)

    def generate_filename(self, filename):
        return self.real.generate_filename(filename)

    def get_available_name(self, name, max_length=None):
        return self.real.get_available_name(name, max_length=max_length)

    def __eq__(self, otro):
        return isinstance(otro, AlmacenProyectos)

    def __hash__(self):
        return hash(AlmacenProyectos)


class ProyectosCloudinary(RawMediaCloudinaryStorage):
    """Cloudinary para archivos que no son imágenes.

    - El nombre ya trae una carpeta al azar (proyectos/<alumno>/<llave>/archivo.sb3), así que se sube con ese
      `public_id` exacto: nunca choca con el de otro alumno y se conserva el nombre del archivo.
    - Para descargarlo se lee poco a poco (sin cargarlo entero en memoria) y con tiempo límite.
    """

    TAG = 'proyectos'
    TIEMPO_SUBIDA = 90

    def _upload(self, name, content):
        respuesta = cloudinary.uploader.upload(content, public_id=name, resource_type='raw', overwrite=False,
                                               tags=self.TAG, timeout=self.TIEMPO_SUBIDA)
        if respuesta.get('existing'):
            # Con la llave al azar no debería pasar nunca; si pasa, jamás devolver el archivo de otra persona
            raise RuntimeError('Ya existía un archivo con ese nombre en Cloudinary')
        return respuesta

    def _open(self, name, mode='rb'):
        respuesta = requests.get(self.url(name), stream=True, timeout=(5, 60), headers={'Accept-Encoding': 'identity'})
        if respuesta.status_code != 200:
            respuesta.close()
            raise ArchivoNoDisponible(respuesta.status_code)
        respuesta.raw.decode_content = True
        archivo = File(respuesta.raw, name=name)
        largo = respuesta.headers.get('Content-Length', '')
        archivo.largo = int(largo) if largo.isdigit() else None
        return archivo

    def exists(self, name):
        try:
            respuesta = requests.head(self.url(name), timeout=10)
        except requests.RequestException:
            return False
        return respuesta.status_code == 200


def borrar_archivo(nombre):
    """Borra un archivo guardado de «Mis proyectos». Si falla (Cloudinary caído) solo lo anota: el registro ya no existe."""
    if not nombre:
        return
    try:
        almacen_proyectos().delete(nombre)
    except Exception:  # noqa: BLE001 — que una falla de Cloudinary no rompa lo que el alumno o el profe hacían
        registro.warning('No se pudo borrar el archivo de proyecto %s', nombre, exc_info=True)
