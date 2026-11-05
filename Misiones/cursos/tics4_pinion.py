"""TIC 4° · Pinion Learn 6.1: ciencia de Pinion + uso de la computadora, en 9 mundos con jefes.

Temas de Pinion: ES-SEA202 (¡Intenta, aprende, avanza! · Materia misteriosa), ES-SEA206 (Gigantes de la
Tierra · Secreto plantástico), ES-SEA207 (SospechosaMente · La rebelión de los árboles) y ES-SEA208
(Helecho bien hecho · Foto familiar). Cada mundo mezcla su tema con una habilidad de computación.

Preguntas: (texto, respuesta correcta, [respuestas incorrectas]); al cargarse se revuelven.
"""
from Misiones.cursos import mision
from Misiones.minijuegos import TEMAS_CLASIFICA, TEMAS_PALABRAS


def jefe(nombre, descripcion, preguntas, xp=150, monedas=50):
    return mision(nombre, 'cuestionario', descripcion, xp, monedas, jefe=True, preguntas=preguntas)


def clasifica(nombre, icono, descripcion, categorias, rondas=10, tiempo=12):
    return {'nombre': nombre, 'icono': icono, 'descripcion': descripcion, 'plantilla': 'clasifica', 'en_arcade': False,
            'configuracion': {'tema': 'personalizado', 'rondas': rondas, 'tiempo': tiempo, 'categorias': [
                {'nombre': n, 'emoji': e, 'tarjetas': list(t)} for n, e, t in categorias]}}


def meteoros(nombre, descripcion, palabras, velocidad='lenta'):
    return {'nombre': nombre, 'icono': '☄️', 'descripcion': descripcion, 'plantilla': 'meteoros', 'en_arcade': True,
            'configuracion': {'palabras': list(palabras), 'duracion': 60, 'velocidad': velocidad}}


