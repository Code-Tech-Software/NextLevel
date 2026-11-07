"""Mundo 2 · ES-DAT307 Inventario del futuro: los inventos de Leonardo da Vinci, pistas, inferencias y conclusiones,
prompts efectivos (y seguros), la IA como lluvia de ideas, la ficha museográfica y un museo virtual del grupo en una
presentación compartida."""
from .base import CARPETA, EDAD_IA, PAREJAS, clasifica, jefe, leccion, mision

JUEGOS = {
    'clasifica_pista_inferencia': clasifica('¿Pista, inferencia o conclusión?', '🔎', 'El caso del pastel '
                                            'desaparecido. ¿Es algo que se observa, una idea probable o la respuesta '
                                            'final con pruebas?', [
        ('Pista (lo observo)', '👀', ['El plato del pastel está vacío', 'La ventana de la cocina está abierta',
                                      'Hay huellas de lodo junto a la mesa', 'El perro tiene betún en el hocico',
                                      'La mamá de Beto dice que le dio una rebanada']),
        ('Inferencia (probablemente)', '🤔', ['Probablemente alguien se comió el pastel',
                                              'Tal vez el perro entró por la ventana',
                                              'Puede ser que las huellas sean del perro',
                                              'Quizá Beto se comió su rebanada en el recreo']),
        ('Conclusión (con pruebas)', '⚖️', ['Por el betún y las huellas, concluimos que fue el perro',
                                            'En conclusión, el perro entró por la ventana abierta',
                                            'Por lo tanto, Beto no fue: su rebanada se la dio su mamá']),
    ], rondas=12),
    'clasifica_prompt_seguro': clasifica('¿Efectivo, vago o riesgoso?', '🛡️', 'Un buen prompt es claro… y seguro. '
                                         '¿Este prompt funciona, no dice nada o pone en riesgo a alguien?', [
        ('Efectivo', '🎯', ['Dame 5 ideas de inventos para ahorrar agua en la escuela',
                            'Explica en 3 pasos cómo funcionaría un traje de buceo del futuro',
                            'Haz una lista de materiales ligeros para una máquina voladora',
                            'Sugiere 3 nombres para mi invento que limpia el aire']),
        ('Vago', '😶', ['inventos', 'algo del futuro', 'ayúdame con mi proyecto', 'dime cosas']),
        ('Riesgoso', '🚫', ['Me llamo Ana López y vivo en calle Pino 23, ¿qué invento?',
                            'Hazme toda la ficha para entregarla como si fuera mía',
                            'Esta es la contraseña de mi correo, ¿es segura?',
                            'Te mando la foto de mi compañero para que la cambies']),
    ], rondas=12),
}

