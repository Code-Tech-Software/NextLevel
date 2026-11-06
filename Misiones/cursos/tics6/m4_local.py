"""Mundo 4 · A la vuelta de la esquina: el ocio y el bienestar, encuestas en línea, entrevistas, análisis de datos en
hoja de cálculo, soporte técnico básico, algoritmos y una guía turística local en el procesador de textos."""
from .base import clasifica, jefe, leccion, mision

JUEGOS = {
    'clasifica_guia': clasifica('¿En qué sección de la guía va?', '🗺️', 'Una buena guía turística ordena su '
                                'información. ¿Dónde pondrías cada dato?', [
        ('Lugares', '📍', ['Parque con canchas de básquet y skatepark', 'Biblioteca pública con zona de cómics',
                           'Mercado con antojitos tradicionales', 'Museo de la ciudad', 'Mirador del cerro']),
        ('Actividades', '🎟️', ['Clases de baile los sábados a las 10:00', 'Concierto al aire libre el domingo',
                               'Torneo de ajedrez en la biblioteca', 'Paseo en bici el primer domingo del mes',
                               'Taller gratuito de dibujo']),
        ('Datos prácticos', 'ℹ️', ['Horario: martes a domingo de 10:00 a 18:00', 'Entrada: 30 pesos; niños gratis',
                                   'Cómo llegar: ruta 5, bajarse en el mercado',
                                   'Lleva agua y protector solar', 'Hay estacionamiento para bicis']),
    ], rondas=12),
    'clasifica_encuesta': clasifica('¿Buena pregunta o hay que arreglarla?', '📝', 'Una encuesta solo sirve si sus '
                                    'preguntas son claras y no influyen en la respuesta.', [
        ('Buena pregunta', '✅', ['¿Cuántos días a la semana sales a jugar o pasear?',
                                  '¿Qué lugar de la colonia visitas más?', 'Del 1 al 5, ¿qué tanto te gusta tu parque?',
                                  '¿Qué actividad te gustaría que hubiera cerca?',
                                  '¿Con quién sueles salir los fines de semana?']),
        ('Hay que arreglarla', '🛠️', ['¿Verdad que el parque está horrible?', '¿Cuál es tu dirección completa?',
                                      '¿Te gusta el deporte y la música y leer?',
                                      '¿No crees que los videojuegos son malos?', '¿Qué opinas de todo?']),
    ], rondas=10),
    'clasifica_soporte': clasifica('Soporte técnico: ¿qué reviso?', '🛠️', 'Antes de decir «no sirve», un técnico '
                                   'revisa en orden. ¿Por dónde empiezas?', [
        ('La conexión', '📶', ['No carga ninguna página', 'Dice «Sin internet» en la esquina',
                               'El mouse de cable no se mueve', 'La impresora no aparece en la lista',
                               'Los audífonos no suenan nada']),
        ('La configuración', '⚙️', ['El video se ve, pero no se oye', 'Todo lo que escribo sale en MAYÚSCULAS',
                                    'La pantalla se ve muy oscura', 'El teclado escribe símbolos raros',
                                    'La página se ve gigante (mucho zoom)']),
        ('Cerrar o reiniciar', '🔄', ['Word se quedó congelado', 'La página no responde a ningún clic',
                                      'La computadora está lentísima con 20 pestañas',
                                      'El juego se trabó en una pantalla', 'Una ventana no se cierra']),
    ], rondas=12),
}

