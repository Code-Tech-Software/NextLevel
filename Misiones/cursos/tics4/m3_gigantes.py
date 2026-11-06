"""Mundo 3 · ES-SEA206 Gigantes de la Tierra: cómo se forman las montañas y modelado 3D en Tinkercad
(mover, rotar, elevar, huecos y agrupar)."""
from .base import TINKERCAD, clasifica, jefe, leccion, mision

JUEGOS = {
    'clasifica_tierra': clasifica('¿Lento o rápido?', '🌋', 'Algunos cambios de la Tierra tardan millones de años y otros segundos.', [
        ('Lento', '🐢', ['Una cordillera que se levanta', 'Un río que excava un cañón', 'Las placas tectónicas que se mueven',
                        'El viento que desgasta una roca', 'Una montaña que la lluvia hace más baja', 'Un glaciar que avanza']),
        ('Rápido', '⚡', ['Una erupción volcánica', 'Un sismo (temblor)', 'Un deslave en un cerro', 'Una avalancha de nieve',
                         'Un tsunami que llega a la costa', 'Una roca que cae de un acantilado']),
    ]),
    'clasifica_herramientas': clasifica('¿Mover, rotar o elevar?', '🧊', '¿Qué herramienta de Tinkercad necesitas?', [
        ('Mover', '↔️', ['Llevar el volcán más a la izquierda', 'Acercar dos montañas para que se toquen',
                        'Poner el árbol junto al río', 'Correr la figura con las flechas del teclado',
                        'Arrastrar la figura sobre el plano de trabajo']),
        ('Rotar', '🔄', ['Girar la montaña 45 grados', 'Poner el cono de cabeza', 'Inclinar una roca para que se vea natural',
                        'Usar las flechas curvas de la figura', 'Acostar un cilindro']),
        ('Elevar', '⬆️', ['Subir la nube para que flote en el cielo', 'Poner la nieve encima de la cima',
                         'Usar el cono negro de arriba de la figura', 'Bajar una figura que quedó flotando',
                         'Subir un pájaro sobre la montaña']),
    ], rondas=14),
}

