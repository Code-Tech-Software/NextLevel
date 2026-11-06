"""Mundo 2 · Escudo marciano: problemas para vivir en Marte, ideas creativas y tecnología responsable, dividir un
problema en subproblemas, un clicker con amenazas en MakeCode Arcade y un mini torneo con tabla de récords."""
from .base import LEYENDA_MAKECODE, MAKECODE, PAREJAS, clasifica, jefe, leccion, makecode, mision

JUEGOS = {
    'clasifica_marte': clasifica('¿Tierra o Marte?', '🪐', 'Datos reales: ¿de qué planeta hablan?', [
        ('Tierra', '🌎', ['Su atmósfera es gruesa y frena la radiación del Sol',
                          'Tiene un campo magnético que la protege como escudo',
                          'El aire tiene oxígeno que podemos respirar', 'Su temperatura promedio es de unos 15 °C',
                          'Su día dura 24 horas', 'Tiene océanos de agua líquida']),
        ('Marte', '🔴', ['Su atmósfera tiene menos del 1 % de la presión de la nuestra',
                         'Su aire es casi todo dióxido de carbono',
                         'Perdió su campo magnético hace miles de millones de años',
                         'Su temperatura promedio es de unos 60 °C bajo cero',
                         'Su día dura 24 horas y 37 minutos', 'Tiene tormentas de polvo que cubren todo el planeta',
                         'Ahí pesarías un poco más de un tercio de lo que pesas aquí']),
    ], rondas=12),
    'clasifica_tecnologia': clasifica('¿Tecnología constructiva o irresponsable?', '⚖️', 'La misma tecnología puede '
                                      'ayudar o dañar. Decide cómo se está usando.', [
        ('Constructiva', '✅', ['Un rover que estudia el suelo de Marte sin dañarlo',
                                'Esterilizar las naves para no llevar microbios de la Tierra',
                                'Usar un dron para buscar personas perdidas',
                                'Pedirle a la IA ideas y luego verificarlas',
                                'Compartir tu juego con el enlace y dar crédito a quien te ayudó',
                                'Reciclar las piezas de una computadora vieja']),
        ('Irresponsable', '⚠️', ['Dejar basura espacial en la órbita de Marte',
                                 'Publicar la foto de un compañero sin su permiso',
                                 'Copiar el juego de otro y decir que es tuyo',
                                 'Usar un dron para espiar el patio del vecino',
                                 'Pedirle a la IA la tarea completa y entregarla como tuya',
                                 'Tirar pilas y aparatos a la basura común']),
    ], rondas=12),
}

