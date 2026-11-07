"""Mundo 7 · ES-DAT304 Cerrando circuitos: el escapista Sombra Veloz, los elementos de un circuito, conductores y
aislantes, la micro:bit y MakeCode, un detector de conductores y un sensor de apertura de puertas con alarma y contador.

El sensor va en el pin P1: en la micro:bit V1 el sonido sale por P0 (con audífonos o bocina), así no chocan."""
from .base import DUPLA_MAKER, LEYENDA_MICROBIT, MICROBIT, clasifica, jefe, leccion, microbit, mision

JUEGOS = {
    'clasifica_conductores': clasifica('¿Conductor o aislante?', '⚡', 'Los conductores dejan pasar la electricidad y '
                                       'los aislantes no. ¿Qué es cada material?', [
        ('Conductor', '🔌', ['Papel aluminio', 'Un clip de metal', 'Una moneda', 'Un cable de cobre',
                             'La punta de grafito de un lápiz', 'Una llave de metal']),
        ('Aislante', '🧤', ['Una liga', 'Una regla de plástico', 'Una hoja de papel', 'Un palito de madera',
                            'Un borrador', 'Un vaso de vidrio']),
    ], rondas=12),
    'clasifica_entrada_salida': clasifica('¿Entrada o salida de la micro:bit?', '🎛️', 'Las entradas le dan '
                                          'información a la micro:bit y las salidas muestran o hacen algo. ¿Qué es '
                                          'cada parte?', [
        ('Entrada', '📥', ['Botón A', 'Botón B', 'El pin P1 cuando cierras el circuito', 'El sensor de luz',
                           'El acelerómetro (detecta si la agitas)', 'El micrófono (micro:bit V2)',
                           'El sensor de temperatura', 'El logotipo táctil (micro:bit V2)']),
        ('Salida', '📤', ['La pantalla de 25 LED', 'La bocina (micro:bit V2)', 'Un LED conectado a un pin',
                          'Unos audífonos conectados a P0 y GND']),
    ], rondas=12),
    'clasifica_abierto_cerrado': clasifica('¿Circuito abierto o cerrado?', '🚪', 'En un circuito cerrado la '
                                           'electricidad da la vuelta completa; en uno abierto está interrumpida.', [
        ('Circuito cerrado', '✅', ['El foco está encendido', 'La puerta cerrada junta las dos tiras de aluminio',
                                    'El interruptor está en encendido', 'Tocas P1 y GND al mismo tiempo',
                                    'Un clip une los dos caimanes', 'La alarma está en silencio y marca ✔']),
        ('Circuito abierto', '⛔', ['Un cable está suelto', 'La puerta se abrió y separó el aluminio',
                                    'El interruptor está apagado', 'Solo tocas P1, sin tocar GND',
                                    'Una liga queda entre los dos caimanes', 'El foco está fundido']),
    ], rondas=12),
}

CODIGO_HOLA = '''
al iniciar
    mostrar cadena "SOMBRA"
al presionarse el botón A
    mostrar ícono [corazón]
al presionarse el botón B
    mostrar número 5
al presionarse el botón A+B
    borrar la pantalla
'''

CODIGO_TOCA = '''
al presionarse pin [P1]
    mostrar ícono [palomita ✔]
    reproduce secuencia (tono [Do alto] durante [1 pulso]) en modo [hasta que termine]
al liberarse pin [P1]
    mostrar ícono [tache ✖]
'''

CODIGO_DETECTOR = '''
para siempre
    si (pin [P1] está presionado) entonces
        mostrar ícono [palomita ✔]
    si no
        mostrar ícono [tache ✖]
'''

CODIGO_ALARMA = '''
al iniciar
    fijar [aperturas] a 0
    mostrar ícono [palomita ✔]
al presionarse pin [P1]
    mostrar ícono [palomita ✔]
al liberarse pin [P1]
    cambiar [aperturas] por 1
    mostrar ícono [tache ✖]
    repetir 3 veces
        reproduce secuencia (tono [Do alto] durante [1 pulso]) en modo [hasta que termine]
        reproduce secuencia (tono [Do medio] durante [1 pulso]) en modo [hasta que termine]
al presionarse el botón B
    mostrar número (aperturas)
al presionarse el botón A+B
    fijar [aperturas] a 0
    mostrar número 0
'''

