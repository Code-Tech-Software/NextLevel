"""Cursos listos para cargar en una clase: mundos, niveles, misiones, jefes y minijuegos."""
import random
from importlib import import_module

from django.db.models import Max

from Misiones.models import Juego, Mision, Mundo, Nivel, OpcionRespuesta, Pregunta, ProgresoMision

CURSOS = {
    'tics4': ('Misiones.cursos.tics4', 'TIC 4° · Pinion Learn 6.1'),
    'tics6': ('Misiones.cursos.tics6', 'TIC 6° · Pinion Learn 6.1'),
    'robotica-baja': ('Misiones.cursos.robotica_primaria_baja', 'Robótica · Primaria Baja (Dash, Blockly y Bee-Bot)'),
    'robotica-alta': ('Misiones.cursos.robotica_primaria_alta', 'Robótica · Primaria Alta (kit Arduino Rexqualis R3)'),
}


def mision(nombre, tipo, descripcion, xp=50, monedas=15, **extra):
    """Una misión del curso; extra admite jefe, link, codigo, juego y preguntas (texto, correcta, [incorrectas])."""
    return {'nombre': nombre, 'tipo': tipo, 'descripcion': descripcion, 'xp': xp, 'monedas': monedas, **extra}


def obtener(clave):
    return import_module(CURSOS[clave][0]).CURSO


def _campos_mision(datos, nivel, orden, juego_de):
    return {
        'nivel': nivel, 'nombre': datos['nombre'], 'tipo': datos['tipo'], 'descripcion': datos['descripcion'],
        'xp_recompensa': datos['xp'], 'monedas_recompensa': datos['monedas'], 'orden': orden,
        'es_jefe': datos.get('jefe', False), 'link': datos.get('link'),
        'codigo': (datos.get('codigo') or '').strip() or None,
        'juego': juego_de(datos['juego']) if datos.get('juego') else None,
    }


def _crear_preguntas(mision, preguntas):
    for numero, (texto, correcta, incorrectas) in enumerate(preguntas, start=1):
        pregunta = Pregunta.objects.create(mision=mision, texto=texto, orden=numero, puntos=10)
        opciones = [(correcta, True)] + [(o, False) for o in incorrectas]
        # Siempre el mismo orden para la misma pregunta, pero la correcta no queda siempre arriba
        random.Random(texto).shuffle(opciones)
        OpcionRespuesta.objects.bulk_create(
            [OpcionRespuesta(pregunta=pregunta, texto=t, es_correcta=ok) for t, ok in opciones])
    return len(preguntas)


def _sincronizar_preguntas(mision, preguntas):
    """Rehace las preguntas solo si cambiaron (así no se pierden las respuestas guardadas sin necesidad)."""
    actuales = [
        (p.texto, next((o.texto for o in p.opciones.all() if o.es_correcta), None),
         sorted(o.texto for o in p.opciones.all() if not o.es_correcta))
        for p in mision.preguntas.prefetch_related('opciones').order_by('orden', 'id')
    ]
    if actuales == [(t, c, sorted(i)) for t, c, i in preguntas]:
        return 0
    mision.preguntas.all().delete()
    return _crear_preguntas(mision, preguntas)


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
                mision = Mision.objects.create(clase=clase, **_campos_mision(datos, nivel, orden, juego_de))
                resumen['misiones'] += 1
                resumen['jefes'] += mision.es_jefe
                resumen['preguntas'] += _crear_preguntas(mision, datos.get('preguntas', []))
    return resumen


