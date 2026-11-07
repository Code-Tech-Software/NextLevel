"""Mundo 4 · ES-DAT301 Prepara y escapa: el tsunami de Bahía Lituya, los fenómenos naturales de México, el plan de
emergencia y un escape room en Scratch con preguntas que abren puertas, vidas y un cargador solar con disfraces."""
from .base import KIDDLE, LEYENDA_SCRATCH, PAREJAS, clasifica, jefe, leccion, mision, scratch

JUEGOS = {
    'clasifica_fenomenos': clasifica('¿Geológico o hidrometeorológico?', '🌋', 'Protección Civil agrupa los '
                                     'fenómenos naturales según su origen: los que vienen de la Tierra y los que vienen '
                                     'del agua y el clima.', [
        ('Geológico (la Tierra)', '🪨', ['Sismo', 'Tsunami', 'Erupción de un volcán', 'Deslizamiento de un cerro',
                                         'Hundimiento del suelo', 'Caída de ceniza volcánica']),
        ('Hidrometeorológico (clima)', '🌀', ['Huracán', 'Inundación', 'Tornado', 'Granizada', 'Ola de calor',
                                              'Sequía']),
    ], rondas=12),
    'clasifica_antes_durante': clasifica('Antes, durante y después', '🚨', 'Lo que haces en un sismo depende del '
                                         'momento. ¿Cuándo se hace cada acción?', [
        ('Antes del sismo', '🎒', ['Preparar la mochila de emergencia', 'Ubicar las zonas de menor riesgo',
                                   'Participar en los simulacros', 'Acordar un punto de reunión con tu familia']),
        ('Durante el sismo', '⚠️', ['No corro, no grito, no empujo', 'Alejarte de ventanas y cosas que puedan caer',
                                    'Si no puedes salir: agáchate, cúbrete y sujétate',
                                    'Seguir la ruta de evacuación sin regresar por tus cosas']),
        ('Después del sismo', '🩹', ['Revisar si hay heridos y avisar a un adulto',
                                     'No usar elevadores ni encender cerillos', 'Informarte solo con fuentes oficiales',
                                     'Mandar mensajes de texto en vez de llamar']),
    ], rondas=12),
}

CODIGO_CARGADOR = '''
OBJETO: Cargador (con 4 disfraces: «carga 0», «carga 1», «carga 2» y «carga 3»)
al presionar bandera verde
    cambiar disfraz a "carga 0"
al hacer clic en este objeto
    siguiente disfraz
'''

CODIGO_CUARTO1 = '''
ESCENARIO
al presionar bandera verde
    cambiar fondo a "cuarto 1"
    fijar "vidas" a 3
    esperar hasta que <(vidas) = 0>
    cambiar fondo a "atrapado"
    detener "todos"

OBJETO: Guía
al presionar bandera verde
    decir "¡Alerta sísmica! Responde bien para salir del búnker." durante 3 segundos
    preguntar "Empieza a temblar. ¿Qué haces? A) Corro a las escaleras B) Uso el elevador C) Voy a la zona de menor riesgo" y esperar
    repetir hasta que <(respuesta) = "C">
        cambiar "vidas" en -1
        preguntar "¡Peligro! Pierdes una vida. Elige otra vez: A, B o C" y esperar
    decir "¡Correcto! La puerta se abrió." durante 2 segundos
    cambiar fondo a "cuarto 2"
'''

CODIGO_CUARTO2 = '''
OBJETO: Cargador (agrega estos programas; borra el de prueba)
al presionar bandera verde
    esconder
    fijar "carga" a 0
    cambiar disfraz a "carga 0"
cuando el fondo cambie a "cuarto 2"
    mostrar
    decir "Sin luz no hay radio. ¡Cárgame con el sol! (haz clic)" durante 3 segundos
al hacer clic en este objeto
    si <(carga) < 3> entonces
        cambiar "carga" en 1
        siguiente disfraz
        iniciar sonido (el que tú elijas)
        si <(carga) = 3> entonces
            decir "¡Batería llena!" durante 2 segundos
            enviar "radio encendida"
cuando el fondo cambie a "cuarto 3"
    esconder

OBJETO: Radio
al presionar bandera verde
    esconder
al recibir "radio encendida"
    mostrar
    decir "Protección Civil: viene un tsunami. Suban a una zona alta por la ruta de evacuación." durante 4 segundos
    cambiar fondo a "cuarto 3"
'''