# ========================
# MINIJUEGOS DEL CURSO (cada uno queda como misión del mapa; los de práctica también en el Arcade)
# ========================
JUEGOS = {
    'meteoros_partes': meteoros('Lluvia de meteoros: partes de la compu', 'Escribe las partes de la computadora antes de que caigan.',
                                TEMAS_PALABRAS['computadora'][2]),
    'clasifica_es': clasifica('Detective digital: ¿entrada o salida?', '🕵️', '¿Le da información a la compu o la saca?', [
        ('Entrada', '⌨️', ['Teclado', 'Mouse', 'Micrófono', 'Cámara web', 'Escáner', 'Control de videojuegos', 'Lápiz digital']),
        ('Salida', '🖥️', ['Monitor', 'Bocinas', 'Impresora', 'Audífonos', 'Proyector']),
        ('Entrada y salida', '🔄', ['Pantalla táctil', 'Audífonos con micrófono', 'Impresora que también escanea']),
    ], rondas=12),
    'robot_piloto': {'nombre': 'Robot piloto: prueba y corrige', 'icono': '🤖', 'plantilla': 'robot', 'en_arcade': True,
                     'descripcion': 'Programa al robot con flechas. Si choca, corrige y vuelve a intentar.',
                     'configuracion': {'dificultad': 'facil', 'niveles': 5, 'modo': 'flechas', 'bucles': False}},
    'teclado_central': {'nombre': 'Teclado misterioso: fila guía', 'icono': '⌨️', 'plantilla': 'teclado', 'en_arcade': True,
                        'descripcion': 'Encuentra las teclas A S D F – J K L Ñ sin mirar.',
                        'configuracion': {'conjunto': 'central', 'rondas': 20, 'modo': 'guiado'}},
    'clasifica_estados': clasifica('¿Sólido, líquido o gas?', '🧊', 'Clasifica cada sustancia según su estado de la materia.', [
        ('Sólido', '🧊', ['Hielo', 'Piedra', 'Lápiz', 'Cuchara', 'Sal', 'Madera', 'Moneda', 'Plastilina']),
        ('Líquido', '💧', ['Agua', 'Leche', 'Jugo de naranja', 'Aceite', 'Miel', 'Vinagre', 'Gotas de lluvia']),
        ('Gas', '💨', ['Vapor de agua', 'Aire', 'Oxígeno', 'Helio de un globo', 'Burbujas del refresco',
                      'Aire dentro de una llanta', 'Lo que exhalas al respirar']),
    ], rondas=12),
    'meteoros_materia': meteoros('Lluvia de meteoros: la materia', 'Escribe las palabras del laboratorio antes de que caigan.', [
        'materia', 'sólido', 'líquido', 'gas', 'vapor', 'hielo', 'agua', 'masa', 'volumen', 'fusión', 'evaporar',
        'condensar', 'mezcla', 'estado', 'calor', 'frío', 'gota', 'burbuja', 'derretir', 'congelar']),
    'clasifica_gigantes': clasifica('¿Extinto o vive hoy?', '🦕', 'Algunos gigantes desaparecieron y otros siguen aquí.', [
        ('Extinto', '🦴', ['Tiranosaurio rex', 'Mamut lanudo', 'Argentinosaurio', 'Megalodón', 'Triceratops',
                          'Tigre dientes de sable', 'Pterodáctilo']),
        ('Vive hoy', '🐘', ['Ballena azul', 'Elefante africano', 'Jirafa', 'Tiburón ballena', 'Secuoya gigante',
                           'Anaconda', 'Árbol del Tule', 'Calamar gigante']),
    ], rondas=12),
    'rutas_buscar': {'nombre': 'Explorador de rutas: ¿dónde lo guardo?', 'icono': '📁', 'plantilla': 'rutas', 'en_arcade': False,
                     'descripcion': 'Encuentra cada archivo en su carpeta.',
                     'configuracion': {'modo': 'buscar', 'dificultad': 'facil', 'rondas': 5}},
    'formato_plantas': {'nombre': 'Copia el formato: ficha de plantas', 'icono': '🎨', 'plantilla': 'formato', 'en_arcade': True,
                        'descripcion': 'Dale a cada frase el mismo formato que el modelo, como en Word.',
                        'configuracion': {'dificultad': 'facil', 'rondas': 5, 'frases': [
                            'La raíz absorbe el agua', 'El tallo sostiene la planta', 'Las hojas fabrican el alimento',
                            'La flor se convierte en fruto', 'La semilla guarda una nueva planta',
                            'Las plantas necesitan luz solar', 'Las plantas liberan oxígeno']}},
    'mensaje_planta': {'nombre': 'Mensaje secreto: el idioma de las plantas', 'icono': '🌻', 'plantilla': 'mensaje',
                       'en_arcade': True, 'descripcion': 'Descifra las palabras secretas de las plantas escritas con símbolos.',
                       'configuracion': {'cifrado': 'simbolos', 'rondas': 5, 'palabras': [
                           'raíz', 'tallo', 'hoja', 'flor', 'fruto', 'semilla', 'sol', 'agua', 'oxígeno', 'clorofila',
                           'polen', 'abeja']}},
    'atajos_texto': {'nombre': 'Atajos ninja: copia y pega del jardín', 'icono': '🥷', 'plantilla': 'atajos', 'en_arcade': False,
                     'descripcion': 'Copiar, pegar, cortar y deshacer sin usar el mouse.',
                     'configuracion': {'atajos': ['copiar', 'pegar', 'cortar', 'deshacer', 'rehacer', 'todo'],
                                       'rondas': 10, 'modo': 'aprende'}},
    'clasifica_datos': clasifica('¿Dato comprobado o mito?', '🔎', 'Separa los datos comprobados de los inventos.', [
        ('Dato comprobado', '✅', ['El agua hierve a 100 °C al nivel del mar', 'La Tierra gira alrededor del Sol',
                                  'Las plantas producen oxígeno', 'El corazón es un músculo', 'El Sol es una estrella',
                                  'Las arañas tienen ocho patas']),
        ('Mito o invento', '🚫', ['Los murciélagos son ciegos', 'Los peces dorados solo recuerdan 3 segundos',
                                 'Un chicle tragado se queda 7 años en tu estómago',
                                 'Un rayo nunca cae dos veces en el mismo lugar',
                                 'Los toros se enojan con el color rojo', 'Los camellos guardan agua en su joroba']),
    ], rondas=12),
    'mensaje_agencia': {'nombre': 'Mensaje cifrado de la agencia', 'icono': '🕵️', 'plantilla': 'mensaje', 'en_arcade': True,
                        'descripcion': 'Descifra los mensajes de la agencia escritos en código César.',
                        'configuracion': {'cifrado': 'cesar', 'desplazamiento': 2, 'rondas': 5, 'palabras': [
                            'pista', 'lupa', 'hipótesis', 'evidencia', 'detective', 'misterio', 'prueba', 'ciencia',
                            'caso', 'huella', 'sospecha']}},
    'clasifica_seguridad': clasifica('¿Seguro o peligroso?', '🛡️', 'Un buen detective también se cuida en internet.',
                                     TEMAS_CLASIFICA['seguridad'][2]),
    'clasifica_privacidad': clasifica('¿Público o privado?', '🔒', '¿Qué puedes compartir y qué es secreto de agente?',
                                      TEMAS_CLASIFICA['privacidad'][2]),
    'clasifica_bosque': clasifica('¿Ayuda o daña al bosque?', '🌳', 'Clasifica cada acción: ¿cuida a los árboles o los daña?', [
        ('Ayuda al bosque', '🌱', ['Plantar un árbol', 'Reciclar papel', 'Usar las hojas por los dos lados',
                                  'Apagar por completo una fogata', 'Regar los árboles del parque',
                                  'Cuidar los nidos de los pájaros', 'Usar bolsas de tela']),
        ('Daña al bosque', '🪓', ['Tirar basura en el bosque', 'Talar árboles sin volver a plantar',
                                 'Quemar pastizales', 'Desperdiciar hojas de papel', 'Dejar vidrios tirados en el pasto',
                                 'Arrancar plantas pequeñas por diversión']),
    ], rondas=12),
    'meteoros_bosque': meteoros('Lluvia de hojas', 'Escribe las palabras del bosque antes de que las hojas toquen el suelo.', [
        'árbol', 'raíz', 'tronco', 'rama', 'hoja', 'semilla', 'bosque', 'selva', 'oxígeno', 'sombra', 'nido', 'suelo',
        'reciclar', 'plantar', 'cuidar', 'agua', 'vida', 'tierra'], velocidad='normal'),
    'clasifica_semillas': clasifica('¿Con semilla o con esporas?', '🌿', 'Algunas plantas nacen de semillas y otras de esporas.', [
        ('Con semilla', '🌰', ['Frijol', 'Maíz', 'Girasol', 'Pino', 'Manzano', 'Aguacate', 'Rosal', 'Calabaza']),
        ('Con esporas', '🍃', ['Helecho', 'Musgo', 'Cola de caballo', 'Helecho arborescente', 'Hepática']),
    ], rondas=12),
    'teclado_superior': {'nombre': 'Teclado misterioso: fila de arriba', 'icono': '⌨️', 'plantilla': 'teclado', 'en_arcade': True,
                         'descripcion': 'Encuentra las teclas Q W E R T Y U I O P sin mirar.',
                         'configuracion': {'conjunto': 'superior', 'rondas': 20, 'modo': 'guiado'}},
    'meteoros_office': meteoros('Lluvia de meteoros: Word y Excel', 'Escribe las palabras de Word y Excel antes de que caigan.',
                                TEMAS_PALABRAS['office'][2], velocidad='normal'),
    'clasifica_herencia': clasifica('¿Lo heredé o lo aprendí?', '🧬', '¿Viene de tu familia, lo aprendiste o te pasó?', [
        ('Heredado', '🧬', ['El color de tus ojos', 'Tu tipo de cabello (lacio o rizado)', 'El color de tu piel',
                           'Los hoyuelos al sonreír', 'La forma de tu nariz', 'Tu tipo de sangre']),
        ('Aprendido', '📚', ['Hablar español', 'Andar en bicicleta', 'Saber nadar', 'Tocar la guitarra',
                            'Escribir en la computadora', 'Bailar']),
        ('Por el ambiente', '🩹', ['Una cicatriz en la rodilla', 'El cabello pintado de azul', 'Piel bronceada por el sol',
                                  'Un diente que se rompió']),
    ], rondas=12),
    'rutas_fotos': {'nombre': 'Explorador de rutas: el álbum perdido', 'icono': '🗂️', 'plantilla': 'rutas', 'en_arcade': True,
                    'descripcion': 'Sigue la ruta entre carpetas para encontrar cada archivo.',
                    'configuracion': {'modo': 'ruta', 'dificultad': 'media', 'rondas': 5}},
    'atajos_archivo': {'nombre': 'Atajos ninja: guarda, busca y da formato', 'icono': '💾', 'plantilla': 'atajos', 'en_arcade': True,
                       'descripcion': 'Guardar, imprimir, buscar, negrita, cursiva y subrayado con el teclado.',
                       'configuracion': {'atajos': ['guardar', 'imprimir', 'buscar', 'negrita', 'cursiva', 'subrayado'],
                                         'rondas': 10, 'modo': 'aprende'}},
    'robot_bucles': {'nombre': 'Robot programador: usa ciclos', 'icono': '🔁', 'plantilla': 'robot', 'en_arcade': True,
                     'descripcion': 'Caminos más largos: usa el bloque de repetir para programar menos.',
                     'configuracion': {'dificultad': 'media', 'niveles': 6, 'modo': 'flechas', 'bucles': True}},
    'mensaje_binario': {'nombre': 'Mensaje secreto: binario del programador', 'icono': '💻', 'plantilla': 'mensaje',
                        'en_arcade': False, 'descripcion': 'Descifra palabras de programación escritas con ceros y unos.',
                        'configuracion': {'cifrado': 'binario', 'rondas': 4, 'palabras': [
                            'bucle', 'robot', 'código', 'error', 'bloque', 'evento', 'scratch', 'ciclo', 'bug', 'datos']}},
    'meteoros_codigo': meteoros('Lluvia de meteoros: programación', 'Escribe las palabras de programación antes de que caigan.',
                                TEMAS_PALABRAS['programacion'][2], velocidad='normal'),
}


