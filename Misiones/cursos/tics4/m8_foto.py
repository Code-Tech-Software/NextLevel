"""Mundo 8 · ES-SEA208 Foto familiar: hechos, opiniones e hipótesis, la entrevista y una presentación digital con
texto, formato, imágenes y una revelación animada."""
from Misiones.minijuegos import TEMAS_CLASIFICA

from .base import clasifica, jefe, leccion, mision

JUEGOS = {
    'clasifica_hechos': clasifica('¿Hecho, opinión o hipótesis?', '🔎', 'Un buen detective separa lo que sabe de lo que supone.', [
        ('Hecho', '📌', ['La foto es en blanco y negro', 'En la foto hay cuatro niños', 'El abuelo nació en 1958',
                        'La foto se tomó en un parque', 'En la foto el abuelo lleva un bigote postizo']),
        ('Opinión', '💭', ['Es la foto más bonita del álbum', 'Mi abuelo se ve muy gracioso',
                          'Antes los juegos eran más divertidos', 'Ese parque es el mejor del mundo',
                          'La ropa de antes era más elegante']),
        ('Hipótesis', '🧩', ['Creo que estaban jugando a los detectives', 'Tal vez la foto es de un cumpleaños',
                            'Quizá el niño de la gorra es su hermano', 'Puede ser que la foto sea de los años setenta',
                            'A lo mejor el bigote era de un disfraz']),
    ], rondas=15),
    'clasifica_preguntas': clasifica('¿Pregunta abierta o cerrada?', '🎤', '¿Esta pregunta abre una historia o pide un dato corto?', [
        ('Abierta', '📖', ['¿Qué juegos jugabas de niño?', '¿Cómo era tu escuela?', '¿Por qué llevabas un bigote postizo?',
                          '¿Qué recuerdas de ese día?', '¿Cómo conociste a tus amigos?', '¿Qué travesura nunca olvidas?']),
        ('Cerrada', '🔒', ['¿Te gustaba la escuela?', '¿Tenías bicicleta?', '¿Cuántos hermanos tienes?',
                          '¿Naciste en esta ciudad?', '¿La foto es de 1970?', '¿Jugabas futbol?']),
    ]),
    'clasifica_privacidad': clasifica('¿Público o privado?', '🔒', '¿Qué puedes compartir y qué es privado?',
                                      TEMAS_CLASIFICA['privacidad'][2]),
}