MUNDO = {
    'nombre': 'Taller Da Vinci', 'tema': 'futuro',
    'descripcion': 'ES-DAT307 · Inventario del futuro. Hace más de 500 años, Leonardo da Vinci llenó cuadernos con '
                   'máquinas voladoras, un traje de buceo y hasta un robot con forma humana. Piensa como detective con '
                   'pistas, inferencias y conclusiones, usa la IA como compañera de ideas con prompts efectivos y crea '
                   'tu invento para el museo virtual del grupo. Pregunta guía: así como da Vinci, ¿qué increíbles '
                   'inventos podrías imaginar hoy?',
    'niveles': [
        {'nombre': 'El cuaderno de Leonardo', 'cofre': 25, 'misiones': [
            mision('Inventos de hace 500 años', 'texto', leccion(
                intro='Leonardo da Vinci (1452-1519) fue pintor de la Mona Lisa, pero también inventor. En sus '
                      'cuadernos, escritos al revés como en un espejo, dibujó una máquina voladora con alas de '
                      'murciélago, un paracaídas, un traje de buceo con tubos para respirar y un caballero robot que se '
                      'movía con poleas y cables. Casi nada se construyó en su época… pero muchas de esas ideas hoy son '
                      'realidad.',
                pasos=['¿Cuál de los inventos de Leonardo ya existe hoy? ¿Cómo se llama ahora?',
                       '¿Por qué crees que no los pudo construir hace 500 años?',
                       'Si tuvieras su cuaderno, ¿qué invento le agregarías tú?'],
                entrega='escribe tus tres respuestas aquí abajo.'), xp=60),
            mision('Leonardo, inventor del futuro', 'cuestionario', leccion(
                intro='Conoce los inventos que Leonardo imaginó antes de que existiera la tecnología para hacerlos.',
                saber=['Máquina voladora (ornitóptero): alas que se movían como las de un pájaro, con la fuerza del '
                       'piloto. Se inspiró en observar aves y murciélagos.',
                       'Tornillo aéreo: una hélice en espiral que debía girar para elevarse. Es el abuelo del '
                       'helicóptero.',
                       'Paracaídas en forma de pirámide: en el año 2000 un paracaidista construyó uno con su diseño, '
                       'saltó… y funcionó.',
                       'Traje de buceo: de cuero, con tubos de caña conectados a una boya para respirar bajo el agua.',
                       'Caballero robot (1495): una armadura que se sentaba, movía los brazos y la cabeza con poleas y '
                       'cables.',
                       'Su método: observar la naturaleza, dibujar con detalle y escribir notas de cómo funcionaría.']),
                xp=60, preguntas=[
                ('¿En qué se inspiró Leonardo para su máquina voladora?', 'En las aves y los murciélagos',
                 ['En los cohetes', 'En los aviones de su época', 'En los globos de helio']),
                ('¿Qué invento actual se parece a su tornillo aéreo?', 'El helicóptero',
                 ['El submarino', 'La bicicleta', 'El teléfono']),
                ('¿Qué pasó en el año 2000 con su diseño de paracaídas?', 'Lo construyeron, lo probaron y funcionó',
                 ['Se perdió para siempre', 'Se prohibió', 'Lo convirtieron en avión']),
                ('¿Cómo respiraba el buzo con el traje de Leonardo?', 'Con tubos conectados a una boya en la superficie',
                 ['Con un tanque de oxígeno', 'Aguantando la respiración', 'Con branquias']),
                ('¿Cómo se movía su caballero robot?', 'Con poleas y cables', ['Con electricidad', 'Con pilas',
                                                                               'Con un motor de gasolina']),
                ('¿Cuál era el método de Leonardo para inventar?', 'Observar, dibujar con detalle y escribir notas',
                 ['Copiar inventos de otros', 'Esperar a que se le ocurriera algo', 'Construir sin planear']),
            ]),
            mision('¿Qué sé de la IA?', 'texto', leccion(
                intro='Antes de usar la IA para inventar, revisa qué sabes. No hay respuestas malas: al final del mundo '
                      'vas a comparar lo que escribiste hoy con lo que aprendiste.',
                pasos=['Explica con tus palabras qué es la inteligencia artificial.',
                       '¿Qué es un prompt? Escribe un ejemplo de un prompt que le pedirías a una IA para inventar algo.',
                       '¿Qué cosas NO le pedirías nunca a una IA? Menciona 2.'],
                entrega='escribe tus respuestas aquí abajo.'), xp=50),
        ]},
        {'nombre': 'Pensar como detective', 'cofre': 30, 'misiones': [
            mision('Pistas, inferencias y conclusiones', 'cuestionario', leccion(
                intro='Los inventores, los científicos y los detectives piensan igual: observan pistas, sacan ideas '
                      'probables y, cuando tienen suficientes pruebas, llegan a una conclusión.',
                saber=['Pista (evidencia): lo que puedes observar o comprobar. «El piso está mojado».',
                       'Inferencia: una idea probable que sacas de las pistas. Puede cambiar si aparece una pista nueva. '
                       'Se reconoce por palabras como «tal vez», «probablemente» o «puede ser».',
                       'Conclusión: la respuesta final después de revisar TODAS las pistas. Se apoya en hechos y usa '
                       'palabras como «por lo tanto» o «en conclusión».',
                       'Error de detective: sacar una conclusión con una sola pista.']), xp=60, preguntas=[
                ('«Hay un paraguas mojado junto a la puerta» es…', 'Una pista', ['Una inferencia', 'Una conclusión',
                                                                                 'Una opinión']),
                ('«Probablemente está lloviendo afuera» es…', 'Una inferencia', ['Una pista', 'Una conclusión',
                                                                                 'Un hecho comprobado']),
                ('¿Qué necesita una conclusión?', 'Apoyarse en todas las pistas', ['Una sola pista',
                                                                                  'Lo que yo quiero que pase',
                                                                                  'Lo que dice la mayoría']),
                ('¿Qué palabra indica una inferencia?', 'Probablemente', ['Por lo tanto', 'En conclusión',
                                                                          'Comprobado']),
                ('Aparece una pista nueva que contradice tu inferencia. ¿Qué haces?', 'Cambio mi inferencia',
                 ['La ignoro', 'Me enojo con la pista', 'Mantengo mi idea como sea']),
                ('¿Cuál es el error de detective?', 'Sacar una conclusión con una sola pista',
                 ['Observar con cuidado', 'Revisar todas las pistas', 'Cambiar de idea con pruebas nuevas']),
            ]),
            mision('¿Pista, inferencia o conclusión?', 'juego', leccion(
                intro='El pastel de la fiesta desapareció. Clasifica cada frase del caso.',
                tip='Las inferencias dudan («tal vez»); las conclusiones cierran el caso con pruebas («por lo '
                    'tanto»).'), juego='clasifica_pista_inferencia'),
            mision('La caja misteriosa', 'presencial', leccion(
                intro='El profe trae una caja cerrada con un objeto adentro. Nadie puede abrirla: solo con pistas, '
                      'inferencias y una conclusión lo van a descubrir.',
                dinamica=['En duplas, con una hoja dividida en 3 columnas: Pistas · Inferencias · Conclusión.',
                          'Semáforo en 🟡. Las preguntas se hacen levantando la mano, una por dupla.',
                          'Nadie dice su respuesta en voz alta hasta el final.'],
                pasos=['Pista 1: el profe agita la caja. Anoten qué escuchan y una inferencia.',
                       'Pista 2: un voluntario la carga y dice si pesa poco o mucho. Nueva inferencia.',
                       'Pista 3: cada dupla hace una pregunta de sí o no. Anoten las respuestas.',
                       'Escriban su conclusión con la frase «Por lo tanto, creemos que es… porque…».',
                       'El profe abre la caja. ¿Qué pista fue la más útil? ¿Cuál los confundió?'],
                logro=['Tu hoja tiene al menos 3 pistas, 3 inferencias y una conclusión con su porque.']), xp=50),
            mision('Caso: el robot que no camina', 'texto', leccion(
                intro='En el taller, el robot de cartón de Mía dejó de caminar justo el día de la exposición. Lee las '
                      'pistas y resuelve el caso como detective.',
                saber=['Pista 1: ayer en la tarde el robot caminaba perfecto.',
                       'Pista 2: Mía lo dejó encendido toda la noche.',
                       'Pista 3: hoy la luz de la pila no prende.',
                       'Pista 4: una rueda está floja, pero el robot de su amigo también tiene una rueda floja y sí '
                       'camina.'],
                pasos=['Escribe 2 inferencias (usa «tal vez» o «probablemente»).',
                       '¿Qué pista descarta que el problema sea la rueda?',
                       'Escribe tu conclusión con «Por lo tanto…» y di en qué pistas te apoyas.',
                       '¿Qué harías para comprobar tu conclusión?'],
                logro=['Tus inferencias usan palabras de duda y tu conclusión se apoya en al menos 2 pistas.'],
                entrega='escribe tus respuestas aquí abajo.'), xp=70, monedas=20),
        ]},
        {'nombre': 'Lluvia de inventos', 'cofre': 30, 'misiones': [
            mision('Un problema, un invento', 'texto', leccion(
                intro='Leonardo no inventaba por inventar: cada máquina resolvía algo, como volar o respirar bajo el '
                      'agua. Todo gran invento empieza con un problema.',
                pasos=['Escribe 3 problemas reales de tu escuela, tu casa o tu ciudad (por ejemplo: el tráfico, la '
                       'basura, el calor en el salón).',
                       'Elige uno y escribe a quién le afecta y por qué.',
                       'Imagina un invento del año 2050 que lo resuelva: ¿qué haría?',
                       'Escribe una inferencia: «Probablemente mi invento ayudaría a… porque…».'],
                logro=['Tienes un problema real, a quién le afecta y la idea de tu invento.'],
                entrega='escribe tu problema y tu idea aquí abajo.'), xp=60),
            mision('Prompts efectivos', 'cuestionario', leccion(
                intro='En el mundo pasado aprendiste los 3 ingredientes. Ahora conoce las características de un prompt '
                      'efectivo… y seguro.',
                saber=['Claro: dice exactamente qué quieres. Específico: da detalles (cuántas ideas, para quién, de qué '
                       'tema).',
                       'Con contexto: explica la situación. «Es para un museo de inventos del futuro de 5.º».',
                       'Con formato: pide cómo quieres la respuesta (lista, 3 pasos, tabla, 5 renglones).',
                       'Seguro: sin datos personales, sin fotos de otras personas y sin pedir que la IA haga tu trabajo '
                       'para entregarlo como tuyo.',
                       EDAD_IA]), xp=60, preguntas=[
                ('¿Qué hace que un prompt sea específico?', 'Que da detalles como cuántas ideas y de qué tema',
                 ['Que es muy corto', 'Que tiene emojis', 'Que está en mayúsculas']),
                ('«Es para un museo de inventos de 5.º» es…', 'Contexto', ['Formato', 'Un dato personal',
                                                                          'Un prompt vago']),
                ('«Responde en una lista de 5 ideas» es…', 'Formato', ['Contexto', 'Un límite de edad',
                                                                       'Una conclusión']),
                ('¿Cuál prompt es seguro?', 'Dame 5 ideas de inventos para ahorrar agua en la escuela',
                 ['Me llamo Ana López y vivo en calle Pino 23, ¿qué invento?',
                  'Te mando la foto de mi compañero para que la cambies',
                  'Esta es mi contraseña, ¿es segura?']),
                ('¿Por qué no se le pide a la IA que haga toda tu ficha?', 'Porque no sería tu trabajo y no aprenderías',
                 ['Porque la IA se cansa', 'Porque la IA no sabe escribir', 'Porque está prohibido escribir']),
                ('¿Cuál es el prompt más efectivo?', 'Haz una lista de materiales ligeros para una máquina voladora',
                 ['inventos', 'dime cosas', 'algo del futuro']),
            ]),
            mision('¿Efectivo, vago o riesgoso?', 'juego', leccion(
                intro='Clasifica cada prompt. Ojo con los que ponen en riesgo tus datos o los de alguien más.'),
                juego='clasifica_prompt_seguro'),
            mision('Lluvia de ideas con IA', 'texto', leccion(
                intro='La IA puede ser una compañera de ideas que nunca se cansa. Pero el inventor eres tú: tú eliges y '
                      'tú decides.',
                saber=[EDAD_IA,
                       'La IA propone; tú eliges, mezclas y mejoras. Si solo copias, el invento no es tuyo.'],
                dinamica=['5 minutos para escribir tu prompt en silencio (semáforo en 🔴).',
                          'El profe usa algunos prompts del grupo en el proyector. Todos leen las respuestas.',
                          'Cada quien decide qué le sirve para su propio invento.'],
                pasos=['Escribe un prompt efectivo que pida 5 ideas para mejorar tu invento (claro, específico, con '
                       'contexto y formato).',
                       'Observa las respuestas de la IA en el proyector.',
                       'Elige una idea (de la IA o tuya) y explica por qué la elegiste.',
                       'Escribe una idea de la IA que NO usarías y por qué.'],
                logro=['Tu prompt cumple las características y tu elección tiene una razón.'],
                entrega='escribe tu prompt, la idea que elegiste y la que no usarías, con sus razones.'),
                xp=70, monedas=20),
        ]},
        {'nombre': 'Ficha e imagen del invento', 'cofre': 35, 'misiones': [
            mision('Boceto al estilo Leonardo', 'evidencia', leccion(
                intro='Leonardo dibujaba sus inventos con todas sus partes señaladas y notas de cómo funcionaban. Haz '
                      'lo mismo con el tuyo.',
                material=['Una hoja blanca', 'Lápiz y colores'],
                pasos=['Dibuja tu invento grande, en el centro de la hoja.',
                       'Señala con flechas al menos 4 partes y escribe para qué sirve cada una.',
                       'Agrega una vista extra: de lado, desde arriba o por dentro.',
                       'Escribe arriba el nombre del invento y abajo «Taller de (tu nombre), 2050».',
                       'Reto Leonardo: escribe el nombre del invento al revés, como en un espejo.'],
                logro=['Tu boceto tiene nombre, 4 partes señaladas y una vista extra.'],
                entrega='sube una foto de tu boceto.'), xp=80, monedas=25),
            mision('Ficha museográfica', 'evidencia', leccion(
                intro='En los museos, junto a cada objeto hay una ficha (cédula) que explica qué es. Crea la de tu '
                      'invento en una diapositiva.',
                saber=['Partes de la ficha: nombre del invento, inventor(a), año, sala del museo (Transporte, Salud, '
                       'Hogar o Planeta), problema que resuelve, cómo funciona (3 pasos), materiales y un dato '
                       'curioso.',
                       'Una ficha se lee de pie y rápido: frases cortas, títulos en negritas y letra de al menos 18 '
                       'puntos.'],
                dinamica=PAREJAS,
                pasos=[f'Abre PowerPoint o Presentaciones de Google y guarda el archivo como Ficha_TuNombre en '
                       f'{CARPETA} › DaVinci.',
                       'Usa una diapositiva con título y contenido. El título es el nombre de tu invento.',
                       'Escribe cada parte de la ficha con su subtítulo en negritas.',
                       'Deja un espacio a la derecha para la imagen.',
                       'Pídele a tu dupla que la lea en 30 segundos: ¿entendió qué hace tu invento?'],
                logro=['Tu ficha tiene todas sus partes, frases cortas y se entiende en 30 segundos.'],
                entrega='sube una captura de tu ficha.'), xp=100, monedas=30),
            mision('Imagen del invento con IA', 'evidencia', leccion(
                intro='Tu ficha necesita una imagen. La puedes crear con IA usando un buen prompt de imagen (tu profe la '
                      'genera) o hacerla tú con tu boceto.',
                saber=[EDAD_IA,
                       'Prompt de imagen: qué es + cómo se ve (forma, tamaño, materiales, colores) + dónde está + '
                       'estilo («dibujo técnico de cuaderno antiguo», «fotografía realista», «ilustración 3D»).',
                       'Toda imagen hecha con IA lleva su etiqueta: «Imagen generada con IA».'],
                pasos=['Escribe tu prompt de imagen usando tu boceto como guía.',
                       'Tu profe genera la imagen (o usas la herramienta que autorice). Si no te convence, cambia una '
                       'sola cosa del prompt.',
                       'Inserta la imagen en tu ficha con su etiqueta. Si prefieres, usa la foto de tu boceto.',
                       'Compara: ¿qué se parece a tu boceto y qué no?'],
                ojo=['No se crean imágenes de personas reales ni de compañeros.'],
                logro=['Tu ficha tiene imagen con su etiqueta y tu prompt describe forma, materiales y estilo.'],
                entrega='sube una captura de tu ficha con la imagen y escribe tu prompt en el comentario.'),
                xp=90, monedas=25),
        ]},
        {'nombre': 'Museo virtual', 'cofre': 40, 'misiones': [
            mision('Abre tu sala', 'evidencia', leccion(
                intro='Todas las fichas se juntan en el Museo de Inventos del Futuro: una presentación del grupo que se '
                      'recorre como un museo de verdad.',
                saber=['Tu profe comparte la presentación del museo (por ejemplo, en Classroom). Cada quien trabaja SOLO '
                       'en su diapositiva: la de su número de lista.',
                       'Copiar tu ficha: en tu archivo, clic derecho en la miniatura → Copiar; en el museo, clic en tu '
                       'lugar → Pegar.',
                       'El museo tiene portada, una diapositiva de índice y una «sala» por tema.'],
                dinamica=['Entran al museo por turnos de fila, cuando el profe lo indica, para no encimarse.',
                          'Nadie mueve, borra ni cambia la diapositiva de otro. Si alguien lo hace por error: Ctrl + Z y '
                          'avisa al profe.'],
                pasos=['Abre la presentación del museo que compartió tu profe.',
                       'Busca la diapositiva con tu número de lista.',
                       'Pega tu ficha completa (con imagen) en tu lugar.',
                       'Revisa que tu ficha esté en la sala correcta y que no tapaste nada de nadie.'],
                logro=['Tu ficha está en el museo, en tu lugar y en la sala correcta.'],
                entrega='sube una captura de tu diapositiva dentro del museo.'), xp=80, monedas=25),
            mision('Recorrido y retroalimentación', 'presencial', leccion(
                intro='Día de inauguración: recorre el museo como visitante y deja comentarios de detective.',
                dinamica=['El profe proyecta el museo o cada quien lo abre en modo presentación (solo para ver).',
                          'Cada alumno comenta 3 inventos que le asigna el profe. Semáforo en 🟡.'],
                pasos=['Lee la ficha de cada invento que te tocó.',
                       'Escribe en una nota (o en un comentario del archivo, si el profe lo permite): 1 estrella '
                       '(algo que te gustó), 1 inferencia («Infiero que tu invento también serviría para… porque…») y '
                       '1 deseo (algo que mejorarías).',
                       'Lee los comentarios que te dejaron a ti.'],
                logro=['Dejaste 3 comentarios con estrella, inferencia y deseo, amables y útiles.']), xp=50),
            mision('Ajustes del curador', 'evidencia', leccion(
                intro='Un buen inventor convierte los comentarios en mejoras.',
                pasos=['Lee los comentarios que recibiste y elige 2 para aplicar.',
                       'Mejora tu ficha (texto, imagen o diseño).',
                       'Agrega abajo, en letra chica: «Versión 2: mejoré… gracias a la sugerencia de…».'],
                logro=['Tu ficha tiene 2 mejoras y la nota de versión 2.'],
                entrega='sube una captura de tu ficha mejorada y escribe qué cambiaste.'), xp=70, monedas=20),
            mision('¿Qué opinas?', 'texto', leccion(
                intro='Cierra el proyecto como lo haría un inventor: revisando qué aprendiste.',
                pasos=['Relee lo que escribiste en «¿Qué sé de la IA?». ¿Qué cambiarías ahora de tu respuesta?',
                       '¿En qué te ayudó la IA y en qué no?',
                       'Del 1 al 5, ¿qué tan bien usaste pistas, inferencias y conclusiones? ¿Por qué?',
                       '¿Qué invento de un compañero te gustaría que existiera de verdad?'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            jefe('Jefe: El Inventor Impostor', leccion(
                intro='El Inventor Impostor copia ideas ajenas y saca conclusiones sin pruebas. Demuéstrale que tú '
                      'piensas como Leonardo: observas, infieres, concluyes con pruebas y usas la IA con '
                      'responsabilidad.'), [
                ('¿Qué invento actual se parece al tornillo aéreo de Leonardo?', 'El helicóptero',
                 ['El tren', 'El teléfono', 'La lavadora']),
                ('«Tal vez llovió anoche» es…', 'Una inferencia', ['Una pista', 'Una conclusión', 'Un hecho']),
                ('¿En qué se apoya una conclusión?', 'En todas las pistas', ['En una sola pista', 'En una corazonada',
                                                                            'En lo que dice un amigo']),
                ('«Responde en una lista de 5 ideas» es una característica de…', 'Formato',
                 ['Contexto', 'Seguridad', 'Inferencia']),
                ('¿Cuál prompt es riesgoso?', 'Me llamo Ana López y vivo en calle Pino 23, ¿qué invento?',
                 ['Dame 5 ideas para ahorrar agua', 'Sugiere 3 nombres para mi invento',
                  'Explica en 3 pasos cómo funcionaría']),
                ('¿Qué debe llevar una imagen hecha con IA en tu ficha?', 'La etiqueta «Imagen generada con IA»',
                 ['Tu firma como si la hubieras dibujado', 'Nada', 'El nombre de otro compañero']),
                ('¿Qué parte de la ficha explica para qué sirve el invento?', 'El problema que resuelve',
                 ['El año', 'La sala', 'El nombre del inventor']),
                ('En el museo compartido, alguien borró tu ficha por error. ¿Qué se hace?',
                 'Ctrl + Z y avisar al profe', ['Borrar la de otro', 'Cerrar todo y no decir nada',
                                                'Empezar el museo de nuevo']),
            ]),
        ]},
    ],
}