CODIGO_CUARTO3 = '''
OBJETO: Guía (agrega este programa)
cuando el fondo cambie a "cuarto 3"
    preguntar "Llegó la alerta de tsunami. ¿A dónde vas? A) A la playa a ver la ola B) A una zona alta lejos de la costa C) Al sótano" y esperar
    repetir hasta que <(respuesta) = "B">
        cambiar "vidas" en -1
        preguntar "¡Peligro! Pierdes una vida. Elige otra vez: A, B o C" y esperar
    cambiar fondo a "salida"
    decir "¡Escapaste! Estás a salvo." durante 3 segundos
    detener "todos"
'''

MUNDO = {
    'nombre': 'Búnker Alerta', 'tema': 'volcan',
    'descripcion': 'ES-DAT301 · Prepara y escapa. En 1958, en Bahía Lituya, Alaska, un terremoto provocó una avalancha '
                   'que, al caer al mar, levantó el tsunami más grande registrado en la historia. Conoce los fenómenos '
                   'naturales que pueden afectar tu región, arma tu plan de emergencia y programa en Scratch un escape '
                   'room donde solo sale quien sabe qué hacer. Pregunta guía: ¿cómo prepararías a tu comunidad ante un '
                   'fenómeno natural?',
    'niveles': [
        {'nombre': 'Alerta en Bahía Lituya', 'cofre': 25, 'misiones': [
            mision('La ola más grande de la historia', 'texto', leccion(
                intro='El 9 de julio de 1958, en Bahía Lituya, al sur de Alaska, un terremoto de magnitud 8 desprendió un '
                      'pedazo enorme de montaña que cayó al mar. La ola subió por la ladera de enfrente hasta 524 metros '
                      'de altura: más que cualquier edificio de México. Solo murieron cinco personas, porque la zona '
                      'casi no estaba habitada. Desde entonces se estudian y vigilan mucho más los tsunamis.',
                pasos=['¿Has vivido un sismo, un huracán, una inundación u otro fenómeno natural? ¿Qué pasó?',
                       '¿Qué sabes que hay que hacer durante un sismo?',
                       '¿Por qué crees que en Bahía Lituya hubo tan pocas víctimas?'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('Fenómenos naturales', 'cuestionario', leccion(
                intro='No se pueden evitar, pero sí se puede estar preparado. Primero hay que conocerlos.',
                saber=['Fenómenos geológicos: vienen del interior de la Tierra. Sismos, tsunamis, volcanes, '
                       'deslizamientos de cerros y hundimientos.',
                       'Fenómenos hidrometeorológicos: vienen del agua y el clima. Huracanes, inundaciones, tornados, '
                       'granizadas, olas de calor y sequías.',
                       'México está en el Cinturón de Fuego del Pacífico, por eso tiembla seguido y tiene volcanes '
                       'activos como el Popocatépetl.',
                       'La temporada de huracanes va de mayo-junio a noviembre.',
                       'Alerta sísmica (SASMEX): suena unos segundos antes de que llegue el temblor a algunas ciudades.',
                       'Tsunami: si el mar se retira de repente de la playa, hay que subir a una zona alta de '
                       'inmediato.']), xp=60, preguntas=[
                ('Un sismo es un fenómeno…', 'Geológico', ['Hidrometeorológico', 'Químico', 'Espacial']),
                ('Un huracán es un fenómeno…', 'Hidrometeorológico', ['Geológico', 'Volcánico', 'Sísmico']),
                ('¿Por qué tiembla seguido en México?', 'Porque está en el Cinturón de Fuego del Pacífico',
                 ['Porque hace mucho calor', 'Porque tiene muchas ciudades', 'Porque hay muchos ríos']),
                ('¿Para qué sirve la alerta sísmica?', 'Para avisar unos segundos antes de que llegue el temblor',
                 ['Para detener el sismo', 'Para medir la lluvia', 'Para avisar que viene un huracán']),
                ('Estás en la playa y el mar se retira de repente. ¿Qué haces?', 'Subo de inmediato a una zona alta',
                 ['Me acerco a ver', 'Tomo fotos', 'Me meto al mar']),
                ('¿Cuál es un volcán activo de México?', 'El Popocatépetl', ['El Everest', 'El Kilimanjaro',
                                                                         'El Monte Fuji']),
            ]),
            mision('¿Geológico o hidrometeorológico?', 'juego', leccion(
                intro='Clasifica cada fenómeno según su origen.',
                tip='Si viene de debajo de la tierra es geológico; si viene del cielo o del agua, '
                    'hidrometeorológico.'), juego='clasifica_fenomenos'),
        ]},
        {'nombre': 'Mi región, mi plan', 'cofre': 30, 'misiones': [
            mision('Investiga tu región', 'texto', leccion(
                intro='Cada lugar tiene sus propios riesgos: no es lo mismo vivir en la costa que junto a un volcán. '
                      'Investiga los de tu región.',
                saber=['Fuentes confiables: Protección Civil de tu estado o municipio, el Servicio Sismológico Nacional, '
                       'Kiddle (el buscador para niños) y lo que saben los adultos de tu familia.',
                       'Siempre anota de dónde sacaste cada dato.'],
                dinamica=['10 minutos de búsqueda en tu computadora, semáforo en 🟡.',
                          'Si encuentras algo que te asuste o no entiendas, lo comentas con el profe.'],
                pasos=['Escribe el nombre de tu municipio y tu estado.',
                       'Busca 3 fenómenos naturales que hayan afectado tu región y cuándo pasó alguno.',
                       'Escribe 2 medidas que se toman en tu escuela o comunidad (simulacros, alarmas, rutas de '
                       'evacuación…).',
                       'Anota tus fuentes.'],
                logro=['Tienes 3 fenómenos de tu región, 2 medidas y tus fuentes.'],
                entrega='escribe tu investigación aquí abajo.'), xp=70, monedas=20, link=KIDDLE),
            mision('Antes, durante y después', 'juego', leccion(
                intro='Un buen plan dice qué hacer en cada momento del sismo.',
                tip='Lo de antes es prepararse; lo de durante es protegerse; lo de después es ayudar e informarse '
                    'bien.'), juego='clasifica_antes_durante'),
            mision('Plan de emergencia', 'cuestionario', leccion(
                intro='Las familias y las escuelas preparadas reaccionan mejor. Repasa lo esencial.',
                saber=['Mochila de emergencia: agua, comida que no se eche a perder, linterna, radio y pilas (o cargador '
                       'solar), botiquín, silbato, copias de documentos, ropa y medicinas.',
                       'Durante un sismo: «No corro, no grito, no empujo». Ve a la zona de menor riesgo o sigue la ruta '
                       'de evacuación.',
                       'Punto de reunión: un lugar acordado con tu familia por si se separan.',
                       'Número de emergencias en México: 911.',
                       'Después: no uses elevadores, no enciendas cerillos (puede haber fuga de gas) y créele solo a la '
                       'información oficial.']), xp=60, preguntas=[
                ('¿Qué va en una mochila de emergencia?', 'Agua, linterna, radio, botiquín y silbato',
                 ['Videojuegos y dulces', 'Solo ropa', 'Nada, no hace falta']),
                ('¿Cuál es la regla durante un sismo?', 'No corro, no grito, no empujo',
                 ['Corro a las escaleras', 'Grito para avisar', 'Empujo para salir primero']),
                ('¿Para qué sirve un punto de reunión?', 'Para encontrarse con tu familia si se separan',
                 ['Para jugar después del sismo', 'Para guardar la mochila', 'Para ver los daños']),
                ('¿Cuál es el número de emergencias en México?', '911', ['123', '000', '555']),
                ('¿Por qué no se encienden cerillos después de un sismo?', 'Porque puede haber una fuga de gas',
                 ['Porque gastan oxígeno', 'Porque hacen ruido', 'Porque están prohibidos siempre']),
                ('¿A quién le crees después de un desastre?', 'A la información oficial de Protección Civil',
                 ['A cualquier mensaje reenviado', 'A los rumores', 'A un video sin fuente']),
            ]),
            mision('Simulacro del laboratorio', 'presencial', leccion(
                intro='Un plan que no se practica no sirve. Hoy el grupo practica cómo se sale del laboratorio de '
                      'cómputo.',
                roles=['Brigadista de puerta: abre la puerta y la mantiene abierta.',
                       'Brigadista de conteo: cuenta a sus compañeros en el punto de reunión.',
                       'Brigadista de equipo: revisa que nadie se quede en el salón.',
                       'Todos los demás: siguen la ruta en fila, sin correr, sin gritar y sin empujar.'],
                dinamica=['El profe explica la ruta y la zona de menor riesgo con el semáforo en 🔴.',
                          'Primera vuelta: caminando despacio. Segunda vuelta: cronometrada.',
                          'Las computadoras se quedan como están: nadie regresa por sus cosas.'],
                pasos=['Ubiquen la ruta de evacuación y la zona de menor riesgo del laboratorio.',
                       'A la señal del profe, salgan en fila hasta el punto de reunión.',
                       'Los brigadistas cuentan y reportan.',
                       'De regreso, comenten: ¿qué tardó más? ¿Qué mejorarían?'],
                logro=['El grupo llega al punto de reunión en orden y en menos tiempo en la segunda vuelta.']), xp=50),
        ]},
        {'nombre': 'Diseña el escape room', 'cofre': 30, 'misiones': [
            mision('Mapa del búnker', 'evidencia', leccion(
                intro='Un escape room es un juego en el que estás encerrado y solo sales resolviendo retos. El tuyo '
                      'tendrá 3 cuartos y en cada uno hay que demostrar que sabes qué hacer ante un fenómeno natural.',
                saber=['Cuarto 1: una pregunta de opción múltiple (A, B o C) sobre qué hacer durante un sismo.',
                       'Cuarto 2: el cargador solar. Hay que cargarlo para encender la radio y escuchar la alerta.',
                       'Cuarto 3: la pregunta final sobre el tsunami. Si aciertas, llegas a la salida.',
                       'El jugador empieza con 3 vidas. Cada respuesta incorrecta resta una; con 0 vidas aparece el '
                       'fondo «atrapado».'],
                material=['Una hoja dividida en 5 recuadros', 'Lápiz y colores'],
                pasos=['Dibuja los 5 fondos: cuarto 1, cuarto 2, cuarto 3, salida y atrapado.',
                       'En los cuartos 1 y 3 escribe tu pregunta con sus 3 opciones y marca la correcta.',
                       'Dibuja con flechas qué pasa si aciertas y qué pasa si te equivocas.',
                       'Revisa con tu dupla: ¿las preguntas tienen una sola respuesta correcta y segura?'],
                logro=['Tu mapa tiene los 5 fondos, 2 preguntas con su respuesta correcta y las flechas de qué pasa.'],
                entrega='sube una foto de tu mapa.'), xp=80, monedas=25),
            mision('Diseña el cargador solar', 'evidencia', leccion(
                intro='En una emergencia puede faltar la luz. Un cargador solar convierte la luz del Sol en electricidad '
                      'para cargar una radio o una linterna. En tu juego será el objeto clave del cuarto 2.',
                saber=['Un objeto de Scratch puede tener varios disfraces: dibujos distintos del mismo objeto.',
                       'Tu cargador tendrá 4 disfraces: «carga 0» (batería vacía), «carga 1», «carga 2» y «carga 3» '
                       '(batería llena).',
                       'Interacción: cada clic del jugador es un rato de sol que suma una rayita de carga.'],
                material=['Una hoja', 'Lápiz y colores'],
                pasos=['Dibuja tu cargador solar: un panel con sus celdas y una batería con 3 rayitas.',
                       'Dibuja los 4 disfraces, uno al lado del otro, con 0, 1, 2 y 3 rayitas llenas.',
                       'Escribe qué pasa con cada clic y qué pasa cuando la batería está llena.'],
                logro=['Tu diseño tiene 4 disfraces distintos y explica qué pasa con cada clic.'],
                entrega='sube una foto de tu diseño.'), xp=70, monedas=20),
        ]},
        {'nombre': 'Programa el búnker', 'cofre': 35, 'misiones': [
            scratch('Dibuja el cargador solar', leccion(
                intro='Pasa tu diseño a Scratch con el editor de dibujo. Es el objeto que vas a programar en el cuarto 2.',
                saber=['Pintar: botón del pincel en «Elegir un objeto». Herramientas: Rectángulo, Círculo, Línea, '
                       'Relleno y Texto.',
                       'Pestaña Disfraces: clic derecho en un disfraz → duplicar. Así copias el dibujo y solo cambias la '
                       'batería.',
                       'Cambia el nombre de cada disfraz arriba del dibujo: «carga 0», «carga 1», «carga 2», '
                       '«carga 3».',
                       LEYENDA_SCRATCH],
                dinamica=PAREJAS,
                pasos=['Proyecto nuevo: Bunker_TuNombre. Borra al gato.',
                       'Pinta el cargador con su panel y su batería vacía. Llama al objeto Cargador y al disfraz '
                       '«carga 0».',
                       'Duplica el disfraz 3 veces y en cada copia llena una rayita más de la batería.',
                       'Arma el código de prueba: cada clic cambia al siguiente disfraz.',
                       'Guarda tu proyecto en tu carpeta Alerta.'],
                logro=['Tu cargador tiene 4 disfraces con nombre y cambia con cada clic.'],
                entrega='sube una captura de la pestaña Disfraces con los 4 disfraces.'), CODIGO_CARGADOR,
                xp=90, monedas=25),
            scratch('Cuarto 1: la pregunta que abre la puerta', leccion(
                intro='Programa el primer cuarto: un Guía hace la pregunta del sismo y solo con la respuesta correcta se '
                      'abre la puerta. Cada error cuesta una vida.',
                saber=['«preguntar … y esperar» (Sensores) muestra un cuadro para escribir. Lo que escribe el jugador '
                       'queda en «respuesta».',
                       'Las respuestas son letras (A, B o C) para que no fallen por la ortografía. A Scratch no le '
                       'importan las mayúsculas: «c» y «C» valen igual.',
                       '«repetir hasta que <(respuesta) = C>» vuelve a preguntar mientras la respuesta sea incorrecta.',
                       '«esperar hasta que <(vidas) = 0>» vigila las vidas todo el juego.',
                       LEYENDA_SCRATCH],
                dinamica=PAREJAS,
                pasos=['En el escenario, pestaña Fondos: pinta o elige 5 fondos y ponles nombre: «cuarto 1», «cuarto 2», '
                       '«cuarto 3», «salida» y «atrapado» (con la herramienta Texto escribe ¡A SALVO! y ATRAPADO).',
                       'Agrega un personaje como Guía.',
                       'Crea la variable «vidas» y arma el código del escenario y del Guía. Usa tu propia pregunta.',
                       'Prueba equivocándote a propósito: ¿baja una vida? Con 3 errores, ¿aparece «atrapado»?',
                       'Guarda.'],
                logro=['Con la respuesta correcta se pasa al cuarto 2; con 3 errores aparece el fondo «atrapado».'],
                entrega='sube una captura del código del Guía y del juego preguntando.'), CODIGO_CUARTO1,
                xp=110, monedas=30),
            scratch('Cuarto 2: energía solar', leccion(
                intro='El cuarto 2 está a oscuras: hay que cargar el cargador solar con 3 clics para encender la radio y '
                      'escuchar el aviso de Protección Civil.',
                saber=['«cuando el fondo cambie a cuarto 2» (Eventos) hace que el cargador aparezca solo en su cuarto.',
                       'Un objeto escondido no se puede tocar: por eso el cargador empieza escondido.',
                       'Un «si» dentro de otro «si»: primero revisa que la batería no esté llena y, después de sumar, '
                       'revisa si ya se llenó.',
                       LEYENDA_SCRATCH],
                dinamica=PAREJAS,
                pasos=['Borra el código de prueba del Cargador.',
                       'Crea la variable «carga» y el mensaje «radio encendida».',
                       'Arma los 4 programas del Cargador.',
                       'Pinta o elige un objeto Radio y arma su código.',
                       'Prueba desde la bandera verde: ¿el cargador aparece en el cuarto 2? ¿Con 3 clics se llena y la '
                       'radio habla?'],
                logro=['El cargador solo aparece en el cuarto 2, se llena con 3 clics y la radio lleva al cuarto 3.'],
                tip='Si el cargador no aparece, revisa que el nombre del fondo sea exactamente «cuarto 2».',
                entrega='sube una captura del código del Cargador.'), CODIGO_CUARTO2, xp=110, monedas=30),
            scratch('Cuarto 3: la gran salida', leccion(
                intro='El último reto: la pregunta del tsunami. Si aciertas, escapas del búnker.',
                saber=['El programa empieza con «cuando el fondo cambie a cuarto 3»: un evento distinto a la bandera '
                       'verde.',
                       '«detener todos» termina el juego cuando el jugador escapa.',
                       LEYENDA_SCRATCH],
                dinamica=PAREJAS,
                pasos=['Agrega al Guía el programa del cuarto 3, con tu propia pregunta.',
                       'Juega el escape room completo, de la bandera verde a la salida.',
                       'Juega otra vez perdiendo a propósito: ¿llegas a «atrapado»?',
                       'Reto: agrega sonidos al acertar y al perder una vida, o un cuarto 4.',
                       'Guarda tu proyecto.'],
                logro=['Se puede jugar de principio a fin: se gana en la salida y se pierde con 0 vidas.'],
                entrega='sube una captura de la pantalla de salida y otra del código del cuarto 3.'), CODIGO_CUARTO3,
                xp=100, monedas=30),
            mision('Pruebas de funcionamiento', 'texto', leccion(
                intro='Los programadores profesionales prueban su juego con una lista. Haz la tuya.',
                pasos=['Prueba 1: respondo bien todo. ¿Llego a la salida? (Sí / No)',
                       'Prueba 2: me equivoco 3 veces en el cuarto 1. ¿Aparece «atrapado»?',
                       'Prueba 3: hago clic en el cargador 5 veces. ¿Se pasa de 3?',
                       'Prueba 4: escribo la respuesta en minúscula. ¿Funciona?',
                       'Escribe el resultado de cada prueba y, si algo falló, cómo lo arreglaste.'],
                logro=['Hiciste las 4 pruebas y corregiste lo que falló.'],
                entrega='escribe tus 4 resultados y tus arreglos aquí abajo.'), xp=60),
        ]},
        {'nombre': 'Torneo de escape', 'cofre': 40, 'misiones': [
            mision('Torneo de escape', 'presencial', leccion(
                intro='Hoy cada quien juega los búnkeres de sus compañeros. ¿Quién escapa más rápido… y quién diseñó el '
                      'búnker más difícil?',
                dinamica=['Rotación por filas: cada 5 minutos el profe da la señal y se cambian a la computadora de al '
                          'lado.',
                          'El autor no ayuda ni da pistas. Semáforo en 🟡.',
                          'Nadie modifica el proyecto de otro.'],
                pasos=['Juega al menos 3 búnkeres.',
                       'En cada uno deja una nota: ¿escapaste? ¿Cuántas vidas te quedaron? Una cosa que te gustó y una '
                       'mejora.',
                       'Vuelve a tu lugar y lee tus notas.',
                       'Votación: búnker más difícil, cargador mejor dibujado y preguntas más útiles.'],
                logro=['Jugaste 3 búnkeres y dejaste notas útiles y amables.']), xp=50),
            mision('Autoevaluación del búnker', 'texto', leccion(
                intro='Cierra el proyecto evaluándote con honestidad.',
                pasos=['Del 1 al 5, califica tu búnker en: funciona sin errores, preguntas útiles y dibujo del cargador. '
                       'Explica cada número.',
                       '¿Qué estructura de control usaste para volver a preguntar cuando la respuesta era incorrecta?',
                       '¿Qué aprendiste de los fenómenos naturales que le contarías a tu familia?',
                       '¿Qué mejorarías si tuvieras una clase más?'],
                entrega='escribe tu autoevaluación aquí abajo.'), xp=60),
            jefe('Jefe: El Megatsunami', leccion(
                intro='El Megatsunami amenaza la costa. Solo lo detiene quien sabe prevenir, reaccionar y programar un '
                      'búnker a prueba de errores.'), [
                ('¿Qué tipo de fenómeno es un tsunami?', 'Geológico', ['Hidrometeorológico', 'Espacial', 'Químico']),
                ('Durante un sismo, ¿cuál es la regla?', 'No corro, no grito, no empujo',
                 ['Corro a las escaleras', 'Uso el elevador', 'Regreso por mis cosas']),
                ('El mar se retira de repente de la playa. ¿Qué haces?', 'Subo a una zona alta de inmediato',
                 ['Me acerco a ver', 'Busco conchas', 'Tomo un video']),
                ('¿Qué bloque guarda lo que escribió el jugador?', 'respuesta', ['puntos', 'cronómetro', 'disfraz']),
                ('¿Qué bloque vuelve a preguntar mientras la respuesta sea incorrecta?', 'repetir hasta que <…>',
                 ['por siempre', 'esperar 1 segundos', 'siguiente disfraz']),
                ('El cargador tiene 4 disfraces. ¿Qué bloque pasa al que sigue?', 'siguiente disfraz',
                 ['cambiar fondo a', 'mostrar', 'enviar']),
                ('¿Por qué el cargador empieza escondido?', 'Para que solo aparezca y se pueda tocar en el cuarto 2',
                 ['Porque no tiene disfraces', 'Para que el juego sea más rápido', 'Por error']),
                ('¿Cuál es el número de emergencias en México?', '911', ['123', '070', '000']),
            ]),
        ]},
    ],
}
