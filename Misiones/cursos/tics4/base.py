"""Piezas comunes del curso TIC 4°: el formato de cada misión-lección, los jefes y los juegos de tarjetas."""
from Misiones.cursos import mision
from Misiones.cursos.formato import clasifica, jefe, leccion

__all__ = ['mision', 'leccion', 'jefe', 'clasifica', 'scratch', 'SCRATCH', 'TINKERCAD', 'KIDDLE', 'LEYENDA_SCRATCH']

SCRATCH = 'https://scratch.mit.edu/projects/editor/'
TINKERCAD = 'https://www.tinkercad.com/'
KIDDLE = 'https://www.kiddle.co/'

LEYENDA_SCRATCH = ('🧩 Cómo leer el código de abajo: cada renglón es un bloque de Scratch. Lo que está más a la derecha '
                   '(con sangría) va DENTRO del bloque de arriba, como en un sándwich. Los nombres entre comillas los '
                   'escribes tú.')


def scratch(nombre, descripcion, codigo, xp=90, monedas=25):
    """Práctica de Scratch: se entrega una captura y trae los bloques escritos para no perderse."""
    return mision(nombre, 'evidencia', descripcion, xp, monedas, codigo=codigo.strip('\n'), link=SCRATCH)
