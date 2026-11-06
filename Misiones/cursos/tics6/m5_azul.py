"""Mundo 5 · ES-DAT306 Explorar el azul profundo: los pulmones y el buceo, los ejes X, Y, Z, las herramientas de
Tinkercad y el modelado 3D de un inspirómetro (incentivador respiratorio) paso a paso."""
from .base import TINKERCAD, clasifica, jefe, leccion, mision, tinkercad

PAREJAS_3D = ['Cada quien modela en su computadora.',
              'Tu dupla (el compañero de al lado) revisa tus medidas al terminar cada paso, y tú las suyas.',
              '¿Atorados? Primero lo intentan entre los dos; si no sale, mano arriba y esperan al profe.']

JUEGOS = {
    'clasifica_ejes': clasifica('¿Eje X, Y o Z?', '🧭', 'X es izquierda-derecha, Y es adelante-atrás y Z es '
                                'arriba-abajo. ¿En qué eje se mueve cada cosa?', [
        ('Eje X (izquierda-derecha)', '↔️', ['Deslizar la goma hacia tu mano derecha',
                                             'Mover la pelota de la cámara del centro a la de la izquierda',
                                             'Un buzo que nada de lado, paralelo a la playa',
                                             'Correr la silla hacia el compañero de al lado']),
        ('Eje Y (adelante-atrás)', '↕️', ['Acercar el cuaderno hacia el pizarrón',
                                          'Alejar la silla del pizarrón hacia el fondo del salón',
                                          'Empujar la boquilla hacia el frente del modelo',
                                          'Un submarino que avanza de frente hacia el arrecife']),
        ('Eje Z (arriba-abajo)', '⬆️', ['Subir la pelota dentro de la cámara al inhalar',
                                        'Un buzo que baja a 400 metros de profundidad',
                                        'Levantar la tapa de la caja del suelo',
                                        'Una burbuja que sube a la superficie']),
    ], rondas=12),
    'clasifica_herramientas3d': clasifica('¿Hueco, agrupar o alinear?', '🧊', 'Elige la herramienta de Tinkercad que '
                                          'resuelve cada situación.', [
        ('Hueco', '🕳️', ['Hacer que la boquilla esté vacía por dentro', 'Hacer un agujero redondo en la base',
                          'Convertir un cilindro en el «molde» de un tubo', 'Hacer el espacio para que entre la pelota']),
        ('Agrupar', '🔗', ['Que el hueco de verdad recorte la pieza', 'Unir las 3 cámaras con la base en una sola pieza',
                           'Mover todo el inspirómetro de un solo jalón', 'Juntar la manguera con la boquilla']),
        ('Alinear', '📏', ['Centrar la pelota justo en medio de la cámara', 'Poner las 3 cámaras en línea recta',
                           'Dejar la boquilla centrada en la punta de la manguera',
                           'Emparejar el texto con el frente de la base']),
    ], rondas=12),
}

