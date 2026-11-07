"""Mundo 5 · ES-DAT306 Explorar el azul profundo: Sylvia Earle y los pulmones, los ejes X, Y, Z con una batalla
naval en 3D, las formas prediseñadas de Tinkercad (sobre todo el Tubo) y el modelado de un inspirómetro de tres
cámaras."""
from .base import LLAVERO, TINKERCAD, clasifica, jefe, leccion, mision, tinkercad

PAREJAS_3D = ['Cada quien modela en su computadora.',
              'Tu dupla (el compañero de al lado) revisa tu modelo al terminar cada paso, y tú el suyo.',
              '¿Atorados? Primero lo intentan entre los dos; si no sale, mano arriba y esperan al profe.',
              'Semáforo de voz en 🟡.']

JUEGOS = {
    'clasifica_xyz': clasifica('¿X, Y o Z?', '🧭', 'X es izquierda-derecha, Y es adelante-atrás y Z es arriba-abajo. '
                               '¿En qué eje pasa cada movimiento?', [
        ('Eje X (izquierda-derecha)', '↔️', ['Arrastrar la pieza hacia la derecha en la cuadrícula',
                                             'Hacer más ancha una caja de izquierda a derecha',
                                             'Un pez que nada de un lado a otro frente a ti',
                                             'Correr la silla hacia tu compañero de al lado']),
        ('Eje Y (adelante-atrás)', '↕️', ['Hacer más profunda la base, de adelante hacia atrás',
                                          'Un buzo que nada alejándose de ti',
                                          'Acercar tu cuaderno hacia el pizarrón',
                                          'Empujar la pieza hacia el fondo de la cuadrícula']),
        ('Eje Z (arriba-abajo)', '⬆️', ['Usar el cono negro para elevar la pieza', 'Hacer más alto un cilindro',
                                        'Una ballena que sube a respirar', 'La tecla D que baja la pieza al plano']),
    ], rondas=12),
    'clasifica_formas': clasifica('¿Caja, esfera o tubo?', '🧊', 'En Tinkercad casi todo se arma con formas '
                                  'prediseñadas. ¿Cuál usarías para cada pieza?', [
        ('Caja', '🟫', ['La base del inspirómetro', 'Un ladrillo', 'Un escalón', 'La tapa plana de una caja']),
        ('Esfera', '⚪', ['La pelota que sube al inhalar', 'Una perla', 'Una burbuja de aire',
                          'El casco redondo de un traje de buzo']),
        ('Tubo', '⭕', ['La cámara hueca donde sube la pelota', 'La manguera por donde pasa el aire',
                        'Un popote', 'Un anillo o una dona']),
    ], rondas=12),
}