def actualizar(clase, curso):
    """Pone al día en la clase un curso que ya estaba cargado.

    Corrige textos, preguntas y orden de lo que ya existe (mismo nombre dentro del mundo, así se conserva el avance de
    los alumnos), agrega lo nuevo y retira lo que era de la versión anterior del curso: si nadie lo ha hecho se borra;
    si algún alumno ya lo hizo, se oculta. Lo que el profe creó por su cuenta nunca se toca.
    """
    anteriores = curso.get('anteriores', {})
    misiones_viejas = set(anteriores.get('misiones', []))
    niveles_viejos = set(anteriores.get('niveles', []))
    juegos_viejos = set(anteriores.get('juegos', []))
    resumen = {'mundos': [], 'actualizados': [], 'niveles': 0, 'nuevas': 0, 'actualizadas': 0, 'retiradas': 0,
               'ocultas': 0, 'preguntas': 0, 'juegos': 0, 'juegos_retirados': 0}

    juegos = {}
    for clave, datos in curso['juegos'].items():
        juego = Juego.objects.filter(clase=clase, nombre=datos['nombre']).first()
        if juego:
            for campo, valor in datos.items():
                setattr(juego, campo, valor)
            juego.activo = True
            juego.save()
        else:
            juego = Juego.objects.create(clase=clase, desbloqueo='mision', monedas_arcade=5, **datos)
            resumen['juegos'] += 1
        juegos[clave] = juego

    orden_mundo = clase.mundos.aggregate(m=Max('orden'))['m'] or 0
    for datos_mundo in curso['mundos']:
        mundo = clase.mundos.filter(nombre=datos_mundo['nombre']).first()
        if mundo:
            mundo.tema, mundo.descripcion = datos_mundo['tema'], datos_mundo['descripcion']
            mundo.save(update_fields=['tema', 'descripcion'])
            resumen['actualizados'].append(mundo.nombre)
        else:
            orden_mundo += 1
            mundo = Mundo.objects.create(clase=clase, nombre=datos_mundo['nombre'], tema=datos_mundo['tema'],
                                         descripcion=datos_mundo['descripcion'], orden=orden_mundo)
            resumen['mundos'].append(mundo.nombre)

        existentes = {}
        for mision in Mision.objects.filter(clase=clase, nivel__mundo=mundo).order_by('id'):
            existentes.setdefault(mision.nombre, mision)
        niveles = {nivel.nombre: nivel for nivel in mundo.niveles.all()}
        usados = set()
        for orden_nivel, datos_nivel in enumerate(datos_mundo['niveles'], start=1):
            nivel = niveles.get(datos_nivel['nombre'])
            if nivel:
                nivel.orden, nivel.recompensa_cofre = orden_nivel, datos_nivel.get('cofre', 25)
                nivel.save(update_fields=['orden', 'recompensa_cofre'])
            else:
                nivel = Nivel.objects.create(clase=clase, mundo=mundo, nombre=datos_nivel['nombre'], orden=orden_nivel,
                                             recompensa_cofre=datos_nivel.get('cofre', 25))
                resumen['niveles'] += 1
            usados.add(nivel.id)
            for orden, datos in enumerate(datos_nivel['misiones'], start=1):
                campos = _campos_mision(datos, nivel, orden, juegos.__getitem__)
                mision = existentes.pop(datos['nombre'], None)
                if mision:
                    for campo, valor in campos.items():
                        setattr(mision, campo, valor)
                    mision.activa = True
                    mision.save()
                    resumen['actualizadas'] += 1
                    resumen['preguntas'] += _sincronizar_preguntas(mision, datos.get('preguntas', []))
                else:
                    mision = Mision.objects.create(clase=clase, **campos)
                    resumen['nuevas'] += 1
                    resumen['preguntas'] += _crear_preguntas(mision, datos.get('preguntas', []))

        for nombre, mision in existentes.items():
            if nombre not in misiones_viejas:
                continue    # la creó el profe: se queda como está
            if ProgresoMision.objects.filter(mision=mision).exists():
                if mision.activa:
                    mision.activa = False
                    mision.save(update_fields=['activa'])
                resumen['ocultas'] += 1
            else:
                mision.delete()
                resumen['retiradas'] += 1

        # Los niveles viejos que quedaron vacíos se borran; los demás (del profe) se acomodan al final del mundo
        siguiente = len(datos_mundo['niveles'])
        for nivel in mundo.niveles.exclude(id__in=usados).order_by('orden', 'id'):
            if nivel.nombre in niveles_viejos and not nivel.misiones.exists():
                nivel.delete()
            else:
                siguiente += 1
                nivel.orden = siguiente
                nivel.save(update_fields=['orden'])

    actuales = {datos['nombre'] for datos in curso['juegos'].values()}
    for juego in Juego.objects.filter(clase=clase, nombre__in=juegos_viejos).exclude(nombre__in=actuales):
        if juego.misiones.exists():
            continue    # el profe lo usa en otra misión
        if juego.partidas.exists():
            juego.activo, juego.en_arcade = False, False
            juego.save(update_fields=['activo', 'en_arcade'])
        else:
            juego.delete()
        resumen['juegos_retirados'] += 1
    return resumen
