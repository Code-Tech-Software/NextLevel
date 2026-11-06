"""Piezas comunes del curso TIC 6°: misiones-lección, jefes, juegos de tarjetas y prácticas de MakeCode y Tinkercad.

El grupo es muy inquieto, así que casi todas las misiones traen «⏱️ Así se trabaja hoy» (tiempos, parejas y reglas) y,
cuando hay equipo, «👥 Roles». El tono es de estudio, laboratorio o redacción: nada infantil.
"""
from Misiones.cursos import mision
from Misiones.cursos.formato import clasifica, jefe, leccion

__all__ = ['mision', 'leccion', 'jefe', 'clasifica', 'makecode', 'tinkercad', 'MAKECODE', 'TINKERCAD', 'KIDDLE',
           'TEACHABLE', 'LEYENDA_MAKECODE', 'PAREJAS', 'CARPETA']

MAKECODE = 'https://arcade.makecode.com/'
TINKERCAD = 'https://www.tinkercad.com/'
KIDDLE = 'https://www.kiddle.co/'
TEACHABLE = 'https://teachablemachine.withgoogle.com/train/image'

CARPETA = 'TIC_6A_TuNombre'

LEYENDA_MAKECODE = (
    '🧩 Cómo leer el código de abajo: cada renglón es un bloque de MakeCode Arcade con el editor en Español (México) '
    '(⚙️ → Idioma). Lo que tiene sangría va DENTRO del bloque de arriba. Lo que está entre comillas lo escribes tú y lo '
    'que está entre [corchetes] lo eliges o lo dibujas. ¿No encuentras un bloque? Escribe una palabra en el buscador de '
    'bloques, por ejemplo «puntaje».')

# La dinámica de trabajo en parejas que se repite en las prácticas de computadora
PAREJAS = ['En parejas: Piloto (mouse y teclado) y Copiloto (lee los pasos en voz baja y revisa cada bloque).',
           'Cada 10 minutos, cuando suene la alarma del profe, cambian de lugar.',
           'Señal del profe «manos arriba»: sueltan el mouse y miran al frente.']


def makecode(nombre, descripcion, codigo, xp=100, monedas=30):
    """Práctica de MakeCode Arcade: se entrega una captura y trae los bloques escritos para no perderse."""
    return mision(nombre, 'evidencia', descripcion, xp, monedas, codigo=codigo.strip('\n'), link=MAKECODE)


def tinkercad(nombre, descripcion, xp=100, monedas=30):
    """Práctica de modelado 3D en Tinkercad: se entrega una captura del modelo."""
    return mision(nombre, 'evidencia', descripcion, xp, monedas, link=TINKERCAD)
