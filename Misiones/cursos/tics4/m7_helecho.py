"""Mundo 7 · ES-SEA208 Helecho bien hecho: el secreto de los helechos y sus tres claves para la vida diaria, en una
presentación digital clara, ordenada y llamativa (diseño, imágenes, gráfica, transiciones y notas)."""
from .base import clasifica, jefe, leccion, mision

JUEGOS = {
    'clasifica_semillas': clasifica('¿Con semilla o con esporas?', '🌿', 'Algunas plantas nacen de semillas y otras de esporas.', [
        ('Con semilla', '🌰', ['Frijol', 'Maíz', 'Girasol', 'Pino', 'Manzano', 'Aguacate', 'Rosal', 'Calabaza']),
        ('Con esporas', '🍃', ['Helecho', 'Musgo', 'Cola de caballo', 'Helecho arborescente', 'Hepática']),
    ]),
    'clasifica_diapositivas': clasifica('¿Buena o mala diapositiva?', '🖼️', '¿Esta idea ayuda o estorba en una presentación?', [
        ('Buena', '👍', ['Un título corto y claro', 'Máximo 6 renglones de texto', 'Letra grande que se lee desde atrás',
                        'Una imagen que explica la idea', 'Letras oscuras sobre fondo claro', 'Una sola idea por diapositiva',
                        'La misma transición suave en todas']),
        ('Mala', '👎', ['Un párrafo enorme copiado de internet', 'Letra amarilla sobre fondo blanco',
                       'Diez imágenes encimadas', 'Letra tamaño 10', 'Una animación diferente en cada palabra',
                       'Faltas de ortografía en el título', 'Un fondo con muchos dibujos detrás del texto']),
    ], rondas=14),
}