MUNDO = {
    'nombre': 'Valle de los Gigantes', 'tema': 'desierto',
    'descripcion': 'ES-SEA206 · Gigantes de la Tierra. En Santiago de Chile hay montañas por todos lados: la Cordillera '
                   'de los Andes, con todo y volcanes. Descubre cómo se forman las montañas y constrúyelas en 3D con '
                   'Tinkercad. Pregunta guía: ¿cómo se forman las montañas?',
    'niveles': [
        {'nombre': '¿Cómo se forman las montañas?', 'cofre': 25, 'misiones': [
            mision('Carta desde Santiago de Chile', 'texto', leccion(
                intro='«Hace tiempo viajé a Santiago de Chile y me sorprendió ver montañas por todos lados. Mi tía '
                      'Pilarica me explicó que era la Cordillera de los Andes, donde incluso hay volcanes. ¡No lo podía '
                      'creer! Además, se puede ver desde varios países. Eso despertó muchas preguntas en mí: ¿qué es una '
                      'cordillera? ¿Por qué hay volcanes ahí?»\n\nPregunta del caso: ¿cómo se forman las montañas?',
                pasos=['Escribe qué crees que es una cordillera.',
                       'Escribe tu hipótesis: ¿cómo crees que se forman las montañas? (No importa si no es la respuesta '
                       'correcta: es tu idea para investigar.)',
                       'Escribe el nombre de una montaña o un volcán que conozcas o que se vea desde tu ciudad.'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('La Tierra es un rompecabezas', 'cuestionario', leccion(
                intro='Repasa cómo es la Tierra por dentro y descubre de dónde salen las montañas.',
                saber=['La Tierra tiene capas, como un durazno: corteza (la cáscara donde vivimos), manto (roca caliente '
                       'que se mueve muy lento) y núcleo (el centro, muy caliente).',
                       'La corteza está partida en placas tectónicas, como un rompecabezas gigante. Se mueven unos '
                       'centímetros por año, ¡como crecen tus uñas!',
                       'Cuando dos placas chocan durante millones de años, la roca se dobla y se levanta: así se forman '
                       'las cordilleras (muchas montañas en fila).',
                       'Los Andes se formaron porque la placa de Nazca (bajo el océano Pacífico) se mete debajo de la '
                       'placa Sudamericana. Por eso también hay volcanes.',
                       'Un volcán es una abertura por donde sale magma (roca derretida). Afuera se llama lava.',
                       'En México, el Pico de Orizaba (la montaña más alta del país) y el Popocatépetl son volcanes.']),
                xp=60, preguntas=[
                ('¿Cómo se llama la capa de la Tierra donde vivimos?', 'Corteza', ['Núcleo', 'Manto', 'Atmósfera']),
                ('La corteza de la Tierra está partida en piezas llamadas…', 'Placas tectónicas',
                 ['Montañas', 'Continentes de papel', 'Volcanes']),
                ('¿Qué pasa cuando dos placas chocan durante millones de años?',
                 'La roca se dobla y se levanta formando montañas', ['Se forma un río', 'Desaparecen', 'Se vuelven agua']),
                ('Una cordillera es…', 'Un conjunto de montañas en fila', ['Una sola piedra', 'Un río muy largo', 'Una nube']),
                ('¿Por qué hay volcanes en los Andes?', 'Porque una placa se mete debajo de otra y el magma sube',
                 ['Porque llueve mucho', 'Porque alguien los construyó', 'Porque hace frío']),
                ('Cuando el magma sale a la superficie se llama…', 'Lava', ['Arena', 'Nieve', 'Hielo']),
                ('¿Qué tan rápido se mueven las placas tectónicas?', 'Unos centímetros por año, como crecen tus uñas',
                 ['Un kilómetro por segundo', 'No se mueven nunca', 'Como un coche en carretera']),
            ]),
            mision('Montañas de plastilina', 'evidencia', leccion(
                intro='Vas a hacer en minutos lo que la Tierra tarda millones de años: ¡levantar montañas!',
                material=['Plastilina de 3 o 4 colores', 'Una regla', 'Tu cuaderno'],
                pasos=['Aplana tiras de plastilina de distintos colores, del mismo tamaño (unos 15 × 5 cm).',
                       'Ponlas una encima de otra: son las capas de roca.',
                       'Pon tus manos en los dos extremos y empuja despacio hacia el centro. ¡Eres dos placas chocando!',
                       'Observa cómo se doblan y se levantan las capas. Esos dobleces se llaman pliegues.',
                       'Corta tu montaña por la mitad con la regla y observa las capas por dentro.'],
                logro=['Tu modelo muestra pliegues y explicas qué representan tus manos.'],
                entrega='sube una foto de tu montaña cortada por la mitad.'), xp=80, monedas=20),
            mision('Vuela por los gigantes con Google Earth', 'link', leccion(
                intro='Con Google Earth vuelas por el planeta como un satélite. ¡Vamos a visitar a los gigantes!',
                saber=['La lupa busca un lugar por su nombre.', 'La rueda del mouse acerca y aleja.',
                       'Para ver las montañas en 3D, mantén presionada la tecla Shift y arrastra con el mouse (o usa el '
                       'botón 3D).'],
                pasos=['Busca «Santiago, Chile» y mira hacia el este: esa muralla de montañas es la Cordillera de los Andes.',
                       'Busca «Aconcagua», la montaña más alta de América, e inclina la vista en 3D.',
                       'Busca «Pico de Orizaba» y luego «Popocatépetl». ¿Ves el cráter?',
                       'Busca «Monte Everest», la montaña más alta del mundo.',
                       'Compara: ¿cuál te pareció más impresionante?'],
                entrega='en el comentario, escribe qué montaña te impresionó más y por qué. Si puedes, sube una captura.'),
                xp=60, link='https://earth.google.com/web/'),
            mision('¿Lento o rápido?', 'juego', leccion(
                intro='Algunos cambios de la Tierra tardan millones de años y otros pasan en segundos. Clasifícalos.',
                tip='Las montañas crecen lento, pero un volcán puede hacer erupción de un momento a otro.'),
                juego='clasifica_tierra'),
        ]},
        {'nombre': 'Tinkercad: mi taller 3D', 'cofre': 30, 'misiones': [
            mision('Bienvenido a Tinkercad', 'link', leccion(
                intro='Tinkercad es un programa gratuito para diseñar objetos en 3D desde el navegador. Es tu taller '
                      'de construcción.',
                saber=['Plano de trabajo: la cuadrícula azul donde construyes.',
                       'Figuras básicas: el panel de la derecha (caja, cilindro, cono, esfera…). Se arrastran al plano.',
                       'Cubo de vista (arriba a la izquierda): da clic en sus caras para ver el diseño de frente, de lado '
                       'o desde arriba.',
                       'Zoom: rueda del mouse. Girar la vista: clic derecho y arrastrar. Deshacer: Ctrl + Z.'],
                pasos=['Abre el enlace y entra a la clase con el código y el apodo que te dé tu profe («Unirse a clase»).',
                       'Crea un diseño nuevo: Crear → Diseño 3D.',
                       'Arrastra al plano una caja, un cilindro y un cono.',
                       'Gira la vista con clic derecho y acércate con la rueda. Usa el cubo de vista para ver desde arriba.',
                       'Cambia el color de una figura: selecciónala y en el panel Forma da clic en el color.',
                       'Cambia el nombre del diseño (arriba a la izquierda) a Taller_TuNombre.'],
                logro=['Agregas figuras, cambias su color y mueves la vista sin perderte.'],
                entrega='en el comentario, escribe para qué sirven el cubo de vista y el clic derecho.'),
                xp=60, link=TINKERCAD),
            mision('Las tres superherramientas', 'presencial', leccion(
                intro='Todo lo que construyas en 3D se hace moviendo, rotando y elevando figuras. Tu profe las demuestra '
                      'y tú practicas.',
                saber=['Mover: arrastra la figura sobre el plano, o usa las flechas del teclado (1 mm por toque; con '
                       'Shift, 10 mm).',
                       'Rotar: al seleccionar una figura aparecen flechas curvas; arrastra una y verás los grados del giro.',
                       'Elevar: el cono negro de arriba de la figura la sube o la baja (también Ctrl + flecha arriba o abajo).',
                       'Escalar: los cuadritos blancos de las esquinas cambian el tamaño; con Shift mantiene la forma.'],
                pasos=['Observa la demostración de tu profe en el proyector.',
                       '«Tinkercad dice»: tu profe da órdenes y tú las haces: «mueve el cubo 20 mm a la derecha», «gira '
                       'el cono 90 grados», «eleva la esfera 15 mm».',
                       'Haz que un cilindro quede acostado (rotado 90°) y flotando 10 mm sobre el plano.',
                       'Enséñale a tu compañero cómo lo hiciste.'],
                logro=['Mueves, rotas y elevas figuras cuando te lo piden.']), xp=50),
            mision('¿Mover, rotar o elevar?', 'juego', leccion(
                intro='Lee cada acción y decide qué herramienta de Tinkercad necesitas.'), juego='clasifica_herramientas'),
            mision('Reto: la torre en espiral', 'evidencia', leccion(
                intro='Usa las tres superherramientas para construir una torre que gira como una escalera de caracol.',
                saber='Ctrl + D duplica la figura. Si mueves o giras la copia y vuelves a presionar Ctrl + D, ¡Tinkercad '
                      'repite lo mismo en la siguiente copia!',
                pasos=['Arrastra una caja al plano y hazla de 40 × 10 × 5 mm (escribe las medidas en los cuadritos blancos).',
                       'Duplícala con Ctrl + D: la copia queda en el mismo lugar.',
                       'Eleva la copia 5 mm (cono negro) y rótala 20 grados.',
                       'Presiona Ctrl + D otra vez, varias veces, hasta tener 10 pisos.',
                       'Pinta cada piso de un color diferente.'],
                logro=['Tu torre tiene 10 pisos girados y elevados por igual.'],
                entrega='sube una captura de tu torre en espiral.'), xp=90, monedas=25),
            mision('Herramientas de Tinkercad', 'cuestionario', leccion(
                intro='Demuestra que dominas tu taller 3D.',
                saber=['Mover: arrastrar o flechas del teclado (Shift + flecha mueve 10 mm).',
                       'Rotar: flechas curvas. Elevar: cono negro.',
                       'Escalar sin deformar: arrastrar una esquina con Shift.',
                       'Ctrl + Z deshace y Ctrl + D duplica.',
                       'El cubo de vista cambia el punto de vista.']), xp=60, preguntas=[
                ('¿Qué herramienta usas para subir una nube y que flote?', 'Elevar con el cono negro',
                 ['Rotar con las flechas curvas', 'Cambiar el color', 'Borrar']),
                ('¿Para qué sirven las flechas curvas de una figura?', 'Para rotarla',
                 ['Para borrarla', 'Para cambiar el color', 'Para guardarla']),
                ('Con el teclado, ¿cómo mueves una figura 10 mm de un jalón?', 'Shift + flecha',
                 ['Solo la barra espaciadora', 'Enter', 'Ctrl + Z']),
                ('¿Qué hace Ctrl + Z?', 'Deshace el último cambio', ['Guarda el diseño', 'Duplica la figura', 'Cierra Tinkercad']),
                ('¿Qué hace Ctrl + D?', 'Duplica la figura seleccionada', ['La borra', 'La pinta de rojo', 'Cambia la vista']),
                ('¿Para qué sirve el cubo de vista?', 'Para ver el diseño de frente, de lado o desde arriba',
                 ['Para agregar cubos', 'Para medir', 'Para cambiar el idioma']),
                ('Para cambiar el tamaño sin deformar, arrastras la esquina mientras presionas…', 'Shift',
                 ['Alt', 'Tab', 'Esc']),
            ]),
        ]},
        {'nombre': 'DTectives en acción: mi cordillera 3D', 'cofre': 35, 'misiones': [
            mision('Boceto de mi cordillera', 'evidencia', leccion(
                intro='Los diseñadores primero dibujan. Planea en papel la cordillera que construirás en Tinkercad.',
                pasos=['Dibuja tu cordillera vista de lado: al menos 3 montañas de diferente altura y un volcán.',
                       'Agrega nieve en la montaña más alta y un río o un valle.',
                       'Escribe junto a cada parte qué figura de Tinkercad usarás (cono, paraboloide, caja…).',
                       'Escribe los colores que usarás.'],
                logro=['Tu boceto tiene 3 montañas, un volcán y la lista de figuras.'],
                entrega='sube una foto de tu boceto.'), xp=70, monedas=20),
            mision('Montañas con conos', 'evidencia', leccion(
                intro='Hora de construir tu cordillera con las tres superherramientas.',
                pasos=['Diseño nuevo: Cordillera_TuNombre. Arrastra una caja de 150 × 100 × 3 mm: será el suelo. '
                       'Píntala de verde.',
                       'Arrastra un cono (o un paraboloide) de 50 × 50 × 60 mm, color café. Elévalo 3 mm para que quede '
                       'justo encima del suelo.',
                       'Agrega 2 montañas más de diferentes tamaños. Rota un poco cada una para que se vean naturales y '
                       'acércalas para que se encimen.',
                       'Haz la nieve: un cono blanco más pequeño, elevado hasta la punta de la montaña más alta.',
                       'Agrega detalles: un río (caja azul delgada), árboles (conos verdes) o rocas.'],
                tip='Si una figura queda «enterrada» o flotando, revisa su elevación con el cono negro.',
                logro=['Tu cordillera tiene suelo, 3 montañas, nieve y detalles, y nada flota por error.'],
                entrega='sube una captura de tu cordillera vista en 3D.'), xp=90, monedas=25),
            mision('El volcán con cráter', 'evidencia', leccion(
                intro='Los volcanes tienen un cráter en la cima. Para hacer un hoyo en Tinkercad se usa un «hueco».',
                saber=['Cualquier figura puede volverse hueco: selecciónala y en el panel Forma elige «Hueco» (se ve '
                       'transparente con rayas).',
                       'Al agrupar (Ctrl + G) una figura sólida con un hueco, el hueco «se come» esa parte.',
                       'Para desagrupar: Ctrl + Shift + G.'],
                pasos=['En tu cordillera agrega un cono de 60 × 60 × 50 mm, color café oscuro: será el volcán.',
                       'Agrega otro cono pequeño (20 × 20 × 20 mm), conviértelo en Hueco y voltéalo de cabeza (rótalo 180°).',
                       'Elévalo y colócalo en la punta del volcán para que se meta en la cima.',
                       'Selecciona los dos (Shift + clic) y agrúpalos con Ctrl + G. ¡Ya tienes cráter!',
                       'Agrega lava: figuras rojas o naranjas que bajen por un lado del volcán.'],
                logro=['Tu volcán tiene un cráter hundido en la cima.'],
                entrega='sube una captura donde se vea el cráter desde arriba.'), xp=90, monedas=25),
            mision('Choque de placas en 3D', 'evidencia', leccion(
                intro='Demuestra en 3D cómo se forman las montañas: dos placas que chocan y levantan la roca.',
                pasos=['Diseño nuevo: Placas_TuNombre. Haz dos cajas de 80 × 60 × 10 mm de colores diferentes: son las placas.',
                       'Acércalas hasta que se toquen en el centro.',
                       'En la orilla donde chocan, construye montañas que se levanten (conos o cuñas rotadas), como si la '
                       'roca se doblara hacia arriba.',
                       'Agrega flechas que muestren hacia dónde empuja cada placa.',
                       'Ponles nombre con la figura Texto: «Placa de Nazca» y «Placa Sudamericana».'],
                logro=['Tu modelo muestra dos placas, sus flechas, las montañas en el choque y los nombres.'],
                entrega='sube una captura de tu modelo de placas.'), xp=90, monedas=25),
        ]},
        {'nombre': '¡Caso resuelto! La cueva del titán', 'cofre': 50, 'misiones': [
            mision('Desafío relámpago Tinkercad', 'presencial', leccion(
                intro='Descubre cuánto aprendiste: tu profe proyecta un modelo misterioso y tienes 10 minutos para '
                      'construirlo.',
                pasos=['Observa el modelo: ¿qué figuras ves? ¿Cuáles están rotadas o elevadas?',
                       'Anota en tu cuaderno las figuras que necesitas.',
                       'Constrúyelo en Tinkercad en 10 minutos.',
                       'Compara con el modelo original: ¿qué te salió igual? ¿Qué cambiarías?'],
                logro=['Usaste mover, rotar y elevar para copiar el modelo.']), xp=60, monedas=20),
            mision('Galería de cordilleras', 'presencial', leccion(
                intro='Los científicos comparten sus hallazgos. Presenta tu cordillera y explica cómo se forman las montañas.',
                pasos=['Deja tu diseño abierto en la vista 3D.',
                       'Cuando lleguen tus compañeros, explícales en 1 minuto qué construiste, qué herramientas usaste y '
                       'cómo se forman las montañas de verdad.',
                       'Visita 3 diseños y dile a cada autor qué te gustó.'],
                logro=['Explicas con tus palabras cómo se forman las montañas usando tu modelo.']), xp=60, monedas=20),
            jefe('Jefe: El Titán de Piedra',
                 'Un titán de piedra despertó en el valle. Solo los exploradores que saben cómo se forman las montañas '
                 'y dominan el taller 3D pueden calmarlo.', [
                     ('¿Qué forma las cordilleras como los Andes?', 'El choque de placas tectónicas durante millones de años',
                      ['Un terremoto de un solo día', 'La lluvia', 'Los ríos']),
                     ('¿Qué sale de un volcán cuando hace erupción?', 'Lava, ceniza y gases',
                      ['Agua de mar', 'Nieve', 'Arena de playa']),
                     ('¿Cuál es la montaña más alta de México?', 'El Pico de Orizaba (Citlaltépetl)',
                      ['El Popocatépetl', 'El monte Everest', 'El Cerro de la Silla']),
                     ('En Tinkercad, ¿qué herramienta usas para poner la nieve encima de la montaña?', 'Elevar',
                      ['Borrar', 'Imprimir', 'Hueco']),
                     ('Para hacer el cráter del volcán usaste…', 'Un cono hueco agrupado con el volcán',
                      ['Una esfera roja', 'El cubo de vista', 'La regla']),
                     ('¿Qué hace agrupar (Ctrl + G)?', 'Une figuras en una sola y aplica los huecos',
                      ['Borra todo', 'Cambia la vista', 'Duplica las figuras']),
                     ('Las flechas curvas de una figura sirven para…', 'Rotarla', ['Elevarla', 'Pintarla', 'Guardarla']),
                     ('¿Qué cambio de la Tierra es rápido?', 'Una erupción volcánica',
                      ['La formación de una cordillera', 'El movimiento de las placas', 'Un río que excava un cañón']),
                 ]),
        ]},
    ],
}
