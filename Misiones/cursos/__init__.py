"""Cursos listos para cargar en una clase: mundos, niveles, misiones, jefes y minijuegos."""
import random
from importlib import import_module

from django.db.models import Max

from Misiones.models import Juego, Mision, Mundo, Nivel, OpcionRespuesta, Pregunta

CURSOS = {
    'tics4': ('Misiones.cursos.tics4_pinion', 'TIC 4° · Pinion Learn 6.1'),
    'robotica-baja': ('Misiones.cursos.robotica_primaria_baja', 'Robótica · Primaria Baja (Dash, Blockly y Bee-Bot)'),
    'robotica-alta': ('Misiones.cursos.robotica_primaria_alta', 'Robótica · Primaria Alta (kit Arduino Rexqualis R3)'),
}


def mision(nombre, tipo, descripcion, xp=50, monedas=15, **extra):
    """Una misión del curso; extra admite jefe, link, codigo, juego y preguntas (texto, correcta, [incorrectas])."""
    return {'nombre': nombre, 'tipo': tipo, 'descripcion': descripcion, 'xp': xp, 'monedas': monedas, **extra}


def obtener(clave):
    return import_module(CURSOS[clave][0]).CURSO


def cargar(clase, curso):
    """Agrega el curso al final del mapa de la clase. Los mundos que ya existen (mismo nombre) se omiten."""
    resumen = {'mundos': [], 'omitidos': [], 'niveles': 0, 'misiones': 0, 'jefes': 0, 'preguntas': 0, 'juegos': 0}
    ya_existen = set(clase.mundos.values_list('nombre', flat=True))
    orden_mundo = clase.mundos.aggregate(m=Max('orden'))['m'] or 0
    juegos = {}

    def juego_de(clave):
        if clave not in juegos:
            datos = curso['juegos'][clave]
            juego = Juego.objects.filter(clase=clase, nombre=datos['nombre']).first()
            if not juego:
                # En el Arcade se abre hasta que el alumno supera su misión del mapa
                juego = Juego.objects.create(clase=clase, desbloqueo='mision', monedas_arcade=5, **datos)
                resumen['juegos'] += 1
            juegos[clave] = juego
        return juegos[clave]

    for datos_mundo in curso['mundos']:
        if datos_mundo['nombre'] in ya_existen:
            resumen['omitidos'].append(datos_mundo['nombre'])
            continue
        orden_mundo += 1
        mundo = Mundo.objects.create(clase=clase, nombre=datos_mundo['nombre'], tema=datos_mundo['tema'],
                                     descripcion=datos_mundo['descripcion'], orden=orden_mundo)
        resumen['mundos'].append(mundo.nombre)
        for orden_nivel, datos_nivel in enumerate(datos_mundo['niveles'], start=1):
            nivel = Nivel.objects.create(clase=clase, mundo=mundo, nombre=datos_nivel['nombre'], orden=orden_nivel,
                                         recompensa_cofre=datos_nivel.get('cofre', 25))
            resumen['niveles'] += 1
            for orden, datos in enumerate(datos_nivel['misiones'], start=1):
                mision = Mision.objects.create(
                    clase=clase, nivel=nivel, nombre=datos['nombre'], tipo=datos['tipo'], descripcion=datos['descripcion'],
                    xp_recompensa=datos['xp'], monedas_recompensa=datos['monedas'], orden=orden,
                    es_jefe=datos.get('jefe', False), link=datos.get('link'),
                    codigo=(datos.get('codigo') or '').strip() or None,
                    juego=juego_de(datos['juego']) if datos.get('juego') else None,
                )
                resumen['misiones'] += 1
                resumen['jefes'] += mision.es_jefe
                for numero, (texto, correcta, incorrectas) in enumerate(datos.get('preguntas', []), start=1):
                    pregunta = Pregunta.objects.create(mision=mision, texto=texto, orden=numero, puntos=10)
                    opciones = [(correcta, True)] + [(o, False) for o in incorrectas]
                    # Siempre el mismo orden para la misma pregunta, pero la correcta no queda siempre arriba
                    random.Random(texto).shuffle(opciones)
                    OpcionRespuesta.objects.bulk_create(
                        [OpcionRespuesta(pregunta=pregunta, texto=t, es_correcta=ok) for t, ok in opciones])
                    resumen['preguntas'] += 1
    return resumen