MUNDO = {
    'nombre': 'Laboratorio Azul Profundo', 'tema': 'oceano',
    'descripcion': 'ES-DAT306 · Explorar el azul profundo. Sylvia Earle, bióloga marina, caminó por el fondo del mar a '
                   'casi 400 metros de profundidad. Para bucear se necesitan pulmones fuertes: aquí aprenderás los ejes '
                   'X, Y, Z y las herramientas de modelado 3D para diseñar un inspirómetro. Pregunta guía: ¿cómo puedes '
                   'fortalecer tus pulmones para practicar deportes como el buceo?',
    'niveles': [
        {'nombre': 'Inmersión profunda', 'cofre': 25, 'misiones': [
            mision('La exploradora de las profundidades', 'texto', leccion(
                intro='En biología marina es necesario certificarse en buceo para investigar el océano de forma segura. '
                      'En 1979, Sylvia Earle caminó libremente por el fondo del mar a 381 metros de profundidad, cerca '
                      'de Hawái, dentro de un traje especial. Nadie lo había hecho antes.',
                pasos=['¿Qué crees que se necesita para bucear de forma segura? Menciona 3 cosas.',
                       '¿Qué deportes o actividades crees que fortalecen los pulmones?',
                       '¿Cuánto tiempo crees que puedes aguantar soplando sin parar? (Lo vas a medir en la siguiente '
                       'misión.)'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('Pulmones de buzo', 'cuestionario', leccion(
                intro='Antes de diseñar un aparato para los pulmones, entiende cómo funcionan.',
                saber=['Inspirar (inhalar): el diafragma, un músculo debajo de los pulmones, baja y los pulmones se '
                       'llenan de aire.',
                       'Espirar (exhalar): el diafragma sube y el aire sale.',
                       'Capacidad pulmonar: la cantidad de aire que cabe en tus pulmones. Se fortalece con ejercicio '
                       'como nadar, correr, andar en bici o bailar, y con ejercicios de respiración.',
                       'Inspirómetro (incentivador respiratorio): al inhalar por su boquilla, unas pelotitas suben '
                       'dentro de sus cámaras. Se usa en hospitales para recuperar los pulmones y para entrenar la '
                       'respiración.',
                       'Seguridad: nunca practiques aguantar la respiración dentro del agua sin un adulto experto.']),
                xp=60, preguntas=[
                ('¿Qué músculo ayuda a llenar los pulmones de aire?', 'El diafragma',
                 ['El bíceps', 'El corazón', 'El estómago']),
                ('¿Qué pasa al inspirar?', 'El aire entra y los pulmones se llenan',
                 ['El aire sale de los pulmones', 'El corazón se detiene', 'Nada']),
                ('¿Qué es la capacidad pulmonar?', 'La cantidad de aire que cabe en tus pulmones',
                 ['La velocidad a la que corres', 'El tamaño de tu nariz', 'La cantidad de agua que tomas']),
                ('¿Cómo funciona un inspirómetro?', 'Al inhalar por la boquilla, las pelotitas suben',
                 ['Al soplar, suena una alarma', 'Mide la temperatura', 'Guarda aire para bucear']),
                ('¿Cuál actividad fortalece los pulmones?', 'Nadar', ['Ver televisión', 'Dormir mucho',
                                                                      'Comer rápido']),
                ('¿Qué NO debes hacer?', 'Aguantar la respiración bajo el agua sin un adulto experto',
                 ['Hacer ejercicio', 'Respirar profundo antes de un examen', 'Nadar con un salvavidas']),
            ]),
            mision('Entrena tus pulmones', 'presencial', leccion(
                intro='Una práctica corta de respiración para empezar la clase en calma y medir tus pulmones.',
                material=['El cronómetro del celular del profe', 'Una hoja para anotar'],
                dinamica=['Todos sentados, espalda derecha, sin hablar durante el ejercicio.',
                          'Si alguien se marea, deja de hacerlo y respira normal.'],
                pasos=['Medición 1: inhala profundo y exhala con un «sssss» largo. Tu compañero cronometra cuántos '
                       'segundos dura. Anótalo.',
                       'Respiración 4-4-6: inhala contando 4, sostén 4 y exhala contando 6. Repite 5 veces.',
                       'Pon una mano en tu abdomen: al inhalar debe inflarse (eso es respirar con el diafragma).',
                       'Medición 2: repite el «sssss» y compara con la primera.',
                       'Comenten: ¿cambió tu tiempo? ¿Cómo te sientes?'],
                logro=['Anotaste tus dos mediciones y sabes respirar con el diafragma.'],
                tip='Esta respiración también sirve antes de un examen o cuando te sientes acelerado.'), xp=50),
        ]},
        {'nombre': 'Ejes X, Y, Z', 'cofre': 30, 'misiones': [
            mision('Ejes con el cuerpo', 'presencial', leccion(
                intro='Todo lo que existe en 3D se ubica con tres ejes. Primero los vas a sentir con el cuerpo.',
                saber=['Eje X: izquierda-derecha. Eje Y: adelante-atrás. Eje Z: arriba-abajo.',
                       'El origen (0, 0, 0) es el punto de partida desde donde se mide.',
                       'Una posición se escribe así: (x, y, z). Ejemplo: (2, 3, 1) = 2 a la derecha, 3 hacia adelante, '
                       '1 hacia arriba.'],
                dinamica=['Todos de pie junto a su lugar. Movimientos en su sitio, sin caminar.',
                          'Quien se equivoca no sale: se queda, pero ayuda a vigilar a los demás.'],
                pasos=['El profe dice «X» y todos estiran los brazos a los lados; «Y», un brazo al frente y otro atrás; '
                       '«Z», uno arriba y otro abajo.',
                       'Ronda rápida: el profe dice ejes cada vez más rápido.',
                       'Elijan una esquina del salón como origen (0, 0, 0) y midan en pasos la posición (x, y) de 3 '
                       'objetos: el escritorio, la puerta y el bote de basura.',
                       '¿Cuál sería la z de un objeto en el piso? ¿Y la de la lámpara?'],
                logro=['Ubicas 3 objetos del salón con coordenadas (x, y, z).']), xp=50),
            mision('Coordenadas y modelado 3D', 'cuestionario', leccion(
                intro='Repasa los ejes y descubre para qué se usa el modelado 3D.',
                saber=['2D: solo ancho y alto, como un dibujo en papel. 3D: ancho, profundidad y alto, como un objeto '
                       'real.',
                       'En Tinkercad, X y Y están sobre el plano de trabajo (la cuadrícula azul) y Z es la altura.',
                       'Modelado 3D: crear objetos en la computadora. Se usa en películas animadas, videojuegos, '
                       'arquitectura, prótesis médicas e impresión 3D.',
                       'Tinkercad mide en milímetros (mm): 10 mm = 1 cm.']), xp=60, preguntas=[
                ('¿Qué eje representa la altura?', 'Z', ['X', 'Y', 'Ninguno']),
                ('¿Qué eje va de izquierda a derecha?', 'X', ['Y', 'Z', 'El origen']),
                ('¿Qué es el origen?', 'El punto (0, 0, 0) desde donde se mide',
                 ['El objeto más grande', 'El último punto', 'La esquina de la pantalla']),
                ('¿Qué tiene un objeto 3D que no tiene un dibujo 2D?', 'Profundidad', ['Color', 'Nombre', 'Bordes']),
                ('¿En qué unidad mide Tinkercad?', 'Milímetros', ['Metros', 'Kilómetros', 'Pulgadas']),
                ('¿Cuál es un uso real del modelado 3D?', 'Diseñar prótesis médicas',
                 ['Escribir correos', 'Hacer sumas', 'Escuchar música']),
            ]),
            mision('¿Eje X, Y o Z?', 'juego', leccion(
                intro='Imagina cada movimiento y decide en qué eje ocurre.',
                tip='Si algo sube o baja, siempre es Z.'), juego='clasifica_ejes'),
        ]},
        {'nombre': 'Taller Tinkercad', 'cofre': 30, 'misiones': [
            mision('Entra al laboratorio 3D', 'link', leccion(
                intro='Tinkercad es un programa gratuito de Autodesk para modelar en 3D desde el navegador.',
                saber=['Entrar con la clase del profe: tinkercad.com → Unirse a la clase → escribe el código de la '
                       'clase y tu apodo. No necesitas correo.',
                       'Plano de trabajo: la cuadrícula azul donde construyes.',
                       'Formas básicas (derecha): arrastra caja, cilindro, esfera, tubo, techo, texto…',
                       'Mover la cámara: clic derecho y arrastrar = girar alrededor; rueda del mouse = acercar; el cubo '
                       'de vista (arriba a la izquierda) cambia a frente, arriba o lado.',
                       'Si te pierdes, la tecla F centra la vista en lo que seleccionaste.'],
                pasos=['Abre el enlace y entra con el código de tu clase.',
                       'Crea un diseño nuevo y cámbiale el nombre (arriba a la izquierda): Pruebas_TuNombre.',
                       'Arrastra una caja al plano de trabajo.',
                       'Gira la cámara alrededor de la caja y usa el cubo de vista para verla de frente y desde arriba.'],
                tip='Tinkercad guarda solo, pero revisa que tu diseño tenga tu nombre para encontrarlo.'),
                xp=40, monedas=10, link=TINKERCAD),
            tinkercad('Herramientas básicas: mini submarino', leccion(
                intro='Antes del inspirómetro, practica todas las herramientas armando un mini submarino.',
                saber=['Manijas blancas (esquinas): cambian el tamaño. Haz clic en un número para escribir la medida '
                       'exacta. Con Shift se mantiene la proporción.',
                       'Cono negro de arriba: eleva la pieza en el eje Z. La tecla D la regresa al plano.',
                       'Flechas curvas: rotan la pieza.',
                       'Flechas del teclado: mueven 1 mm. Ctrl + D duplica.',
                       'Hueco: convierte una forma en «molde» que recorta. Agrupar (Ctrl + G) aplica el recorte y une '
                       'piezas.'],
                dinamica=PAREJAS_3D,
                pasos=['Cuerpo: arrastra un cilindro, gíralo 90° para que quede acostado y hazlo de 60 mm de largo y 20 '
                       'mm de diámetro.',
                       'Torre: una caja de 15 × 10 × 12 mm sobre el cuerpo (elévala con el cono negro).',
                       'Ventanas: 3 cilindros pequeños de 6 mm convertidos en Hueco, uno al lado del otro (usa Ctrl + D '
                       'y las flechas).',
                       'Hélice: un techo o una caja delgada en la parte de atrás, rotada 45°.',
                       'Selecciona todo (Ctrl + A) y agrupa (Ctrl + G). Las ventanas deben quedar recortadas.'],
                logro=['Tu submarino tiene cuerpo, torre, 3 ventanas recortadas y hélice, todo agrupado.'],
                entrega='sube una captura de tu submarino.'), xp=90, monedas=25),
            mision('¿Hueco, agrupar o alinear?', 'juego', leccion(
                intro='Las tres herramientas que más usarás en el inspirómetro. ¿Cuál resuelve cada situación?',
                saber=['Hueco: la forma se vuelve transparente y rayada; al agrupar, recorta.',
                       'Alinear (tecla L): selecciona varias piezas y empareja sus orillas o centros.']),
                juego='clasifica_herramientas3d'),
        ]},
        {'nombre': 'Construye el inspirómetro', 'cofre': 35, 'misiones': [
            mision('Plano del inspirómetro', 'evidencia', leccion(
                intro='Los ingenieros no empiezan en la computadora: primero dibujan un plano con medidas.',
                saber=['Un inspirómetro de tres cámaras tiene: base, 3 cámaras transparentes con una pelota cada una, '
                       'una manguera y una boquilla.',
                       'Las cámaras suelen tener etiquetas de 600, 900 y 1200: la fuerza de inhalación que se necesita '
                       'para subir cada pelota.',
                       'En el plano se dibuja la vista de frente y se anotan las medidas en milímetros.'],
                pasos=['En una hoja, dibuja la vista de frente del inspirómetro.',
                       'Señala cada parte y anota sus medidas: base 90 × 40 × 10 mm; cámaras de 20 mm de diámetro y 70 '
                       'mm de alto; pelotas de 14 mm; manguera de 10 mm de diámetro y 80 mm de largo; boquilla de 18 mm.',
                       'Dibuja los ejes X y Z en una esquina del plano.',
                       'Inventa una marca para tu inspirómetro y escríbela en la base.'],
                logro=['Tu plano tiene todas las partes con sus medidas y los ejes dibujados.'],
                entrega='sube una foto de tu plano.'), xp=80, monedas=25),
            tinkercad('Base y cámaras', leccion(
                intro='Empieza el modelo: la base y las tres cámaras huecas.',
                dinamica=PAREJAS_3D,
                pasos=['Crea un diseño nuevo: Inspirometro_TuNombre.',
                       'Base: caja de 90 (X) × 40 (Y) × 10 (Z) mm.',
                       'Cámara: cilindro de 20 × 20 mm y 70 mm de alto. Elévalo 10 mm para que quede sobre la base.',
                       'Hueco interior: otro cilindro de 16 × 16 × 68 mm convertido en Hueco. Alinéalo al centro de la '
                       'cámara (selecciona los dos → L → centro en X y en Y) y elévalo 12 mm.',
                       'Agrupa la cámara con su hueco: ahora es un tubo.',
                       'Duplica la cámara (Ctrl + D) y muévela 30 mm a la derecha. Vuelve a presionar Ctrl + D: '
                       'Tinkercad repite el movimiento y aparece la tercera.',
                       'Alinea las 3 cámaras con la base.'],
                logro=['La base tiene 3 cámaras huecas en línea recta, separadas 30 mm entre sí.'],
                entrega='sube una captura vista de frente y otra en perspectiva.')),
            tinkercad('Pelotas y transparencia', leccion(
                intro='Ahora se ve como un aparato real: cámaras transparentes y pelotas de colores.',
                saber=['Para que una pieza sea transparente: selecciónala → en el panel de color marca «Transparente».',
                       'Alinear centra una pieza dentro de otra sin calcular nada.'],
                dinamica=PAREJAS_3D,
                pasos=['Selecciona cada cámara y márcala como Transparente.',
                       'Crea una esfera de 14 mm y píntala de azul.',
                       'Selecciona la esfera y la primera cámara → L → centra en X y en Y.',
                       'Elévala para que quede en el fondo de la cámara (unos 12 mm).',
                       'Repite con una esfera amarilla en la segunda cámara y una roja en la tercera.',
                       'Sube la pelota roja a la mitad de su cámara: así se ve cuando alguien inhala fuerte.'],
                logro=['Las tres pelotas están centradas dentro de cámaras transparentes.'],
                entrega='sube una captura donde se vean las pelotas dentro de las cámaras.')),
            tinkercad('Manguera y boquilla', leccion(
                intro='Sin manguera no hay por dónde inhalar. Esta es la parte que más usa la rotación.',
                dinamica=PAREJAS_3D,
                pasos=['Manguera: cilindro de 10 × 10 mm y 80 mm de alto. Rótalo 90° para que quede acostado.',
                       'Pégalo al lado derecho de la base, a la altura de la base (usa Alinear y el cono para la altura).',
                       'Hazla hueca: un cilindro de 6 mm, también acostado, convertido en Hueco y centrado dentro → '
                       'Agrupar.',
                       'Boquilla: cilindro de 18 × 18 × 20 mm acostado al final de la manguera.',
                       'Hueco de la boquilla: un cilindro de 12 mm convertido en Hueco y centrado → Agrupar.',
                       'Gira la cámara: la manguera y la boquilla deben verse huecas por dentro.'],
                logro=['La manguera y la boquilla están unidas al modelo, alineadas y huecas por dentro.'],
                entrega='sube una captura donde se vea el hueco de la boquilla.')),
            tinkercad('Etiquetas y presentación', leccion(
                intro='Los detalles hacen que un modelo se vea profesional.',
                pasos=['Con la forma Texto escribe 600, 900 y 1200: 2 mm de alto, sobre la base, cada uno frente a su '
                       'cámara.',
                       'Escribe la marca de tu inspirómetro en el frente de la base.',
                       'Elige colores que combinen (máximo 4).',
                       'Agrupa todo menos las pelotas (así se conservan sus colores).',
                       'Toma 3 capturas: de frente, desde arriba y en perspectiva.',
                       'Opcional: Exportar → .STL, el formato que usan las impresoras 3D.'],
                logro=['Tu modelo tiene etiquetas, marca y tres capturas desde distintos ángulos.'],
                entrega='sube tus 3 capturas.'), xp=110, monedas=30),
        ]},
        {'nombre': 'Expo del laboratorio', 'cofre': 40, 'misiones': [
            mision('Expo de inspirómetros', 'presencial', leccion(
                intro='Los modelos se presentan como en una feria de ciencias.',
                dinamica=['Galería: cada quien deja su modelo abierto en pantalla y su plano a un lado.',
                          'Recorrido en orden, en el sentido de las manecillas del reloj, 1 minuto por computadora.',
                          'Se observa con las manos atrás: nadie toca el mouse de otro.'],
                pasos=['Recorre los modelos de tus compañeros.',
                       'Deja 2 estrellas y 1 deseo en una nota adhesiva junto a cada modelo que visites.',
                       'Votación final: modelo más realista y modelo más creativo.',
                       'Vuelve a tu lugar y lee tus notas: ¿qué mejorarías?'],
                logro=['Diste retroalimentación a al menos 4 modelos y explicaste el tuyo.']), xp=50),
            jefe('Jefe: El Kraken', leccion(
                intro='El Kraken vive en lo más profundo y solo deja pasar a quien domina los ejes, las herramientas 3D '
                      'y los pulmones de buzo.'), [
                ('¿Qué eje representa la altura en Tinkercad?', 'Z', ['X', 'Y', 'W']),
                ('¿Qué hace la tecla D en Tinkercad?', 'Baja la pieza al plano de trabajo',
                 ['Duplica la pieza', 'Borra la pieza', 'La hace transparente']),
                ('Quieres que un cilindro recorte un agujero. ¿Qué haces?', 'Lo conviertes en Hueco y agrupas',
                 ['Lo pintas de negro', 'Lo haces más grande', 'Lo elevas']),
                ('¿Qué atajo duplica una pieza?', 'Ctrl + D', ['Ctrl + G', 'L', 'F']),
                ('Seleccionas dos piezas y presionas L. ¿Qué herramienta abres?', 'Alinear',
                 ['Agrupar', 'Hueco', 'Reflejar']),
                ('¿Para qué sirve un inspirómetro?', 'Para ejercitar los pulmones al inhalar',
                 ['Para medir la temperatura', 'Para bucear sin tanque', 'Para limpiar el aire']),
                ('¿Qué músculo baja cuando inspiras?', 'El diafragma', ['El corazón', 'El bíceps', 'La lengua']),
                ('¿Quién caminó por el fondo del mar a 381 metros de profundidad?', 'Sylvia Earle',
                 ['Marie Curie', 'Frida Kahlo', 'Jacques Cousteau']),
            ]),
        ]},
    ],
}
