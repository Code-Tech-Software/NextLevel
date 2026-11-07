"""Mundo 1 · ES-DAT307 Día a día en otros planetas: las reglas de la estación, la rotación de los planetas en una hoja
de cálculo con gráfica, cómo aprende una IA (Quick, Draw!), prompts de 3 ingredientes para editar, AutoDraw para
ilustrar y un periódico mural con columnas y su convocatoria."""
from .base import AUTODRAW, CARPETA, EDAD_IA, PAREJAS, QUICKDRAW, clasifica, jefe, leccion, mision

JUEGOS = {
    'clasifica_dia_planetas': clasifica('¿Día más corto o más largo?', '🪐', 'En la Tierra el día dura 24 horas. ¿El '
                                        'día de este lugar dura menos o más que el nuestro?', [
        ('Más corto que en la Tierra', '⚡', ['Júpiter: casi 10 horas', 'Saturno: unas 10 horas y media',
                                              'Urano: unas 17 horas', 'Neptuno: unas 16 horas',
                                              'Ceres, planeta enano: unas 9 horas',
                                              'Haumea, planeta enano: unas 4 horas']),
        ('Más largo que en la Tierra', '🐢', ['Mercurio: 59 días terrestres', 'Venus: 243 días terrestres',
                                              'La Luna: unos 27 días', 'Plutón: más de 6 días terrestres',
                                              'Marte: 24 horas y 37 minutos',
                                              'El Sol, en su ecuador: unos 25 días']),
    ], rondas=12),
    'clasifica_tiene_ia': clasifica('¿Tiene IA o no?', '🤖', 'Algunas máquinas aprenden de ejemplos y otras solo siguen '
                                    'una orden fija. ¿Cuál usa inteligencia artificial?', [
        ('Usa IA', '🤖', ['El teclado del celular que sugiere la siguiente palabra',
                          'Quick, Draw! adivinando lo que dibujas',
                          'Una app que dice qué planta es con una foto', 'Los subtítulos automáticos de un video',
                          'Una app de música que arma listas con tus gustos',
                          'El celular que reconoce tu voz cuando le hablas',
                          'Un traductor que entiende una frase completa']),
        ('No usa IA', '🔌', ['Un semáforo que cambia cada 60 segundos', 'Un microondas con temporizador',
                             'Una calculadora sumando 8 + 5', 'Un timbre que suena al presionarlo',
                             'Una lámpara que prende con el apagador', 'Un reloj despertador',
                             'Un elevador que va al piso que presionas']),
    ], rondas=12),
    'clasifica_prompt_claro': clasifica('¿Prompt claro o flojo?', '💬', 'Un prompt claro tiene 3 ingredientes: qué '
                                        'quiero, detalles y lo que no debe cambiar. ¿Este funcionaría?', [
        ('Prompt claro', '🎯', ['Corrige la ortografía de mi cuento sin cambiar la historia',
                                'Dame 3 títulos para un cuento sobre un día en Venus',
                                'Explica qué es la rotación para niños de 5.º en 4 renglones',
                                'Marca en negritas las palabras que corregiste',
                                'Sugiere un mejor final, pero no reescribas mi cuento',
                                'Dime qué partes de mi cuento son difíciles de entender']),
        ('Prompt flojo', '😴', ['arréglalo', 'hazme un cuento', 'pon algo de planetas', 'mejóralo todo',
                                'escribe mi tarea', 'corrige']),
    ], rondas=12),
}