MUNDO = {
    'nombre': 'Bahía Foto Familiar', 'tema': 'oceano',
    'descripcion': 'ES-SEA208 · Foto familiar. En el desván del abuelo apareció una foto con un misterio: él de niño, '
                   'con amigos y un enorme bigote postizo. Entrevista a tu familia, separa hechos de opiniones y cuenta '
                   'la historia en una presentación digital. Pregunta guía: ¿cuántas historias puedes encontrar en una '
                   'fotografía?',
    'niveles': [
        {'nombre': 'La caja del desván', 'cofre': 25, 'misiones': [
            mision('El misterio de la foto', 'texto', leccion(
                intro='«Buscando un viejo balón en el desván de mi abuelo, encontré una caja de madera llena de fotos '
                      'antiguas: bodas, cumpleaños, viajes… Una me llamó la atención: mi abuelo de niño, jugando con '
                      'unos amigos en un parque, ¡con un bigote postizo enorme! ¿Qué estaban jugando? ¿Quiénes eran esos '
                      'amigos? Cuando le pregunté, sus ojos se iluminaron y empezó a contarme historias.»\n\n'
                      'Pregunta del caso: ¿cuántas historias puedes encontrar en una fotografía?',
                pasos=['Observa la foto antigua que proyecta tu profe (o una de tu familia).',
                       'Escribe 3 cosas que VES (por ejemplo: «hay dos niños», «es en blanco y negro»).',
                       'Escribe 3 preguntas que te hace la foto.',
                       'Escribe una posible historia: ¿qué crees que pasaba ese día?'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('Detectives de la información', 'cuestionario', leccion(
                intro='Para resolver el misterio de una foto necesitas distinguir tipos de información.',
                saber=['Hecho: algo que pasó y se puede comprobar. «La foto es de 1975.»',
                       'Dato: una información concreta, muchas veces un número o un nombre. «Mi abuelo tenía 8 años.»',
                       'Opinión: lo que alguien piensa o siente; no se puede comprobar. «Es la foto más bonita.»',
                       'Hipótesis: una posible explicación que todavía hay que comprobar. «Creo que jugaban a los piratas.»',
                       'Evidencia: lo que demuestra algo (una foto, un documento, lo que cuenta un testigo).',
                       'Investigación: el trabajo de buscar evidencias para comprobar una hipótesis.']), xp=60, preguntas=[
                ('«La foto se tomó en 1975.» Esto es…', 'Un hecho', ['Una opinión', 'Una hipótesis', 'Un chiste']),
                ('«Mi abuelo se ve muy gracioso.» Esto es…', 'Una opinión', ['Un hecho', 'Un dato', 'Una evidencia']),
                ('«Creo que estaban jugando a los detectives.» Esto es…', 'Una hipótesis',
                 ['Un hecho comprobado', 'Una opinión segura', 'Una fecha']),
                ('¿Qué es una evidencia?', 'Algo que demuestra lo que dices, como un documento o una foto',
                 ['Lo que te imaginas', 'Un chisme', 'Un sueño']),
                ('¿Cómo compruebas una hipótesis sobre la foto?',
                 'Investigando: preguntando a quien estuvo ahí y buscando evidencias',
                 ['Inventando el final', 'Eligiendo la que más te guste', 'Borrando la foto']),
                ('«Mi abuelo tenía 8 años en la foto.» Esto es…', 'Un dato', ['Una opinión', 'Una hipótesis', 'Un invento']),
            ]),
            mision('¿Hecho, opinión o hipótesis?', 'juego', leccion(
                intro='Clasifica cada frase sobre la foto del abuelo.',
                tip='Si se puede comprobar, es hecho; si es un gusto, es opinión; si empieza con «creo», «tal vez» o '
                    '«quizá», es hipótesis.'), juego='clasifica_hechos'),
            mision('Leer fotos antiguas', 'presencial', leccion(
                intro='Las fotos guardan pistas. En equipos, leerán fotos antiguas como verdaderos detectives.',
                pasos=['Tu profe reparte o proyecta fotos antiguas (de su familia, de la ciudad o de internet).',
                       'Busquen pistas: ¿es a color o en blanco y negro? ¿Cómo son la ropa, los peinados, los coches y '
                       'los objetos?',
                       'Con esas pistas escriban una hipótesis de en qué época se tomó.',
                       'Separen en su cuaderno los hechos (lo que se ve) y las hipótesis (lo que suponen).',
                       'Compartan con el grupo: ¿qué pista fue la más útil?'],
                logro=['Su equipo separó hechos de hipótesis y justificó la época con pistas.']), xp=50),
        ]},
        {'nombre': 'La entrevista', 'cofre': 30, 'misiones': [
            mision('¿Qué es una entrevista?', 'cuestionario', leccion(
                intro='La mejor fuente sobre una foto familiar es quien estuvo ahí. Aprende a entrevistar.',
                saber=['Una entrevista es una conversación para obtener información: el entrevistador pregunta y el '
                       'entrevistado responde.',
                       'Preguntas abiertas: piden explicar o contar (¿Qué…?, ¿Cómo…?, ¿Por qué…?). Dan historias.',
                       'Preguntas cerradas: se responden con sí, no o un dato corto.',
                       'Antes: pedir permiso y preparar preguntas. Durante: escuchar con atención y tomar notas. '
                       'Después: agradecer.']), xp=60, preguntas=[
                ('En una entrevista, ¿quién hace las preguntas?', 'El entrevistador', ['El entrevistado', 'Nadie', 'El público']),
                ('¿Cuál es una pregunta abierta?', '¿Qué juegos jugabas cuando eras niño?',
                 ['¿Tenías bicicleta?', '¿Te gustaba la escuela?', '¿Naciste en esta ciudad?']),
                ('Las preguntas cerradas se responden con…', 'Sí, no o un dato corto',
                 ['Una historia larga', 'Un dibujo', 'Una canción']),
                ('¿Qué debes hacer ANTES de la entrevista?', 'Pedir permiso y preparar mis preguntas',
                 ['Inventar las respuestas', 'Publicarla en internet', 'Nada']),
                ('Mientras entrevistas a tu abuelo, lo mejor es…', 'Escuchar con atención y tomar notas',
                 ['Ver el celular', 'Interrumpirlo', 'Irte a jugar']),
            ]),
            mision('¿Pregunta abierta o cerrada?', 'juego', leccion(
                intro='Las preguntas abiertas sacan las mejores historias. Clasifica cada una.'), juego='clasifica_preguntas'),
            mision('Mi hipótesis y mis preguntas', 'texto', leccion(
                intro='Prepara tu investigación sobre una foto de tu familia.',
                pasos=['Elige una foto de tu familia (pide permiso para usarla). Si no tienes, usa una que te preste tu profe.',
                       'Descríbela en 2 renglones (sin datos privados como direcciones).',
                       'Escribe tu hipótesis: ¿qué historia crees que esconde?',
                       'Escribe 8 preguntas para entrevistar a un familiar: al menos 5 abiertas.'],
                entrega='escribe tu hipótesis y tus 8 preguntas aquí abajo.'), xp=70, monedas=20),
            mision('La entrevista en casa', 'evidencia', leccion(
                intro='Hora de investigar: entrevista a un familiar sobre la foto.',
                pasos=['Pide permiso y acuerden un momento tranquilo.',
                       'Muéstrale la foto y haz tus preguntas.',
                       'Toma notas (o, con permiso, graba el audio).',
                       'Pregunta si puedes usar la foto en una presentación del salón.',
                       'Agradece la entrevista.'],
                tip='Si una respuesta te da curiosidad, pregunta «¿y luego qué pasó?». ¡Ahí salen las mejores historias!',
                logro=['Tienes respuestas a tus 8 preguntas y permiso para usar la foto.'],
                entrega='sube una foto de tus notas (sin direcciones ni teléfonos).'), xp=90, monedas=25),
        ]},
        {'nombre': 'Trazo mis pistas: el guion', 'cofre': 30, 'misiones': [
            mision('Ordena lo que descubriste', 'texto', leccion(
                intro='Un detective resume lo importante y reconoce lo que todavía no sabe.',
                pasos=['Lee tus notas de la entrevista.',
                       'Escribe 4 HECHOS que descubriste (cosas que pasaron).',
                       'Escribe 2 OPINIONES de tu familiar (lo que piensa o siente).',
                       '¿Se comprobó tu hipótesis? Explica.',
                       'Escribe 1 cosa que todavía no sabes y que te gustaría investigar más.'],
                entrega='escribe tu resumen aquí abajo.'), xp=70, monedas=20),
            mision('Storyboard de la presentación', 'evidencia', leccion(
                intro='Un storyboard es el plan dibujado de tu presentación, cuadro por cuadro.',
                pasos=['Dobla una hoja en 6 cuadros.',
                       'Cuadro 1: Portada (un título misterioso y tu nombre).',
                       'Cuadro 2: ¿Quiénes salen en la foto? · Cuadro 3: ¿Dónde y cuándo?',
                       'Cuadro 4: La historia (lo que te contaron) · Cuadro 5: ¡El secreto revelado!',
                       'Cuadro 6: Cierre (qué aprendiste y qué falta investigar).',
                       'En cada cuadro dibuja dónde irá la imagen y escribe la idea principal.'],
                logro=['Tu storyboard tiene los 6 cuadros con su idea y su imagen.'],
                entrega='sube una foto de tu storyboard.'), xp=80, monedas=20),
        ]},
        {'nombre': 'DTectives en acción: estudio digital', 'cofre': 35, 'misiones': [
            mision('Digitaliza la foto', 'evidencia', leccion(
                intro='Para usar una foto de papel en la computadora hay que digitalizarla.',
                saber=['Digitalizar es convertir algo de papel en un archivo de computadora (con un escáner o con una cámara).',
                       'Para que salga bien: buena luz, sin reflejos, la cámara de frente y sin moverse.',
                       'Recortar quita las orillas que sobran; girar endereza la foto.',
                       'Un buen nombre de archivo dice qué es: Foto_Abuelo_1975.jpg, no IMG_4821.jpg.'],
                pasos=['Con permiso, toma una foto de la foto con la tableta o la cámara del salón, de frente y sin reflejos.',
                       'Pásala a la computadora (con cable o por la carpeta compartida que indique tu profe).',
                       'Ábrela con Fotos o Paint: recórtala y enderézala.',
                       'Guárdala en tu carpeta › Presentaciones con un nombre claro.'],
                logro=['La foto se ve derecha, sin orillas de más y con un nombre claro.'],
                entrega='sube una captura de tu carpeta donde se vea la foto con su nombre.'), xp=90, monedas=25),
            mision('¿Público o privado?', 'juego', leccion(
                intro='Las fotos y los datos de tu familia son valiosos. ¿Qué se puede compartir y qué es privado?',
                saber=['Antes de publicar una foto, pide permiso a las personas que salen en ella.',
                       'Nunca compartas direcciones, teléfonos ni contraseñas.']), juego='clasifica_privacidad'),
            mision('Estructura y textos', 'evidencia', leccion(
                intro='Construye el esqueleto de tu presentación siguiendo tu storyboard.',
                pasos=['Abre PowerPoint y guarda la presentación como FotoFamiliar_TuNombre en tu carpeta.',
                       'Crea 6 diapositivas como en tu storyboard (diseños Título, Título y contenido y Dos objetos).',
                       'Escribe los textos de cada diapositiva: cortos, con viñetas y con tus propias palabras.',
                       'Si necesitas texto en otro lugar, usa Insertar → Cuadro de texto.',
                       'Revisa la ortografía.'],
                logro=['Tus 6 diapositivas tienen título y texto, en el orden del storyboard.'],
                entrega='sube una captura del panel de miniaturas con tus 6 diapositivas.'), xp=90, monedas=25),
            mision('Formato que cuenta historias', 'evidencia', leccion(
                intro='El formato ayuda a contar la historia: que se vea como un álbum antiguo y que todo se lea bien.',
                saber=['Usa máximo 2 fuentes: una para títulos y otra para el texto.',
                       'WordArt hace títulos llamativos (Insertar → WordArt).',
                       'Los colores deben contrastar con el fondo y combinar entre sí.',
                       'Copiar formato (la brochita de la pestaña Inicio) pasa el formato de un texto a otro.'],
                pasos=['Elige un tema o un fondo que recuerde a las fotos antiguas (tonos sepia o café).',
                       'Cambia el título de la portada a WordArt.',
                       'Da el mismo formato a todos los títulos con la brochita «Copiar formato».',
                       'Resalta en negrita o con color las palabras clave de tu historia.',
                       'Revisa el contraste en modo presentación (F5).'],
                logro=['Todos los títulos tienen el mismo formato y todo se lee bien.'],
                entrega='sube una captura de tu portada y de otra diapositiva con formato.'), xp=90, monedas=25),
            mision('Imágenes con estilo', 'evidencia', leccion(
                intro='La foto familiar es la estrella. Dale un lugar especial.',
                saber=['Insertar → Imágenes para poner tu foto digitalizada.',
                       'Formato de imagen → Recortar quita lo que sobra; Estilos de imagen le pone marco o sombra.',
                       'Traer adelante / Enviar atrás decide qué imagen queda encima.'],
                pasos=['Inserta tu foto familiar en la diapositiva 2 y dale un estilo con marco.',
                       'Agrega imágenes que ayuden a contar la historia (el lugar, los juegos de antes…).',
                       'Recorta las que tengan orillas de más.',
                       'Acomoda las imágenes para que no tapen los textos.'],
                logro=['La foto familiar tiene marco y ninguna imagen tapa el texto.'],
                entrega='sube una captura de una diapositiva con tu foto y su estilo.'), xp=90, monedas=25),
            mision('La gran revelación', 'evidencia', leccion(
                intro='Toda historia de misterio tiene un momento de revelación. Haz que tu secreto aparezca con un clic.',
                saber=['Pestaña Animaciones: elige un efecto de entrada (Aparecer, Desvanecer o Zoom).',
                       '«Al hacer clic» hace que el elemento aparezca cuando tú quieras, no antes.'],
                pasos=['En la diapositiva 5 escribe una pregunta de suspenso, por ejemplo: ¿Por qué mi abuelo llevaba un '
                       'bigote postizo?',
                       'Debajo, en un cuadro de texto grande, escribe el secreto.',
                       'Dale al secreto la animación de entrada «Zoom» o «Desvanecer» al hacer clic.',
                       'Prueba con F5 que el secreto aparezca solo cuando das clic.'],
                logro=['La pregunta se ve primero y el secreto aparece hasta el clic.'],
                entrega='sube una captura de la diapositiva de la revelación con su animación.'), xp=90, monedas=25),
        ]},
        {'nombre': '¡Caso resuelto! El faro de los recuerdos', 'cofre': 50, 'misiones': [
            mision('Revelo mis hallazgos', 'presencial', leccion(
                intro='Presenta la historia de tu foto familiar y revela su secreto.',
                pasos=['Practica con tus notas del orador.',
                       'Presenta en 2 o 3 minutos: no leas, ¡cuenta la historia!',
                       'Haz una pausa antes de la revelación para crear suspenso.',
                       'Al final, el grupo puede hacerte 2 preguntas.'],
                logro=['Contaste la historia con hechos de tu entrevista y revelaste el secreto.']), xp=70, monedas=20),
            mision('Autoevaluación del detective', 'texto', leccion(
                intro='Un buen detective revisa su trabajo al cerrar el caso.',
                pasos=['¿Qué aprendiste de tu familia que no sabías?',
                       '¿En qué se parecía tu hipótesis a lo que descubriste? ¿En qué era diferente?',
                       '¿Qué herramienta de las presentaciones te gustó más usar y por qué?',
                       '¿Qué información te falta investigar todavía?',
                       'Califícate del 1 al 10 y explica por qué.'],
                entrega='escribe tu autoevaluación aquí abajo.'), xp=60),
            jefe('Jefe: El Monstruo del Álbum Perdido',
                 'El Monstruo del Álbum Perdido revolvió todas las fotos familiares. Ordénalas con lo que sabes de hechos, '
                 'entrevistas y presentaciones.', [
                     ('«En la foto hay cuatro niños.» Esto es…', 'Un hecho', ['Una opinión', 'Una hipótesis', 'Un invento']),
                     ('«Antes los juegos eran más divertidos.» Esto es…', 'Una opinión',
                      ['Un hecho', 'Un dato', 'Una evidencia']),
                     ('¿Cuál pregunta da una respuesta más larga en una entrevista?', '¿Cómo era tu escuela cuando eras niño?',
                      ['¿Tenías bicicleta?', '¿Te gustaba el futbol?', '¿Naciste aquí?']),
                     ('Digitalizar una foto es…', 'Convertirla en un archivo de computadora',
                      ['Romperla', 'Pintarla a mano', 'Guardarla en un cajón']),
                     ('¿Cuál es un buen nombre para el archivo de tu foto?', 'Foto_Abuelo_1975.jpg',
                      ['IMG_4821.jpg', 'asdf.jpg', 'nuevo.jpg']),
                     ('Antes de publicar una foto familiar en internet debes…', 'Pedir permiso a quienes salen en ella',
                      ['Publicarla sin preguntar', 'Escribir tu dirección', 'Etiquetar a desconocidos']),
                     ('Para que el secreto aparezca solo cuando des clic, usas…', 'Una animación de entrada «al hacer clic»',
                      ['Una transición en todas', 'Un tema nuevo', 'Un salto de página']),
                     ('¿Qué herramienta copia el formato de un título a otro?', 'Copiar formato (la brochita)',
                      ['Recortar', 'Borrar', 'Zoom']),
                 ]),
        ]},
    ],
}
