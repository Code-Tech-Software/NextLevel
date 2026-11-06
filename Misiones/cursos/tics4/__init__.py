"""TIC 4° · Pinion Learn 6.1 (versión 2): los temas de Pinion como punto de partida y, sobre todo, habilidades de
computación de verdad (Scratch, Tinkercad, procesador de textos y presentaciones), en 9 mundos con jefes.

Cada misión está escrita como una pequeña clase (lo que necesitas saber, paso a paso, cómo saber que lo lograste),
porque el profe la usa para dar la clase. Preguntas: (texto, respuesta correcta, [incorrectas]); al cargarse se
revuelven.
"""
from . import (
    m1_despegue, m2_materia, m3_gigantes, m4_plantastico, m5_sospechosamente, m6_arboles, m7_helecho, m8_foto, m9_codigo,
)
from .anteriores import ANTERIORES

MODULOS = [m1_despegue, m2_materia, m3_gigantes, m4_plantastico, m5_sospechosamente, m6_arboles, m7_helecho, m8_foto,
           m9_codigo]

JUEGOS = {}
for _modulo in MODULOS:
    JUEGOS.update(_modulo.JUEGOS)

CURSO = {
    'nombre': 'TIC 4° · Pinion Learn 6.1',
    'juegos': JUEGOS,
    'mundos': [modulo.MUNDO for modulo in MODULOS],
    # Al actualizar una clase que ya tenía la versión anterior, se retira lo que ya no forma parte del curso
    'anteriores': ANTERIORES,
}