# ========================
# MUNDOS
# ========================
MUNDOS = [
    # ---------- ES-SEA202 · ¡Intenta, aprende, avanza! ----------
    {'nombre': 'Estación Despegue', 'tema': 'espacio',
     'descripcion': 'ES-SEA202 · ¡Intenta, aprende, avanza! Conoce tu nave (la computadora) y descubre el superpoder '
                    'de equivocarte y volver a intentarlo.',
     'niveles': [
         {'nombre': 'Conoce tu nave', 'cofre': 25, 'misiones': [
             mision('Reglas de la estación', 'presencial',
                    'Antes de despegar, la tripulación hace sus acuerdos del laboratorio de cómputo.\n\n'
                    '1. Escucha con tu equipo las reglas: manos limpias, nada de comida ni bebidas, cuidar cables y audífonos.\n'
                    '2. Aprende a encender la computadora y a apagarla desde el menú Inicio.\n'
                    '3. Siéntate como piloto: espalda recta, pies en el piso y la pantalla a la altura de tus ojos.\n\n'
                    'Tu profe marca esta misión cuando la tripulación la complete.', xp=40, monedas=10),
             mision('Lluvia de meteoros: partes de la compu', 'juego',
                    'Escribe el nombre de cada parte de la computadora antes de que el meteoro toque tu nave. '
                    '¡Si fallas, respira y vuelve a intentarlo!', juego='meteoros_partes'),
             mision('¿Conoces tu nave?', 'cuestionario', 'Demuestra que conoces las partes de la computadora y cómo usarla.',
                    xp=60, preguntas=[
                        ('¿Qué parte de la computadora muestra las imágenes?', 'El monitor', ['El teclado', 'Las bocinas', 'El mouse']),
                        ('¿Cuál es un dispositivo de entrada?', 'El teclado', ['La impresora', 'Las bocinas', 'El monitor']),
                        ('¿Qué parte es el «cerebro» de la computadora?', 'El procesador (CPU)', ['El mouse', 'La pantalla', 'El cable de luz']),
                        ('Para apagar la computadora correctamente debes…', 'Apagarla desde el menú Inicio',
                         ['Desconectar el cable', 'Apretar todas las teclas', 'Cerrar la tapa sin guardar']),
                        ('¿Qué haces con el mouse para abrir una carpeta?', 'Doble clic', ['Lo sacudes', 'Lo pones de cabeza', 'Lo desconectas']),
                        ('¿Cuál es la postura correcta frente a la computadora?', 'Espalda recta y pies en el piso',
                         ['Acostado en la silla', 'Con la cara pegada a la pantalla', 'Hincado sobre la silla']),
                    ]),
             mision('Detective digital: ¿entrada o salida?', 'juego',
                    '¿El dispositivo le da información a la computadora o la saca? Clasifica cada uno.', juego='clasifica_es'),
         ]},
         {'nombre': 'El error es mi copiloto', 'cofre': 30, 'misiones': [
             mision('Bitácora: el día que no me rendí', 'texto',
                    'Los ingenieros dicen: «Intenta, aprende, avanza». Escribe sobre algo que al principio no te salía y '
                    'que lograste con práctica (andar en bici, un videojuego, una tabla de multiplicar…).\n\n'
                    '• ¿Qué era?\n• ¿Qué cambiaste en cada intento?\n• ¿Qué aprendiste del error?', xp=60),
             mision('Reto Pinion: la torre que no se cae', 'evidencia',
                    'Usa el ciclo del ingeniero con tu kit Pinion (o con materiales del salón):\n\n'
                    '1. Pregunta: ¿cómo hago la torre más alta que aguante una goma?\n'
                    '2. Imagina y planea tu diseño.\n3. Crea tu torre.\n'
                    '4. Prueba: ¿se cayó? ¡Perfecto, ya sabes qué mejorar!\n5. Mejora y vuelve a probar.\n\n'
                    'Sube una foto de tu mejor versión.', xp=90, monedas=25),
             mision('Robot piloto: prueba y corrige', 'juego',
                    'Programa al robot con flechas para llegar a la batería. Si choca, revisa paso a paso y corrige: '
                    'así trabajan los ingenieros.', xp=60, juego='robot_piloto'),
             jefe('Jefe: Capitán Rendirse-Jamás',
                  'El Capitán Rendirse-Jamás solo deja pasar a quien sabe aprender de sus errores. '
                  '¡Responde todo para conquistar la estación!', [
                      ('Cuando algo no te sale a la primera, lo mejor es…', 'Intentarlo otra vez con una idea nueva',
                       ['Rendirte', 'Culpar a alguien más', 'Copiarle al de junto']),
                      ('Un error sirve para…', 'Aprender qué cambiar', ['Sentirte mal', 'Dejar de intentarlo', 'Nada']),
                      ('¿Cuál es el orden del ciclo del ingeniero?', 'Preguntar → Imaginar → Planear → Crear → Probar y mejorar',
                       ['Crear → Rendirse → Imaginar', 'Probar → Terminar sin mejorar', 'Mejorar → Crear → Preguntar']),
                      ('Decir «todavía no lo sé hacer» significa que…', 'Puedo aprenderlo con práctica',
                       ['Nunca lo voy a lograr', 'No sirvo para eso', 'Otro lo debe hacer por mí']),
                      ('¿Cuál de estos es un dispositivo de salida?', 'Las bocinas', ['El teclado', 'El micrófono', 'El mouse']),
                      ('El mouse sirve para…', 'Señalar y seleccionar en la pantalla', ['Imprimir', 'Guardar la luz', 'Cargar la batería']),
                      ('Si tu robot no llega a la meta, ¿qué haces primero?', 'Reviso paso a paso dónde se equivocó',
                       ['Borro todo y me rindo', 'Digo que la compu está mal', 'Apago la compu']),
                      ('¿Cuál regla del laboratorio es correcta?', 'No comer ni beber cerca de la computadora',
                       ['Jalar los cables para apagarla', 'Golpear el teclado si se traba', 'Cambiar la configuración de otra compu']),
                  ]),
         ]},
     ]},

    # ---------- ES-SEA202 · Materia misteriosa ----------
    {'nombre': 'Laboratorio de la Materia Misteriosa', 'tema': 'hielo',
     'descripcion': 'ES-SEA202 · Materia misteriosa. Sólidos, líquidos y gases te esperan en un laboratorio congelado… '
                    'y una sustancia que no sabe si es sólida o líquida.',
     'niveles': [
         {'nombre': 'Detectives de la materia', 'cofre': 25, 'misiones': [
             mision('Teclado misterioso: fila guía', 'juego',
                    'Los científicos escriben sus descubrimientos rapidísimo. Coloca tus dedos en la fila guía '
                    '(A S D F – J K L Ñ) y encuentra cada tecla sin mirar.', juego='teclado_central'),
             mision('¿Qué es la materia?', 'cuestionario', 'Todo lo que te rodea es materia… ¿o no? Compruébalo.', xp=60, preguntas=[
                 ('La materia es…', 'Todo lo que tiene masa y ocupa un lugar',
                  ['Solo lo que podemos comer', 'Solo lo que es sólido', 'Solo los seres vivos']),
                 ('¿Cuál de estos NO es materia?', 'Una sombra', ['El aire', 'El agua', 'Una piedra']),
                 ('Los tres estados de la materia que más vemos son…', 'Sólido, líquido y gaseoso',
                  ['Frío, tibio y caliente', 'Grande, mediano y chico', 'Duro, blando y suave']),
                 ('Un líquido…', 'Toma la forma del recipiente que lo contiene',
                  ['Siempre tiene la misma forma', 'No ocupa espacio', 'No tiene masa']),
                 ('Un gas…', 'Se expande y ocupa todo el espacio que tiene',
                  ['Tiene forma fija como una piedra', 'Siempre se puede ver', 'Se puede cortar con tijeras']),
                 ('¿Con qué instrumento medimos la masa de un objeto?', 'Con una balanza o báscula', ['Con un termómetro', 'Con una regla', 'Con un reloj']),
             ]),
             mision('¿Sólido, líquido o gas?', 'juego', 'Clasifica cada sustancia según su estado de la materia.', juego='clasifica_estados'),
         ]},
         {'nombre': 'La sustancia misteriosa', 'cofre': 30, 'misiones': [
             mision('Experimento: la materia misteriosa', 'evidencia',
                    'Con ayuda de tu profe, mezcla 2 tazas de maicena con 1 taza de agua (puedes agregar colorante).\n\n'
                    '1. Toca la mezcla despacio: ¿qué pasa?\n2. Ahora golpéala rápido con el dedo: ¿qué pasa?\n'
                    '3. Toma un puño, apriétalo y luego abre la mano.\n\n'
                    'Sube una foto de tu experimento. ⚠️ No la tires al lavabo: lo tapa.', xp=90, monedas=25),
             mision('¿Sólido o líquido? Tú decides', 'texto',
                    'Después del experimento, explica con tus palabras: ¿la materia misteriosa es sólida, líquida o las dos '
                    'cosas? Da al menos dos evidencias de lo que observaste.', xp=60),
             mision('Lluvia de meteoros: la materia', 'juego',
                    'Escribe las palabras del laboratorio antes de que caigan. Los acentos son opcionales.', juego='meteoros_materia'),
         ]},
         {'nombre': 'El congelador del jefe', 'cofre': 40, 'misiones': [
             mision('Carrera de cubos de hielo', 'presencial',
                    'En equipos, cada uno recibe un cubo de hielo. Gana el equipo que lo derrita más rápido ¡sin meterlo a la boca!\n\n'
                    'Antes de empezar, escriban su hipótesis: ¿qué método funcionará mejor y por qué? '
                    'Al terminar, comparen: ¿acertaron?'),
             jefe('Jefe: La Gelatina Mutante',
                  'Una gelatina mutante cambia de estado a su antojo. Solo podrás vencerla si dominas la fusión, '
                  'la evaporación, la condensación y la solidificación.', [
                      ('Cuando el hielo se derrite pasa de sólido a líquido. A eso se le llama…', 'Fusión',
                       ['Evaporación', 'Condensación', 'Solidificación']),
                      ('Cuando el agua de un charco desaparece con el sol, se…', 'Evapora', ['Congela', 'Solidifica', 'Condensa']),
                      ('Las gotitas que aparecen afuera de un vaso con agua muy fría se forman por…', 'Condensación',
                       ['Fusión', 'Evaporación', 'Magia']),
                      ('Si metes agua al congelador se convierte en hielo. Eso es…', 'Solidificación',
                       ['Evaporación', 'Fusión', 'Condensación']),
                      ('¿Qué hace que la materia cambie de estado?', 'Subir o bajar su temperatura',
                       ['Cambiarla de color', 'Ponerle nombre', 'Moverla de lugar']),
                      ('La mezcla de maicena con agua es misteriosa porque…', 'Se pone dura si la golpeas y escurre si la mueves despacio',
                       ['Es un gas', 'Brilla en la oscuridad', 'Se evapora al instante']),
                      ('¿Qué estado de la materia tiene forma propia?', 'El sólido', ['El líquido', 'El gaseoso', 'Ninguno']),
                      ('Cuando el agua hierve se convierte en vapor. El vapor es agua en estado…', 'Gaseoso',
                       ['Sólido', 'Líquido', 'Congelado']),
                  ]),
         ]},
     ]},

    # ---------- ES-SEA206 · Gigantes de la Tierra ----------
    {'nombre': 'Valle de los Gigantes', 'tema': 'desierto',
     'descripcion': 'ES-SEA206 · Gigantes de la Tierra. Montañas, volcanes, dinosaurios y los seres vivos más enormes '
                    'del planeta. ¡Investiga en internet como un explorador de verdad!',
     'niveles': [
         {'nombre': 'Expedición a los gigantes', 'cofre': 25, 'misiones': [
             mision('Vuela por el planeta con Google Earth', 'link',
                    'Abre Google Earth y busca estos gigantes:\n\n'
                    '1. El Pico de Orizaba (Citlaltépetl), la montaña más alta de México.\n2. El volcán Popocatépetl.\n'
                    '3. El monte Everest, la montaña más alta del mundo.\n4. El Árbol del Tule, en Oaxaca.\n\n'
                    'En el comentario, cuéntale a tu profe cuál te pareció más impresionante y por qué.',
                    xp=60, link='https://earth.google.com/web/'),
             mision('Gigantes de ayer y hoy', 'cuestionario', '¿Cuánto sabes de los gigantes del planeta?', xp=60, preguntas=[
                 ('¿Cuál es el animal más grande que se conoce?', 'La ballena azul',
                  ['El tiranosaurio rex', 'El elefante africano', 'La jirafa']),
                 ('Un fósil es…', 'El resto o la huella de un ser vivo de hace mucho tiempo, guardado en la roca',
                  ['Una piedra preciosa', 'Un dinosaurio vivo', 'Un tipo de planta']),
                 ('¿Cuál es la montaña más alta de México?', 'El Pico de Orizaba (Citlaltépetl)',
                  ['El Popocatépetl', 'El monte Everest', 'El Cerro de la Silla']),
                 ('¿Cuál es la montaña más alta del mundo?', 'El monte Everest',
                  ['El Pico de Orizaba', 'El Iztaccíhuatl', 'El Cerro del Tepeyac']),
                 ('Los dinosaurios…', 'Se extinguieron hace unos 66 millones de años',
                  ['Viven en las selvas de hoy', 'Convivieron con nuestros abuelos', 'Nunca existieron']),
                 ('El Árbol del Tule, en Oaxaca, es famoso porque…', 'Tiene uno de los troncos más anchos del mundo',
                  ['Es el árbol más bajito', 'Da manzanas gigantes', 'Está hecho de plástico']),
             ]),
             mision('¿Extinto o vive hoy?', 'juego',
                    'Algunos gigantes desaparecieron hace millones de años y otros siguen aquí. ¡Clasifícalos!', juego='clasifica_gigantes'),
         ]},
         {'nombre': 'Buscadores de datos', 'cofre': 30, 'misiones': [
             mision('Búsqueda segura con Kiddle', 'link',
                    'Kiddle es un buscador para niños. Elige un gigante (un dinosaurio, un volcán, un animal o un árbol) e investiga:\n\n'
                    '• ¿Cuánto mide o medía?\n• ¿Dónde vive o vivía?\n• Un dato curioso.\n\n'
                    '💡 Usa palabras clave: escribe «tamaño ballena azul», no «hola quiero saber cuánto mide la ballena azul».\n\n'
                    'Escribe tus tres datos en el comentario para tu profe.', xp=60, link='https://www.kiddle.co/'),
             mision('Explorador de rutas: ¿dónde lo guardo?', 'juego',
                    'Antes de crear tu ficha, aprende a encontrar cada archivo en su carpeta.', juego='rutas_buscar'),
             mision('Ficha del gigante en Word', 'evidencia',
                    'Crea en Word (o Google Docs) la ficha de tu gigante:\n\n'
                    '1. Un título grande con el nombre del gigante.\n2. Una imagen.\n3. Tres datos que investigaste.\n'
                    '4. Al final: «Fuente:» y la página de donde sacaste la información.\n\n'
                    'Guárdala con tu nombre (por ejemplo: Ficha_Ana) y sube una foto o captura de pantalla.', xp=90, monedas=25),
         ]},
         {'nombre': 'La cueva del titán', 'cofre': 40, 'misiones': [
             jefe('Jefe: El Titán de Piedra',
                  'Un titán de piedra despertó en el valle. Solo los exploradores que saben de gigantes y de búsquedas '
                  'seguras pueden calmarlo.', [
                      ('¿Qué sale de un volcán cuando hace erupción?', 'Lava, ceniza y gases', ['Agua de mar', 'Nieve', 'Arena de playa']),
                      ('El Popocatépetl es…', 'Un volcán activo de México', ['Un dinosaurio', 'Un río', 'Una isla']),
                      ('Un paleontólogo estudia…', 'Los fósiles', ['Las estrellas', 'Las computadoras', 'El clima de mañana']),
                      ('Para buscar información de forma segura es mejor…', 'Usar palabras clave en un buscador para niños',
                       ['Dar clic en cualquier anuncio', 'Escribir tus datos personales', 'Abrir todas las ventanas que aparezcan']),
                      ('¿Cuál es la mejor búsqueda para saber cuánto medía un tiranosaurio?', 'tamaño tiranosaurio rex',
                       ['hola', 'dinosaurio', 'dime cosas por favor']),
                      ('Si usas información de internet en tu trabajo debes…', 'Escribir de qué página la sacaste',
                       ['Decir que tú la inventaste', 'Copiarla toda sin leer', 'Borrar el nombre del autor']),
                      ('Para guardar tu ficha en una carpeta específica usas…', 'Guardar como… y eliges la carpeta',
                       ['Imprimir', 'Cerrar sin guardar', 'Copiar']),
                      ('¿Qué comía el tiranosaurio rex?', 'Carne: era carnívoro', ['Solo plantas', 'Solo frutas', 'Nada']),
                  ]),
         ]},
     ]},

    # ---------- ES-SEA206 · Secreto plantástico ----------
    {'nombre': 'Jardín Plantástico', 'tema': 'dulces',
     'descripcion': 'ES-SEA206 · Secreto plantástico. Las plantas guardan un secreto: fabrican su propia comida con la '
                    'luz del sol. Descúbrelo mientras dominas Word.',
     'niveles': [
         {'nombre': 'Una semilla curiosa', 'cofre': 25, 'misiones': [
             mision('Germinador: mi frijol mágico', 'evidencia',
                    'Pon algodón húmedo en un vaso transparente y coloca 2 o 3 frijoles pegados a la pared del vaso. '
                    'Déjalo cerca de una ventana y mantén el algodón húmedo.\n\n'
                    'Sube una foto del primer día. ¡En las siguientes clases verás qué pasa!', xp=80, monedas=20),
             mision('Partes de la planta', 'cuestionario', 'Raíz, tallo, hojas, flor, fruto y semilla: ¿para qué sirve cada una?',
                    xp=60, preguntas=[
                        ('¿Qué parte de la planta absorbe el agua del suelo?', 'La raíz', ['La flor', 'La hoja', 'El fruto']),
                        ('El tallo sirve para…', 'Sostener la planta y llevar el agua a las hojas',
                         ['Producir semillas', 'Atraer abejas', 'Nada']),
                        ('¿En qué parte de la planta se fabrica su alimento?', 'En las hojas', ['En la raíz', 'En la semilla', 'En la maceta']),
                        ('¿Qué se forma a partir de la flor?', 'El fruto, con semillas adentro', ['La raíz', 'El tallo', 'Las hojas']),
                        ('¿Qué necesita una planta para vivir?', 'Luz, agua, aire y suelo con nutrientes',
                         ['Solo oscuridad', 'Solo refresco', 'Música fuerte']),
                        ('La semilla…', 'Guarda una nueva planta y su primer alimento',
                         ['Es una hoja seca', 'Es una piedra', 'Es una raíz muerta']),
                    ]),
             mision('Copia el formato: ficha de plantas', 'juego',
                    'Selecciona las palabras y dales el mismo formato que el modelo, como en Word.', juego='formato_plantas'),
         ]},
         {'nombre': 'El secreto verde', 'cofre': 30, 'misiones': [
             mision('Mensaje secreto: el idioma de las plantas', 'juego',
                    'Las plantas te dejaron mensajes escritos con símbolos. Descífralos para descubrir sus partes secretas.',
                    juego='mensaje_planta'),
             mision('Atajos ninja: copia y pega del jardín', 'juego',
                    'Copiar, pegar, cortar y deshacer sin usar el mouse. ¡Así se escribe rápido una ficha!', juego='atajos_texto'),
             mision('Diario de mi frijol en Word', 'evidencia',
                    'Haz en Word una tabla para registrar cómo crece tu frijol con tres columnas: Día · ¿Qué observo? · '
                    'Altura (cm).\n\nLlena al menos 3 días, ponle un título en negrita y agrega una imagen o un dibujo. '
                    'Sube una captura de pantalla.', xp=90, monedas=25),
         ]},
         {'nombre': 'Invernadero del jefe', 'cofre': 40, 'misiones': [
             jefe('Jefe: La Planta Carnívora Gigante',
                  '¡Una planta carnívora gigante custodia el invernadero! Solo se calmará si demuestras que conoces el '
                  'secreto plantástico: la fotosíntesis.', [
                      ('¿Cómo se llama el proceso con el que las plantas fabrican su alimento con la luz del sol?', 'Fotosíntesis',
                       ['Digestión', 'Evaporación', 'Germinación']),
                      ('Durante la fotosíntesis, las plantas liberan al aire…', 'Oxígeno', ['Humo', 'Plástico', 'Arena']),
                      ('El color verde de las hojas se debe a la…', 'Clorofila', ['Pintura', 'Tierra', 'Lluvia']),
                      ('Cuando a una semilla le sale su primera raíz decimos que…', 'Germinó', ['Se evaporó', 'Se derritió', 'Se apagó']),
                      ('Las abejas ayudan a las plantas porque…', 'Llevan el polen de flor en flor',
                       ['Se comen sus raíces', 'Les dan sombra', 'Las riegan']),
                      ('En Word, para poner una palabra en negrita primero debes…', 'Seleccionarla',
                       ['Borrarla', 'Imprimirla', 'Cerrar Word']),
                      ('Para poner en otro lugar un texto que copiaste usas…', 'Pegar', ['Cortar', 'Borrar', 'Cerrar']),
                      ('Una planta que pasa muchos días en un cuarto oscuro…', 'Se pone amarilla y débil porque no puede hacer fotosíntesis',
                       ['Se pone más verde', 'Da más frutos', 'No le pasa nada']),
                  ]),
         ]},
     ]},

    # ---------- ES-SEA207 · SospechosaMente ----------
    {'nombre': 'Agencia SospechosaMente', 'tema': 'ciudad',
     'descripcion': 'ES-SEA207 · SospechosaMente. Piensa como detective y como científico: observa, haz hipótesis, busca '
                    'evidencias y no te dejes engañar por lo que ves en internet.',
     'niveles': [
         {'nombre': 'Academia de detectives', 'cofre': 25, 'misiones': [
             mision('El método del detective', 'cuestionario', 'Los científicos investigan como detectives. ¿Conoces sus pasos?',
                    xp=60, preguntas=[
                        ('¿Cuál es el primer paso para investigar como científico?', 'Observar y hacerte una pregunta',
                         ['Escribir la conclusión', 'Adivinar sin mirar', 'Rendirte']),
                        ('Una hipótesis es…', 'Una posible respuesta que vas a comprobar',
                         ['Una respuesta segura y final', 'Un tipo de lupa', 'Un dibujo']),
                        ('Para saber si tu hipótesis es correcta debes…', 'Hacer un experimento y observar los resultados',
                         ['Preguntarle a tu mascota', 'Elegir la que más te guste', 'Hacer una votación']),
                        ('Una evidencia es…', 'Algo que puedes observar o medir y que apoya una idea',
                         ['Lo que piensas sin pruebas', 'Un chisme', 'Un sueño']),
                        ('¿Cuál es una opinión y no un dato?', 'El helado de fresa es el más rico',
                         ['El agua hierve a 100 °C al nivel del mar', 'La Tierra gira alrededor del Sol', 'Una araña tiene ocho patas']),
                        ('Si el experimento no sale como tu hipótesis…', 'Aprendes algo nuevo y haces otra hipótesis',
                         ['Escondes los resultados', 'Cambias los resultados', 'Dejas de investigar']),
                    ]),
             mision('La caja misteriosa', 'presencial',
                    'Tu profe tiene una caja con un objeto secreto. Sin ver adentro:\n\n'
                    '1. Agítala, escúchala y siente su peso.\n2. Escribe tu hipótesis: ¿qué crees que es?\n'
                    '3. Anota tus evidencias (suena como…, pesa como…).\n4. ¡Comprueba al final si acertaste!'),
             mision('Caso: la planta marchita', 'texto',
                    'La planta del salón amaneció marchita. Como detective-científico:\n\n'
                    '1. Escribe dos hipótesis de lo que pudo pasar.\n2. Elige una y explica qué experimento harías para comprobarla.\n'
                    '3. ¿Qué evidencia te diría que tenías razón?', xp=70, monedas=20),
         ]},
         {'nombre': 'Caso: noticias falsas', 'cofre': 30, 'misiones': [
             mision('¿Dato comprobado o mito?', 'juego',
                    'En internet circulan muchos mitos. Usa tu mente sospechosa para separar los datos comprobados de los inventos.',
                    juego='clasifica_datos'),
             mision('Mensaje cifrado de la agencia', 'juego',
                    'La agencia manda sus mensajes en código César: cada letra se recorre dos lugares en el abecedario. ¡Descífralos!',
                    juego='mensaje_agencia'),
             mision('¿Verdad o engaño? Investiga', 'texto',
                    'Elige uno de estos rumores e investígalo en Kiddle o en una página confiable:\n\n'
                    '• «Los murciélagos son ciegos.»\n• «Los peces dorados solo recuerdan 3 segundos.»\n'
                    '• «Los toros se enojan con el color rojo.»\n\n'
                    'Escribe: ¿es verdad o mito?, ¿qué evidencia encontraste? y ¿de qué página la sacaste?', xp=70, monedas=20),
         ]},
         {'nombre': 'Ciberdetectives', 'cofre': 40, 'misiones': [
             mision('¿Seguro o peligroso?', 'juego', 'Un buen detective también se cuida en internet. Clasifica cada situación.',
                    juego='clasifica_seguridad'),
             mision('¿Público o privado?', 'juego', '¿Qué información puedes compartir y cuál debes guardar como un secreto de agente?',
                    juego='clasifica_privacidad'),
             jefe('Jefe: El Gran Embaucador',
                  'El Gran Embaucador llena internet de engaños. Usa tu mente sospechosa: hipótesis, evidencias, fuentes '
                  'confiables y cuidado de tus datos.', [
                      ('Ves en internet: «¡Comer 10 chocolates al día te hace más inteligente!». ¿Qué haces?',
                       'Desconfío y lo reviso en fuentes confiables', ['Lo comparto con todos', 'Lo creo porque está en internet', 'Me como 10 chocolates']),
                      ('Una fuente confiable es…', 'La página de un museo, una universidad o una institución reconocida',
                       ['Un comentario sin nombre', 'Un video que solo dice «créeme»', 'Un mensaje en cadena']),
                      ('Un mensaje dice: «Reenvía esto a 10 personas o tendrás mala suerte». Es…', 'Un engaño: no lo reenvío',
                       ['Verdad', 'Una tarea', 'Un premio']),
                      ('¿Cómo es una contraseña segura?', 'Larga, con letras, números y símbolos, y solo tú la sabes',
                       ['Tu nombre', '1234', 'La misma que la de tu amigo']),
                      ('¿Con quién puedes compartir tus contraseñas?', 'Con mis papás o tutores',
                       ['Con mi mejor amigo', 'Con quien me la pida en un juego', 'Con cualquiera que la quiera']),
                      ('Alguien que no conoces te pide tu dirección en un videojuego. ¿Qué haces?',
                       'No respondo, lo bloqueo y le aviso a un adulto', ['Le doy mi dirección', 'Le mando una foto', 'Lo invito a mi casa']),
                      ('La planta del salón se marchitó. ¿Cuál es una buena hipótesis?', 'Se marchitó porque le faltó agua',
                       ['Las plantas son aburridas', 'Los martes no hay plantas', 'Porque sí']),
                      ('Si cada letra se recorre un lugar (A→B), ¿cómo se escribe CASA?', 'DBTB', ['BZRZ', 'CASA', 'EBUB']),
                  ]),
         ]},
     ]},

    # ---------- ES-SEA207 · La rebelión de los árboles ----------
    {'nombre': 'Bosque en Rebelión', 'tema': 'bosque',
     'descripcion': 'ES-SEA207 · La rebelión de los árboles. ¡Los árboles están hartos de que los talen! Descubre todo lo '
                    'que hacen por nosotros y crea una campaña digital para defenderlos.',
     'niveles': [
         {'nombre': '¿Por qué se rebelan?', 'cofre': 25, 'misiones': [
             mision('Lo que los árboles hacen por nosotros', 'cuestionario', 'Oxígeno, sombra, hogar… ¿qué más nos dan los árboles?',
                    xp=60, preguntas=[
                        ('Los árboles producen…', 'El oxígeno que respiramos', ['Plástico', 'Humo', 'Gasolina']),
                        ('Las raíces de los árboles ayudan a…', 'Sostener el suelo para que la lluvia no se lo lleve',
                         ['Hacer ruido', 'Atraer rayos', 'Secar los ríos']),
                        ('¿Qué es la deforestación?', 'Cortar o destruir muchos árboles de un bosque o una selva',
                         ['Plantar árboles', 'Regar flores', 'Un tipo de fruta']),
                        ('¿Quién pierde su hogar cuando se tala un bosque?', 'Aves, ardillas, insectos y muchos animales más',
                         ['Nadie', 'Solo los peces del mar', 'Solo las mascotas']),
                        ('¿Qué puedes hacer para ahorrar papel?', 'Usar las hojas por los dos lados y reciclar',
                         ['Tirar hojas casi nuevas', 'Imprimir todo dos veces', 'Usar una hoja por cada palabra']),
                        ('Las tres R significan…', 'Reducir, Reutilizar y Reciclar',
                         ['Romper, Rayar y Regalar', 'Reír, Rodar y Rugir', 'Rápido, Recto y Redondo']),
                    ]),
             mision('¿Ayuda o daña al bosque?', 'juego', 'Clasifica cada acción: ¿cuida a los árboles o los daña?', juego='clasifica_bosque'),
             mision('Lluvia de hojas', 'juego', 'Escribe las palabras del bosque antes de que las hojas toquen el suelo.',
                    juego='meteoros_bosque'),
         ]},
         {'nombre': 'Campaña verde', 'cofre': 30, 'misiones': [
             mision('Póster digital: ¡Salva un árbol!', 'evidencia',
                    'Dibuja en Paint (o en el programa de dibujo de tu compu) un póster para defender a los árboles:\n\n'
                    '• Un título llamativo.\n• Un dibujo de un árbol y de lo que nos da.\n• Una acción que todos podemos hacer.\n\n'
                    'Guárdalo como imagen con tu nombre (por ejemplo: Poster_Ana) y súbelo.', xp=90, monedas=25),
             mision('Presentación: el juicio de los árboles', 'evidencia',
                    'Crea una presentación de 4 diapositivas en PowerPoint (o Google Slides):\n\n'
                    '1. Portada con título e integrantes.\n2. El problema: ¿qué les pasa a los bosques?\n'
                    '3. ¿Por qué importan los árboles?\n4. ¿Qué podemos hacer nosotros?\n\n'
                    'Agrega imágenes y una transición. Sube una captura de tu diapositiva favorita.', xp=100, monedas=30),
             mision('Exposición: los árboles tienen la palabra', 'presencial',
                    'Presenta tu campaña frente al grupo como si fueras el abogado de los árboles. ¡Convence a todos de cuidarlos!',
                    xp=60, monedas=20),
         ]},
         {'nombre': 'El claro del leñador', 'cofre': 40, 'misiones': [
             jefe('Jefe: El Leñador de Humo',
                  'El Leñador de Humo quiere talar todo el bosque. Demuestra lo que sabes de los árboles y de tus '
                  'herramientas digitales para detenerlo.', [
                      ('Un árbol grande da sombra y…', 'Ayuda a refrescar el ambiente', ['Calienta la ciudad', 'Contamina el aire', 'Seca el suelo']),
                      ('Los árboles toman del aire un gas llamado…', 'Dióxido de carbono', ['Helio', 'Vapor de chocolate', 'Gas de la risa']),
                      ('Un incendio forestal puede empezar por…', 'Una fogata mal apagada o vidrios tirados',
                       ['Regar las plantas', 'Plantar árboles', 'Reciclar']),
                      ('En una presentación, cada página se llama…', 'Diapositiva', ['Celda', 'Carpeta', 'Pestaña']),
                      ('Para que una diapositiva cambie a la siguiente con un efecto se usa una…', 'Transición',
                       ['Tabla', 'Fórmula', 'Contraseña']),
                      ('Para dibujar un póster en la computadora puedes usar…', 'Paint u otro programa de dibujo',
                       ['La calculadora', 'El reproductor de música', 'El reloj']),
                      ('Antes de usar una imagen de internet en tu presentación…', 'Reviso que se pueda usar y escribo de dónde la tomé',
                       ['La copio sin decir de dónde es', 'Le quito el nombre del autor', 'Uso fotos de personas sin permiso']),
                      ('¿Qué necesita un arbolito para crecer?', 'Agua, luz del sol, buen suelo y cuidados',
                       ['Solo oscuridad', 'Pintura verde', 'Música fuerte']),
                  ]),
         ]},
     ]},

    # ---------- ES-SEA208 · Helecho bien hecho ----------
    {'nombre': 'Isla del Helecho', 'tema': 'volcan',
     'descripcion': 'ES-SEA208 · Helecho bien hecho. En esta isla volcánica crecen plantas tan antiguas como los '
                    'dinosaurios. Aprende cómo se reproducen sin semillas y organiza tus datos en una hoja de cálculo.',
     'niveles': [
         {'nombre': 'Plantas sin semilla', 'cofre': 25, 'misiones': [
             mision('¿Cómo nace un helecho?', 'cuestionario', 'Los helechos no tienen flores ni semillas… entonces, ¿cómo nacen?',
                    xp=60, preguntas=[
                        ('Los helechos se reproducen por medio de…', 'Esporas', ['Semillas', 'Huevos', 'Flores']),
                        ('¿Dónde están las esporas de un helecho?', 'En puntitos cafés debajo de sus hojas',
                         ['En sus flores', 'En sus frutos', 'En la maceta']),
                        ('Los helechos viven mejor en lugares…', 'Húmedos y con sombra',
                         ['Muy secos, como el desierto', 'Dentro del congelador', 'Sin agua nunca']),
                        ('¿Cuál de estas plantas NO tiene flores ni semillas?', 'El musgo', ['El girasol', 'El frijol', 'El maíz']),
                        ('Las hojas nuevas de los helechos salen enrolladas como…', 'Un caracol o una espiral',
                         ['Un cubo', 'Un triángulo', 'Una estrella']),
                        ('Los helechos son plantas muy antiguas: ya existían…', 'En la época de los dinosaurios',
                         ['Apenas desde el año pasado', 'Desde que hay computadoras', 'Nunca existieron']),
                    ]),
             mision('¿Con semilla o con esporas?', 'juego', 'Algunas plantas nacen de semillas y otras de esporas. ¡Clasifícalas!',
                    juego='clasifica_semillas'),
             mision('Cazador de esporas', 'evidencia',
                    'Observa con una lupa la parte de abajo de la hoja de un helecho. ¿Ves unos puntitos cafés? '
                    '¡Ahí guarda sus esporas!\n\nDibuja o toma una foto de lo que observaste y súbela.', xp=80, monedas=20),
         ]},
         {'nombre': 'Datos en celdas', 'cofre': 30, 'misiones': [
             mision('Teclado misterioso: fila de arriba', 'juego',
                    'Ya dominas la fila guía. Ahora encuentra las teclas Q W E R T Y U I O P sin mirar.', juego='teclado_superior'),
             mision('Lluvia de meteoros: Word y Excel', 'juego',
                    'Escribe las palabras de las herramientas de oficina antes de que caigan.', juego='meteoros_office'),
             mision('Mi primera hoja de cálculo: plantas', 'evidencia',
                    'Abre Excel (o Google Sheets) y haz una tabla:\n\n'
                    '• A1: Planta · B1: ¿Semilla o espora? · C1: ¿Tiene flor? · D1: ¿Dónde vive?\n'
                    '• Llena 6 plantas (incluye un helecho y un musgo).\n'
                    '• Pon los títulos en negrita y colorea la fila 1.\n\nSube una captura de pantalla.', xp=90, monedas=25),
         ]},
         {'nombre': 'El cráter del jefe', 'cofre': 40, 'misiones': [
             jefe('Jefe: El Helecho Gigante Prehistórico',
                  'Un helecho gigante, viejo como los dinosaurios, despertó en el cráter. Véncelo con lo que sabes de '
                  'esporas, semillas y hojas de cálculo.', [
                      ('Un pino tiene semillas pero no flores. Sus semillas están en…', 'Sus piñas (conos)',
                       ['Esporas', 'Frutos de colores', 'Sus raíces']),
                      ('¿Qué tienen en común un helecho y un musgo?', 'Se reproducen por esporas',
                       ['Tienen flores', 'Dan frutos', 'Tienen semillas']),
                      ('Clasificar significa…', 'Agrupar cosas según sus características', ['Desordenarlas', 'Borrarlas', 'Dibujarlas']),
                      ('En una hoja de cálculo, cada casilla donde escribes se llama…', 'Celda', ['Diapositiva', 'Carpeta', 'Página']),
                      ('En una hoja de cálculo, las filas se nombran con…', 'Números', ['Letras', 'Colores', 'Emojis']),
                      ('En una hoja de cálculo, las columnas se nombran con…', 'Letras', ['Números', 'Colores', 'Formas']),
                      ('La celda B3 está en…', 'La columna B y la fila 3', ['La fila B y la columna 3', 'La hoja 3', 'La página B']),
                      ('¿Con qué letras empieza la fila de arriba del teclado?', 'Q W E R T Y', ['A S D F G', 'Z X C V B', '1 2 3 4 5']),
                  ]),
         ]},
     ]},

    # ---------- ES-SEA208 · Foto familiar ----------
    {'nombre': 'Bahía Foto Familiar', 'tema': 'oceano',
     'descripcion': 'ES-SEA208 · Foto familiar. ¿Por qué te pareces a tu familia? Descubre qué heredamos y qué aprendemos, '
                    'y conviértete en fotógrafo digital.',
     'niveles': [
         {'nombre': '¿A quién me parezco?', 'cofre': 25, 'misiones': [
             mision('¿Por qué me parezco a mi familia?', 'cuestionario', 'Ojos, cabello, sonrisa… ¿qué heredamos?', xp=60, preguntas=[
                 ('Las características que recibimos de nuestros papás se llaman…', 'Heredadas', ['Aprendidas', 'Compradas', 'Inventadas']),
                 ('¿Cuál es una característica heredada?', 'El color de tus ojos',
                  ['Saber andar en bici', 'Hablar inglés', 'Tu corte de cabello']),
                 ('¿Cuál es una característica aprendida?', 'Saber leer', ['El color de tu piel', 'La forma de tu nariz', 'Tu tipo de cabello']),
                 ('Los cachorros se parecen a sus papás porque…', 'Heredan sus características',
                  ['Los copian al verlos', 'Comen lo mismo', 'Viven en la misma casa']),
                 ('Las semillas de un girasol darán…', 'Girasoles', ['Rosas', 'Manzanos', 'Helechos']),
                 ('Antes de publicar una foto familiar en internet debes…', 'Pedir permiso a las personas que salen en ella',
                  ['Publicarla sin preguntar', 'Escribir tu dirección', 'Etiquetar a desconocidos']),
             ]),
             mision('¿Lo heredé o lo aprendí?', 'juego', '¿Viene de tu familia, lo aprendiste o te pasó por el ambiente?',
                    juego='clasifica_herencia'),
             mision('Mi árbol de características', 'texto',
                    'Elige a un familiar (o a una mascota y sus crías).\n\n'
                    '• Escribe 3 características en las que se parecen (heredadas).\n'
                    '• Escribe 2 cosas que cada uno aprendió.\n\n🤫 No escribas nombres completos ni direcciones.', xp=60),
         ]},
         {'nombre': 'Estudio de fotografía', 'cofre': 30, 'misiones': [
             mision('Explorador de rutas: el álbum perdido', 'juego',
                    'Las fotos de la familia se perdieron entre carpetas. Sigue la ruta para encontrarlas.', juego='rutas_fotos'),
             mision('Collage: las familias de los seres vivos', 'evidencia',
                    'Haz un collage digital (en PowerPoint, Word o Paint) con fotos de animales o plantas junto a sus crías: '
                    'gata y gatitos, tortuga y tortuguitas, girasol y semillas…\n\n'
                    '• Recorta las imágenes para que se vean bien.\n• Escribe una característica heredada en cada pareja.\n\n'
                    'Sube tu collage.', xp=100, monedas=30),
             mision('Atajos ninja: guarda, busca y da formato', 'juego',
                    'Guardar, imprimir, buscar, negrita, cursiva y subrayado con el teclado. ¡Un fotógrafo digital no pierde su trabajo!',
                    juego='atajos_archivo'),
         ]},
         {'nombre': 'El faro del jefe', 'cofre': 40, 'misiones': [
             mision('La foto del recuerdo (con permiso)', 'presencial',
                    'En equipos, tomen una foto grupal con la cámara o la tableta del salón. Antes, pregunten a todos si están '
                    'de acuerdo. Después pásenla a la computadora, guárdenla en la carpeta del grupo con un nombre claro y '
                    'aplíquenle un recorte o un filtro.', xp=60, monedas=20),
             jefe('Jefe: El Monstruo del Álbum Perdido',
                  'El Monstruo del Álbum Perdido revolvió todas las fotos familiares. Ordénalas con lo que sabes de '
                  'herencia y de archivos digitales.', [
                      ('Las tortugas marinas nacen de huevos y al crecer…', 'Se parecen a sus papás',
                       ['Se convierten en peces', 'Se vuelven pájaros', 'Nunca crecen']),
                      ('¿Qué es un ciclo de vida?', 'Las etapas de un ser vivo: nace, crece, se reproduce y muere',
                       ['Una bicicleta', 'Un programa de computadora', 'Un juego de mesa']),
                      ('Una cicatriz en la rodilla…', 'No se hereda: aparece por un accidente',
                       ['Se hereda de los abuelos', 'Viene en las semillas', 'Se aprende en la escuela']),
                      ('Para quitarle las orillas que sobran a una foto usas la herramienta…', 'Recortar',
                       ['Imprimir', 'Guardar como', 'Borrar todo']),
                      ('¿Cuál es la mejor forma de organizar tus fotos?', 'En carpetas con nombres claros',
                       ['Todas sueltas en el escritorio', 'Con nombres como «asdf»', 'Borrándolas']),
                      ('La ruta Documentos › Fotos › Familia indica…', 'En qué carpeta está guardado un archivo',
                       ['Un camino en el bosque', 'Una contraseña', 'Un video']),
                      ('¿Por qué es importante guardar tu trabajo seguido?', 'Para no perderlo si se apaga la computadora',
                       ['Para que se borre', 'Para que se vea más bonito', 'No es importante']),
                      ('Un collage es…', 'Una imagen hecha con varias fotos juntas', ['Un virus', 'Un cable', 'Una tecla']),
                  ]),
         ]},
     ]},

    # ---------- Gran final: programación ----------
    {'nombre': 'Galaxia del Código', 'tema': 'espacio',
     'descripcion': 'El gran final: algoritmos, ciclos y errores (¡bugs!). Programa robots y crea tu propio proyecto en '
                    'Scratch con todo lo que aprendiste en el año.',
     'niveles': [
         {'nombre': 'Algoritmos', 'cofre': 30, 'misiones': [
             mision('Algoritmos en todas partes', 'cuestionario', 'Un algoritmo es una receta de pasos. ¿Los sabes ordenar?',
                    xp=60, preguntas=[
                        ('Un algoritmo es…', 'Una serie de pasos ordenados para resolver algo', ['Un tipo de robot', 'Un virus', 'Una tecla']),
                        ('¿Cuál es el orden correcto para lavarte los dientes?', 'Poner pasta → cepillar → enjuagar',
                         ['Enjuagar → guardar el cepillo → poner pasta', 'Cepillar → poner pasta → comprar el cepillo', 'Guardar el cepillo → cepillar → poner pasta']),
                        ('Un ciclo (bucle) sirve para…', 'Repetir instrucciones varias veces',
                         ['Borrar el programa', 'Apagar la compu', 'Cambiar el color del teclado']),
                        ('En programación, un «bug» es…', 'Un error en el programa', ['Un insecto dentro de la compu', 'Un premio', 'Un juego']),
                        ('Encontrar y arreglar los errores de un programa se llama…', 'Depurar', ['Imprimir', 'Descargar', 'Dibujar']),
                        ('En Scratch, los programas se arman con…', 'Bloques de colores que se encajan', ['Plastilina', 'Cables', 'Pinturas']),
                    ]),
             mision('Robot humano', 'presencial',
                    'En parejas: uno es el robot y el otro el programador. El programador da instrucciones exactas '
                    '(avanza 2 pasos, gira a la derecha…) para que el robot llegue a un objeto del salón. '
                    'Si el robot se equivoca, ¡busquen el bug y corríjanlo!'),
             mision('Robot programador: usa ciclos', 'juego',
                    'Ahora los caminos son más largos. Usa el bloque de repetir para programar menos y llegar más lejos.',
                    xp=70, monedas=20, juego='robot_bucles'),
         ]},
         {'nombre': 'Código secreto', 'cofre': 30, 'misiones': [
             mision('Mensaje secreto: binario del programador', 'juego',
                    'Las computadoras guardan todo con ceros y unos. Descifra las palabras de programación escritas en binario.',
                    xp=60, juego='mensaje_binario'),
             mision('Lluvia de meteoros: programación', 'juego', 'Escribe las palabras de programación antes de que caigan.',
                    juego='meteoros_codigo'),
             mision('La Hora del Código', 'link',
                    'Entra a code.org y completa una actividad de la Hora del Código. Cuando termines, cuéntale a tu profe en '
                    'el comentario qué fue lo más difícil y cómo lo resolviste.', xp=70, monedas=20, link='https://code.org/'),
         ]},
         {'nombre': 'Proyecto final', 'cofre': 50, 'misiones': [
             mision('Scratch: tu primer personaje', 'link',
                    'Entra a Scratch, elige un personaje y prográmalo para que se mueva y diga algo cuando hagas clic en la '
                    'bandera verde. Sube una captura de tu programa.', xp=70, monedas=20, link='https://scratch.mit.edu/'),
             mision('Proyecto final: animación científica en Scratch', 'evidencia',
                    'Crea en Scratch una animación sobre tu tema favorito del año: la materia misteriosa, los gigantes de la '
                    'Tierra, el secreto plantástico, los árboles, los helechos o la foto familiar.\n\n'
                    '• Al menos 2 personajes que hablen.\n• Un fondo relacionado con el tema.\n• Un ciclo (repetir) en algún lugar.\n\n'
                    'Sube una captura de tu proyecto.', xp=120, monedas=35),
             jefe('Jefe final: El Glitch Supremo',
                  '¡El Glitch Supremo quiere borrar todo lo que aprendiste este año! Demuestra que dominas la ciencia y la '
                  'tecnología para vencerlo de una vez por todas.', [
                      ('Cuando el chocolate se derrite con el calor ocurre una…', 'Fusión', ['Condensación', 'Evaporación', 'Solidificación']),
                      ('El animal más grande que se conoce es…', 'La ballena azul', ['El tiranosaurio rex', 'El elefante', 'El megalodón']),
                      ('Las plantas fabrican su alimento gracias a la…', 'Fotosíntesis', ['Digestión', 'Respiración', 'Germinación']),
                      ('Una hipótesis es…', 'Una posible respuesta que vas a comprobar', ['Un dato seguro', 'Una opinión', 'Un chisme']),
                      ('Los árboles nos dan…', 'Oxígeno, sombra y hogar para muchos animales', ['Humo', 'Plástico', 'Basura']),
                      ('Los helechos se reproducen por…', 'Esporas', ['Semillas', 'Huevos', 'Frutos']),
                      ('El color de tus ojos es una característica…', 'Heredada', ['Aprendida', 'Comprada', 'Por accidente']),
                      ('¿Cuál es un dispositivo de entrada?', 'El teclado', ['El monitor', 'Las bocinas', 'La impresora']),
                      ('Un ciclo en programación sirve para…', 'Repetir instrucciones', ['Borrar todo', 'Apagar la compu', 'Pintar la pantalla']),
                      ('Cuando tu programa falla, lo mejor es…', 'Buscar el error paso a paso y volver a intentarlo',
                       ['Rendirte', 'Culpar a la compu', 'Borrar todo el proyecto']),
                  ], xp=200, monedas=80),
         ]},
     ]},
]

CURSO = {
    'nombre': 'TIC 4° · Pinion Learn 6.1',
    'juegos': JUEGOS,
    'mundos': MUNDOS,
}
