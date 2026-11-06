"""TIC 6° · Pinion Learn 6.1: los temas de Pinion (videojuegos, documentos, 3D e IA) como punto de partida y, sobre
todo, habilidades de computación de verdad: MakeCode Arcade, procesador de textos en equipo, hoja de cálculo,
encuestas, Tinkercad, IA responsable y ciberseguridad, en 9 mundos con jefes.

El grupo es muy inquieto y ya se siente grande: cada misión está escrita como una pequeña clase con tiempos, roles y
señales claras («⏱️ Así se trabaja hoy», «👥 Roles»), y el tono es de estudio, laboratorio o redacción, nada infantil.
Preguntas: (texto, respuesta correcta, [incorrectas]); al cargarse se revuelven.
"""
from . import m1_abismo, m2_marte, m3_dinero, m4_local, m5_azul, m6_lluvia, m7_scifi, m8_museo, m9_ciber

MODULOS = [m1_abismo, m2_marte, m3_dinero, m4_local, m5_azul, m6_lluvia, m7_scifi, m8_museo, m9_ciber]

JUEGOS = {}
for _modulo in MODULOS:
    JUEGOS.update(_modulo.JUEGOS)

CURSO = {
    'nombre': 'TIC 6° · Pinion Learn 6.1',
    'juegos': JUEGOS,
    'mundos': [modulo.MUNDO for modulo in MODULOS],
}