MUNDO = {
    'nombre': 'Modo Local', 'tema': 'ciudad',
    'descripcion': 'A la vuelta de la esquina. Juan pensaba que su barrio era aburrido… hasta que buscó bien. '
                   'Investiga tu comunidad con encuestas y entrevistas, analiza los datos en una hoja de cálculo, '
                   'resuelve fallas técnicas y crea una guía turística local en el procesador de textos. Pregunta guía: '
                   '¿cómo dar a conocer lugares y actividades de esparcimiento cerca de tu casa?',
    'niveles': [
        {'nombre': 'Tu barrio en modo desconocido', 'cofre': 25, 'misiones': [
            mision('El barrio «aburrido» de Juan', 'texto', leccion(
                intro='La familia de Juan vendrá de visita y su mamá le pide organizar un itinerario. Él piensa que su '
                      'barrio es aburrido, pero al buscar con su hermano descubre una escuela de baile, conciertos al '
                      'aire libre y restaurantes que no conocía. Entonces se pregunta: ¿qué tan bien conozco mi entorno?',
                pasos=['Escribe 5 lugares para pasar el rato a menos de 15 minutos de tu casa.',
                       '¿Cuántos has visitado en el último mes?',
                       'En tu tiempo libre, ¿cuántas horas al día pasas frente a una pantalla?',
                       'Si tuvieras visitas, ¿a dónde las llevarías? ¿Por qué?'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('Ocio con estrategia', 'cuestionario', leccion(
                intro='El tiempo libre también se administra. No se trata de no usar pantallas, sino de equilibrar.',
                saber=['Ocio o esparcimiento: lo que haces en tu tiempo libre para descansar, divertirte o convivir.',
                       'La Organización Mundial de la Salud recomienda que niñas, niños y adolescentes hagan al menos '
                       '60 minutos diarios de actividad física.',
                       'Ocio activo: deporte, baile, paseos, juegos al aire libre. Ocio tranquilo: leer, dibujar, ver una '
                       'película. Los dos son valiosos; el problema es cuando todo el tiempo libre es pantalla.',
                       'Gestionar el tiempo: decidir a qué le dedicas tu tiempo en lugar de que una app lo decida por '
                       'ti.']), xp=60, preguntas=[
                ('¿Qué es el ocio o esparcimiento?', 'Lo que haces en tu tiempo libre para descansar o divertirte',
                 ['Las tareas de la escuela', 'El tiempo que duermes', 'El trabajo de los adultos']),
                ('¿Cuánta actividad física diaria recomienda la OMS para niñas, niños y adolescentes?',
                 'Al menos 60 minutos', ['5 minutos', '10 horas', 'Ninguna']),
                ('¿Cuál de estos es ocio activo?', 'Jugar básquet en el parque',
                 ['Ver videos acostado', 'Dormir la siesta', 'Hacer la tarea']),
                ('¿Cuándo se vuelve un problema el tiempo frente a pantallas?',
                 'Cuando ocupa casi todo tu tiempo libre', ['Nunca', 'Cuando ves una película',
                                                            'Cuando haces una tarea en la computadora']),
                ('¿Qué significa gestionar tu tiempo de ocio?', 'Decidir tú a qué le dedicas tu tiempo libre',
                 ['Dejar que una app decida por ti', 'No tener tiempo libre', 'Hacer todo al mismo tiempo']),
            ]),
        ]},
        {'nombre': 'Investiga como reportero', 'cofre': 30, 'misiones': [
            mision('Anatomía de una guía turística', 'cuestionario', leccion(
                intro='Antes de hacer tu guía, analiza cómo están hechas las de verdad. Tu profe proyecta un ejemplo.',
                saber=['Guías impresas: folleto, tríptico, revista o libro. Guías digitales: sitio web, mapa '
                       'interactivo, app o video.',
                       'Guías por tema: de comida, de cultura, de aventura, familiar…',
                       'Partes típicas: portada, índice, mapa, fichas de lugares (nombre, dirección, horario, costo, '
                       'cómo llegar, foto y recomendación), consejos y datos de contacto.',
                       'Lo más importante: que la información sea correcta y esté actualizada.']), xp=60, preguntas=[
                ('¿Cuál es una guía turística digital?', 'Un mapa interactivo en internet',
                 ['Un tríptico impreso', 'Un libro de la biblioteca', 'Un cartel en la pared']),
                ('¿Qué datos lleva la ficha de un lugar?', 'Nombre, dirección, horario, costo y cómo llegar',
                 ['Solo una foto', 'El nombre de tu mejor amigo', 'Tu dirección']),
                ('¿Qué es lo más importante de una guía turística?', 'Que su información sea correcta y actual',
                 ['Que tenga muchos colores', 'Que sea muy larga', 'Que tenga letras grandes']),
                ('Una guía solo de restaurantes y antojitos es una guía…', 'Gastronómica',
                 ['De aventura', 'Deportiva', 'De museos']),
                ('¿Para qué sirve el índice en una guía?', 'Para encontrar rápido cada sección',
                 ['Para decorar', 'Para poner el precio', 'Para que pese más']),
            ]),
            mision('¿En qué sección de la guía va?', 'juego', leccion(
                intro='Ordena la información como editor de guías: lugares, actividades o datos prácticos.'),
                juego='clasifica_guia'),
            mision('Diseña tu encuesta', 'evidencia', leccion(
                intro='Para saber qué lugares recomendar, pregunta a la gente. Vas a crear una encuesta en línea.',
                saber=['Google Forms o Microsoft Forms crean encuestas gratis y juntan las respuestas en una tabla.',
                       'Tipos de pregunta: opción múltiple (una respuesta), casillas (varias), escala (del 1 al 5) y '
                       'respuesta corta.',
                       'Una buena pregunta pregunta una sola cosa, es clara y no empuja hacia una respuesta.',
                       'Privacidad: no pidas nombres completos, direcciones ni teléfonos. Las encuestas son anónimas.'],
                pasos=['Crea un formulario nuevo: «¿Qué hacer cerca de casa?».',
                       'Escribe una descripción corta: quién eres y para qué usarás las respuestas.',
                       'Agrega de 6 a 8 preguntas; usa al menos 3 tipos distintos.',
                       'Incluye una pregunta de escala del 1 al 5 y una de opción múltiple sobre el lugar favorito.',
                       'Prueba tu encuesta en «Vista previa» y corrige lo que no se entienda.',
                       'Comparte el enlace con tu profe para que lo revise antes de enviarlo.'],
                logro=['Tu encuesta tiene de 6 a 8 preguntas claras, de 3 tipos distintos, y no pide datos personales.'],
                entrega='sube una captura de tu formulario en vista previa.'), xp=100, monedas=30),
            mision('¿Buena pregunta o hay que arreglarla?', 'juego', leccion(
                intro='Revisa como experto en encuestas: ¿la pregunta sirve o hay que arreglarla?',
                tip='Desconfía de las preguntas que empiezan con «¿verdad que…?» o «¿no crees que…?».'),
                juego='clasifica_encuesta'),
        ]},
        {'nombre': 'Datos y soporte técnico', 'cofre': 30, 'misiones': [
            mision('Entrevista a un experto local', 'texto', leccion(
                intro='Las encuestas dan números; las entrevistas dan historias. Entrevista a alguien que conozca bien '
                      'tu colonia: un comerciante, un abuelo, alguien que dé clases o cuide un parque.',
                pasos=['Escribe 5 preguntas abiertas (que no se respondan con sí o no). Ejemplo: «¿Qué lugar de la '
                       'colonia ha cambiado más y cómo?».',
                       'Pide permiso antes de grabar o tomar fotos.',
                       'Durante la entrevista escucha y anota las ideas clave, no cada palabra.',
                       'Al final agradece y pregunta cómo quiere aparecer en tu guía (o si prefiere no aparecer).',
                       'Escribe aquí las 5 preguntas, las respuestas más importantes y un dato que no sabías.'],
                logro=['Tus preguntas son abiertas y tu resumen tiene al menos un dato que solo una persona experta '
                       'podía darte.'],
                entrega='escribe tus preguntas y las respuestas aquí abajo.'), xp=70),
            mision('Soporte técnico nivel 1', 'cuestionario', leccion(
                intro='A la mitad de un proyecto, la computadora falla. Un técnico no entra en pánico: sigue un método.',
                saber=['1) Describe el problema: ¿qué hacías?, ¿qué esperabas?, ¿qué pasó?',
                       '2) Revisa lo básico: cables, encendido, wifi, volumen, batería, Bloq Mayús.',
                       '3) Cierra y vuelve a abrir el programa o la página (F5 recarga).',
                       '4) Si un programa se congela: Ctrl + Shift + Esc abre el Administrador de tareas → selecciona el '
                       'programa → Finalizar tarea.',
                       '5) Reinicia la computadora. 6) Si sigue igual, pide ayuda y cuenta qué ya intentaste.',
                       'Para no perder trabajo: guarda seguido o usa documentos en la nube que se guardan solos.']),
                xp=60, preguntas=[
                ('¿Cuál es el primer paso para resolver una falla?', 'Describir bien qué pasó',
                 ['Golpear la computadora', 'Apagarla del cable', 'Comprar otra']),
                ('El video se ve, pero no se oye. ¿Qué revisas primero?', 'El volumen y que no esté silenciado',
                 ['El wifi', 'La impresora', 'El mouse']),
                ('Todo lo que escribes sale en MAYÚSCULAS. ¿Qué pasa?', 'Está activado Bloq Mayús',
                 ['Tiene virus', 'Se descompuso el teclado', 'Se acabó la batería']),
                ('Word se congeló. ¿Qué atajo abre el Administrador de tareas?', 'Ctrl + Shift + Esc',
                 ['Ctrl + C', 'Alt + Tab', 'Ctrl + P']),
                ('¿Qué tecla recarga una página que no carga bien?', 'F5', ['F1', 'Esc', 'Supr']),
                ('Pides ayuda a tu profe. ¿Qué le dices?', 'Qué estabas haciendo, qué pasó y qué ya intentaste',
                 ['Solo «no sirve»', 'Nada, que lo adivine', 'Que la computadora está mal hecha']),
            ]),
            mision('Soporte técnico: ¿qué reviso?', 'juego', leccion(
                intro='Clasifica cada falla según lo primero que revisarías: la conexión, la configuración o cerrar y '
                      'reiniciar.',
                tip='Primero lo más sencillo: un cable flojo o el volumen en cero resuelven muchas «fallas».'),
                juego='clasifica_soporte'),
            mision('Analiza tu encuesta', 'evidencia', leccion(
                intro='Ya tienes respuestas. Ahora conviértelas en información: cuenta, grafica y saca conclusiones.',
                saber=['Las respuestas se pasan a una hoja de cálculo (Google Forms: Respuestas → Vincular a Hojas de '
                       'cálculo; Microsoft Forms: Abrir en Excel).',
                       '=CONTAR.SI(B2:B40,"Parque") cuenta cuántas veces aparece «Parque» en esa columna. Si marca '
                       'error, cambia la coma por punto y coma.',
                       'Gráfica de barras: compara cantidades. Gráfica de pastel: muestra partes de un total.',
                       'Una conclusión se apoya en los datos: «12 de 20 personas prefieren el parque, por eso será la '
                       'primera ficha de la guía».'],
                pasos=['Abre las respuestas en la hoja de cálculo.',
                       'Elige la pregunta del lugar favorito y haz una tabla: Lugar | Votos.',
                       'Cuenta los votos con CONTAR.SI.',
                       'Selecciona la tabla → Insertar → Gráfico. Ponle título.',
                       'Escribe 2 conclusiones apoyadas en los números.'],
                logro=['Tu gráfica tiene título y tus conclusiones mencionan los números de la encuesta.'],
                entrega='sube una captura de tu tabla con la gráfica y escribe tus conclusiones en el comentario.'),
                xp=100, monedas=30),
        ]},
        {'nombre': 'Arma tu guía', 'cofre': 35, 'misiones': [
            mision('Verifica los lugares en línea', 'texto', leccion(
                intro='Tu guía no puede mandar a nadie a un lugar cerrado. Verifica cada dato en internet.',
                saber=['En Google Maps o en el mapa de tu navegador puedes buscar un lugar y ver su dirección, horario, '
                       'fotos y cómo llegar.',
                       'Las reseñas son opiniones: léelas varias y no te quedes con una sola.',
                       'Los horarios cambian: si puedes, confírmalo en la página oficial o en un letrero del lugar.',
                       'Privacidad: recomienda solo lugares públicos. Nunca pongas la dirección de tu casa ni la de '
                       'tus compañeros.'],
                pasos=['Elige 4 lugares para tu guía (usa los resultados de tu encuesta).',
                       'Para cada uno anota: nombre, dirección, horario, costo y cómo llegar.',
                       'Copia el enlace del lugar en el mapa: lo usarás en tu guía.',
                       'Marca con ⚠️ los datos que no pudiste confirmar.'],
                logro=['Tus 4 lugares tienen datos completos y su enlace del mapa.'],
                entrega='escribe la información de tus 4 lugares aquí abajo.'), xp=70),
            mision('El itinerario es un algoritmo', 'evidencia', leccion(
                intro='Un algoritmo es una lista de pasos ordenados para lograr algo. Un buen itinerario también lo es… '
                      'y tiene planes B.',
                saber=['Un algoritmo tiene inicio, pasos en orden y un final.',
                       'Las decisiones (condicionales) dicen qué hacer en cada caso: «Si llueve, entonces vamos al museo; '
                       'si no, al parque».',
                       'En un diagrama de flujo, el óvalo es inicio o fin, el rectángulo es una acción y el rombo es '
                       'una decisión.'],
                pasos=['Diseña el itinerario de un sábado para la familia de Juan con 4 lugares de tu guía.',
                       'Escríbelo como algoritmo numerado, con horarios.',
                       'Agrega al menos 2 decisiones: si llueve, si se acaba el presupuesto, si alguien se cansa…',
                       'Dibuja el diagrama de flujo con las formas correctas (en papel o con Insertar → Formas).'],
                logro=['Tu itinerario tiene inicio, pasos en orden, 2 decisiones con su plan B y un final.'],
                entrega='sube una foto o captura de tu diagrama de flujo.'), xp=100, monedas=30),
            mision('Portada y columnas', 'evidencia', leccion(
                intro='Empieza a armar tu guía en el procesador de textos con diseño de revista.',
                saber=['Columnas: el texto se acomoda como en los periódicos. Word: Disposición → Columnas. Google '
                       'Docs: Formato → Columnas.',
                       'Cuadro de texto: un recuadro que puedes mover libremente; ideal para «datos curiosos». Word: '
                       'Insertar → Cuadro de texto. Google Docs: Insertar → Dibujo → Cuadro de texto.',
                       'Salto de página: empieza una página nueva sin dar muchos Enter (Ctrl + Enter).'],
                pasos=['Abre un documento nuevo: Guia_Local_TuNombre.',
                       'Portada: nombre llamativo de tu guía, una imagen y tu nombre. Luego un salto de página.',
                       'Escribe una introducción: para quién es la guía y por qué vale la pena tu colonia.',
                       'Pon el texto de la introducción en 2 columnas.',
                       'Agrega un cuadro de texto con un dato curioso de la entrevista.'],
                logro=['Tu guía tiene portada, salto de página, introducción en 2 columnas y un cuadro de texto.'],
                entrega='sube una captura de la portada y de la primera página.'), xp=100, monedas=30),
            mision('Fichas con tabla, enlace y QR', 'evidencia', leccion(
                intro='Cada lugar tendrá su ficha con todos los datos y un código QR para abrirlo en el mapa desde el '
                      'celular.',
                saber=['Tabla: Insertar → Tabla. Úsala para que todas las fichas se vean ordenadas.',
                       'Vínculo (hipervínculo): selecciona el texto → Insertar → Vínculo y pega la dirección.',
                       'Código QR: en Chrome o Edge, abre el lugar en el mapa → clic derecho en la página → «Crear código '
                       'QR para esta página» → Descargar. Luego insértalo como imagen.',
                       'Usa los resultados de la encuesta: ordena las fichas del lugar más votado al menos votado.'],
                pasos=['Para cada lugar, inserta una tabla de 2 columnas: Dato | Información (dirección, horario, costo, '
                       'cómo llegar y recomendación).',
                       'Agrega una foto del lugar con su fuente.',
                       'Convierte la palabra «Ver en el mapa» en un vínculo.',
                       'Crea el QR del lugar e insértalo junto a la tabla.',
                       'Agrega encabezado con el nombre de la guía y número de página.'],
                logro=['Tienes 4 fichas con tabla, foto, vínculo y código QR que sí abre el lugar.'],
                entrega='sube el PDF de tu guía o capturas de 2 fichas.'), xp=110, monedas=30),
        ]},
        {'nombre': 'Publica tu guía', 'cofre': 40, 'misiones': [
            mision('Intercambio de guías', 'presencial', leccion(
                intro='Las guías se hicieron para usarse. Intercambia la tuya y pruébala como turista.',
                dinamica=['Cada quien recibe la guía de otro compañero (el profe la asigna).',
                          '8 minutos de lectura en silencio y 2 minutos para escribir la retroalimentación.'],
                pasos=['Escanea uno de los códigos QR con un celular (el del profe): ¿abre el lugar correcto?',
                       '¿Te dan ganas de visitar algún lugar? ¿Cuál y por qué?',
                       'Escribe 2 estrellas (cosas que funcionan) y 1 deseo (algo que mejorarías).',
                       'Devuelve la guía con tu retroalimentación.'],
                logro=['Probaste un código QR y tu retroalimentación es concreta.']), xp=50),
            jefe('Jefe: El Scroll Infinito', leccion(
                intro='El Scroll Infinito quiere que pases todo tu tiempo libre deslizando la pantalla. Derrótalo con lo '
                      'que aprendiste de tu comunidad, tus datos y tus herramientas.'), [
                ('¿Cuál de estas es una buena pregunta para una encuesta?',
                 '¿Qué lugar de la colonia visitas más?', ['¿Verdad que el parque está horrible?',
                                                           '¿Cuál es tu dirección completa?', '¿Qué opinas de todo?']),
                ('¿Qué hace =CONTAR.SI(B2:B40,"Parque")?', 'Cuenta cuántas veces aparece «Parque»',
                 ['Suma los números de la columna', 'Borra la palabra Parque', 'Hace una gráfica']),
                ('¿Qué gráfica usas para comparar cuántos votos tuvo cada lugar?', 'De barras',
                 ['De líneas de temperatura', 'Ninguna', 'Un mapa del clima']),
                ('Una conclusión apoyada en datos es…', '«12 de 20 personas prefieren el parque»',
                 ['«El parque es el mejor porque sí»', '«A mí me gusta el parque»', '«Nadie sabe»']),
                ('En un diagrama de flujo, ¿qué forma representa una decisión?', 'El rombo',
                 ['El óvalo', 'El rectángulo', 'La flecha']),
                ('Un programa se congeló. ¿Qué atajo abre el Administrador de tareas?', 'Ctrl + Shift + Esc',
                 ['Ctrl + Z', 'Ctrl + V', 'F7']),
                ('¿Qué dato NO debe aparecer en tu guía?', 'La dirección de tu casa',
                 ['El horario del museo', 'El costo de la entrada', 'Cómo llegar al parque']),
                ('¿Cómo pones el texto en 2 columnas en Word?', 'Disposición → Columnas',
                 ['Insertar → Tabla', 'Archivo → Imprimir', 'Revisar → Ortografía']),
            ]),
        ]},
    ],
}