MUNDO = {
    'nombre': 'Operación Sombra Veloz', 'tema': 'cyber',
    'descripcion': 'ES-DAT304 · Cerrando circuitos. Sombra Veloz es un experto escapista contratado para poner a prueba '
                   'la cárcel local… y siempre logra salir sin que nadie se dé cuenta. Descubre qué es un circuito '
                   'abierto y uno cerrado, programa la micro:bit y construye un sensor que detecte cuando se abre una '
                   'puerta. Pregunta guía: ¿cómo detectar a Sombra Veloz en cuanto abra la puerta?',
    'niveles': [
        {'nombre': 'El caso Sombra Veloz', 'cofre': 25, 'misiones': [
            mision('El escapista imposible', 'texto', leccion(
                intro='Sombra Veloz es un experto escapista. Lo contrataron para poner a prueba la seguridad de la cárcel '
                      'local y en cada intento escapa sin problemas. Se niega a revelar cómo lo hace, y los que diseñan '
                      'sistemas de seguridad cada vez más avanzados no salen de su asombro.',
                pasos=['¿Cómo crees que logra escapar sin que nadie se dé cuenta?',
                       '¿Qué aparatos de seguridad conoces (en tiendas, casas, bancos)? Menciona 3.',
                       'Si tuvieras que avisar en el instante en que se abre una puerta, ¿qué inventarías?'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('Circuitos eléctricos', 'cuestionario', leccion(
                intro='Todo aparato de seguridad funciona con circuitos. Primero entiende cómo son.',
                saber=['Un circuito eléctrico es el camino por donde viaja la electricidad.',
                       'Sus elementos: fuente de energía (pila o batería), conductores (cables), un receptor que usa la '
                       'energía (foco, LED, motor, bocina) y un interruptor que abre o cierra el camino.',
                       'Circuito cerrado: el camino está completo y la electricidad circula. Circuito abierto: el camino '
                       'está cortado y no circula.',
                       'Conductores: materiales que dejan pasar la electricidad, como los metales (cobre, aluminio) y el '
                       'grafito. Aislantes: no la dejan pasar, como el plástico, la madera, el hule y el vidrio.',
                       'Seguridad: solo se experimenta con pilas o con la micro:bit. Nunca con los contactos de la '
                       'pared.']), xp=60, preguntas=[
                ('¿Qué es un circuito eléctrico?', 'El camino por donde viaja la electricidad',
                 ['Una pila', 'Un foco', 'Un enchufe de pared']),
                ('¿Qué elemento le da la energía al circuito?', 'La pila o batería', ['El interruptor', 'El foco',
                                                                                     'El cable']),
                ('¿Para qué sirve un interruptor?', 'Para abrir o cerrar el circuito',
                 ['Para guardar energía', 'Para hacer más brillante el foco', 'Para enfriar los cables']),
                ('En un circuito abierto…', 'La electricidad no circula', ['La electricidad circula',
                                                                           'El foco brilla más',
                                                                           'La pila se recarga']),
                ('¿Cuál es un buen conductor?', 'El papel aluminio', ['Una liga', 'Un palito de madera',
                                                                     'Una regla de plástico']),
                ('¿Con qué NUNCA se experimenta?', 'Con los contactos de la pared', ['Con pilas',
                                                                                   'Con la micro:bit',
                                                                                   'Con papel aluminio']),
            ]),
            mision('¿Conductor o aislante?', 'juego', leccion(
                intro='Clasifica cada material. Más adelante los vas a comprobar con la micro:bit.',
                tip='Casi todos los metales son conductores.'), juego='clasifica_conductores'),
            mision('Circuito humano', 'presencial', leccion(
                intro='Sin cables: el grupo será un circuito y la electricidad será un apretón de manos.',
                roles=['Pila: empieza el pulso apretando la mano de su compañero.',
                       'Foco: levanta la mano libre cuando le llega el pulso.',
                       'Interruptor: decide si se toma de las manos (cerrado) o se suelta (abierto).',
                       'Todos los demás: son los cables y pasan el apretón.'],
                dinamica=['En círculo, de pie y sin moverse de su lugar. Semáforo en 🔴: el pulso se pasa en silencio.',
                          'El profe nombra a la pila, al foco y al interruptor en cada ronda.'],
                pasos=['Ronda 1: circuito cerrado. La pila aprieta y el pulso da la vuelta hasta el foco. ¿Cuánto tarda?',
                       'Ronda 2: el interruptor se suelta. ¿El pulso llega al foco?',
                       'Ronda 3: el interruptor decide en secreto si cierra o abre; el grupo adivina por el foco.',
                       'Comenten: ¿cómo se parece esto a una puerta que se abre y corta el circuito?'],
                logro=['Explicas con tus palabras la diferencia entre circuito abierto y cerrado.']), xp=50),
        ]},
        {'nombre': 'Conoce la micro:bit', 'cofre': 30, 'misiones': [
            mision('Anatomía de la micro:bit', 'cuestionario', leccion(
                intro='La micro:bit es una pequeña computadora programable del tamaño de una galleta. Con ella vas a '
                      'construir la alarma.',
                saber=['Pantalla de 25 LED (5 × 5): muestra números, letras e íconos. También mide la luz.',
                       'Botones A y B: entradas que tú presionas.',
                       'Pines dorados (abajo): 0, 1, 2, 3V y GND. GND es «tierra», el regreso del circuito. Cuando unes '
                       'un pin con GND, cierras un circuito.',
                       'Sensores: acelerómetro (movimiento), brújula, temperatura y luz. La versión 2 (V2) además tiene '
                       'micrófono, bocina y un logotipo táctil.',
                       'Se conecta por USB para programarla, o con un portapilas de 2 pilas AAA.']), xp=60, preguntas=[
                ('¿Cuántos LED tiene la pantalla de la micro:bit?', '25', ['5', '10', '100']),
                ('¿Qué es GND?', 'La tierra: el regreso del circuito', ['Un botón', 'Una pila', 'Un sensor de luz']),
                ('¿Cómo cierras un circuito con la micro:bit?', 'Uniendo un pin con GND',
                 ['Presionando el botón A', 'Desconectando el USB', 'Agitándola']),
                ('¿Qué sensor detecta si la agitas?', 'El acelerómetro', ['La brújula', 'El micrófono',
                                                                         'El sensor de luz']),
                ('¿Qué tiene la micro:bit V2 que no tiene la V1?', 'Micrófono y bocina', ['Botones', 'Pantalla',
                                                                                         'Pines']),
                ('Los botones A y B son…', 'Entradas', ['Salidas', 'Pilas', 'Cables']),
            ]),
            mision('¿Entrada o salida de la micro:bit?', 'juego', leccion(
                intro='Clasifica cada parte: ¿le da información a la micro:bit o muestra algo?',
                tip='Si la micro:bit «siente» algo, es entrada. Si ella hace algo que tú ves u oyes, es salida.'),
                juego='clasifica_entrada_salida'),
            mision('Entra a MakeCode', 'link', leccion(
                intro='MakeCode es el editor de bloques de Microsoft para programar la micro:bit, con un simulador para '
                      'probar antes de pasar el programa a la tarjeta.',
                saber=['Idioma: ⚙️ (arriba a la derecha) → Idioma → «Español (España)». Es el único español que tiene y '
                       'así están escritos todos los bloques de las misiones.',
                       'El simulador (izquierda) es una micro:bit virtual: puedes hacer clic en sus botones y en sus '
                       'pines.',
                       'Para pasar el programa a la tarjeta: conéctala por USB → Descargar. Si te pide «Conectar '
                       'dispositivo», sigue los pasos; si se descarga un archivo .hex, arrástralo a la unidad '
                       'MICROBIT.',
                       'Tu proyecto se guarda en ese navegador. Ponle nombre (abajo, junto a Descargar).'],
                dinamica=DUPLA_MAKER,
                pasos=['Abre el enlace y cambia el idioma.',
                       'Nuevo proyecto: SombraVeloz_TuNombre.',
                       'Del cajón Básico arrastra «mostrar ícono» dentro de «al iniciar» y mira el simulador.',
                       'Ubica los cajones Básico, Entrada, Música, Lógica y Variables.'],
                logro=['Tu MakeCode está en Español (España) y sabes usar el simulador.'],
                entrega='en el comentario, escribe 3 cajones de bloques y para qué crees que sirve cada uno.'),
                xp=50, monedas=15, link=MICROBIT),
            microbit('Hola, micro:bit', leccion(
                intro='Tu primer programa: la micro:bit se presenta y responde a sus botones.',
                saber=['«al iniciar» se ejecuta una sola vez, cuando la micro:bit se enciende.',
                       '«al presionarse el botón A» es un evento: espera a que presiones A.',
                       LEYENDA_MICROBIT],
                dinamica=DUPLA_MAKER,
                pasos=['Arma el código en tu proyecto.',
                       'Pruébalo en el simulador: presiona A, B y A+B.',
                       'Cuando el profe lo indique, conecta la micro:bit y descarga el programa.',
                       'Cambia el texto y el ícono por los tuyos.'],
                logro=['La micro:bit muestra tu texto al iniciar y responde a los botones A, B y A+B.'],
                entrega='sube una captura de tus bloques o una foto de la micro:bit mostrando tu ícono.'),
                CODIGO_HOLA, xp=80, monedas=25),
        ]},
        {'nombre': 'Circuitos con la micro:bit', 'cofre': 30, 'misiones': [
            microbit('Tú cierras el circuito', leccion(
                intro='Tu cuerpo conduce un poquito de electricidad. Si tocas GND con una mano y el pin 1 con la otra, '
                      'cierras el circuito… y la micro:bit lo detecta.',
                saber=['«al presionarse pin P1» (Entrada) pasa cuando el pin 1 se une con GND: el circuito se cierra.',
                       '«al liberarse pin P1» pasa cuando se separan: el circuito se abre. (Si no lo ves, está en '
                       'Entrada → más.)',
                       'En el simulador, haz clic en el pin 1 para probar.',
                       LEYENDA_MICROBIT],
                dinamica=DUPLA_MAKER,
                pasos=['Arma el código. En «al presionarse pin» elige P1.',
                       'Pruébalo en el simulador haciendo clic en el pin 1.',
                       'Descárgalo a la tarjeta.',
                       'Toca con un dedo el GND y con un dedo de la otra mano el pin 1. Luego suelta.',
                       'Prueba haciendo una cadena: tú tocas GND, tu dupla toca el pin 1 y se toman de la mano.'],
                logro=['Al cerrar el circuito aparece la palomita y suena un tono; al abrirlo aparece el tache.'],
                entrega='sube una foto de la micro:bit con la palomita o una captura del simulador.'),
                CODIGO_TOCA, xp=80, monedas=25),
            microbit('Detector de conductores', leccion(
                intro='Convierte la micro:bit en un detector: si un material cierra el circuito, es conductor.',
                saber=['«pin P1 está presionado» (Entrada) es una pregunta: responde verdadero o falso.',
                       '«si … entonces / si no» (Lógica) decide qué mostrar en cada caso.',
                       '«para siempre» revisa sin parar.',
                       LEYENDA_MICROBIT],
                material=['La micro:bit', '2 cables con caimanes', 'Materiales para probar: clip, liga, papel aluminio, '
                          'moneda, lápiz con punta, borrador, palito de madera'],
                dinamica=DUPLA_MAKER,
                pasos=['Arma el código y descárgalo.',
                       'Conecta un caimán al pin 1 y otro al GND.',
                       'Une las dos puntas libres: debe aparecer la palomita. Sepáralas: el tache.',
                       'Pon cada material entre las dos puntas (sin tocar los metales con los dedos) y anota en una tabla: '
                       'material · ✔ o ✖ · ¿conductor o aislante?',
                       'Compara con lo que contestaste en el juego de conductores.'],
                logro=['Tu tabla tiene al menos 6 materiales probados y sabes cuáles son conductores.'],
                entrega='sube una foto de tu tabla y otra del detector probando un material.'), CODIGO_DETECTOR,
                xp=100, monedas=30),
            mision('¿Circuito abierto o cerrado?', 'juego', leccion(
                intro='Decide si en cada situación el circuito está abierto o cerrado.',
                tip='Si algo corta el camino (un cable suelto, una puerta abierta, un aislante), está abierto.'),
                juego='clasifica_abierto_cerrado'),
        ]},
        {'nombre': 'Sensor de puerta', 'cofre': 35, 'misiones': [
            mision('Plano del sensor', 'evidencia', leccion(
                intro='Así funcionará la trampa para Sombra Veloz: con la puerta cerrada, dos tiras de aluminio se tocan '
                      'y el circuito queda cerrado. Si alguien abre la puerta, las tiras se separan, el circuito se abre '
                      'y suena la alarma.',
                saber=['Una tira de aluminio va en el canto de la puerta y la otra en el marco, justo donde chocan al '
                       'cerrar.',
                       'Un caimán une la tira de la puerta con el pin 1 y el otro une la tira del marco con GND.',
                       'Los cables deben quedar flojos para que la puerta abra sin jalarlos.'],
                material=['Una hoja', 'Lápiz y colores'],
                pasos=['Dibuja la celda (una caja) con su puerta, vista de frente.',
                       'Dibuja dónde van las dos tiras de aluminio.',
                       'Dibuja los dos caimanes y a qué pin va cada uno.',
                       'Dibuja con flechas qué pasa con la puerta cerrada y con la puerta abierta.',
                       'Escribe la lista de materiales y quién hará cada parte.'],
                logro=['Tu plano muestra las tiras, los cables a P1 y GND y qué pasa en cada caso.'],
                entrega='sube una foto de tu plano.'), xp=80, monedas=25),
            mision('Maqueta de la celda', 'presencial', leccion(
                intro='Hoy se construye la parte maker: la celda de cartón con su puerta y las tiras de aluminio.',
                roles=['Constructor: arma la caja, la puerta y el tope.',
                       'Electricista: pega las tiras de aluminio y prueba que se toquen bien al cerrar.'],
                material=['Una caja de cartón (de zapatos o similar)', 'Papel aluminio', 'Cinta adhesiva',
                          'Tijeras escolares', 'Una tira de cartón para el tope de la puerta'],
                dinamica=['En duplas, en su lugar. Semáforo en 🟡.',
                          'El cúter lo usa SOLO el profe, que corta las puertas que lo necesiten.',
                          'Al terminar, cada dupla limpia su lugar antes de salir.'],
                pasos=['Marca en una cara de la caja una puerta de unos 8 × 12 cm y pide que la corten en 3 lados (el '
                       'cuarto lado es la bisagra).',
                       'Pega por dentro una tira de cartón como tope, para que la puerta choque con ella al cerrarse.',
                       'Pega una tira de aluminio en el tope y otra en la puerta, justo donde se tocan. Deja una punta '
                       'libre en cada una para el caimán.',
                       'Prueba: cierra la puerta y revisa que las tiras se toquen bien.'],
                logro=['Al cerrar la puerta las dos tiras se tocan, y al abrirla se separan.']), xp=60),
            microbit('Programa la alarma', leccion(
                intro='Ahora el cerebro de la trampa: la micro:bit vigila la puerta, suena cuando se abre y cuenta '
                      'cuántas veces la abrieron.',
                saber=['Variable «aperturas»: Variables → Crear una variable. Cuenta las veces que se abrió la puerta.',
                       '«al liberarse pin P1» se activa justo cuando el circuito se abre: el momento en que alguien abre la '
                       'puerta.',
                       '«repetir 3 veces» (Bucles) repite los dos tonos y suena como sirena.',
                       'Botón B: muestra cuántas veces se abrió. A+B: reinicia el contador.',
                       LEYENDA_MICROBIT],
                dinamica=DUPLA_MAKER,
                pasos=['Crea la variable «aperturas» y arma el código.',
                       'Pruébalo en el simulador con clic en el pin 1 (cerrar) y soltándolo (abrir).',
                       'Descárgalo a la micro:bit.',
                       'Conecta: caimán de la tira de la puerta → pin 1; caimán de la tira del tope → GND.',
                       'Cierra la puerta (✔), ábrela (sirena y ✖) y presiona B para ver el contador.',
                       'Si tu micro:bit es V1 y no suena, conecta unos audífonos o una bocina a P0 y GND.'],
                logro=['Con la puerta cerrada se ve ✔; al abrirla suena la sirena y el contador sube.'],
                entrega='sube un video corto o una foto de tu celda con la micro:bit conectada, y una captura de tus '
                        'bloques.'), CODIGO_ALARMA, xp=110, monedas=30),
            mision('Prueba contra Sombra Veloz', 'presencial', leccion(
                intro='Ninguna alarma está lista hasta que alguien intenta burlarla. Hoy cada dupla será Sombra Veloz '
                      'para la celda de otra dupla.',
                dinamica=['Las duplas se intercambian las celdas por filas, cuando el profe lo indica.',
                          'Se vale intentarlo despacio, rápido o con trucos, pero sin romper ni despegar nada.',
                          'Semáforo en 🟡. Cada intento se anota.'],
                pasos=['Intenten abrir la puerta de la otra dupla sin que suene la alarma. Hagan 3 intentos distintos.',
                       'Anoten qué truco intentaron y si la alarma lo detectó.',
                       'Regresen la celda y cuéntenles a sus dueños qué falló.',
                       'Mejoren su propia celda con lo que les dijeron (más aluminio, mejor tope, cables más flojos…).'],
                logro=['Probaste otra celda 3 veces y mejoraste la tuya con lo que encontraron.']), xp=50),
        ]},
        {'nombre': 'Caso cerrado', 'cofre': 40, 'misiones': [
            mision('Reporte del caso', 'texto', leccion(
                intro='Los investigadores cierran cada caso con un reporte. Escribe el tuyo.',
                pasos=['Explica en 3 renglones cómo funciona tu sensor (usa las palabras circuito abierto y cerrado).',
                       '¿Qué truco de Sombra Veloz casi venció a tu alarma? ¿Cómo lo arreglaste?',
                       'Propón una mejora con otro sensor de la micro:bit (luz, movimiento o sonido) y explica cómo '
                       'funcionaría.'],
                entrega='escribe tu reporte aquí abajo.'), xp=60),
            jefe('Jefe: Sombra Veloz', leccion(
                intro='Sombra Veloz en persona viene a probar tu sistema de seguridad. Solo lo atrapas si dominas los '
                      'circuitos y la micro:bit.'), [
                ('¿Qué pasa con el circuito cuando Sombra Veloz abre la puerta?', 'Se abre y la electricidad deja de '
                 'circular', ['Se cierra', 'Se vuelve más fuerte', 'No le pasa nada']),
                ('¿Qué bloque se activa justo cuando el circuito se abre?', 'al liberarse pin P1',
                 ['al iniciar', 'al presionarse el botón A', 'mostrar número']),
                ('¿Con qué se une el pin 1 para cerrar el circuito?', 'Con GND', ['Con el botón B', 'Con la pantalla',
                                                                                  'Con el USB']),
                ('¿Cuál de estos materiales cierra el circuito del detector?', 'Un clip de metal',
                 ['Una liga', 'Un borrador', 'Un palito de madera']),
                ('¿Para qué sirve la variable «aperturas»?', 'Para contar cuántas veces se abrió la puerta',
                 ['Para encender la pantalla', 'Para cambiar el tono', 'Para abrir la puerta']),
                ('¿Qué hace «repetir 3 veces» en la alarma?', 'Repite los tonos para que suene como sirena',
                 ['Abre la puerta 3 veces', 'Reinicia la micro:bit', 'Muestra el número 3']),
                ('¿Cuál es una entrada de la micro:bit?', 'El botón A', ['La pantalla de LED', 'La bocina',
                                                                        'Un LED conectado a un pin']),
                ('¿Cuál es un elemento de todo circuito?', 'Una fuente de energía, como una pila',
                 ['Un videojuego', 'Una pantalla táctil', 'Una contraseña']),
            ]),
        ]},
    ],
}
