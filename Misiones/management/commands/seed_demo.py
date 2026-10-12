import random

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from Misiones import gamificacion as juego
from Misiones import minijuegos
from Misiones.models import (
    Alumno, ArticuloTienda, Clase, Comportamiento, Equipo, Juego, MetaGrupo, Mision, Mundo, Nivel, OpcionRespuesta,
    PartidaJuego, Pregunta, ProgresoMision,
)

NOMBRE_CLASE = 'Robótica Demo'

ALUMNOS = [
    ('Valentina', 'Ríos'), ('Mateo', 'García'), ('Sofía', 'Hernández'), ('Santiago', 'López'),
    ('Regina', 'Martínez'), ('Diego', 'Torres'), ('Camila', 'Flores'), ('Emiliano', 'Cruz'),
]

ESTRUCTURA = [
    ('Bosque de los Circuitos', 'bosque', 'Donde la electricidad cobra vida entre los árboles.', [
        ('Primeras chispas', [
            ('¿Qué es un circuito?', 'video', 'Mira el video y descubre cómo viaja la electricidad.',
             {'link': 'https://www.youtube.com/watch?v=VnnpLaKsqGU'}),
            ('Quiz de electricidad', 'cuestionario', 'Demuestra lo que aprendiste sobre circuitos.', {}),
            ('¡Enciende un LED!', 'arduino', 'Conecta un LED al pin 13 y haz que parpadee cada segundo.',
             {'codigo': 'void setup() {\n  pinMode(13, OUTPUT);\n}\n\nvoid loop() {\n  digitalWrite(13, HIGH);\n  delay(1000);\n  digitalWrite(13, LOW);\n  delay(1000);\n}'}),
        ]),
        ('El semáforo', [
            ('Arma tu semáforo', 'evidencia', 'Construye un semáforo con 3 LEDs y toma una foto de tu circuito.', {}),
            ('Explica tu semáforo', 'texto', 'Con tus palabras, explica cómo funciona tu código del semáforo.', {}),
            ('Guardián del Bosque', 'cuestionario', '¡La batalla final del bosque! Responde todo para vencer al guardián.',
             {'es_jefe': True, 'xp_recompensa': 120, 'monedas_recompensa': 40}),
        ]),
    ]),
    ('Océano del Código', 'oceano', 'Sumérgete en el mundo de la programación por bloques.', [
        ('Bloques mágicos', [
            ('Explora Scratch', 'link', 'Entra a Scratch y crea tu primer personaje que se mueva.',
             {'link': 'https://scratch.mit.edu/'}),
            ('Lluvia de meteoros', 'juego', 'Escribe las palabras de robótica para destruir los meteoros antes de que caigan.',
             {'juego': 'meteoros'}),
            ('Exposición en equipo', 'presencial', 'Presenta tu proyecto frente al grupo.', {}),
        ]),
        ('Corrientes y ciclos', [
            ('Ciclos infinitos', 'cuestionario', '¿Sabes cuándo usar un ciclo? ¡Compruébalo!', {}),
            ('Kraken del Código', 'evidencia', 'Programa un juego de atrapar peces y sube una captura.',
             {'es_jefe': True, 'xp_recompensa': 150, 'monedas_recompensa': 50}),
        ]),
    ]),
    ('Galaxia Arduino', 'espacio', 'Sensores, motores y robots que exploran las estrellas.', [
        ('Sensores estelares', [
            ('El sensor ultrasónico', 'video', 'Aprende cómo los murciélagos (y los robots) miden distancias.',
             {'link': 'https://www.youtube.com/watch?v=6F1B_N6LuKw'}),
            ('Radar de proximidad', 'arduino', 'Haz que un buzzer suene cuando algo se acerque a menos de 10 cm.', {}),
            ('Rover explorador', 'juego', 'Programa al rover para que llegue a la batería sin chocar con las rocas.',
             {'juego': 'robot'}),
        ]),
    ]),
]

PREGUNTAS = [
    ('¿Qué necesita un circuito para funcionar?', ['Un camino cerrado', 'Un camino abierto', 'Solo un cable', 'Agua'], 0),
    ('¿Qué componente produce luz?', ['Resistencia', 'LED', 'Botón', 'Motor'], 1),
    ('El polo positivo de una pila se marca con…', ['−', '+', '×', '='], 1),
    ('¿Para qué sirve una resistencia?', ['Para limitar la corriente', 'Para dar luz', 'Para medir', 'Para nada'], 0),
]