MUNDO = {
    'nombre': 'Protocolo Marte', 'tema': 'marte',
    'descripcion': 'Escudo marciano. La atmósfera de Marte es tan delgada que no frena la radiación del Sol: cualquier '
                   'misión humana estaría en peligro. Investiga los problemas de vivir allá, diseña un escudo '
                   'tecnológico, prográmalo como videojuego y organiza un torneo. Pregunta guía: ¿cómo hacer que Marte '
                   'sea seguro para el ser humano?',
    'niveles': [
        {'nombre': 'Briefing: Planeta Rojo', 'cofre': 25, 'misiones': [
            mision('Alerta de radiación', 'texto', leccion(
                intro='Desde hace siglos los científicos sueñan con hacer Marte habitable. Pero hay un problema enorme: '
                      'su atmósfera es tan delgada que no detiene la radiación del Sol. En Marte, cada partícula que '
                      'llega del Sol puede ser peligrosa.',
                pasos=['¿Qué te llevarías a Marte para sobrevivir el primer día? Haz una lista de 5 cosas.',
                       '¿Por qué crees que en la Tierra no nos afecta tanto la radiación del Sol?',
                       '¿Te irías a vivir a Marte? Explica por qué sí o por qué no.'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('Marte contra la Tierra', 'cuestionario', leccion(
                intro='Para resolver un problema primero hay que conocer los hechos. Este es el expediente de Marte.',
                saber=['La Tierra tiene dos escudos: una atmósfera gruesa y un campo magnético (la magnetosfera) que '
                       'desvía las partículas del Sol.',
                       'Marte perdió su campo magnético hace unos 4 mil millones de años y, poco a poco, el viento '
                       'solar se llevó gran parte de su atmósfera.',
                       'Hoy su atmósfera tiene menos del 1 % de la presión de la Tierra y es casi toda dióxido de '
                       'carbono: no se puede respirar.',
                       'Temperatura promedio: unos 60 °C bajo cero. Gravedad: 38 % de la terrestre.',
                       'Un día en Marte (el tiempo que tarda en girar sobre sí mismo) dura 24 horas y 37 minutos.',
                       'Un mensaje de la Tierra tarda entre 3 y 22 minutos en llegar a Marte: no hay llamadas en vivo.']),
                xp=60, preguntas=[
                ('¿Qué dos escudos protegen a la Tierra de la radiación del Sol?',
                 'Su atmósfera gruesa y su campo magnético', ['Las nubes y la Luna', 'Los océanos y los volcanes',
                                                              'Los satélites y los aviones']),
                ('¿Por qué la atmósfera de Marte es tan delgada?',
                 'Perdió su campo magnético y el viento solar se llevó el aire',
                 ['Porque está muy cerca del Sol', 'Porque los rovers la gastaron', 'Porque Marte es más grande']),
                ('¿De qué está hecho casi todo el aire de Marte?', 'Dióxido de carbono', ['Oxígeno', 'Vapor de agua',
                                                                                         'Helio']),
                ('¿Cuánto dura un día en Marte?', '24 horas y 37 minutos', ['12 horas', '3 días', '1 año']),
                ('¿Cuánto tarda un mensaje de la Tierra en llegar a Marte?', 'Entre 3 y 22 minutos',
                 ['Un segundo', 'Una semana', 'Lo mismo que un mensaje de WhatsApp']),
                ('¿Cuál es la temperatura promedio en Marte?', 'Unos 60 °C bajo cero',
                 ['Unos 25 °C', 'Unos 100 °C', 'Igual que en la Tierra']),
            ]),
            mision('¿Tierra o Marte?', 'juego', leccion(
                intro='Clasifica cada dato: ¿es de la Tierra o de Marte?',
                tip='Si el dato suena peligroso para vivir, probablemente es de Marte.'), juego='clasifica_marte'),
        ]},
        {'nombre': 'Ideas que salvan colonias', 'cofre': 30, 'misiones': [
            mision('Lluvia de problemas marcianos', 'presencial', leccion(
                intro='Antes de inventar soluciones hay que tener claros TODOS los problemas. Los equipos de la NASA '
                      'hacen esto con notas adhesivas.',
                material=['Notas adhesivas o papelitos', 'Plumones', 'Un pedazo de pizarrón o una cartulina por equipo'],
                dinamica=['Equipos de 4. El Productor controla el tiempo.',
                          'Ronda 1 (4 minutos, en silencio): cada quien escribe problemas de vivir en Marte, uno por '
                          'papel.',
                          'Ronda 2 (4 minutos, en voz baja): pegan todo y agrupan los papeles parecidos.',
                          'Regla: en la lluvia de ideas no se critica ninguna idea.'],
                pasos=['Escriban problemas: radiación, frío, aire, comida, agua, tormentas de polvo, comunicación, '
                       'gravedad baja, soledad…',
                       'Agrupen los papeles en familias y pónganle nombre a cada grupo.',
                       'Voten (cada quien 2 puntitos) el problema más grave.',
                       'Tomen foto de su mapa de problemas.'],
                logro=['Su mapa tiene al menos 10 problemas agrupados en familias con nombre.']), xp=50),
            mision('Ideas locas pero útiles', 'texto', leccion(
                intro='Una idea creativa no es solo una idea rara: es novedosa Y útil. Hoy entrenas ese músculo.',
                saber=['Idea creativa = novedosa (nadie la ha pensado así) + útil (sí resuelve el problema).',
                       'Truco «¿Y si…?»: cambia una parte del problema. ¿Y si la casa estuviera bajo tierra? ¿Y si el '
                       'escudo fuera de agua?',
                       'Truco «combina»: une dos cosas que no tienen que ver (una sombrilla + un imán).'],
                pasos=['Elige el problema que más votó tu equipo (o la radiación).',
                       'Escribe 1 idea normal, 1 idea muy loca y 1 idea que combine las dos.',
                       'Califica cada idea del 1 al 5 en: ¿es novedosa?, ¿es útil?, ¿es posible?',
                       'Elige tu mejor idea y explica en 3 renglones cómo funcionaría.'],
                logro=['Tu idea elegida es novedosa y además explicas cómo resuelve el problema.'],
                entrega='escribe tus ideas y calificaciones aquí abajo.'), xp=60),
            mision('¿Tecnología constructiva o irresponsable?', 'juego', leccion(
                intro='Ir a Marte también tiene reglas: hay que usar la tecnología de forma constructiva y responsable. '
                      'Decide en cada caso.',
                saber=['Uso constructivo: ayuda a las personas o al planeta y respeta a los demás.',
                       'Uso irresponsable: daña, engaña, invade la privacidad o deja basura.',
                       'La «protección planetaria» es una regla real: las naves se esterilizan para no llevar microbios '
                       'de la Tierra a otros planetas.']), juego='clasifica_tecnologia'),
        ]},
        {'nombre': 'Diseña el escudo', 'cofre': 30, 'misiones': [
            mision('Escudos que ya existen', 'cuestionario', leccion(
                intro='Antes de inventar, revisa qué han propuesto los científicos. Muchas buenas ideas mejoran otras '
                      'que ya existen.',
                saber=['Vivir bajo tierra: cubrir las casas con 2 o 3 metros de suelo marciano frena gran parte de la '
                       'radiación.',
                       'Tubos de lava: cuevas naturales que dejaron antiguos volcanes y que podrían servir de refugio.',
                       'Muros de agua o hielo: el agua es muy buena para frenar la radiación.',
                       'En 2017, científicos de la NASA propusieron un escudo magnético colocado entre Marte y el Sol, '
                       'como una magnetosfera artificial.',
                       'MOXIE, un aparato del rover Perseverance, logró fabricar oxígeno a partir del aire de Marte.']),
                xp=60, preguntas=[
                ('¿Por qué cubrir las casas con suelo marciano ayuda a los astronautas?', 'Porque frena la radiación',
                 ['Porque las hace más bonitas', 'Porque da oxígeno', 'Porque las hace flotar']),
                ('¿Qué es un tubo de lava?', 'Una cueva natural que dejó un antiguo volcán',
                 ['Un tubo para tomar agua', 'Un cohete', 'Una tormenta de polvo']),
                ('¿Qué material es muy bueno para frenar la radiación?', 'El agua o el hielo',
                 ['El papel', 'El aire de Marte', 'El cristal delgado']),
                ('¿Qué propusieron científicos de la NASA en 2017?',
                 'Un escudo magnético entre Marte y el Sol', ['Mudar Marte de órbita', 'Pintar Marte de azul',
                                                              'Llenar Marte de árboles en un año']),
                ('¿Qué logró MOXIE en el rover Perseverance?', 'Fabricar oxígeno con el aire de Marte',
                 ['Encontrar extraterrestres', 'Llenar Marte de agua', 'Crear un campo magnético']),
            ]),
            mision('Ficha técnica del escudo', 'evidencia', leccion(
                intro='Tu estudio presenta su propuesta de escudo como lo haría un equipo de ingeniería: en una ficha '
                      'técnica clara.',
                roles=['Piloto: escribe la ficha en la computadora.', 'Copiloto: revisa ortografía y datos.',
                       'Tester: hace el dibujo con las partes señaladas.', 'Productor: cuida el tiempo (20 minutos).'],
                pasos=['Abre un documento nuevo y ponle de título el nombre de su escudo.',
                       'Problema que resuelve (con un dato real del expediente de Marte).',
                       'Cómo funciona, en 3 pasos numerados.',
                       'Materiales y de dónde sale la energía.',
                       '¿A quién beneficia? (el bien común) y ¿qué riesgo tiene y cómo lo cuidarían?',
                       'Inserta una foto del dibujo con las partes señaladas.',
                       'Guarda como Escudo_NombreDelEstudio en su carpeta.'],
                logro=['La ficha tiene problema, funcionamiento en 3 pasos, materiales, beneficio, riesgo y dibujo.'],
                entrega='sube una captura o el PDF de su ficha técnica.'), xp=100, monedas=30),
            mision('Divide y vencerás', 'evidencia', leccion(
                intro='«Haz un videojuego» es un problema gigante. Los programadores lo parten en subproblemas pequeños '
                      'que sí se pueden resolver uno por uno. Eso se llama descomposición.',
                saber=['Descomponer: dividir un problema grande en partes pequeñas y manejables.',
                       'Cada subproblema debe poder probarse por separado (por ejemplo: «¿ya suma puntos el clic?»).',
                       'Ejemplo: «hacer un pastel» → comprar ingredientes, mezclar, hornear, decorar.'],
                pasos=['En una hoja, escribe al centro: «Juego: Escudo marciano».',
                       'Dibuja 6 ramas, una por subproblema: escenario, jugador, clic que activa la atmósfera, '
                       'amenazas (radiación), escudo y mejoras, cómo se gana o se pierde.',
                       'En cada rama escribe qué bloque o categoría de MakeCode crees que necesitas.',
                       'Numera las ramas en el orden en que las programarías.'],
                logro=['Tu mapa tiene 6 subproblemas, el orden para programarlos y los bloques de cada uno.'],
                entrega='sube una foto de tu mapa de subproblemas.'), xp=90, monedas=25),
        ]},
        {'nombre': 'Programa el escudo', 'cofre': 35, 'misiones': [
            makecode('Sprint 1: activa la atmósfera', leccion(
                intro='Meta del sprint (15 minutos): cada clic activa un poco la atmósfera de Marte. Al llegar a 100 % '
                      'la colonia está a salvo.',
                saber=['Aquí el puntaje representa el porcentaje de atmósfera activada.',
                       '«mostrar» (cajón Juego) enseña un título y un subtítulo antes de empezar.',
                       LEYENDA_MAKECODE],
                dinamica=PAREJAS,
                pasos=['Crea un proyecto nuevo: EscudoMarciano_TuNombre.',
                       'Fondo naranja o rojo y un sprite de tipo Player llamado marte (dibuja el planeta o tu base).',
                       'Agrega el «mostrar» con el nombre del juego y la instrucción.',
                       'Crea la variable porClic; «marcar puntaje en 0».',
                       'Programa el botón A para sumar porClic y el evento «en puntaje 100» para ganar.'],
                logro=['Al presionar A sube la atmósfera y al llegar a 100 ganas.'],
                entrega='sube una captura de tus bloques.'), '''
al inicio
    establecer color de fondo a [naranja]
    establecer marte como objeto [dibuja Marte o tu base] de tipo Player
    mostrar "PROTOCOLO MARTE" "A: activar atmósfera"
    establecer porClic como 1
    marcar puntaje en 0

cuando el botón A sea presionado
    cambiar puntaje por porClic
    marte empieza [elige un efecto] efecto para 200 ms

en puntaje 100
    game over GANASTE
''', xp=100, monedas=30),
            makecode('Sprint 2: tormentas solares', leccion(
                intro='Meta del sprint: cada 2 segundos llega un rayo de radiación desde la derecha. Si toca la '
                      'colonia, pierdes una vida. Ahora el juego tiene tensión.',
                saber=['Los rayos son sprites de tipo Enemy que se crean solos, una y otra vez.',
                       '«escoger al azar de 30 a 90» (Matemáticas) hace que cada rayo salga a una altura distinta.',
                       '«fijar rayo auto destruir ACTIVADO» borra el rayo cuando sale de la pantalla (si no, el juego '
                       'se pone lento).',
                       'Cuando las vidas llegan a 0, el juego termina solo.'],
                dinamica=PAREJAS,
                pasos=['En «al inicio» agrega «fijar vidas en 3».',
                       'Del cajón Juego, saca «actualizar juego cada 500 ms» y cámbialo a 2000.',
                       'Adentro crea el rayo: «establecer rayo como objeto de tipo Enemy» (dibújalo amarillo).',
                       'Ponlo a la derecha con «establecer rayo en la posición x 160 y …» y la velocidad hacia la '
                       'izquierda.',
                       'Del cajón Sprites, saca «cuando el sprite de tipo Enemy coincide con otherSprite de tipo Player»: '
                       'destruye el rayo, quita una vida y sacude la cámara.',
                       'Prueba: ¿alcanzas el 100 % antes de perder las 3 vidas?'],
                logro=['Los rayos aparecen a distintas alturas, quitan vidas y el juego se puede ganar o perder.'],
                entrega='sube una captura de tus bloques.'), '''
al inicio
    fijar vidas en 3
    (… lo que ya tenías …)

actualizar juego cada 2000 ms
    establecer rayo como objeto [dibuja el rayo] de tipo Enemy
    establecer rayo en la posición x 160 y (escoger al azar de 30 a 90)
    ajustar la velocidad de rayo a vx -40 vy 0
    fijar rayo auto destruir ACTIVADO

cuando el sprite de tipo Enemy coincide con otherSprite de tipo Player
    destroy sprite
    cambiar vidas por -1
    sacudir la camera por 4 píxeles para 500 ms
''', xp=110, monedas=30),
            makecode('Sprint 3: el escudo y las mejoras', leccion(
                intro='Meta del sprint: el jugador decide cómo gastar su atmósfera. Con B activa el escudo (borra todos '
                      'los rayos) y con la flecha arriba compra paneles que hacen cada clic más potente.',
                saber=['Gastar puntos para salvarte es una decisión: así aparece la estrategia (una dinámica).',
                       'Recuerda: «cambiar porClic a 1» SUMA 1.'],
                dinamica=PAREJAS,
                pasos=['Botón B: si tienes 15 o más, resta 15 y usa «destruir todos los objetos de tipo Enemy».',
                       'Haz que marte diga «¡Escudo!» por 500 ms.',
                       'Flecha arriba: si tienes 20 o más, resta 20 y suma 1 a porClic.',
                       'Juega 3 partidas: ¿conviene más comprar paneles al principio o guardar para el escudo?',
                       'Ajusta los precios hasta que el juego sea retador, pero posible.'],
                logro=['El escudo y los paneles funcionan solo si te alcanzan los puntos.',
                       'Puedes explicar qué estrategia te funcionó mejor.'],
                entrega='sube una captura de tus bloques y escribe en el comentario tu mejor estrategia.'), '''
cuando el botón B sea presionado
    si puntuación ≥ 15 entonces
        cambiar puntaje por -15
        destruir todos los objetos de tipo Enemy
        marte decir "¡Escudo!" por 500 ms

cuando el botón arriba sea presionado
    si puntuación ≥ 20 entonces
        cambiar puntaje por -20
        cambiar porClic a 1          ← suma 1 a porClic
        marte decir "+1 panel solar" por 500 ms
''', xp=110, monedas=30),
            mision('Lee el código como pro', 'cuestionario', leccion(
                intro='Un buen programador puede leer un programa y predecir qué va a pasar sin correrlo. Practica con '
                      'tu propio juego.',
                saber=['Un evento se dispara cuando algo pasa: presionar un botón, que choquen dos sprites, llegar a un '
                       'puntaje.',
                       'Un «si … entonces» solo ejecuta lo de adentro si la condición es verdadera.',
                       'Un bug es un error: el juego hace algo distinto de lo que querías.']), xp=60, preguntas=[
                ('Tienes 10 puntos y presionas B (el escudo cuesta 15). ¿Qué pasa?', 'No pasa nada: no te alcanza',
                 ['Se borran los rayos y quedas con -5', 'Ganas el juego', 'Pierdes una vida']),
                ('¿Qué hace «fijar rayo auto destruir ACTIVADO»?', 'Borra el rayo cuando sale de la pantalla',
                 ['Destruye a Marte', 'Termina el juego', 'Hace el rayo invisible']),
                ('¿Qué pasa si quitas el bloque «actualizar juego cada 2000 ms»?', 'Ya no aparecen rayos',
                 ['Aparecen el doble de rayos', 'El juego no inicia', 'El puntaje baja solo']),
                ('El rayo toca a Marte pero no quita vidas. ¿Dónde está el bug?',
                 'En el evento de cuando el Enemy coincide con el Player', ['En el fondo de pantalla',
                                                                          'En el bloque mostrar', 'En la música']),
                ('¿Para qué sirve «escoger al azar de 30 a 90»?', 'Para que cada rayo salga a una altura distinta',
                 ['Para elegir el color del fondo', 'Para sumar puntos', 'Para cambiar de nivel']),
                ('Si cambias «actualizar juego cada 2000 ms» a 500 ms, el juego será…', 'Más difícil: más rayos',
                 ['Más fácil', 'Igual', 'Más lento']),
            ]),
        ]},
        {'nombre': 'Torneo marciano', 'cofre': 40, 'misiones': [
            mision('Organiza el torneo', 'presencial', leccion(
                intro='Un torneo también es un problema grande. Apliquen lo que ya saben: divídanlo en subproblemas y '
                      'repártanlos.',
                dinamica=['Todo el grupo junto, con el profe como moderador. Se habla levantando la mano.',
                          'Cada equipo se queda con un subproblema y tiene 10 minutos para resolverlo.'],
                pasos=['Reglas: ¿cuánto dura cada partida?, ¿qué pasa en un empate? (por ejemplo, muerte súbita de 20 '
                       'segundos).',
                       'Formato: ¿quién juega contra quién?, ¿cuántas rondas? Dibujen la tabla de eliminación.',
                       'Roles del día: árbitro, cronometrista, anotador, presentador y técnico (revisa que las '
                       'computadoras estén listas).',
                       'Tabla de récords: alguien prepara la hoja de cálculo (siguiente misión).',
                       'Reconocimientos: además del ganador, premien el juego más creativo y el más difícil.'],
                logro=['El torneo tiene reglas escritas, tabla de rondas y una persona responsable de cada tarea.']),
                xp=50),
            mision('Tabla de récords', 'evidencia', leccion(
                intro='Los torneos de esports llevan sus estadísticas en hojas de cálculo. Prepara la del torneo de tu '
                      'grupo en Excel o Google Sheets.',
                saber=['Celda: cada cuadrito; se nombra por su columna y su fila (B2).',
                       'Toda fórmula empieza con «=».',
                       '=MAX(B2:B30) da el puntaje más alto, =MIN(B2:B30) el más bajo y =PROMEDIO(B2:B30) el promedio.',
                       'B2:B30 significa «de la celda B2 a la B30».'],
                pasos=['Columna A: Jugador · Columna B: Juego (de qué estudio) · Columna C: Puntaje · Columna D: Vidas '
                       'que le quedaron.',
                       'Pon en negritas y con color de relleno la primera fila (los encabezados).',
                       'Debajo de la tabla calcula el récord (=MAX), el más bajo (=MIN) y el promedio (=PROMEDIO).',
                       'Ordena de mayor a menor puntaje: selecciona la tabla → Datos → Ordenar.',
                       'Guarda como Torneo_Marte en tu carpeta.'],
                logro=['Las fórmulas calculan solas: si cambias un puntaje, el récord y el promedio se actualizan.'],
                entrega='sube una captura de tu tabla con las fórmulas.'), xp=90, monedas=25),
            mision('¡Torneo marciano!', 'presencial', leccion(
                intro='Llegó el día. Cada jugador juega el juego de OTRO estudio: así probamos de verdad las evidencias '
                      'que crearon.',
                dinamica=['Cada uno con su rol del torneo. El árbitro tiene la última palabra.',
                          'Partidas de 60 segundos. El anotador registra los puntajes en la tabla de récords.',
                          'Regla de oro: se celebra con los brazos, no con gritos. El equipo que grite pierde su turno.'],
                pasos=['El presentador explica las reglas y el formato.',
                       'Primera ronda: todos juegan una partida en un juego ajeno.',
                       'Los mejores puntajes pasan a la final.',
                       'Final en el proyector con todo el grupo de público.',
                       'Entrega de reconocimientos: campeón, juego más creativo y juego más difícil.'],
                logro=['Jugaste en otro juego, respetaste los roles y tu puntaje quedó registrado.']), xp=60),
            mision('Mis hallazgos', 'texto', leccion(
                intro='Cierra el proyecto como lo hace un equipo de verdad: con una revisión honesta.',
                pasos=['¿Qué subproblema de tu juego fue el más difícil de programar y cómo lo resolviste?',
                       '¿Qué dinámica apareció en el torneo que no esperabas?',
                       '¿Tu escudo usa la tecnología de forma constructiva? Explica.',
                       'Si tuvieras una semana más, ¿qué le agregarías a tu juego?'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            jefe('Jefe: Tormenta Solar', leccion(
                intro='Una tormenta solar se acerca a la colonia. Solo resiste quien domina los datos de Marte, la '
                      'descomposición y el código de su escudo.'), [
                ('¿Por qué la radiación del Sol es tan peligrosa en Marte?',
                 'Porque Marte casi no tiene atmósfera ni campo magnético', ['Porque Marte está más cerca del Sol',
                                                                            'Porque en Marte siempre es de día',
                                                                            'Porque Marte es de color rojo']),
                ('¿Qué es una idea creativa?', 'Una idea novedosa y útil',
                 ['Cualquier idea rara', 'Una idea copiada de internet', 'Una idea imposible']),
                ('¿Qué es descomponer un problema?', 'Dividirlo en partes pequeñas que se resuelven una por una',
                 ['Borrarlo y empezar de nuevo', 'Pedirle a otro que lo resuelva', 'Ignorar las partes difíciles']),
                ('¿Cuál de estos es un uso irresponsable de la tecnología?',
                 'Publicar la foto de un compañero sin su permiso', ['Usar un rover para estudiar el suelo',
                                                                     'Reciclar una computadora vieja',
                                                                     'Dar crédito a quien te ayudó']),
                ('En tu juego, ¿qué tipo de sprite son los rayos de radiación?', 'Enemy',
                 ['Player', 'Food', 'Ninguno']),
                ('¿Qué bloque borra todos los rayos de un golpe?', 'destruir todos los objetos de tipo Enemy',
                 ['marcar puntaje en 0', 'fijar vidas en 3', 'establecer color de fondo a']),
                ('¿Qué fórmula da el puntaje más alto de la tabla?', '=MAX(C2:C30)',
                 ['=PROMEDIO(C2:C30)', '=MIN(C2:C30)', 'MAX C2 C30']),
                ('¿Qué propusieron científicos de la NASA para proteger a Marte?',
                 'Un escudo magnético entre Marte y el Sol', ['Mover Marte más lejos del Sol',
                                                              'Pintar Marte de blanco', 'Construir un muro de papel']),
            ]),
        ]},
    ],
}
