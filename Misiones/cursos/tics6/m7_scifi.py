"""Mundo 7 · ES-DAT307 Día a día en otros planetas: la rotación de los planetas, cómo funciona la inteligencia
artificial (entrenando un modelo propio), prompts para editar texto y crear imágenes con responsabilidad, y un periódico
mural de ciencia ficción con su convocatoria."""
from .base import TEACHABLE, clasifica, jefe, leccion, mision

EDAD_IA = ('La mayoría de las herramientas de IA generativa piden tener 13 años o más. Por eso en clase se usan con tu '
           'profe: la opera en el proyector o con la cuenta escolar que autorice.')

JUEGOS = {
    'clasifica_usa_ia': clasifica('¿Usa IA o no?', '🤖', 'La IA está en más lugares de los que crees… y en otros no. '
                                  '¿Este aparato o app usa inteligencia artificial?', [
        ('Usa IA', '🤖', ['Las recomendaciones de videos en YouTube', 'El filtro que te pone orejas de perro en una foto',
                          'Un traductor que traduce la foto de un letrero', 'Un chatbot que responde preguntas',
                          'El celular que se desbloquea con tu cara', 'El mapa que busca la ruta con menos tráfico',
                          'Un asistente de voz que entiende lo que dices']),
        ('No usa IA', '🔌', ['Una calculadora sumando 2 + 2', 'Un foco que prende con el apagador', 'Un reloj de pared',
                             'Un control remoto que cambia de canal', 'Un timbre que suena al presionarlo',
                             'Una impresora sacando una copia', 'Un ventilador con tres velocidades']),
    ], rondas=12),
    'clasifica_mitos_ia': clasifica('¿Mito o realidad de la IA?', '🧠', 'Separa lo que de verdad hace la IA de lo que '
                                    'la gente cree.', [
        ('Realidad', '✅', ['La IA aprende de muchísimos ejemplos (datos)', 'La IA puede inventar datos que suenan reales',
                            'Si los datos tienen prejuicios, la IA también', 'Hay que verificar lo que dice la IA',
                            'La IA no siente emociones, aunque escriba como si sí',
                            'Muchas apps de IA piden tener 13 años o más']),
        ('Mito', '❌', ['La IA siempre dice la verdad', 'La IA piensa y siente como una persona',
                        'Si la IA lo escribió, no hay que revisarlo', 'La IA sabe todo lo que pasa en el mundo',
                        'Que la IA haga toda tu tarea es aprender', 'Lo que le escribes a una IA siempre es privado']),
    ], rondas=12),
    'clasifica_prompts': clasifica('¿Prompt claro o flojo?', '💬', 'Un prompt claro dice qué quieres, para qué y cómo. '
                                   '¿Cuál funcionaría mejor?', [
        ('Prompt claro', '🎯', ['Corrige la ortografía de mi cuento sin cambiar la historia',
                                'Dame 3 títulos para un cuento de ciencia ficción en Venus',
                                'Explica la rotación de Júpiter para alumnos de 6.º en 5 líneas',
                                'Sugiere un final sorpresa, pero no reescribas mi cuento',
                                'Haz una lista de 5 datos de Marte y di de dónde salen',
                                'Ilustración estilo cómic de una base en Marte al atardecer']),
        ('Prompt flojo', '😴', ['hazlo mejor', 'escribe algo', 'dibuja un planeta', 'corrige', 'dame ideas',
                                'haz mi tarea de ciencias']),
    ], rondas=12),
}