MUNDO = {
    'nombre': 'Isla del Helecho', 'tema': 'volcan',
    'descripcion': 'ES-SEA208 · Helecho bien hecho. Un ser vivo está en la Tierra desde antes que los dinosaurios: el '
                   'helecho. Descubre su secreto, practica sus tres claves en tu vida diaria y cuéntalo en una '
                   'presentación digital clara, ordenada y llamativa. Pregunta guía: ¿cómo lo ha logrado?',
    'niveles': [
        {'nombre': 'El secreto del helecho', 'cofre': 25, 'misiones': [
            mision('Un sobreviviente de millones de años', 'texto', leccion(
                intro='Hay un secreto escondido entre las plantas: un ser vivo que está en la Tierra desde hace más de '
                      '300 millones de años. Muchas especies desaparecieron, pero él sigue aquí, creciendo y '
                      'adaptándose. Es el helecho.\n\nPregunta del caso: ¿cómo lo ha logrado?',
                pasos=['Observa un helecho de verdad (o una foto): ¿cómo son sus hojas?, ¿dónde vive?, ¿tiene flores?',
                       'Escribe 2 hipótesis: ¿qué le ha ayudado a sobrevivir tanto tiempo?',
                       'Piensa en ti: ¿qué te ayuda a seguir adelante cuando algo es difícil?'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('¿Cómo nace un helecho?', 'cuestionario', leccion(
                intro='Los helechos no tienen flores ni semillas… entonces, ¿cómo nacen? Repasa y contesta.',
                saber=['Los helechos se reproducen por esporas, no por semillas.',
                       'Las esporas están en puntitos cafés debajo de sus hojas. El viento las lleva lejos.',
                       'Viven mejor en lugares húmedos y con sombra.',
                       'Sus hojas nuevas salen enrolladas como un caracol y se desenrollan poco a poco.',
                       'Tienen tallos bajo tierra (rizomas) que vuelven a brotar aunque se queme la parte de arriba.',
                       'Ya existían antes que los dinosaurios.']), xp=60, preguntas=[
                ('Los helechos se reproducen por medio de…', 'Esporas', ['Semillas', 'Huevos', 'Flores']),
                ('¿Dónde están las esporas de un helecho?', 'En puntitos cafés debajo de sus hojas',
                 ['En sus flores', 'En sus frutos', 'En la maceta']),
                ('Los helechos viven mejor en lugares…', 'Húmedos y con sombra',
                 ['Muy secos, como el desierto', 'Dentro del congelador', 'Sin agua nunca']),
                ('¿Cuál de estas plantas NO tiene flores ni semillas?', 'El musgo', ['El girasol', 'El frijol', 'El maíz']),
                ('Las hojas nuevas de los helechos salen enrolladas como…', 'Un caracol o una espiral',
                 ['Un cubo', 'Un triángulo', 'Una estrella']),
                ('Los helechos son plantas muy antiguas: ya existían…', 'Desde antes que los dinosaurios',
                 ['Apenas desde el año pasado', 'Desde que hay computadoras', 'Nunca existieron']),
            ]),
            mision('¿Con semilla o con esporas?', 'juego', leccion(
                intro='Algunas plantas nacen de semillas y otras de esporas. ¡Clasifícalas!'), juego='clasifica_semillas'),
            mision('Cazador de esporas', 'evidencia', leccion(
                intro='Busca la evidencia del secreto del helecho con tus propios ojos.',
                material=['Una hoja de helecho', 'Una lupa'],
                pasos=['Voltea la hoja del helecho y obsérvala con la lupa.',
                       '¿Ves unos puntitos cafés? ¡Ahí guarda sus esporas!',
                       'Dibuja lo que observas o toma una foto de cerca.',
                       'Escribe junto a tu dibujo para qué sirven las esporas.'],
                entrega='sube tu dibujo o tu foto.'), xp=80, monedas=20),
        ]},
        {'nombre': 'El arte de presentar', 'cofre': 30, 'misiones': [
            mision('¿Qué hace buena una presentación?', 'cuestionario', leccion(
                intro='Antes de hacer tu presentación, aprende el arte de que sea clara, ordenada y llamativa.',
                saber=['Una presentación digital ayuda a explicar un tema frente a otros. Cada página se llama diapositiva.',
                       'Ordenada: portada → desarrollo → cierre.',
                       'Clara: una idea por diapositiva, títulos cortos y máximo 6 renglones.',
                       'Legible: letra de 24 puntos o más y buen contraste (letra oscura en fondo claro o al revés).',
                       'Llamativa: imágenes que explican, colores que combinan y transiciones con medida.',
                       'Honesta: escribe de dónde tomaste la información y las imágenes.']), xp=60, preguntas=[
                ('¿Cómo se llama cada página de una presentación?', 'Diapositiva', ['Celda', 'Carpeta', 'Pestaña']),
                ('¿Cuál es el orden de una presentación?', 'Portada → desarrollo → cierre',
                 ['Cierre → portada → desarrollo', 'Solo desarrollo', 'Desarrollo → portada']),
                ('¿Cuánto texto debe tener una diapositiva?', 'Pocas ideas, máximo unos 6 renglones',
                 ['Un párrafo enorme', 'Todo el libro', 'Nunca nada']),
                ('¿Qué combinación se lee mejor?', 'Letra azul oscuro sobre fondo blanco',
                 ['Letra amarilla sobre fondo blanco', 'Letra verde sobre fondo verde', 'Letra gris clara sobre fondo blanco']),
                ('¿Para qué sirven las imágenes en una diapositiva?', 'Para explicar mejor la idea',
                 ['Para llenar todos los huecos', 'Para tapar el texto', 'Para que nadie lea']),
                ('Si usas información de internet, al final debes…', 'Escribir de dónde la tomaste',
                 ['Decir que la inventaste', 'Borrarla', 'No decir nada']),
            ]),
            mision('¿Buena o mala diapositiva?', 'juego', leccion(
                intro='¿Cada idea ayuda o estorba en una presentación? Clasifícalas como un experto.'),
                juego='clasifica_diapositivas'),
            mision('Conoce tu programa de presentaciones', 'presencial', leccion(
                intro='PowerPoint, Google Slides o LibreOffice Impress sirven para hacer presentaciones. Conoce sus partes.',
                saber=['Panel de miniaturas (izquierda): todas tus diapositivas en orden; ahí las mueves o las borras.',
                       'Nueva diapositiva (pestaña Inicio) y Diseño de diapositiva (Título, Título y contenido, Dos objetos…).',
                       'Pestaña Diseño: temas de colores. Insertar: imágenes, formas y gráficos. Transiciones y '
                       'Animaciones: efectos.',
                       'F5 inicia la presentación en pantalla completa; Esc la termina.'],
                pasos=['Abre PowerPoint → Presentación en blanco.',
                       'Agrega 3 diapositivas nuevas con diseños diferentes.',
                       'Cambia el orden arrastrándolas en el panel de miniaturas y borra una.',
                       'Prueba 3 temas de la pestaña Diseño.',
                       'Presiona F5 para verla en pantalla completa y Esc para salir.'],
                logro=['Agregas, mueves y borras diapositivas, cambias el diseño e inicias la presentación.']), xp=50),
        ]},
        {'nombre': 'Las claves del helecho', 'cofre': 35, 'misiones': [
            mision('Clave 1: adaptarse', 'texto', leccion(
                intro='Primera clave del helecho: se adapta. Vive en selvas, bosques, entre rocas y hasta en paredes '
                      'húmedas: busca la sombra y la humedad que necesita.',
                pasos=['Piensa en un cambio que hayas vivido (escuela nueva, grupo nuevo, una mudanza, un hermanito…).',
                       'Escribe: ¿qué cambió?, ¿qué hiciste para adaptarte? y ¿qué aprendiste?',
                       'Esta semana practica la clave 1: cuando algo cambie, busca lo que SÍ puedes hacer. Escribe un ejemplo.'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('La portada que atrapa', 'evidencia', leccion(
                intro='Empieza tu presentación «El secreto del helecho» con una portada que dé ganas de verla.',
                pasos=['Abre PowerPoint → Presentación en blanco. Guárdala como Helecho_TuNombre en tu carpeta › '
                       'Presentaciones.',
                       'Elige un tema en la pestaña Diseño (los verdes combinan con el helecho).',
                       'Título: El secreto del helecho. Subtítulo: tu nombre y grupo.',
                       'Inserta una imagen de un helecho y acomódala sin tapar el título.',
                       'Revisa que el título se lea desde el fondo del salón.'],
                logro=['Tu portada tiene título, subtítulo, imagen y buen contraste.'],
                entrega='sube una captura de tu portada.'), xp=80, monedas=20),
            mision('Clave 2: resistir y volver a brotar', 'presencial', leccion(
                intro='Segunda clave: el helecho resiste. Aunque un incendio queme sus hojas, sus tallos bajo tierra '
                      'vuelven a brotar. Y sus esporas esperan el momento justo para crecer.',
                pasos=['Reto en equipos: construyan la torre más alta con vasos o tarjetas en 5 minutos.',
                       'A la mitad, su profe dirá «¡Terremoto!» y tendrán que tirarla.',
                       'Vuelvan a construir: ¿la segunda torre salió mejor? ¿Qué aprendieron de la primera?',
                       'Comenten: ¿cuándo te ha tocado volver a empezar algo?'],
                logro=['Explicas cómo se parece tu equipo a un helecho que vuelve a brotar.']), xp=50),
            mision('Diapositivas de las tres claves', 'evidencia', leccion(
                intro='Desarrollo: una diapositiva para cada clave del helecho.',
                saber=['Usa el diseño «Título y contenido» o «Dos objetos» (texto de un lado, imagen del otro).',
                       'Escribe ideas cortas con viñetas, no párrafos.'],
                pasos=['Agrega 3 diapositivas: Clave 1: Adaptarse · Clave 2: Resistir y volver a brotar · Clave 3: '
                       'Crecer poco a poco.',
                       'En cada una escribe 3 viñetas: qué hace el helecho y cómo lo aplicas tú en tu vida diaria.',
                       'Inserta en cada diapositiva una imagen que explique la idea.',
                       'Revisa que la letra sea de 24 o más y que nada se encime.'],
                logro=['Cada clave tiene título, 3 viñetas cortas y una imagen.'],
                entrega='sube una captura del panel de miniaturas con tus diapositivas.'), xp=100, monedas=30),
            mision('Gráfica: ¿quién llegó primero?', 'evidencia', leccion(
                intro='Los datos convencen. Agrega una gráfica que compare cuánto tiempo llevan en la Tierra los '
                      'helechos y otros seres vivos.',
                saber=['Insertar → Gráfico → Columna. Se abre una pequeña hoja de cálculo: ahí escribes tus datos en celdas.',
                       'Cada fila es una barra: en la columna A va el nombre y en la B el número.',
                       'La gráfica cambia sola cuando cambias los datos.'],
                pasos=['Agrega una diapositiva con el título ¿Quién llegó primero?',
                       'Inserta un gráfico de columnas.',
                       'En la hoja de datos escribe (en millones de años): Helechos 360 · Dinosaurios 230 · Plantas con '
                       'flores 130 · Seres humanos 0.3. Borra las filas y columnas que sobren.',
                       'Cierra la hoja de datos y cambia el título del gráfico a Millones de años en la Tierra.',
                       'Escribe abajo una frase con tu conclusión.'],
                logro=['Tu gráfica tiene 4 barras con sus nombres, un título y una conclusión.'],
                entrega='sube una captura de la diapositiva con tu gráfica.'), xp=90, monedas=25),
        ]},
        {'nombre': 'Clave 3 y el gran cierre', 'cofre': 50, 'misiones': [
            mision('Clave 3: crecer poco a poco', 'texto', leccion(
                intro='Tercera clave: las hojas nuevas del helecho salen enrolladas y se abren poco a poco. Las metas '
                      'grandes también se logran paso a paso.',
                pasos=['Escribe una meta que quieras lograr este mes (leer un libro, mejorar en algo, ahorrar…).',
                       'Divídela en 3 pasos pequeños, como una hoja que se desenrolla.',
                       'Escribe qué harás esta semana para dar el primer paso.'],
                entrega='escribe tu plan aquí abajo.'), xp=60),
            mision('Transiciones y animaciones con medida', 'evidencia', leccion(
                intro='Los efectos hacen llamativa una presentación… si no se exageran.',
                saber=['Transición: el efecto al pasar de una diapositiva a otra (pestaña Transiciones).',
                       'Animación: el efecto de un elemento dentro de la diapositiva, como una imagen que aparece '
                       '(pestaña Animaciones).',
                       'Regla de oro: una sola transición para toda la presentación y pocas animaciones. ¡El efecto no '
                       'debe ser más importante que la idea!'],
                pasos=['Elige una transición suave (Desvanecer o Empujar) y da clic en «Aplicar a todas».',
                       'En la diapositiva de la gráfica, anima la gráfica con «Aparecer».',
                       'Presiona F5 y revisa que todo se vea bien.',
                       'Si algún efecto distrae, quítalo.'],
                logro=['Todas las diapositivas tienen la misma transición y hay máximo 2 animaciones.'],
                entrega='sube una captura de la pestaña Transiciones con tu efecto elegido.'), xp=80, monedas=20),
            mision('El cierre y las fuentes', 'evidencia', leccion(
                intro='Toda buena presentación termina con una conclusión clara y dice de dónde salió la información.',
                saber='Las notas del orador (debajo de la diapositiva) solo las ves tú: te ayudan a no leer la diapositiva.',
                pasos=['Agrega una diapositiva de conclusión: El secreto del helecho es… (en una o dos frases tuyas).',
                       'Agrega una diapositiva de Fuentes con las páginas de donde tomaste información e imágenes.',
                       'Agrega una diapositiva final de agradecimiento.',
                       'En las Notas de cada diapositiva escribe lo que dirás al presentar.',
                       'Guarda.'],
                logro=['Tu presentación tiene portada, desarrollo, gráfica, conclusión, fuentes y notas.'],
                entrega='sube una captura de tu diapositiva de conclusión.'), xp=80, monedas=20),
            mision('¡A presentar!', 'presencial', leccion(
                intro='Hora de compartir el secreto del helecho con el grupo.',
                saber=['Habla fuerte y despacio, mira al público y no leas todo: tus diapositivas son solo la guía.',
                       'Practica antes con tus notas del orador.',
                       'Inicia con F5 y avanza con las flechas o con clic.'],
                pasos=['Practica tu presentación 2 veces con un compañero.',
                       'Presenta al grupo en 2 minutos.',
                       'Escucha a tus compañeros y dale a cada uno una estrella: algo que hizo muy bien.'],
                logro=['Presentaste sin leer todo y explicaste las 3 claves del helecho.']), xp=70, monedas=20),
            jefe('Jefe: El Helecho Gigante Prehistórico',
                 'Un helecho gigante, más viejo que los dinosaurios, despertó en el cráter. Véncelo con lo que sabes de '
                 'su secreto y del arte de presentar.', [
                     ('Los helechos se reproducen por…', 'Esporas', ['Semillas', 'Huevos', 'Flores']),
                     ('¿Dónde están las esporas de un helecho?', 'En puntitos cafés debajo de sus hojas',
                      ['En sus flores', 'En sus frutos', 'En la maceta']),
                     ('¿Qué le ayuda a un helecho a volver a brotar después de un incendio?',
                      'Sus tallos bajo tierra (rizomas)', ['Sus flores', 'Sus frutos', 'Nada, no vuelve a brotar']),
                     ('¿Qué combinación de letra y fondo se lee mejor?', 'Letra oscura sobre fondo claro',
                      ['Amarillo sobre blanco', 'Gris claro sobre blanco', 'Verde sobre verde']),
                     ('¿Cuál es la diferencia entre transición y animación?',
                      'La transición es entre diapositivas; la animación es dentro de una diapositiva',
                      ['Son lo mismo', 'La animación cambia el tema', 'La transición borra la diapositiva']),
                     ('¿Qué tecla inicia la presentación en pantalla completa?', 'F5', ['Esc', 'Enter', 'F1']),
                     ('Para hacer una gráfica en tu presentación usas…', 'Insertar → Gráfico',
                      ['Diseño → Tema', 'Archivo → Cerrar', 'Transiciones → Desvanecer']),
                     ('¿Para qué sirven las notas del orador?', 'Para recordar lo que vas a decir sin leer la diapositiva',
                      ['Para que el público las lea', 'Para borrar diapositivas', 'Para cambiar el tema']),
                 ]),
        ]},
    ],
}
