"""Mundo 8 · Inventario del futuro: los inventos de Leonardo da Vinci, inferencias y conclusiones, la IA generativa
como compañera de ideas (con prompts de nivel 2), fichas museográficas y un museo virtual navegable hecho con
presentaciones y vínculos entre diapositivas."""
from .base import clasifica, jefe, leccion, mision

EDAD_IA = ('La mayoría de las herramientas de IA generativa piden tener 13 años o más: en clase se usan con tu profe o '
           'con la cuenta escolar que autorice.')

JUEGOS = {
    'clasifica_existe': clasifica('¿Ya existe o es del futuro?', '🔮', 'Algunos inventos que parecen de película ya '
                                  'existen. ¿Cuáles todavía no?', [
        ('Ya existe', '✅', ['Robots aspiradora que limpian solos', 'Prótesis de mano impresas en 3D',
                             'Drones que entregan paquetes', 'Robots que ayudan en cirugías',
                             'Un celular que traduce lo que dices en voz alta', 'Un paracaídas como el que dibujó Leonardo']),
        ('Todavía no existe', '⏳', ['Teletransportar personas de una ciudad a otra', 'Una máquina para viajar al pasado',
                                     'Ciudades habitadas en Marte', 'Una píldora que te enseña inglés en un día',
                                     'Un robot que siente emociones de verdad', 'Ropa que te hace invisible']),
    ], rondas=12),
    'clasifica_inferencia': clasifica('¿Inferencia o conclusión?', '🕵️', 'Una inferencia es una idea probable a partir '
                                      'de pistas; una conclusión es el juicio final con todas las pruebas.', [
        ('Inferencia', '💭', ['Veo el piso mojado: tal vez llovió', 'Tiene tubos de caña: quizá sirve para respirar',
                              'Lleva mochila deportiva: puede que tenga entrenamiento',
                              'El dibujo tiene alas: tal vez quería volar',
                              'La hoja está escrita al revés: quizá es un código',
                              'Hay migajas en la mesa: alguien comió aquí']),
        ('Conclusión', '⚖️', ['Revisé el clima y las fotos: sí llovió anoche',
                              'Tras analizar las 4 pistas: es un traje de buceo',
                              'Tres fuentes confiables coinciden: el dato es cierto',
                              'La encuesta y la entrevista lo confirman: falta un parque',
                              'Probamos el paracaídas 3 veces y siempre funcionó',
                              'Con todas las pruebas: el robot se movía con poleas']),
    ], rondas=12),
}