MUNDO = {
    'nombre': 'Redacción Sci-Fi', 'tema': 'espacio',
    'descripcion': 'ES-DAT307 · Día a día en otros planetas. Hace 400 años, Kepler imaginó cómo serían el día y la '
                   'noche en la Luna. Escribe ciencia ficción con datos reales de los planetas, entiende cómo funciona '
                   'la inteligencia artificial, úsala con buenos prompts para editar e ilustrar, y publica un periódico '
                   'mural con una convocatoria. Pregunta guía: ¿cómo difundir nuestras historias y hacer que nuestro '
                   'grupo crezca?',
    'niveles': [
        {'nombre': 'Hora local: otros planetas', 'cofre': 25, 'misiones': [
            mision('Kepler soñó con la Luna', 'texto', leccion(
                intro='La ciencia ficción mezcla imaginación y ciencia. Johannes Kepler, el astrónomo que descubrió cómo '
                      'se mueven los planetas, escribió «El sueño»: la historia de un viaje a la Luna donde describe '
                      'cómo se vivirían allá el día y la noche. Muchos lo consideran uno de los primeros relatos de '
                      'ciencia ficción.',
                pasos=['¿Qué historia, película o serie de ciencia ficción conoces? ¿Qué tiene de ciencia y qué de '
                       'imaginación?',
                       'Imagina que vives en un planeta donde el día dura 243 días. ¿Cómo sería tu rutina?',
                       '¿Te gustaría que tus historias las leyera más gente? ¿Cómo las darías a conocer?'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('¿Cuánto dura un día?', 'cuestionario', leccion(
                intro='Un día es lo que tarda un planeta en girar sobre sí mismo (su rotación). Y cada planeta gira a su '
                      'propio ritmo.',
                saber=['Mercurio: 59 días terrestres. Venus: 243 días… y gira al revés. Su día dura más que su año (225 '
                       'días).',
                       'Tierra: 24 horas. Marte: 24 horas y 37 minutos, casi igual que nosotros.',
                       'Júpiter: casi 10 horas, el día más corto del sistema solar. Saturno: unas 10 horas y media.',
                       'Urano: unas 17 horas, y gira acostado. Neptuno: unas 16 horas.',
                       'La Luna tarda 27 días en girar y siempre nos muestra la misma cara. En el relato de Kepler, la '
                       'noche lunar dura unas dos semanas.']), xp=60, preguntas=[
                ('¿Qué es un día en un planeta?', 'Lo que tarda en girar sobre sí mismo',
                 ['Lo que tarda en darle la vuelta al Sol', 'Lo que dura la luz del Sol', 'Siempre 24 horas']),
                ('¿Qué planeta tiene el día más corto?', 'Júpiter', ['Venus', 'Mercurio', 'La Tierra']),
                ('¿Qué tiene de raro Venus?', 'Su día dura más que su año', ['No gira', 'Es de hielo',
                                                                             'Tiene dos soles']),
                ('¿Qué planeta tiene un día casi igual al nuestro?', 'Marte', ['Júpiter', 'Venus', 'Neptuno']),
                ('¿Por qué siempre vemos la misma cara de la Luna?',
                 'Porque gira sobre sí misma en el mismo tiempo que tarda en darle la vuelta a la Tierra',
                 ['Porque no gira', 'Porque está pegada a la Tierra', 'Porque la otra cara no existe']),
                ('¿Cuánto dura un día en Mercurio?', '59 días terrestres', ['10 horas', '24 horas', '1 hora']),
            ]),
        ]},
        {'nombre': 'IA sin humo', 'cofre': 30, 'misiones': [
            mision('La IA explicada sin humo', 'cuestionario', leccion(
                intro='Todo mundo habla de inteligencia artificial, pero pocos saben explicarla. Al terminar esta misión, '
                      'tú sí.',
                saber=['La IA son programas que aprenden patrones a partir de muchísimos ejemplos (datos) y con eso '
                       'reconocen, predicen o crean cosas nuevas.',
                       'Entrenar: le das miles de ejemplos (fotos de gatos con la etiqueta «gato») hasta que encuentra '
                       'el patrón y puede reconocer gatos que nunca vio.',
                       'IA generativa: crea texto, imágenes o música a partir de una instrucción llamada prompt. Un '
                       'chatbot escribe eligiendo, palabra por palabra, la que es más probable que siga.',
                       'Límites: puede inventar datos que suenan reales («alucinar»), copia los prejuicios de sus datos '
                       'y no siente ni entiende como una persona.',
                       EDAD_IA]), xp=60, preguntas=[
                ('¿Cómo aprende una IA?', 'Encontrando patrones en muchísimos ejemplos',
                 ['Leyendo la mente de las personas', 'Sola, sin ningún dato', 'Copiando un solo libro']),
                ('¿Qué es un prompt?', 'La instrucción que le das a una IA', ['Un virus', 'Un tipo de robot',
                                                                              'Una pieza de la computadora']),
                ('¿Qué significa que una IA «alucina»?', 'Que inventa datos que suenan reales',
                 ['Que se apaga', 'Que se pone feliz', 'Que se conecta a internet']),
                ('¿Cómo escribe un chatbot?', 'Eligiendo la palabra más probable que sigue',
                 ['Pensando como una persona', 'Copiando siempre la misma respuesta', 'Preguntándole a un humano']),
                ('Si los datos de entrenamiento tienen prejuicios, la IA…', 'También puede tenerlos',
                 ['Los corrige sola', 'No funciona', 'Se vuelve más justa']),
                ('¿Qué debes hacer con lo que responde una IA?', 'Verificarlo en otras fuentes',
                 ['Creerlo todo', 'Compartirlo sin leer', 'Borrarlo siempre']),
            ]),
            mision('¿Usa IA o no?', 'juego', leccion(
                intro='Detecta dónde hay inteligencia artificial en tu vida diaria.',
                tip='Si el aparato aprende de datos o reconoce algo (caras, voces, gustos), probablemente usa IA.'),
                juego='clasifica_usa_ia'),
            mision('Entrena tu propia IA', 'evidencia', leccion(
                intro='La mejor forma de entender la IA es entrenar una. Con Teachable Machine de Google vas a enseñarle '
                      'a la computadora a reconocer gestos con la cámara, en el navegador y sin crear cuenta.',
                saber=['Clase: cada cosa que la IA debe reconocer (por ejemplo, «Pulgar arriba» y «Pulgar abajo»).',
                       'Muestras: las fotos de ejemplo de cada clase. Más muestras y más variadas = mejor IA.',
                       'Entrenar: la IA busca el patrón de cada clase. Vista previa: la pruebas con ejemplos nuevos y te '
                       'dice qué tan segura está (en porcentaje).'],
                dinamica=['En duplas, en la computadora de uno: uno hace los gestos frente a la cámara y el otro maneja '
                          'el mouse. Después cambian a la computadora del otro.',
                          '15 minutos para entrenar y probar. Al final, ronda de «¿quién engaña a su IA?».'],
                pasos=['Abre el enlace → Proyecto de imagen → Modelo de imagen estándar.',
                       'Renombra Class 1 como «Pulgar arriba» y Class 2 como «Pulgar abajo».',
                       'En cada clase usa la Webcam y mantén presionado el botón para grabar unas 50 muestras.',
                       'Clic en «Entrenar modelo» y espera sin cambiar de pestaña.',
                       'Prueba en la vista previa: ¿acierta? Ahora prueba con otra mano o más lejos.',
                       'Experimento: agrega una tercera clase con solo 5 muestras. ¿Qué pasa?'],
                ojo=['Tus imágenes se quedan en el navegador. No guardes el proyecto en la nube y ciérralo al terminar.'],
                logro=['Tu IA reconoce tus dos gestos y explicas por qué falla la clase con pocas muestras.'],
                entrega='sube una captura de la vista previa y explica en el comentario qué descubriste.'),
                xp=100, monedas=30, link=TEACHABLE),
            mision('¿Mito o realidad de la IA?', 'juego', leccion(
                intro='Después de entrenar tu propia IA ya sabes cómo funciona. Separa los mitos de la realidad.'),
                juego='clasifica_mitos_ia'),
        ]},
        {'nombre': 'Escribe ciencia ficción', 'cofre': 30, 'misiones': [
            mision('Receta de una historia sci-fi', 'texto', leccion(
                intro='La buena ciencia ficción toma un dato real y se pregunta «¿y si…?». Planea tu historia antes de '
                      'escribirla.',
                saber=['Ingrediente científico: un dato real (por ejemplo, el día de Venus dura 243 días terrestres).',
                       'Personaje: alguien con un objetivo claro.',
                       'Conflicto: el problema que el dato científico le provoca al personaje.',
                       'Giro: algo inesperado. Final: cómo se resuelve (o no).'],
                pasos=['Elige un planeta y su dato de rotación.',
                       'Escribe tu «¿y si…?». Ejemplo: «¿Y si tu cumpleaños en Venus llegara antes que el amanecer?».',
                       'Describe a tu personaje en 2 renglones.',
                       'Escribe el conflicto, el giro y el final en una línea cada uno.'],
                logro=['Tu plan tiene dato real, personaje, conflicto, giro y final.'],
                entrega='escribe tu plan aquí abajo.'), xp=60),
            mision('Primer borrador', 'evidencia', leccion(
                intro='Escribe tu historia TÚ. La IA vendrá después como editora, no como autora.',
                dinamica=['20 minutos de escritura en silencio, con audífonos y música suave si el profe lo permite.',
                          'El que termina antes no molesta: revisa su ortografía o agrega un detalle.'],
                pasos=['Abre un documento: SciFi_TuNombre.',
                       'Escribe un título y tu historia de 250 a 400 palabras (la barra de estado cuenta las palabras).',
                       'Usa el dato científico en la historia, no como un dato suelto.',
                       'Guárdala: esta versión es tu prueba de que la escribiste tú.'],
                logro=['Tu historia tiene de 250 a 400 palabras y el dato científico es parte de la trama.'],
                entrega='sube una captura de tu borrador donde se vea el conteo de palabras.'), xp=100, monedas=30),
        ]},
        {'nombre': 'Editor con IA', 'cofre': 35, 'misiones': [
            mision('Anatomía de un prompt', 'cuestionario', leccion(
                intro='La calidad de lo que responde una IA depende de la calidad de lo que le pides.',
                saber=['Fórmula de un prompt claro: Rol + Tarea + Contexto + Formato + Límites.',
                       'Rol: «Actúa como editor de una revista juvenil». Tarea: «Corrige la ortografía de mi cuento».',
                       'Contexto: «Es para un periódico mural de 6.º». Formato: «Marca los cambios en negritas y dame 3 '
                       'sugerencias en lista». Límites: «No cambies la historia ni los nombres».',
                       'Prompt de imagen: sujeto + acción + lugar + estilo + detalles (luz, colores, encuadre).',
                       'Nunca pongas en un prompt datos personales: tu nombre completo, dirección, escuela o fotos de '
                       'personas.']), xp=60, preguntas=[
                ('¿Cuál es la fórmula de un prompt claro?', 'Rol + Tarea + Contexto + Formato + Límites',
                 ['Escribir lo más corto posible', 'Solo poner una palabra', 'Escribir todo en mayúsculas']),
                ('«No cambies la historia ni los nombres» es la parte de…', 'Límites', ['Rol', 'Formato', 'Contexto']),
                ('«Actúa como editor de una revista juvenil» es la parte de…', 'Rol', ['Tarea', 'Límites', 'Formato']),
                ('¿Cuál es el mejor prompt de imagen?',
                 'Una astronauta mirando dos atardeceres en Marte, estilo cómic, colores naranjas',
                 ['Marte', 'algo bonito', 'una imagen']),
                ('¿Qué NO debes poner en un prompt?', 'Tu nombre completo y tu dirección',
                 ['El tema de tu cuento', 'El estilo que quieres', 'El número de palabras']),
                ('La IA te dio una respuesta que no te gustó. ¿Qué haces?', 'Mejoro el prompt y lo vuelvo a intentar',
                 ['Me rindo', 'Copio la respuesta como sea', 'Escribo el mismo prompt en mayúsculas']),
            ]),
            mision('El prompt humano', 'presencial', leccion(
                intro='Sin computadora: tu compañero será la IA y hará EXACTAMENTE lo que diga tu prompt, ni más ni menos.',
                dinamica=['En duplas: uno escribe prompts, el otro es la «IA» y los sigue al pie de la letra.',
                          'Rondas de 3 minutos; luego cambian de papel. Todo se dibuja en una hoja, en silencio.'],
                pasos=['Ronda 1: el autor escribe un prompt flojo para un dibujo: «Dibuja un planeta». La IA dibuja.',
                       'Ronda 2: el autor usa la fórmula: «Dibuja un planeta con anillos y tres lunas, visto desde la '
                       'superficie de una de sus lunas, con una base espacial pequeña abajo a la izquierda».',
                       'Comparen los dos dibujos con lo que el autor imaginaba.',
                       'Cambien de papel y repitan con un prompt para corregir un texto corto.'],
                logro=['Explicas con tus palabras por qué el segundo prompt dio un resultado más cercano a lo que querías.']),
                xp=50),
            mision('¿Prompt claro o flojo?', 'juego', leccion(
                intro='Decide qué prompt daría una buena respuesta y cuál uno que no sirve.'), juego='clasifica_prompts'),
            mision('Edita con IA, decide tú', 'evidencia', leccion(
                intro='Ahora la IA será tu editora. Pero el autor eres tú: tú decides qué cambios aceptas.',
                saber=[EDAD_IA,
                       'La IA sugiere; el autor decide. Si aceptas todo sin leer, la historia deja de ser tuya.',
                       'Al final se dice en qué ayudó la IA. Ejemplo: «Corrección de ortografía con apoyo de IA».'],
                pasos=['Escribe tu prompt con la fórmula, pidiendo corregir ortografía y puntuación y dar 3 sugerencias '
                       'SIN reescribir tu historia.',
                       'Tu profe lo usa con tu texto (o lo hacen con la herramienta escolar que autorice).',
                       'Lee cada cambio y anota cuáles aceptas y cuáles no, y por qué.',
                       'Pasa a tu documento solo los cambios que aceptaste.',
                       'Agrega al final de tu historia: «Edición con apoyo de IA (herramienta, fecha)».'],
                logro=['Tienes tu prompt, la lista de cambios aceptados y rechazados con su razón y tu versión final.'],
                entrega='sube una captura de tu versión final y escribe en el comentario tu prompt y 2 decisiones.'),
                xp=100, monedas=30),
            mision('Ilustra con IA', 'evidencia', leccion(
                intro='Una historia del periódico mural necesita una imagen que atrape. La crearás con IA y con un buen '
                      'prompt de imagen.',
                saber=[EDAD_IA,
                       'Prompt de imagen: sujeto + acción + lugar + estilo + detalles. Ejemplo: «Un chico astronauta '
                       'desayunando bajo un cielo con dos soles en una base de Marte, estilo novela gráfica, colores '
                       'naranjas, vista panorámica».',
                       'Para mejorar una imagen cambia una sola cosa a la vez (el estilo, la luz, el encuadre).',
                       'Toda imagen hecha con IA se etiqueta: «Imagen generada con IA (herramienta)».'],
                pasos=['Escribe 2 versiones de tu prompt de imagen para la escena más importante de tu historia.',
                       'Tu profe genera las imágenes (o lo hacen con la herramienta escolar que autorice).',
                       'Elige la que mejor cuente tu historia y explica por qué.',
                       'Insértala en tu documento con el pie «Imagen generada con IA».'],
                ojo=['No se generan imágenes de personas reales ni de compañeros.',
                     'Si una imagen sale rara o incómoda, se descarta y se avisa al profe.'],
                logro=['Tu imagen ilustra una escena de tu historia y está etiquetada como generada con IA.'],
                entrega='sube una captura de tu historia con la imagen y escribe tu mejor prompt en el comentario.'),
                xp=100, monedas=30),
        ]},
        {'nombre': 'Periódico mural', 'cofre': 40, 'misiones': [
            mision('Diseña la convocatoria', 'evidencia', leccion(
                intro='Para que el grupo de escritores crezca, invita a otros a participar con una convocatoria.',
                saber=['Partes de una convocatoria: título llamativo, quién convoca, a quién va dirigida, qué hay que '
                       'hacer, bases (requisitos, extensión, tema), fecha límite, cómo y dónde entregar, premio o '
                       'reconocimiento y contacto.',
                       'Diseño: título grande (WordArt), información en secciones, poco texto y una imagen.'],
                pasos=['Abre un documento: Convocatoria_TuNombre.',
                       'Título llamativo con WordArt (Insertar → WordArt) o un título grande.',
                       'Escribe cada parte de la convocatoria con su subtítulo en negritas.',
                       'Agrega una imagen (tuya o generada con IA y etiquetada).',
                       'Revisa la ortografía y pídele a un compañero que la lea: ¿entiende qué tiene que hacer?'],
                logro=['Tu convocatoria tiene todas sus partes y alguien que la lee sabe exactamente cómo participar.'],
                entrega='sube tu convocatoria en PDF o una captura.'), xp=100, monedas=30),
            mision('Arma el periódico mural', 'presencial', leccion(
                intro='Es hora de publicar: el grupo arma su periódico mural de ciencia ficción. Cada dupla se encarga '
                      'de una parte.',
                roles=['Dupla editora: decide el nombre del periódico y el orden de las secciones.',
                       'Dupla de la cabecera: diseña el nombre, el número y la fecha.',
                       'Duplas de historias: cada una prepara sus dos historias con su imagen.',
                       'Dupla de datos: arma la sección «Hora local en otros planetas».',
                       'Dupla de la IA: escribe la sección «Cómo usamos la IA».',
                       'Dupla correctora: revisa la ortografía de todo antes de pegarlo.'],
                dinamica=['Cada dupla prepara su parte en su lugar. Al mural pasa una sola dupla a la vez, cuando el profe '
                          'la llama.',
                          'La dupla que termina ayuda a la que vaya más atrasada.',
                          '30 minutos de armado; la última parte de la clase es la inauguración.'],
                pasos=['Impriman las historias con sus imágenes, los datos de los planetas y la convocatoria.',
                       'Cabecera: nombre del periódico, número y fecha.',
                       'Secciones: historias, «Hora local en otros planetas» (datos), «Cómo usamos la IA» y la '
                       'convocatoria en un lugar visible.',
                       'Peguen el periódico en un pasillo de la escuela.',
                       'Inauguración: 3 voluntarios leen el inicio de su historia en voz alta.'],
                logro=['El periódico tiene cabecera, historias ilustradas, datos, una sección sobre la IA y la '
                       'convocatoria.']), xp=60),
            jefe('Jefe: La IA Alucinada', leccion(
                intro='La IA Alucinada inventa datos con toda seguridad. Solo la vence quien sabe cómo funciona la IA, '
                      'cómo pedirle las cosas y cómo verificar.'), [
                ('¿Qué planeta tiene el día más largo que su año?', 'Venus', ['Júpiter', 'Marte', 'La Tierra']),
                ('¿Cuánto dura un día en Júpiter?', 'Casi 10 horas', ['24 horas', '243 días', '59 días']),
                ('¿Cómo aprende una IA?', 'Encontrando patrones en muchísimos ejemplos',
                 ['Pensando como una persona', 'Sin usar datos', 'Leyendo la mente']),
                ('En Teachable Machine, ¿qué pasa si una clase tiene muy pocas muestras?', 'La IA se equivoca más',
                 ['La IA funciona mejor', 'No pasa nada', 'La computadora se apaga']),
                ('La IA te dice un dato que suena raro. ¿Qué haces?', 'Lo verifico en fuentes confiables',
                 ['Lo publico tal cual', 'Lo creo porque lo dijo la IA', 'Lo comparto en redes']),
                ('¿Cuál es un prompt claro?', 'Corrige la ortografía de mi cuento sin cambiar la historia',
                 ['hazlo mejor', 'corrige', 'escribe algo']),
                ('¿Qué debe llevar una imagen hecha con IA en tu periódico?', 'Una etiqueta que diga que la generó una IA',
                 ['Tu firma como si la hubieras dibujado', 'Nada', 'El nombre de un compañero']),
                ('¿Qué parte de una convocatoria dice hasta cuándo se puede participar?', 'La fecha límite',
                 ['El título', 'El premio', 'La imagen']),
            ]),
        ]},
    ],
}
