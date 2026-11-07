"""TIC 5° · Pinion Learn 6.1: los temas de Pinion (IA, Scratch, modelado 3D y circuitos con micro:bit) como punto de
partida y, sobre todo, habilidades de computación de verdad: hoja de cálculo con gráficas y fórmulas, procesador de
textos con columnas, presentaciones compartidas, IA responsable (Quick, Draw!, AutoDraw y prompts), Scratch,
Tinkercad, MakeCode para micro:bit y ciudadanía digital, en 9 mundos con jefes.

Pinion repite en 5.º algunas prácticas de 6.º (Azul profundo, Rescatador de lluvia, Día a día en otros planetas e
Inventario del futuro); aquí tienen su propia versión, más guiada y con otras herramientas, para que no sea una copia.
El grupo es inquieto y platicador: cada misión trae tiempos, duplas de máximo 2 y el «semáforo de voz».
Preguntas: (texto, respuesta correcta, [incorrectas]); al cargarse se revuelven.
"""
from . import m1_kepler, m2_davinci, m3_hubble, m4_alerta, m5_azul, m6_lluvia, m7_sombra, m8_respira, m9_ciudad

MODULOS = [m1_kepler, m2_davinci, m3_hubble, m4_alerta, m5_azul, m6_lluvia, m7_sombra, m8_respira, m9_ciudad]

JUEGOS = {}
for _modulo in MODULOS:
    JUEGOS.update(_modulo.JUEGOS)

CURSO = {
    'nombre': 'TIC 5° · Pinion Learn 6.1',
    'juegos': JUEGOS,
    'mundos': [modulo.MUNDO for modulo in MODULOS],
}