MUNDO = {
    'nombre': 'Museo del Futuro', 'tema': 'futuro',
    'descripcion': 'Inventario del futuro. En el siglo XV, Leonardo da Vinci diseñó máquinas voladoras, un traje de '
                   'buceo y hasta un robot. Piensa como detective, usa la IA generativa como compañera de ideas, '
                   'documenta tus inventos en fichas museográficas y monta un museo virtual navegable. Pregunta guía: '
                   'así como da Vinci, ¿qué increíbles inventos podrías imaginar hoy?',
    'niveles': [
        {'nombre': 'El cuaderno de Leonardo', 'cofre': 25, 'misiones': [
            mision('Inventos de hace 500 años', 'texto', leccion(
                intro='Leonardo da Vinci no solo pintó la Mona Lisa: llenó miles de páginas de cuadernos con inventos '
                      'adelantados a su tiempo. Muchos inspiraron tecnologías que hoy son reales.',
                pasos=['Si pudieras enviarle a Leonardo un objeto de hoy, ¿cuál sería y por qué?',
                       '¿Qué invento de hoy crees que la gente del año 2500 verá como algo antiguo?',
                       'Escribe un problema de tu vida diaria que te gustaría que un invento resolviera.'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('Leonardo, el inventor', 'cuestionario', leccion(
                intro='Conoce los inventos que Leonardo dibujó hace más de 500 años.',
                saber=['Leonardo da Vinci (1452-1519): pintor, inventor, ingeniero y estudioso del cuerpo humano.',
                       'Escribía de derecha a izquierda, en espejo: para leer sus notas se necesita un espejo.',
                       'Ornitóptero: una máquina con alas que se movían como las de un ave. Nunca voló, pero inspiró '
                       'a quienes estudiaron el vuelo.',
                       'Paracaídas en forma de pirámide: en el año 2000, un paracaidista construyó uno siguiendo su '
                       'diseño, saltó con él y funcionó.',
                       'Traje de buceo: de cuero, con tubos de caña conectados a una campana flotante para respirar.',
                       'Robot caballero: una armadura que movía los brazos y la cabeza con poleas y cables.']),
                xp=60, preguntas=[
                ('¿Cómo escribía Leonardo sus notas?', 'De derecha a izquierda, en espejo',
                 ['Solo con números', 'En computadora', 'Con letras gigantes']),
                ('¿Qué era el ornitóptero?', 'Una máquina con alas que se movían como las de un ave',
                 ['Un submarino', 'Un reloj', 'Un tipo de pintura']),
                ('¿Qué pasó en el año 2000 con el paracaídas de Leonardo?', 'Alguien lo construyó, saltó y funcionó',
                 ['Se perdió el dibujo', 'Se demostró que no servía', 'Lo pusieron en un cohete']),
                ('¿Para qué servían los tubos de caña del traje de buceo?', 'Para respirar bajo el agua',
                 ['Para nadar más rápido', 'Para comer', 'Para iluminar']),
                ('¿Cómo se movía el robot caballero de Leonardo?', 'Con poleas y cables',
                 ['Con baterías', 'Con inteligencia artificial', 'Con energía solar']),
                ('¿En qué siglo vivió Leonardo?', 'En el siglo XV', ['En el siglo XXI', 'En el siglo I',
                                                                    'En el siglo XX']),
            ]),
            mision('¿Ya existe o es del futuro?', 'juego', leccion(
                intro='Algunos inventos que parecen de ciencia ficción ya existen. Separa los reales de los que todavía '
                      'esperan a su inventor.'), juego='clasifica_existe'),
        ]},
        {'nombre': 'Pensar como detective', 'cofre': 30, 'misiones': [
            mision('Inferencias y conclusiones', 'cuestionario', leccion(
                intro='Los inventores, los científicos y los detectives piensan igual: observan pistas, hacen '
                      'inferencias y llegan a conclusiones.',
                saber=['Inferencia: una idea probable que sacas a partir de pistas. Puede cambiar si aparecen nuevas '
                       'pistas. Suele sonar a «tal vez», «quizá», «probablemente».',
                       'Conclusión: el juicio final al que llegas después de revisar todas las pruebas. Se apoya en '
                       'hechos y responde la pregunta.',
                       'Ejemplo: ves el piso mojado → infieres que llovió. Revisas: no hay nubes y la manguera está '
                       'mojada → concluyes que alguien regó.',
                       'Una buena conclusión dice en qué pruebas se apoya.']), xp=60, preguntas=[
                ('¿Qué es una inferencia?', 'Una idea probable a partir de pistas',
                 ['Una prueba definitiva', 'Una opinión sin pistas', 'Un dato inventado']),
                ('¿Qué es una conclusión?', 'El juicio final después de revisar todas las pruebas',
                 ['La primera idea que se te ocurre', 'Una pregunta', 'Un chisme']),
                ('«Tiene alas, así que tal vez quería volar» es…', 'Una inferencia',
                 ['Una conclusión', 'Un dato falso', 'Una regla']),
                ('¿Qué puede pasar con una inferencia si aparecen pistas nuevas?', 'Puede cambiar',
                 ['Nunca cambia', 'Se vuelve ley', 'Desaparece la pista']),
                ('¿Qué necesita una buena conclusión?', 'Decir en qué pruebas se apoya',
                 ['Ser muy larga', 'Sonar segura aunque no haya pruebas', 'Tener muchas opiniones']),
                ('Ves el piso mojado, no hay nubes y la manguera está mojada. ¿Qué concluyes?', 'Que alguien regó',
                 ['Que llovió', 'Que nevó', 'Que no se puede saber nada']),
            ]),
            mision('¿Inferencia o conclusión?', 'juego', leccion(
                intro='Clasifica cada frase: ¿es una idea probable o el juicio final con pruebas?',
                tip='«Tal vez», «quizá», «puede que» suelen ser inferencias.'), juego='clasifica_inferencia'),
            mision('Caso: el invento misterioso', 'presencial', leccion(
                intro='Tu profe revela, una por una, las pistas de un invento de Leonardo. Las duplas compiten por '
                      'descubrirlo con inferencias y llegar a la conclusión correcta.',
                dinamica=['En duplas con una hoja: uno escribe y el otro propone en voz baja. En el caso 2 cambian.',
                          'Después de cada pista tienen 1 minuto para escribir una inferencia.',
                          'Puntos: 3 por acertar con la pista 2, 2 con la pista 3 y 1 con la pista 4. Si gritan la '
                          'respuesta, pierden sus puntos.'],
                pasos=['Caso 1 · Pista 1: «Está hecho de cuero». Pista 2: «Tiene tubos de caña». Pista 3: «Se conecta a '
                       'una campana que flota». Pista 4: «Lo diseñó para Venecia, una ciudad de canales».',
                       'Caso 2 · Pista 1: «Es de tela de lino». Pista 2: «Tiene forma de pirámide». Pista 3: «Su '
                       'estructura de madera mide unos 7 metros». Pista 4: «En el año 2000 alguien saltó con él desde '
                       'un globo».',
                       'Al final de cada caso escriban su conclusión con las pruebas: «Es un…, porque…».',
                       'Comparen: ¿qué inferencias tuvieron que cambiar con las pistas nuevas?'],
                logro=['Su conclusión menciona al menos 3 pistas como pruebas.'],
                tip='No lean las pistas de adelante: el chiste es inferir con lo que tienen y corregir con cada pista.'),
                xp=50),
        ]},
        {'nombre': 'Lluvia de inventos con IA', 'cofre': 30, 'misiones': [
            mision('Problemas que valen un invento', 'texto', leccion(
                intro='Todo gran invento empieza con un problema. Elige el tuyo.',
                pasos=['Escribe 3 problemas que podrían existir en el año 2075 (agua, basura, transporte, salud, '
                       'energía, escuela, mascotas, soledad…).',
                       'Elige el que más te importe y explica en 3 renglones a quién afecta y por qué.',
                       'Escribe una inferencia: ¿por qué crees que ese problema crecerá? ¿Qué pistas tienes hoy?'],
                logro=['Tu problema es concreto y tu inferencia se apoya en una pista de hoy.'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('Prompts de nivel 2', 'cuestionario', leccion(
                intro='Ya conoces la fórmula de un prompt claro. Estos son los trucos de quienes usan la IA como '
                      'profesionales.',
                saber=['Iterar: casi nunca sale perfecto a la primera. Pide cambios concretos: «hazlo más corto», '
                       '«cambia el estilo a cómic».',
                       'Pedir formato: «dámelo en una tabla con columnas Invento | Problema | Cómo funciona».',
                       'Dar ejemplos: «quiero ideas como esta: …».',
                       'Pedir que te pregunte: «antes de responder, hazme 3 preguntas para entender mi idea».',
                       'La idea final es tuya: usa a la IA para explorar y después decide, combina y mejora tú.',
                       EDAD_IA]), xp=60, preguntas=[
                ('¿Qué significa iterar con una IA?', 'Pedir cambios concretos hasta mejorar el resultado',
                 ['Escribir el mismo prompt muchas veces', 'Rendirse rápido', 'Borrar el chat']),
                ('¿Cómo pides que la IA te dé la información ordenada?', 'Le pido un formato, como una tabla',
                 ['Le escribo en mayúsculas', 'No se puede', 'Le pido que se apure']),
                ('«Antes de responder, hazme 3 preguntas» sirve para…', 'Que la IA entienda mejor tu idea',
                 ['Que la IA se calle', 'Que la IA haga tu tarea', 'Que la IA se apague']),
                ('¿De quién es la idea final de tu invento?', 'Tuya: tú decides, combinas y mejoras',
                 ['De la IA', 'De nadie', 'De la empresa de la IA']),
                ('Dar un ejemplo en el prompt ayuda a…', 'Que la IA entienda el estilo que buscas',
                 ['Gastar más batería', 'Confundir a la IA', 'Nada']),
            ]),
            mision('La IA como compañera de ideas', 'evidencia', leccion(
                intro='Una lluvia de ideas con un compañero que nunca se cansa. Pero tú eres quien decide.',
                saber=[EDAD_IA,
                       'Prompt sugerido: «Soy estudiante de 6.º de primaria. Dame 5 ideas de inventos para [tu problema] '
                       'en el año 2075. Que sean creativas, pero posibles con la ciencia. Dámelas en una tabla: Invento '
                       '| Cómo funciona | Qué problema resuelve».',
                       'Después evalúa cada idea con inferencias: ¿qué pistas de hoy dicen que podría funcionar?'],
                pasos=['Escribe tu prompt con la fórmula y tu problema.',
                       'Tu profe lo usa (o lo hacen con la herramienta escolar que autorice) y copias la tabla.',
                       'Pide un cambio (itera): «hazlas más baratas» o «para niños».',
                       'Elige una idea, combínala con otra o mejórala con algo tuyo.',
                       'Escribe tu conclusión: «Mi invento será… porque…» con al menos 2 razones.'],
                logro=['Muestras el prompt, la respuesta, tu iteración y tu invento final con 2 razones.'],
                entrega='sube una captura de tu tabla de ideas y escribe tu conclusión en el comentario.'),
                xp=100, monedas=30),
        ]},
        {'nombre': 'Fichas y salas', 'cofre': 35, 'misiones': [
            mision('Ficha museográfica', 'evidencia', leccion(
                intro='En los museos, junto a cada objeto hay una ficha (cédula museográfica) que explica qué es. Crea '
                      'la de tu invento en una diapositiva.',
                saber=['Partes: nombre del invento, inventor(a) y año, problema que resuelve, cómo funciona (3 pasos), '
                       'materiales, dato curioso, imagen y créditos.',
                       'Una ficha se lee de pie y en 30 segundos: frases cortas y letra grande (mínimo 20 puntos).',
                       'Créditos: di qué hiciste tú y en qué ayudó la IA.'],
                pasos=['Abre PowerPoint o Google Slides: Museo_TuNombre.',
                       'Crea una diapositiva con todas las partes de la ficha.',
                       'Usa un diseño (Diseño → Temas) y máximo 2 tipos de letra.',
                       'Deja un espacio para la imagen del invento.',
                       'Pide a un compañero que la lea en 30 segundos: ¿entendió el invento?'],
                logro=['Tu ficha tiene todas las partes y se entiende en 30 segundos.'],
                entrega='sube una captura de tu ficha.'), xp=100, monedas=30),
            mision('La imagen del invento', 'evidencia', leccion(
                intro='Tu invento necesita una imagen. La generarás con IA y la harás accesible para todos.',
                saber=[EDAD_IA,
                       'Prompt de imagen: sujeto + acción + lugar + estilo + detalles. Ejemplo: «Mochila que purifica el '
                       'aire, usada por una estudiante en una ciudad del año 2075, estilo ilustración técnica, fondo '
                       'blanco, vista de tres cuartos».',
                       'Texto alternativo: una descripción de la imagen para personas que usan lectores de pantalla. '
                       'Clic derecho en la imagen → Texto alternativo.'],
                pasos=['Escribe tu prompt de imagen y genera 2 versiones con tu profe.',
                       'Elige una e insértala en tu ficha.',
                       'Agrega el pie: «Imagen generada con IA (herramienta)».',
                       'Escribe el texto alternativo: qué se ve, en una o dos frases.'],
                ojo=['No se generan imágenes de personas reales ni de compañeros.'],
                logro=['Tu ficha tiene la imagen con pie de crédito y texto alternativo.'],
                entrega='sube una captura de tu ficha con la imagen.'), xp=90, monedas=25),
            mision('Construye el museo virtual', 'evidencia', leccion(
                intro='Ahora tú y tu dupla unen sus fichas en un museo que se recorre con clics, como una página web.',
                saber=['Vestíbulo: la primera diapositiva, con botones que llevan a cada sala.',
                       'Vínculo a otra diapositiva: selecciona el botón → Insertar → Vínculo → «Lugar de este documento» '
                       '(PowerPoint) o «Diapositivas de esta presentación» (Google Slides).',
                       'Cada ficha lleva un botón «Volver al vestíbulo».',
                       'Los vínculos funcionan en modo presentación (F5).'],
                roles=['Curador/a y diseñador/a: decide las salas y arma el vestíbulo y los botones con el mismo estilo.',
                       'Integrador/a y tester: copia las fichas a la presentación y prueba que TODOS los vínculos lleven a '
                       'donde deben.',
                       'Si la presentación está en la nube (Google Slides o PowerPoint en línea), los dos trabajan al mismo '
                       'tiempo, cada quien en su computadora.'],
                pasos=['Creen la presentación de la dupla: Museo_del_Futuro_NombreDupla.',
                       'Diapositiva 1: vestíbulo con el nombre del museo y un botón por sala (Insertar → Formas).',
                       'Una diapositiva de portada por sala y después las fichas de esa sala.',
                       'Vinculen cada botón con su sala y agreguen «Volver al vestíbulo» en cada ficha.',
                       'El Tester recorre el museo en modo presentación y anota los vínculos que fallan.'],
                logro=['Desde el vestíbulo se llega a cada sala y desde cada ficha se puede volver.'],
                entrega='sube capturas del vestíbulo y de una ficha con su botón de regreso.'), xp=110, monedas=30),
        ]},
        {'nombre': 'Inauguración', 'cofre': 40, 'misiones': [
            mision('Recorrido y retroalimentación', 'presencial', leccion(
                intro='Día de inauguración: las duplas visitan los museos de las demás.',
                dinamica=['Rotación por las computadoras cada 4 minutos con la alarma del profe.',
                          'Uno de la dupla se queda como guía de su museo y el otro visita; a la mitad cambian.',
                          'Se recorre en modo presentación. Se habla con voz de museo (bajito).'],
                pasos=['Recorre al menos 3 museos.',
                       'En cada uno deja una nota con la fórmula EPS: un Elogio, una Pregunta y una Sugerencia.',
                       'Escribe una inferencia sobre un invento ajeno: «Creo que este invento también podría servir '
                       'para…».',
                       'Regresa con tu dupla y lean juntos las notas que recibieron.'],
                logro=['Dejaste notas EPS en al menos 3 museos.']), xp=50),
            mision('Ajustes finales', 'evidencia', leccion(
                intro='Una buena dupla convierte la retroalimentación en mejoras.',
                pasos=['Lean todas las notas EPS que recibieron.',
                       'Elijan las 2 sugerencias más útiles y háganlas.',
                       'Respondan por escrito las preguntas que les dejaron (pueden agregar una diapositiva de '
                       '«Preguntas frecuentes»).',
                       'Escriban su conclusión del proyecto: ¿qué invento del museo creen que sí podría existir en '
                       '2075 y por qué? Apóyenla en hechos.'],
                logro=['Hicieron 2 mejoras basadas en la retroalimentación y su conclusión cita pruebas.'],
                entrega='sube una captura de los cambios y escribe tu conclusión en el comentario.'), xp=90, monedas=25),
            jefe('Jefe: El Autómata de Leonardo', leccion(
                intro='El robot caballero de Leonardo despertó y no deja salir a nadie del museo. Demuestra que piensas '
                      'como inventor y como detective.'), [
                ('¿Qué invento de Leonardo se probó en el año 2000 y funcionó?', 'El paracaídas',
                 ['El ornitóptero', 'El tanque', 'El submarino']),
                ('«Tiene tubos de caña: quizá sirve para respirar» es…', 'Una inferencia',
                 ['Una conclusión', 'Un hecho comprobado', 'Una regla']),
                ('¿Qué necesita una buena conclusión?', 'Apoyarse en pruebas', ['Ser muy larga', 'Sonar segura',
                                                                               'Tener emojis']),
                ('¿Qué significa iterar con una IA?', 'Pedir cambios concretos hasta mejorar el resultado',
                 ['Escribir el mismo prompt muchas veces', 'Copiar la primera respuesta', 'Cerrar la app']),
                ('¿Qué es el texto alternativo de una imagen?', 'Una descripción para quien usa lectores de pantalla',
                 ['El nombre del archivo', 'Un filtro de color', 'El pie de foto']),
                ('¿Cómo haces que un botón lleve a otra diapositiva?', 'Insertar → Vínculo → Lugar de este documento',
                 ['Copiar y pegar la diapositiva', 'Cambiar el diseño', 'Insertar → Tabla']),
                ('¿Qué lleva una ficha museográfica?', 'Nombre, inventor, problema, cómo funciona, imagen y créditos',
                 ['Solo una imagen', 'Solo el precio', 'Tu dirección']),
                ('¿De quién es la idea final de un invento hecho con apoyo de IA?', 'De quien decide, combina y mejora',
                 ['De la IA', 'De nadie', 'Del primero que la vea']),
            ]),
        ]},
    ],
}
