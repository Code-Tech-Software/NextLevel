"""Piezas comunes del curso TIC 5°: misiones-lección, jefes, juegos de tarjetas y prácticas de Scratch, Tinkercad y
micro:bit.

El grupo es inquieto y muy platicador, así que casi todas las misiones traen «⏱️ Así se trabaja hoy» con tiempos,
duplas (máximo 2, las arma el profe) y el «semáforo de voz» que se acuerda en la primera misión. El tono es de agencia
espacial, laboratorio o taller: retador, nada infantil.

Los bloques están escritos tal como aparecen en los editores: Scratch en «Español Latinoamericano» y MakeCode para
micro:bit en «Español (España)», que es el único español que ofrece.
"""
from Misiones.cursos import mision
from Misiones.cursos.formato import clasifica, jefe, leccion

__all__ = ['mision', 'leccion', 'jefe', 'clasifica', 'scratch', 'tinkercad', 'microbit', 'SCRATCH', 'TINKERCAD',
           'MICROBIT', 'KIDDLE', 'QUICKDRAW', 'AUTODRAW', 'LEYENDA_SCRATCH', 'LEYENDA_MICROBIT', 'PAREJAS', 'DUPLA_MAKER',
           'CARPETA', 'EDAD_IA', 'LLAVERO']

SCRATCH = 'https://scratch.mit.edu/projects/editor/'
TINKERCAD = 'https://www.tinkercad.com/'
MICROBIT = 'https://makecode.microbit.org/'
KIDDLE = 'https://www.kiddle.co/'
QUICKDRAW = 'https://quickdraw.withgoogle.com/'
AUTODRAW = 'https://www.autodraw.com/'

CARPETA = 'TIC_5_TuNombre'

EDAD_IA = ('La mayoría de las herramientas de IA que escriben o crean imágenes piden tener 13 años o más. Por eso en '
           'clase las usa tu profe: escribe tu prompt en el proyector o usa la cuenta escolar que autorice.')

LLAVERO = ('Tu usuario, tu contraseña y el código de la clase están en tu Perfil de Next-Level, en «🔑 Mi llavero de '
           'apps» (si tu profe ya los cargó).')

LEYENDA_SCRATCH = (
    '🧩 Cómo leer el código de abajo: cada renglón es un bloque de Scratch con el idioma en «Español Latinoamericano» '
    '(globo terráqueo, arriba a la izquierda). Lo que tiene sangría va DENTRO del bloque de arriba. Lo que está entre '
    'comillas lo escribes o lo eliges en la lista del bloque, y lo que está entre <picos> es una condición que se '
    'encaja en el hueco del bloque.')

LEYENDA_MICROBIT = (
    '🧩 Cómo leer el código de abajo: cada renglón es un bloque de MakeCode para micro:bit con el idioma en «Español '
    '(España)» (⚙️ → Idioma). Lo que tiene sangría va DENTRO del bloque de arriba. Lo que está entre comillas lo '
    'escribes tú y lo que está entre [corchetes] lo eliges en el bloque. ¿No encuentras uno? Escribe una palabra en el '
    'buscador de bloques, por ejemplo «pin».')

# La dinámica de las prácticas de computadora: cada quien en su compu, con su dupla al lado
PAREJAS = ['Cada quien en su computadora, con su propio proyecto.',
           'Tu dupla (el compañero de al lado) es tu copiloto: al terminar cada paso se revisan antes de seguir.',
           '¿Atorado? 1) Relee el paso, 2) pregúntale a tu dupla, 3) mano arriba y esperas al profe sin pararte.',
           'Semáforo de voz en 🟡: solo susurros con tu dupla. Señal «manos arriba»: sueltan el mouse y miran al '
           'frente.']

# La dinámica de las prácticas con la micro:bit: una tarjeta por dupla y los papeles se turnan
DUPLA_MAKER = ['Una micro:bit por dupla. Una persona programa en la computadora y la otra arma y conecta; a la mitad '
               'de la clase cambian de papel.',
               'La micro:bit se conecta y se desconecta solo cuando el profe lo indica, y siempre se toma por las '
               'orillas.',
               'Semáforo de voz en 🟡. Si algo no funciona, primero revisen juntos el cable y los bloques; después, '
               'mano arriba.']


def scratch(nombre, descripcion, codigo, xp=100, monedas=30):
    """Práctica de Scratch: se entrega una captura y trae los bloques escritos para no perderse."""
    return mision(nombre, 'evidencia', descripcion, xp, monedas, codigo=codigo.strip('\n'), link=SCRATCH)


def tinkercad(nombre, descripcion, xp=100, monedas=30):
    """Práctica de modelado 3D en Tinkercad: se entrega una captura del modelo."""
    return mision(nombre, 'evidencia', descripcion, xp, monedas, link=TINKERCAD)


def microbit(nombre, descripcion, codigo, xp=100, monedas=30):
    """Práctica de MakeCode para micro:bit: se entrega una captura (o foto de la tarjeta) y trae los bloques escritos."""
    return mision(nombre, 'evidencia', descripcion, xp, monedas, codigo=codigo.strip('\n'), link=MICROBIT)