ARTICULOS = [
    ('Stickers de robots', 'fisico', 'Un paquete de 5 stickers holográficos.', 40, 12, None, 1, True),
    ('Llavero Arduino', 'fisico', 'Llavero de acrílico con forma de placa Arduino.', 120, 3, 1, 2, True),
    ('Kit de LEDs de colores', 'fisico', '10 LEDs para tus proyectos en casa.', 200, 0, None, 1, False),
    ('Elige tu lugar por un día', 'permiso', 'Siéntate donde quieras durante una clase.', 60, None, None, 1, False),
    ('5 minutos extra de recreo', 'permiso', 'Úsalo con permiso del profe.', 90, None, 2, 1, False),
    ('Comodín de tarea', 'permiso', 'Cambia una tarea por otra actividad.', 250, None, 1, 3, True),
    ('DJ de la clase', 'permiso', 'Elige la música de fondo mientras trabajamos.', 75, None, None, 1, False),
]


class Command(BaseCommand):
    help = 'Crea una clase de demostración con mundos, misiones, tienda y alumnos con avances.'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Borra la clase demo anterior y la vuelve a crear')

    @transaction.atomic
    def handle(self, *args, **opciones):
        existente = Clase.objects.filter(nombre=NOMBRE_CLASE).first()
        if existente and not opciones['reset']:
            self.stdout.write(self.style.WARNING('La clase demo ya existe. Usa --reset para recrearla.'))
            return
        if existente:
            Alumno.objects.filter(clases=existente, apellido__in=[a for _, a in ALUMNOS]).delete()
            existente.delete()
            ArticuloTienda.objects.filter(nombre__in=[a[0] for a in ARTICULOS]).delete()

        clase = Clase.objects.create(nombre=NOMBRE_CLASE, grado='4°', grupo='B', anio=timezone.localdate().year,
                                     icono='🤖', color='cielo', descripcion='Clase de ejemplo de Next-Level')

        # Un juego que es misión del mapa (y se abre en el Arcade al superarla) y otro solo para el Arcade
        juegos = {
            'meteoros': Juego.objects.create(
                clase=clase, nombre='Lluvia de meteoros: Robótica', icono='☄️', plantilla='meteoros', desbloqueo='mision',
                descripcion='Practica escribiendo palabras de robótica.', monedas_arcade=5,
                configuracion={'palabras': minijuegos.TEMAS_PALABRAS['robotica'][2], 'duracion': 60, 'velocidad': 'lenta'}),
            'teclado': Juego.objects.create(
                clase=clase, nombre='Teclado misterioso: fila guía', icono='⌨️', plantilla='teclado', monedas_arcade=5,
                descripcion='Encuentra las teclas de la fila guía sin mirar.',
                configuracion={'conjunto': 'central', 'rondas': 20, 'modo': 'guiado'}),
            'robot': Juego.objects.create(
                clase=clase, nombre='Robot programador: primeros pasos', icono='🤖', plantilla='robot', monedas_arcade=5,
                descripcion='Programa al robot con flechas para llegar a la batería.',
                configuracion={'dificultad': 'facil', 'niveles': 5, 'modo': 'flechas', 'bucles': True}),
            'detective': Juego.objects.create(
                clase=clase, nombre='Detective digital: ¿sensor o actuador?', icono='🕵️', plantilla='clasifica',
                monedas_arcade=5, descripcion='¿Mide algo o hace algo? Clasifica los componentes del robot.',
                configuracion={'tema': 'robotica', 'rondas': 10, 'tiempo': 8, 'categorias': [
                    {'nombre': n, 'emoji': e, 'tarjetas': t} for n, e, t in minijuegos.TEMAS_CLASIFICA['robotica'][2]]}),
            'atajos': Juego.objects.create(
                clase=clase, nombre='Atajos ninja: editar texto', icono='🥷', plantilla='atajos', monedas_arcade=5,
                descripcion='Copiar, pegar, cortar y deshacer como un ninja del teclado.',
                configuracion={'atajos': minijuegos.GRUPOS_ATAJOS['texto'][2], 'rondas': 10, 'modo': 'aprende'}),
            'mensaje': Juego.objects.create(
                clase=clase, nombre='Mensaje secreto: código Morse', icono='📡', plantilla='mensaje', monedas_arcade=5,
                descripcion='Descifra palabras de robótica escritas en Morse.',
                configuracion={'cifrado': 'morse', 'palabras': minijuegos.TEMAS_PALABRAS['robotica'][2], 'rondas': 5}),
            'rutas': Juego.objects.create(
                clase=clase, nombre='Explorador de rutas: ¿dónde lo guardarías?', icono='📁', plantilla='rutas',
                monedas_arcade=5, descripcion='Encuentra cada archivo en su carpeta.',
                configuracion={'modo': 'buscar', 'dificultad': 'media', 'rondas': 5}),
            'formato': Juego.objects.create(
                clase=clase, nombre='Copia el formato: como en Word', icono='🎨', plantilla='formato', monedas_arcade=5,
                descripcion='Selecciona palabras y dales el mismo formato que el modelo.',
                configuracion={'dificultad': 'media', 'rondas': 5}),
        }

        misiones = []
        for orden_mundo, (nombre, tema, desc, niveles) in enumerate(ESTRUCTURA, start=1):
            mundo = Mundo.objects.create(clase=clase, nombre=nombre, tema=tema, descripcion=desc, orden=orden_mundo)
            for orden_nivel, (nombre_nivel, lista) in enumerate(niveles, start=1):
                nivel = Nivel.objects.create(clase=clase, mundo=mundo, nombre=nombre_nivel, orden=orden_nivel,
                                             recompensa_cofre=25)
                for orden, (titulo, tipo, descripcion, extra) in enumerate(lista, start=1):
                    datos = {'xp_recompensa': 60, 'monedas_recompensa': 20, **extra}
                    if tipo == 'juego':
                        datos['juego'] = juegos[extra['juego']]
                    mision = Mision.objects.create(clase=clase, nivel=nivel, nombre=titulo, tipo=tipo,
                                                   descripcion=descripcion, orden=orden, **datos)
                    if tipo == 'cuestionario':
                        for i, (texto, opciones_p, correcta) in enumerate(PREGUNTAS, start=1):
                            pregunta = Pregunta.objects.create(mision=mision, texto=texto, orden=i, puntos=10)
                            for j, opcion in enumerate(opciones_p):
                                OpcionRespuesta.objects.create(pregunta=pregunta, texto=opcion, es_correcta=(j == correcta))
                    misiones.append(mision)

        for nombre, tipo, desc, costo, stock, limite, nivel, destacado in ARTICULOS:
            ArticuloTienda.objects.create(nombre=nombre, tipo=tipo, descripcion=desc, costo_monedas=costo, stock=stock,
                                          limite_por_alumno=limite, nivel_requerido=nivel, destacado=destacado,
                                          requiere_validacion=tipo != 'avatar')

        rnd = random.Random(7)
        for indice, (nombre, apellido) in enumerate(ALUMNOS):
            alumno = Alumno.objects.create(nombre=nombre, apellido=apellido, pin='1234', monedas=30)
            alumno.clases.add(clase)
            avance = max(0, len(misiones) - 3 - indice * 2)
            for mision in misiones[:avance]:
                juego.calificar(ProgresoMision(alumno=alumno, mision=mision), rnd.choice([70, 80, 90, 100, 100]),
                                avisar=False)
            if avance < len(misiones) and mision_revisable(misiones[avance]) and indice % 2 == 0:
                ProgresoMision.objects.create(alumno=alumno, mision=misiones[avance], estado='pendiente',
                                              respuesta_texto='¡Ya quedó mi circuito, profe!')
            alumno.notificaciones.all().delete()

        # Casas, comportamientos y una meta del grupo para mostrar el modo clase
        for orden, (nombre, emoji, color) in enumerate(
                [('Leones', '🦁', 'ambar'), ('Dragones', '🐉', 'coral'), ('Águilas', '🦅', 'cielo'), ('Lobos', '🐺', 'uva')],
                start=1):
            Equipo.objects.create(clase=clase, nombre=nombre, emoji=emoji, color=color, orden=orden)
        juego.repartir_equipos(clase)
        positivos = list(Comportamiento.objects.filter(activo=True, monedas__gte=0))
        for alumno in clase.alumnos.all():
            for comportamiento in rnd.sample(positivos, min(2, len(positivos))):
                juego.registrar_conducta(alumno, clase, comportamiento)
            alumno.notificaciones.all().delete()
        MetaGrupo.objects.create(clase=clase, titulo='¡Viernes de película!', icono='🍿', tipo='conducta', objetivo=40,
                                 recompensa='🍿 Película con palomitas el viernes', monedas_recompensa=10)

        # Algunas partidas del Arcade para que el ranking ya tenga récords
        for alumno in list(clase.alumnos.all())[:5]:
            aciertos = rnd.randint(11, 20)
            PartidaJuego.objects.create(
                juego=juegos['teclado'], alumno=alumno, clase=clase, terminada=True, aciertos=aciertos, duracion=40,
                calificacion=aciertos * 5, estrellas=minijuegos.estrellas_de(aciertos * 5), precision=rnd.randint(75, 98),
                puntaje=aciertos * 100 + (20 - aciertos) * 40 + rnd.randint(2, 9) * 50)

        self.stdout.write(self.style.SUCCESS(
            f'Clase "{NOMBRE_CLASE}" creada con {len(misiones)} misiones y {len(ALUMNOS)} alumnos (PIN de todos: 1234).'
        ))


def mision_revisable(mision):
    return mision.tipo in ('arduino', 'link', 'evidencia', 'texto')