MUNDO = {
    'nombre': 'Expedición Azul Profundo', 'tema': 'oceano',
    'descripcion': 'ES-DAT306 · Explorar el azul profundo. Para investigar el océano los biólogos marinos se certifican '
                   'en buceo. Sylvia Earle llegó a caminar por el fondo del mar a casi 400 metros de profundidad. Aprende '
                   'los ejes X, Y, Z, domina las formas prediseñadas de Tinkercad y modela en 3D un inspirómetro para '
                   'entrenar los pulmones. Pregunta guía: ¿cómo puedes fortalecer tus pulmones para practicar deportes '
                   'como el buceo?',
    'niveles': [
        {'nombre': 'Inmersión', 'cofre': 25, 'misiones': [
            mision('Sylvia, la exploradora', 'texto', leccion(
                intro='Sylvia Earle es una bióloga marina estadounidense a quien apodan «Su Profundidad». En 1979, '
                      'dentro de un traje especial, caminó libremente por el fondo del mar a 381 metros de profundidad, '
                      'cerca de Hawái. Hoy dirige un proyecto para proteger zonas del océano a las que llama «puntos de '
                      'esperanza».',
                pasos=['¿Qué crees que vio Sylvia a 381 metros, donde casi no llega la luz?',
                       '¿Qué necesita una persona para bucear de forma segura? Menciona 3 cosas.',
                       '¿Qué deporte o actividad que tú haces ayuda a tus pulmones?'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('Pulmones de explorador', 'cuestionario', leccion(
                intro='Antes de diseñar un aparato para los pulmones, entiende cómo trabajan.',
                saber=['El aire entra por la nariz, baja por la tráquea, pasa por los bronquios y llega a los '
                       'pulmones.',
                       'En los alvéolos (bolsitas pequeñísimas dentro de los pulmones) el oxígeno pasa a la sangre.',
                       'Inspirar: el diafragma (un músculo debajo de los pulmones) baja y entra el aire. Espirar: sube y '
                       'el aire sale.',
                       'Los pulmones se fortalecen con ejercicio: nadar, correr, andar en bici, bailar o tocar un '
                       'instrumento de viento.',
                       'Inspirómetro: al INHALAR por su boquilla, unas pelotitas suben dentro de sus cámaras. Se usa '
                       'para entrenar y recuperar los pulmones.',
                       'Seguridad: nunca practiques aguantar la respiración bajo el agua sin un adulto experto.']),
                xp=60, preguntas=[
                ('¿Dónde pasa el oxígeno a la sangre?', 'En los alvéolos', ['En la nariz', 'En el estómago',
                                                                           'En el diafragma']),
                ('¿Qué músculo baja cuando inspiras?', 'El diafragma', ['El corazón', 'El bíceps', 'La lengua']),
                ('¿Por dónde baja el aire hacia los pulmones?', 'Por la tráquea', ['Por el esófago', 'Por las venas',
                                                                                  'Por el estómago']),
                ('¿Cómo se usa un inspirómetro?', 'Se inhala por la boquilla y las pelotas suben',
                 ['Se sopla fuerte y suena', 'Se pone en el pecho', 'Se llena de agua']),
                ('¿Qué actividad fortalece los pulmones?', 'Nadar', ['Dormir de más', 'Ver series', 'Comer rápido']),
                ('¿Qué NO se debe hacer?', 'Aguantar la respiración bajo el agua sin un adulto experto',
                 ['Respirar profundo antes de un examen', 'Correr en el recreo', 'Nadar con salvavidas']),
            ]),
            mision('Respira como buzo', 'presencial', leccion(
                intro='Los buzos entrenan su respiración para estar tranquilos bajo el agua. Este ejercicio también '
                      'sirve para empezar la clase en calma.',
                dinamica=['Todos sentados, espalda derecha. Semáforo en 🔴 durante todo el ejercicio.',
                          'Si alguien se marea, deja de hacerlo y respira normal.'],
                pasos=['Medición 1: inhala profundo y exhala con una «fffff» suave y larga. Tu dupla cronometra los '
                       'segundos. Anótalos.',
                       'Respiración 4-4-6: inhala contando 4, sostén 4 y exhala contando 6. Repite 5 veces.',
                       'Pon una mano en tu abdomen: al inhalar debe inflarse. Así se respira con el diafragma.',
                       'Medición 2: repite la «fffff» y compara con la primera.'],
                logro=['Anotaste tus dos mediciones y sabes respirar con el diafragma.'],
                tip='Usa la respiración 4-4-6 antes de un examen o cuando estés muy acelerado.'), xp=50),
        ]},
        {'nombre': 'Ejes X, Y, Z', 'cofre': 30, 'misiones': [
            mision('Batalla naval 3D', 'presencial', leccion(
                intro='En una batalla naval normal hay 2 coordenadas. En el océano hay 3: también importa la '
                      'profundidad. Así se ubica todo en el modelado 3D.',
                saber=['Una posición en 3D se escribe (x, y, z).',
                       'En este juego: x va de 1 a 4 (izquierda a derecha), y de 1 a 4 (adelante hacia atrás) y z de 1 a '
                       '3 (1 = superficie, 2 = medio, 3 = fondo).'],
                dinamica=['En duplas, uno frente al otro, con una carpeta de pie como pared para no ver la hoja del otro.',
                          'Semáforo en 🟡: solo se dicen coordenadas y respuestas.',
                          '12 minutos de juego. Gana quien hunda más submarinos.'],
                pasos=['Dibuja 3 cuadrículas de 4 × 4: una para cada profundidad (z = 1, 2 y 3).',
                       'Esconde 4 submarinos (uno por casilla) y anota sus coordenadas.',
                       'Por turnos, disparen diciendo una coordenada: «(2, 3, 1)».',
                       'El otro responde «¡tocado!», «agua» o «agua, pero a esa profundidad hay un submarino».',
                       'Anoten sus disparos para no repetirlos.'],
                logro=['Dices y entiendes coordenadas (x, y, z) sin equivocarte de eje.']), xp=50),
            mision('El mundo en 3D', 'cuestionario', leccion(
                intro='Repasa los ejes y descubre para qué se usa el modelado 3D.',
                saber=['2D: solo ancho y alto, como un dibujo en papel. 3D: ancho, profundidad y alto, como un objeto '
                       'real.',
                       'En Tinkercad, X y Y están sobre el plano de trabajo (la cuadrícula azul) y Z es la altura.',
                       'Modelado 3D: crear objetos en la computadora. Se usa en videojuegos, películas, arquitectura, '
                       'prótesis médicas e impresión 3D.',
                       'Tinkercad mide en milímetros: 10 mm = 1 cm.']), xp=60, preguntas=[
                ('¿Qué eje es la altura en Tinkercad?', 'Z', ['X', 'Y', 'Ninguno']),
                ('¿Qué eje va de izquierda a derecha?', 'X', ['Y', 'Z', 'El origen']),
                ('En la batalla naval 3D, ¿qué significa la z?', 'La profundidad', ['La columna', 'El barco',
                                                                                    'El turno']),
                ('¿Qué tiene un objeto 3D que no tiene un dibujo 2D?', 'Profundidad', ['Color', 'Bordes', 'Nombre']),
                ('¿Cuántos milímetros son 2 centímetros?', '20 mm', ['2 mm', '200 mm', '12 mm']),
                ('¿Cuál es un uso real del modelado 3D?', 'Diseñar prótesis médicas',
                 ['Escribir correos', 'Hacer sumas', 'Escuchar música']),
            ]),
            mision('¿X, Y o Z?', 'juego', leccion(
                intro='Imagina cada movimiento y decide en qué eje pasa.',
                tip='Si algo sube o baja, siempre es Z.'), juego='clasifica_xyz'),
        ]},
        {'nombre': 'Taller Tinkercad', 'cofre': 30, 'misiones': [
            mision('Entra a Tinkercad', 'link', leccion(
                intro='Tinkercad es un programa gratuito para modelar en 3D desde el navegador.',
                saber=['Entrar con la clase del profe: tinkercad.com → Unirse a la clase → escribe el código de la clase '
                       'y tu apodo. No necesitas correo.',
                       LLAVERO,
                       'Formas básicas (a la derecha): caja, cilindro, esfera, techo, cono, tubo, texto… Se arrastran al '
                       'plano de trabajo.',
                       'Mover la cámara: clic derecho y arrastrar = girar alrededor; rueda del mouse = acercar; el cubo de '
                       'vista (arriba a la izquierda) pone la vista de frente, de arriba o de lado.',
                       'Si te pierdes: tecla F centra la vista en lo que seleccionaste.'],
                pasos=['Abre el enlace y entra con el código de tu clase y tu apodo.',
                       'Crea un diseño nuevo y cámbiale el nombre (arriba a la izquierda): Pruebas_TuNombre.',
                       'Arrastra una caja, un cilindro, una esfera y un tubo.',
                       'Gira la cámara y usa el cubo de vista para ver tus formas de frente y desde arriba.'],
                tip='Tinkercad guarda solo, pero tu diseño debe tener tu nombre para que lo encuentres.'),
                xp=40, monedas=10, link=TINKERCAD),
            tinkercad('Práctica: tanque de buceo', leccion(
                intro='Antes del inspirómetro, practica las herramientas armando el tanque de aire de un buzo con formas '
                      'prediseñadas.',
                saber=['Manijas blancas (esquinas): cambian el tamaño. Haz clic en un número para escribir la medida '
                       'exacta.',
                       'Cono negro (arriba de la pieza): la eleva en el eje Z. La tecla D la baja al plano.',
                       'Flechas del teclado: mueven 1 mm; con Shift, 10 mm. Ctrl + D duplica.',
                       'Panel de la forma (arriba a la derecha): ahí se cambia el color y, en el Tubo, el radio y el '
                       'grosor de su pared.',
                       'Alinear (tecla L): selecciona varias piezas y centra una con otra.'],
                dinamica=PAREJAS_3D,
                pasos=['Diseño nuevo: Tanque_TuNombre.',
                       'Tanque: un cilindro de 20 × 20 mm y 50 mm de alto.',
                       'Tapa redonda: una esfera de 20 mm. Elévala para que la mitad quede dentro del tanque, arriba.',
                       'Válvula: un cilindro de 6 × 6 × 8 mm encima de la esfera. Selecciónalo con el tanque → L → '
                       'centra en X y en Y.',
                       'Correa: un tubo con radio 12 y pared delgada, de 5 mm de alto, alrededor del tanque a media '
                       'altura (centrado con L).',
                       'Pinta el tanque de amarillo y la correa de negro. Selecciona todo (Ctrl + A) y agrupa (Ctrl + '
                       'G).'],
                logro=['Tu tanque tiene cuerpo, tapa redonda, válvula centrada y correa, todo agrupado.'],
                entrega='sube una captura de tu tanque.'), xp=90, monedas=25),
            mision('¿Caja, esfera o tubo?', 'juego', leccion(
                intro='Elige la forma prediseñada que usarías para cada pieza.',
                tip='Si es hueco por dentro y redondo, piensa en el tubo.'), juego='clasifica_formas'),
        ]},
        {'nombre': 'Modela el inspirómetro', 'cofre': 35, 'misiones': [
            mision('Boceto con medidas', 'evidencia', leccion(
                intro='Los diseñadores dibujan antes de modelar. Haz el boceto de tu inspirómetro con sus medidas.',
                saber=['Partes: base, 3 cámaras transparentes con una pelota cada una, manguera y boquilla.',
                       'Medidas sugeridas: base de 80 × 40 × 10 mm; cámaras (tubos) de 20 mm de diámetro y 60 mm de alto; '
                       'pelotas de 12 mm; manguera de 10 mm de diámetro y 60 mm de largo; boquilla de 16 mm.',
                       'Las cámaras suelen tener los números 1, 2 y 3 (o 600, 900 y 1200): cada pelota necesita una '
                       'inhalación más fuerte para subir.'],
                material=['Una hoja', 'Lápiz, regla y colores'],
                pasos=['Dibuja la vista de frente de tu inspirómetro.',
                       'Señala cada parte y escribe su medida.',
                       'Dibuja en una esquina las flechas de los ejes X y Z.',
                       'Inventa un nombre de marca y escríbelo en la base.'],
                logro=['Tu boceto tiene todas las partes con sus medidas y los ejes dibujados.'],
                entrega='sube una foto de tu boceto.'), xp=80, monedas=25),
            tinkercad('Base y cámaras', leccion(
                intro='Empieza el modelo con la base y las 3 cámaras. Usarás el Tubo: una forma prediseñada que ya viene '
                      'hueca.',
                dinamica=PAREJAS_3D,
                pasos=['Diseño nuevo: Inspirometro_TuNombre.',
                       'Base: una caja de 80 (X) × 40 (Y) × 10 (Z) mm.',
                       'Primera cámara: arrastra un Tubo ENCIMA de la base (Tinkercad lo pone sobre ella). En su panel, '
                       'radio 10 y una pared delgada; hazlo de 60 mm de alto.',
                       'Acomódalo cerca de la orilla izquierda de la base.',
                       'Ctrl + D para duplicarlo y muévelo 25 mm a la derecha (Shift + → dos veces y → cinco veces). '
                       'Repite para la tercera.',
                       'Selecciona las 3 cámaras y la base → L → centra todo en Y.'],
                logro=['La base tiene 3 cámaras huecas en línea recta, bien centradas.'],
                entrega='sube una captura de frente y otra en perspectiva.')),
            tinkercad('Pelotas y transparencia', leccion(
                intro='Ahora se va a ver como un aparato de verdad: cámaras transparentes y pelotas de colores adentro.',
                saber=['Transparente: selecciona la pieza → en el panel, abre el color y marca «Transparente».',
                       'Para meter una pelota justo en medio de la cámara: ponla sobre la base, selecciónala junto con su '
                       'cámara → L → centra en X y en Y.'],
                dinamica=PAREJAS_3D,
                pasos=['Marca las 3 cámaras como transparentes.',
                       'Arrastra una esfera de 12 mm sobre la base y píntala de azul.',
                       'Céntrala dentro de la primera cámara con Alinear.',
                       'Repite con una esfera amarilla en la segunda cámara y una roja en la tercera.',
                       'Sube la pelota azul hasta la mitad de su cámara con el cono negro: así se ve cuando alguien '
                       'inhala.'],
                logro=['Las 3 pelotas están centradas dentro de cámaras transparentes.'],
                entrega='sube una captura donde se vean las pelotas dentro de las cámaras.')),
            tinkercad('Manguera y boquilla', leccion(
                intro='Sin manguera no hay por dónde inhalar. Esta parte usa la rotación.',
                saber=['Rotar: las flechas curvas que aparecen alrededor de la pieza. Mientras giras, una regla marca los '
                       'grados; suelta en 90.'],
                dinamica=PAREJAS_3D,
                pasos=['Manguera: un Tubo con radio 5, de 60 mm de alto. Rótalo 90° para que quede acostado.',
                       'Pégalo al lado derecho de la base, a la altura de la base.',
                       'Boquilla: otro Tubo con radio 8 y 15 mm de alto, también acostado, en la punta de la manguera.',
                       'Selecciona la manguera y la boquilla → L → centra en Y y en Z.',
                       'Gira la cámara: la manguera y la boquilla deben verse huecas por dentro.'],
                logro=['La manguera y la boquilla están unidas al modelo, alineadas y huecas.'],
                entrega='sube una captura donde se vea el hueco de la boquilla.')),
            tinkercad('Toques finales', leccion(
                intro='Los detalles hacen que un modelo se vea profesional.',
                pasos=['Con la forma Texto escribe 1, 2 y 3 (de 2 mm de alto) frente a cada cámara, sobre la base.',
                       'Escribe la marca de tu inspirómetro en el frente de la base.',
                       'Usa máximo 4 colores que combinen.',
                       'Toma 3 capturas: de frente, desde arriba y en perspectiva.'],
                logro=['Tu modelo tiene números, marca, colores que combinan y 3 capturas desde distintos ángulos.'],
                entrega='sube tus 3 capturas.'), xp=100, monedas=30),
        ]},
        {'nombre': 'Expo submarina', 'cofre': 40, 'misiones': [
            mision('Expo de inspirómetros', 'presencial', leccion(
                intro='Los modelos se presentan como en una feria de ciencias.',
                dinamica=['Galería: cada quien deja su modelo abierto en pantalla y su boceto a un lado.',
                          'Recorrido en orden por filas, 1 minuto por computadora, cuando el profe da la señal.',
                          'Se observa con las manos atrás: nadie toca el mouse de otro.'],
                pasos=['Recorre los modelos de tus compañeros.',
                       'Deja en una nota adhesiva 2 estrellas (lo que te gustó) y 1 deseo (lo que mejorarías).',
                       'Votación: modelo más realista y modelo más creativo.',
                       'Vuelve a tu lugar y lee tus notas.'],
                logro=['Dejaste notas en al menos 4 modelos y explicaste el tuyo si te lo preguntaron.']), xp=50),
            jefe('Jefe: El Calamar Gigante', leccion(
                intro='El Calamar Gigante cuida las profundidades y solo deja pasar a quien domina los ejes, las formas '
                      'de Tinkercad y los pulmones de buzo.'), [
                ('¿Qué eje es la altura en Tinkercad?', 'Z', ['X', 'Y', 'W']),
                ('¿Qué hace la tecla D en Tinkercad?', 'Baja la pieza al plano de trabajo',
                 ['Duplica la pieza', 'Borra la pieza', 'La hace transparente']),
                ('¿Qué atajo duplica una pieza?', 'Ctrl + D', ['Ctrl + G', 'L', 'F']),
                ('¿Qué forma prediseñada ya viene hueca por dentro?', 'El tubo', ['La caja', 'La esfera',
                                                                                 'El cilindro']),
                ('Seleccionas dos piezas y presionas L. ¿Qué abres?', 'Alinear', ['Agrupar', 'Hueco', 'Rotar']),
                ('¿Cómo se usa un inspirómetro?', 'Se inhala por la boquilla y las pelotas suben',
                 ['Se sopla y suena', 'Se mete al agua', 'Se aprieta con la mano']),
                ('¿Dónde pasa el oxígeno a la sangre?', 'En los alvéolos', ['En la tráquea', 'En la nariz',
                                                                           'En el diafragma']),
                ('¿A qué profundidad caminó Sylvia Earle?', 'A 381 metros', ['A 3 metros', 'A 10 kilómetros',
                                                                            'A 38 metros']),
            ]),
        ]},
    ],
}