MUNDO = {
    'nombre': 'Estación Kepler', 'tema': 'espacio',
    'descripcion': 'ES-DAT307 · Día a día en otros planetas. Hace más de 400 años, el astrónomo Johannes Kepler escribió '
                   'una historia sobre un viaje a la Luna y cómo se viviría allá el día y la noche. Aquí vas a medir el '
                   'día de cada planeta en una hoja de cálculo, descubrir cómo aprende una inteligencia artificial, '
                   'escribir ciencia ficción, editarla e ilustrarla con IA y publicar un periódico mural. Pregunta guía: '
                   '¿cómo difundir nuestras historias y hacer que nuestro grupo crezca?',
    'niveles': [
        {'nombre': 'Reglas de la estación', 'cofre': 25, 'misiones': [
            mision('Contrato de la estación', 'presencial', leccion(
                intro='Toda estación espacial funciona con reglas claras: si cada quien hace lo que quiere, la misión '
                      'fracasa. Hoy el grupo acuerda cómo se va a trabajar en el laboratorio todo el año.',
                saber=['Semáforo de voz: 🔴 silencio total (el profe explica o es tiempo de concentración), 🟡 solo '
                       'susurros con tu dupla, 🟢 voz normal para compartir.',
                       'Señal «manos arriba»: el profe levanta la mano y todos sueltan el mouse, miran al frente y se '
                       'callan. Gana XP el grupo que lo logra en menos de 5 segundos.',
                       'Regla 1-2-3 para pedir ayuda: 1) releo la misión, 2) le pregunto a mi dupla, 3) levanto la mano '
                       'y espero en mi lugar.',
                       'Duplas: el profe las arma y son de máximo 2. Tu dupla es tu copiloto, no tu chofer: nadie hace '
                       'el trabajo del otro.'],
                dinamica=['10 minutos de explicación con el semáforo en 🔴.',
                          'Practiquen 3 veces la señal «manos arriba»: el profe cronometra.',
                          'Cada dupla propone una regla más en voz 🟡; el grupo vota las 2 mejores.'],
                pasos=['Escuchen el semáforo de voz y la señal «manos arriba».',
                       'Practiquen la señal hasta lograrla en menos de 5 segundos.',
                       'Propongan y voten 2 reglas extra del grupo.',
                       'Cada alumno firma el contrato que queda pegado en el laboratorio.'],
                logro=['Explicas qué significa cada color del semáforo y la regla 1-2-3.',
                       'El grupo logra la señal «manos arriba» en menos de 5 segundos.']), xp=50),
            mision('Tu base de trabajo', 'evidencia', leccion(
                intro='Una buena tripulación sabe dónde guarda cada cosa. Hoy armas tu carpeta del año y aprendes los '
                      'atajos que vas a usar en todas las misiones.',
                saber=[f'Tu carpeta se llamará {CARPETA} (con tu nombre real, sin espacios ni acentos). Dentro va una '
                       'carpeta por mundo.',
                       'Atajos: Ctrl + C copia, Ctrl + V pega, Ctrl + Z deshace, Ctrl + S guarda y Alt + Tab cambia de '
                       'ventana.',
                       'Captura de pantalla en Windows: tecla Windows + Shift + S → arrastra el recuadro → la imagen '
                       'queda copiada; pégala con Ctrl + V. Así vas a entregar casi todas tus evidencias.'],
                dinamica=PAREJAS,
                pasos=['Abre el Explorador de archivos → Documentos (o donde indique el profe).',
                       f'Clic derecho → Nuevo → Carpeta y llámala {CARPETA}.',
                       'Dentro crea estas carpetas: Kepler, DaVinci, Hubble, Alerta, AzulProfundo, Lluvia, SombraVeloz y '
                       'RespiraHondo.',
                       'Practica: escribe una palabra en el Bloc de notas, cópiala y pégala 5 veces con los atajos; '
                       'luego deshaz con Ctrl + Z.',
                       'Toma una captura de tu carpeta con Windows + Shift + S.'],
                logro=['Tu carpeta tiene tu nombre y las 8 carpetas de los mundos.',
                       'Sabes tomar una captura y pegarla.'],
                entrega='sube la captura de tu carpeta con sus 8 carpetas.'), xp=70, monedas=20),
        ]},
        {'nombre': 'Un día en otro planeta', 'cofre': 25, 'misiones': [
            mision('Kepler soñó con la Luna', 'texto', leccion(
                intro='La ciencia ficción mezcla imaginación y ciencia. En 1608, Johannes Kepler (el astrónomo que '
                      'descubrió cómo se mueven los planetas alrededor del Sol) escribió «El sueño»: un viaje a la Luna '
                      'en el que describe que allá el día y la noche duran casi dos semanas cada uno. Muchos lo '
                      'consideran el primer relato de ciencia ficción.',
                pasos=['¿Qué película, serie, libro o videojuego de ciencia ficción conoces? ¿Qué tiene de ciencia y qué '
                       'de imaginación?',
                       'Si en la Luna la noche dura dos semanas, ¿qué sería lo más difícil de vivir allá?',
                       'Si escribieras una historia que pasa en otro planeta, ¿cómo harías para que la leyera mucha '
                       'gente?'],
                entrega='escribe tus tres respuestas aquí abajo.'), xp=60),
            mision('El reloj de cada planeta', 'cuestionario', leccion(
                intro='En la Tierra un día dura 24 horas… pero en otros planetas no. Aprende por qué.',
                saber=['Rotación: el giro de un planeta sobre sí mismo. Lo que tarda en dar una vuelta completa es la '
                       'duración de su día.',
                       'Traslación: la vuelta completa alrededor del Sol. Lo que tarda es la duración de su año.',
                       'Júpiter gira tan rápido que su día dura casi 10 horas, el más corto de los planetas.',
                       'Venus gira lentísimo y al revés: su día dura 243 días terrestres, más que su año (225 días).',
                       'Marte tiene un día casi igual al nuestro: 24 horas y 37 minutos.',
                       'La Luna tarda 27 días en girar y siempre nos enseña la misma cara.']), xp=60, preguntas=[
                ('¿Qué es la rotación?', 'El giro de un planeta sobre sí mismo',
                 ['La vuelta alrededor del Sol', 'La luz que da el Sol', 'Un eclipse']),
                ('La duración del día de un planeta depende de…', 'Lo que tarda en girar sobre sí mismo',
                 ['Lo que tarda en darle la vuelta al Sol', 'Su color', 'Cuántas lunas tiene']),
                ('¿Qué planeta tiene el día más corto?', 'Júpiter', ['Venus', 'Mercurio', 'Marte']),
                ('¿Qué tiene de especial Venus?', 'Su día dura más que su año', ['No tiene día', 'Gira muy rápido',
                                                                                  'Es el planeta más frío']),
                ('¿Qué planeta tiene un día parecido al de la Tierra?', 'Marte', ['Júpiter', 'Venus', 'Neptuno']),
                ('¿Por qué siempre vemos la misma cara de la Luna?',
                 'Porque gira sobre sí misma en el mismo tiempo que tarda en darle la vuelta a la Tierra',
                 ['Porque no gira', 'Porque la otra cara está apagada', 'Porque la Tierra no gira']),
            ]),
            mision('¿Día más corto o más largo?', 'juego', leccion(
                intro='Compara cada día con el de la Tierra: 24 horas. Ojo: algunos están en horas y otros en días.',
                tip='Un día terrestre son 24 horas, así que «59 días» es muchísimo más que «10 horas».'),
                juego='clasifica_dia_planetas'),
            mision('Gráfica de los días', 'evidencia', leccion(
                intro='Los científicos no solo leen datos: los acomodan en tablas y gráficas para descubrir cosas. Hoy '
                      'usas una hoja de cálculo (Excel u Hojas de cálculo de Google) para comparar el día de cada '
                      'planeta.',
                saber=['Una hoja de cálculo está hecha de celdas. Cada celda tiene un nombre: su columna (letra) y su '
                       'fila (número). Ejemplo: B3.',
                       'Para escribir en una celda, haz clic en ella, escribe y presiona Enter.',
                       'Para hacer una gráfica: selecciona los datos (con sus títulos) → Insertar → Gráfico de '
                       'columnas.',
                       'Duración del día en horas: Mercurio 1408, Venus 5832, Tierra 24, Marte 24.6, Júpiter 9.9, '
                       'Saturno 10.7, Urano 17.2, Neptuno 16.1.'],
                dinamica=PAREJAS,
                pasos=['Abre una hoja de cálculo nueva y guárdala en tu carpeta Kepler como DiasPlanetas_TuNombre.',
                       'En A1 escribe «Planeta» y en B1 «Horas de su día». Ponlos en negritas.',
                       'Llena los 8 planetas con sus horas, del A2 al B9.',
                       'Ordena de menor a mayor: selecciona A1:B9 → Datos → Ordenar (por la columna B).',
                       'Selecciona A1:B9 → Insertar → Gráfico de columnas. Ponle el título «¿Cuánto dura un día?».',
                       'Observa: ¿por qué casi no se ven las barras de los demás planetas?',
                       'Haz una segunda gráfica solo con los 6 primeros planetas (A1:B7). ¿Ahora qué descubres?'],
                logro=['Tu tabla está ordenada de menor a mayor y tiene dos gráficas con título.',
                       'Explicas por qué Mercurio y Venus «aplastan» a los demás en la primera gráfica.'],
                tip='Si la gráfica sale con los planetas revueltos, revisa que hayas ordenado los datos antes.',
                entrega='sube una captura con tu tabla y tus dos gráficas, y escribe en el comentario lo que '
                        'descubriste.'), xp=100, monedas=30),
            mision('Mi día en Júpiter', 'texto', leccion(
                intro='Imagina que te mudas a una base espacial en Júpiter, donde el día dura 10 horas. Tu horario de '
                      'siempre ya no cabe: tienes que rediseñarlo.',
                pasos=['Escribe cómo repartirías las 10 horas: dormir, escuela, comer, jugar y lo que quieras. Las horas '
                       'deben sumar 10.',
                       '¿Qué cambiarías de tu vida si cada «día» fuera de 10 horas?',
                       'Ahora imagina Venus, con días de 243 días terrestres: ¿cuándo festejarías tu cumpleaños?'],
                logro=['Tu horario suma exactamente 10 horas y explicas qué cambiaría en tu vida.'],
                entrega='escribe tu horario y tus respuestas aquí abajo.'), xp=60),
        ]},
        {'nombre': '¿Cómo aprende una IA?', 'cofre': 30, 'misiones': [
            mision('La IA en palabras simples', 'cuestionario', leccion(
                intro='Todo mundo habla de inteligencia artificial (IA). Al terminar esta misión podrás explicarla en '
                      'palabras simples.',
                saber=['La IA son programas que aprenden de muchísimos ejemplos. A esos ejemplos se les llama datos.',
                       'Entrenar una IA es darle miles de ejemplos («esto es un gato», «esto no») hasta que encuentra '
                       'el patrón y reconoce gatos que nunca había visto.',
                       'Una IA que platica (un chatbot) escribe adivinando cuál es la palabra que más probablemente '
                       'sigue. Por eso a veces inventa datos que suenan reales: se dice que «alucina».',
                       'Prompt: la instrucción que le escribes a una IA.',
                       'La IA se equivoca, no siente y no piensa como una persona: lo que dice siempre se revisa.',
                       EDAD_IA]), xp=60, preguntas=[
                ('¿De qué aprende una IA?', 'De muchísimos ejemplos (datos)',
                 ['De un solo ejemplo', 'De lo que siente', 'De nada, ya nace sabiendo']),
                ('¿Qué es entrenar una IA?', 'Darle muchos ejemplos hasta que encuentra el patrón',
                 ['Ponerla a hacer ejercicio', 'Apagarla y prenderla', 'Conectarla a la luz']),
                ('¿Cómo escribe un chatbot?', 'Adivinando la palabra que más probablemente sigue',
                 ['Pensando como una persona', 'Copiando siempre el mismo texto', 'Preguntándole a un humano']),
                ('¿Qué significa que una IA «alucina»?', 'Que inventa datos que suenan reales',
                 ['Que ve fantasmas', 'Que se apaga sola', 'Que se pone feliz']),
                ('¿Qué es un prompt?', 'La instrucción que le escribes a una IA',
                 ['Una pieza de la computadora', 'Un virus', 'Un tipo de robot']),
                ('¿Qué haces con lo que responde una IA?', 'Lo reviso antes de usarlo',
                 ['Lo copio sin leer', 'Lo creo porque lo dijo la IA', 'Lo publico de inmediato']),
            ]),
            mision('Entrena a la IA humana', 'presencial', leccion(
                intro='Sin computadora: tu dupla será una IA que no sabe nada y tú la vas a entrenar con ejemplos. Así '
                      'entenderás por qué la IA acierta… y por qué se equivoca.',
                dinamica=['En duplas, cada quien en su lugar. Semáforo en 🟡: solo susurros.',
                          'El profe dibuja en el pizarrón; las duplas responden escribiendo en una hoja, sin gritar.',
                          'Cada ronda dura 3 minutos. Al final se comparan los resultados.'],
                pasos=['Ronda 1 · Entrenamiento: el profe dibuja 3 «Glorps» (todas las figuras tienen exactamente 3 '
                       'picos, de distintas formas y tamaños) y 3 «No Glorps» (con 2 o con 4 picos). La IA de cada '
                       'dupla busca el patrón.',
                       'Ronda 2 · Prueba: el profe dibuja 4 figuras nuevas. La IA decide si cada una es Glorp o no. ¿Cuántas '
                       'acertó?',
                       'Ronda 3 · La trampa: el profe dibuja un Glorp gigante y de otro color. Si la IA se fijó en el '
                       'tamaño o el color en lugar de los picos, falla. ¡Eso le pasa a la IA de verdad cuando sus '
                       'ejemplos no son variados!',
                       'Ronda 4 · Adivina la palabra: el profe dice «Hoy en la mañana desayuné…» y cada dupla escribe la '
                       'palabra que más probablemente sigue. Así escribe un chatbot.',
                       'Comenten: ¿por qué una IA con pocos ejemplos se equivoca más?'],
                logro=['Explicas con tus palabras cómo aprende una IA y por qué necesita ejemplos variados.']), xp=50),
            mision('Quick, Draw!: la IA que adivina', 'evidencia', leccion(
                intro='Quick, Draw! es un experimento de Google: tú dibujas y una IA intenta adivinar qué es en menos de '
                      '20 segundos. Aprendió viendo millones de dibujos de personas de todo el mundo.',
                saber=['No necesitas cuenta. Tus dibujos se guardan sin tu nombre en la colección del experimento, así que '
                       'nunca escribas ni dibujes datos personales.',
                       'Al terminar, haz clic en un dibujo para ver qué pensó la IA y cómo dibujaron eso otras '
                       'personas: esos son sus datos de entrenamiento.'],
                dinamica=['Cada quien en su compu, con audífonos o con el sonido bajo.',
                          '10 minutos de juego. Semáforo en 🟡: puedes festejar con tu dupla, sin gritar.'],
                pasos=['Abre el enlace y presiona «¡Vamos a dibujar!» (o «Let\'s Draw!»).',
                       'Juega una ronda completa de 6 dibujos.',
                       'En los resultados, abre un dibujo que la IA NO adivinó y mira cómo lo dibujaron otras '
                       'personas.',
                       'Juega otra ronda tratando de dibujar como dibuja la mayoría. ¿Adivinó más?'],
                logro=['Completaste dos rondas y explicas por qué la IA no adivinó uno de tus dibujos.'],
                entrega='sube una captura de tus resultados y escribe en el comentario por qué crees que la IA falló en '
                        'uno de tus dibujos.'), xp=80, monedas=25, link=QUICKDRAW),
            mision('¿Tiene IA o no?', 'juego', leccion(
                intro='Detecta qué aparatos y apps usan inteligencia artificial.',
                tip='Si la máquina aprende de ejemplos o reconoce algo (voces, caras, dibujos, gustos), probablemente '
                    'usa IA. Si siempre hace lo mismo, no.'), juego='clasifica_tiene_ia'),
        ]},
        {'nombre': 'Escribe tu historia', 'cofre': 30, 'misiones': [
            mision('Receta de ciencia ficción', 'texto', leccion(
                intro='La buena ciencia ficción toma un dato real y se pregunta «¿y si…?». Planea tu historia antes de '
                      'escribirla.',
                saber=['Dato real: por ejemplo, «en Júpiter el día dura casi 10 horas».',
                       '¿Y si…?: la idea que cambia todo. «¿Y si mi escuela estuviera en Júpiter y las clases duraran '
                       'una hora?».',
                       'Personaje: quién es y qué quiere.',
                       'Problema: lo que el dato científico le complica al personaje.',
                       'Final: cómo lo resuelve (o cómo no).'],
                pasos=['Elige un planeta o una luna y su dato de rotación.',
                       'Escribe tu «¿y si…?».',
                       'Describe a tu personaje en 2 renglones.',
                       'Escribe el problema y el final en un renglón cada uno.'],
                logro=['Tu receta tiene dato real, «¿y si…?», personaje, problema y final.'],
                entrega='escribe tu receta aquí abajo.'), xp=60),
            mision('Tu borrador', 'evidencia', leccion(
                intro='Ahora escribe tu historia. TÚ eres el autor: la IA llegará después como editora, nunca como '
                      'escritora.',
                dinamica=['15 minutos de escritura con el semáforo en 🔴. Audífonos con música suave si el profe lo '
                          'permite.',
                          'Si terminas antes, no molestas: revisas tu ortografía o agregas un detalle.'],
                pasos=['Abre el procesador de textos (Word o Documentos de Google).',
                       'Escribe un título y tu historia de 150 a 250 palabras. El contador de palabras está en la barra '
                       'de abajo (Word) o en Herramientas → Contar palabras (Google).',
                       'Usa tu dato real dentro de la historia, no como un dato suelto al final.',
                       'Guárdala en tu carpeta Kepler como SciFi_TuNombre. Esta versión demuestra que la escribiste '
                       'tú.'],
                logro=['Tu historia tiene título, de 150 a 250 palabras y el dato real es parte de lo que pasa.'],
                entrega='sube una captura de tu borrador donde se vea el número de palabras.'), xp=100, monedas=30),
            mision('Prompts de 3 ingredientes', 'cuestionario', leccion(
                intro='Una IA responde tan bien como le pidas las cosas. Esta receta funciona casi siempre.',
                saber=['Ingrediente 1 · Qué quiero: la tarea. «Corrige la ortografía de mi cuento».',
                       'Ingrediente 2 · Detalles: para quién, cómo y cuánto. «Es para niños de 5.º; marca cada cambio en '
                       'negritas».',
                       'Ingrediente 3 · Lo que NO debe hacer: los límites. «No cambies mi historia ni los nombres».',
                       'Si la respuesta no te gusta, cambia una sola cosa del prompt y vuelve a intentar.',
                       'En un prompt nunca van datos personales: tu nombre completo, tu dirección, tu escuela o fotos '
                       'de personas.']), xp=60, preguntas=[
                ('¿Cuáles son los 3 ingredientes de un prompt claro?', 'Qué quiero, detalles y lo que no debe hacer',
                 ['Saludo, pregunta y despedida', 'Mayúsculas, signos y emojis', 'Nombre, edad y escuela']),
                ('«No cambies mi historia» es el ingrediente de…', 'Lo que no debe hacer', ['Qué quiero', 'Detalles',
                                                                                          'Ninguno']),
                ('«Es para niños de 5.º y marca los cambios en negritas» son…', 'Detalles',
                 ['Lo que no debe hacer', 'Qué quiero', 'Datos personales']),
                ('¿Cuál es el prompt más claro?', 'Corrige la ortografía de mi cuento sin cambiar la historia',
                 ['arréglalo', 'mejóralo todo', 'corrige']),
                ('¿Qué NO debe ir en un prompt?', 'Tu dirección', ['El tema de tu cuento', 'Para quién es',
                                                                   'Cuántas palabras quieres']),
                ('La IA te respondió algo que no querías. ¿Qué haces?', 'Cambio una cosa del prompt y lo intento otra vez',
                 ['Me rindo', 'Copio la respuesta de todos modos', 'Escribo lo mismo en mayúsculas']),
            ]),
            mision('¿Prompt claro o flojo?', 'juego', leccion(
                intro='Decide qué prompts darían una buena respuesta y cuáles no sirven.',
                tip='Si el prompt no dice qué quieres exactamente, es flojo.'), juego='clasifica_prompt_claro'),
        ]},
        {'nombre': 'IA editora e ilustradora', 'cofre': 35, 'misiones': [
            mision('Edita con IA, decide tú', 'evidencia', leccion(
                intro='La IA será tu editora. Ella sugiere, pero tú decides: el autor sigue siendo tú.',
                saber=[EDAD_IA,
                       'Si aceptas todos los cambios sin leerlos, la historia deja de ser tuya.',
                       'Al final se avisa en qué ayudó la IA. Ejemplo: «Ortografía revisada con apoyo de IA».'],
                dinamica=['Cada quien escribe su prompt en silencio (5 minutos).',
                          'El profe usa la IA con algunos prompts en el proyector; todos observan con el semáforo en 🔴.',
                          'Después cada quien revisa los cambios de su propio texto.'],
                pasos=['Escribe tu prompt con los 3 ingredientes: pide corregir ortografía y puntuación y 2 '
                       'sugerencias, SIN reescribir tu historia.',
                       'Tu profe lo usa con tu texto (o con la herramienta escolar que autorice).',
                       'Haz una tabla de 2 columnas: «Cambios que acepto» y «Cambios que no acepto», con una razón para '
                       'cada uno.',
                       'Pasa a tu documento solo los cambios que aceptaste.',
                       'Escribe al final de tu historia: «Ortografía revisada con apoyo de IA».'],
                logro=['Tienes tu prompt, tu tabla de decisiones y tu historia corregida.'],
                entrega='sube una captura de tu tabla y de tu historia final, y escribe tu prompt en el comentario.'),
                xp=100, monedas=30),
            mision('Ilustra con AutoDraw', 'evidencia', leccion(
                intro='AutoDraw es una herramienta de Google con IA: tú haces un garabato y la IA adivina qué querías '
                      'dibujar y te ofrece dibujos limpios. No necesita cuenta.',
                saber=['Herramienta AutoDraw (la del lápiz con estrella): dibuja algo rápido y arriba aparecen las '
                       'sugerencias de la IA. Haz clic en la que quieras.',
                       'También tienes Texto, Relleno y Formas para completar la escena.',
                       'Para guardar: menú ☰ → Download (descargar). La imagen se baja como PNG.'],
                dinamica=PAREJAS,
                pasos=['Elige la escena más importante de tu historia.',
                       'Dibuja con AutoDraw al menos 4 elementos: el personaje, el planeta, un objeto y el cielo.',
                       'Usa Relleno para darle color y Texto para un título corto.',
                       'Descarga tu imagen y guárdala en tu carpeta Kepler.',
                       'Insértala en tu historia: Insertar → Imagen. Debajo escribe: «Ilustración hecha con AutoDraw».'],
                logro=['Tu ilustración tiene al menos 4 elementos, color y está dentro de tu historia con su pie de '
                       'imagen.'],
                entrega='sube una captura de tu historia con la ilustración.'), xp=90, monedas=25, link=AUTODRAW),
            mision('Prompt de imagen', 'texto', leccion(
                intro='Las IA de imágenes también funcionan con prompts. Escribe uno para la portada del periódico '
                      'mural: tu profe generará algunos en el proyector.',
                saber=[EDAD_IA,
                       'Receta de un prompt de imagen: quién o qué + qué está haciendo + dónde + estilo + detalles '
                       '(colores, luz, hora del día).',
                       'Ejemplo: «Una niña astronauta desayunando en una base de Júpiter mientras sale el Sol por '
                       'segunda vez en el día, estilo cómic, colores naranjas».',
                       'Toda imagen hecha con IA se etiqueta: «Imagen generada con IA».'],
                pasos=['Escribe un prompt flojo de una sola palabra, por ejemplo «planeta».',
                       'Escribe un prompt completo con la receta para una escena de tu historia.',
                       'Escribe qué crees que saldría distinto entre los dos prompts.'],
                ojo=['No se piden imágenes de personas reales ni de compañeros.'],
                logro=['Tu prompt completo tiene quién, qué hace, dónde, estilo y detalles.'],
                entrega='escribe tus dos prompts y tu predicción aquí abajo.'), xp=60),
        ]},
        {'nombre': 'Periódico mural', 'cofre': 40, 'misiones': [
            mision('Página de periódico', 'evidencia', leccion(
                intro='Los periódicos acomodan el texto en columnas para que se lea rápido. Convierte tu historia en una '
                      'página de periódico.',
                saber=['Columnas: Word → Disposición → Columnas → Dos. Documentos de Google → Formato → Columnas.',
                       'Ajustar texto de una imagen: haz clic en la imagen → Ajustar texto → Cuadrado. Así el texto la '
                       'rodea.',
                       'Encabezado de periódico: nombre del periódico, número y fecha, en letra grande.'],
                dinamica=PAREJAS,
                pasos=['Guarda una copia de tu historia como Periodico_TuNombre.',
                       'Arriba escribe el nombre del periódico que eligió el grupo, el número y la fecha.',
                       'Selecciona solo tu historia y ponla en dos columnas.',
                       'Acomoda tu ilustración con Ajustar texto → Cuadrado.',
                       'Agrega al final un recuadro «Dato real» con el dato científico de tu historia.'],
                logro=['Tu página tiene encabezado, texto en dos columnas, la imagen rodeada por el texto y el recuadro '
                       'del dato real.'],
                entrega='sube tu página en PDF o una captura de la página completa.'), xp=100, monedas=30),
            mision('Convocatoria del club', 'evidencia', leccion(
                intro='Para que el grupo de escritores crezca, hay que invitar a otros. Eso se hace con una '
                      'convocatoria.',
                saber=['Partes de una convocatoria: título llamativo, quién invita, a quién, qué hay que hacer, bases '
                       '(tema, extensión, requisitos), fecha límite, dónde entregar y qué reconocimiento hay.',
                       'Una buena convocatoria se entiende en 10 segundos: títulos grandes, poco texto y una imagen.'],
                dinamica=PAREJAS,
                pasos=['Abre un documento nuevo: Convocatoria_TuNombre.',
                       'Título llamativo en letra grande, por ejemplo «¿Te atreves a escribir el futuro?».',
                       'Escribe cada parte de la convocatoria con su subtítulo en negritas.',
                       'Agrega una imagen tuya de AutoDraw.',
                       'Pide a tu dupla que la lea en 10 segundos: ¿entendió qué tiene que hacer?'],
                logro=['Tu convocatoria tiene todas sus partes y alguien que la lee sabe cómo participar.'],
                entrega='sube tu convocatoria en PDF o una captura.'), xp=90, monedas=25),
            mision('Armamos el periódico mural', 'presencial', leccion(
                intro='Es hora de publicar. El grupo arma su periódico mural de ciencia ficción y cada dupla tiene una '
                      'tarea.',
                roles=['Dupla editora: decide el orden de las páginas y revisa que todo esté.',
                       'Dupla de portada: arma el encabezado y la portada.',
                       'Dupla de datos: prepara la sección «¿Cuánto dura un día?» con la gráfica.',
                       'Dupla de la IA: escribe «Cómo usamos la IA» (qué hizo la IA y qué hicimos nosotros).',
                       'Dupla correctora: lee todo antes de pegarlo.',
                       'Las demás duplas: cada una pega sus dos páginas de historias.'],
                dinamica=['Cada dupla prepara su parte en su lugar. Al mural pasa una sola dupla a la vez, cuando el profe '
                          'la llama.',
                          'La dupla que termina ayuda a la que va más atrasada.',
                          'Los últimos 10 minutos son la inauguración.'],
                pasos=['Impriman las páginas, la gráfica y la convocatoria.',
                       'Peguen la portada, las historias, la sección de datos y «Cómo usamos la IA».',
                       'Pongan la convocatoria en un lugar muy visible.',
                       'Inauguración: 3 voluntarios leen el inicio de su historia en voz alta.'],
                logro=['El periódico tiene portada, historias ilustradas, gráfica, la sección de la IA y la '
                       'convocatoria.']), xp=60),
            jefe('Jefe: El Robot Copión', leccion(
                intro='El Robot Copión copia todo lo que encuentra e inventa datos con toda seguridad. Solo lo vence '
                      'quien sabe cómo funciona la IA, cómo pedirle las cosas y cómo revisar lo que dice.'), [
                ('¿Qué es la rotación de un planeta?', 'Su giro sobre sí mismo', ['Su vuelta al Sol', 'Su color',
                                                                                    'Su tamaño']),
                ('¿Qué planeta tiene el día más corto?', 'Júpiter', ['Venus', 'La Tierra', 'Mercurio']),
                ('En una hoja de cálculo, ¿qué es B3?', 'La celda de la columna B y la fila 3',
                 ['La fila B y la columna 3', 'Una fórmula', 'Una gráfica']),
                ('¿Cómo aprende una IA?', 'Con muchísimos ejemplos', ['Pensando como una persona', 'Sin datos',
                                                                      'Leyendo la mente']),
                ('Una IA dice un dato que suena raro. ¿Qué haces?', 'Lo reviso en una fuente confiable',
                 ['Lo publico tal cual', 'Lo creo porque lo dijo la IA', 'Lo comparto con todos']),
                ('¿Cuál es un prompt claro?', 'Dame 3 títulos para un cuento sobre un día en Venus',
                 ['hazme un cuento', 'mejóralo todo', 'arréglalo']),
                ('¿Qué atajo deshace lo último que hiciste?', 'Ctrl + Z', ['Ctrl + C', 'Ctrl + V', 'Alt + Tab']),
                ('¿Qué parte de una convocatoria dice hasta cuándo se puede participar?', 'La fecha límite',
                 ['El título', 'Las bases', 'La imagen']),
            ]),
        ]},
    ],
}
