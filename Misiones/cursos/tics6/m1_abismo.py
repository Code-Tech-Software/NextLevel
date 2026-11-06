"""Mundo 1 · ES-DAT302 Aventura submarina: mecánicas y dinámicas de los videojuegos, el género clicker y un clicker
del fondo del mar programado en MakeCode Arcade."""
from .base import LEYENDA_MAKECODE, MAKECODE, PAREJAS, clasifica, jefe, leccion, makecode, mision

JUEGOS = {
    'clasifica_mecanica': clasifica('¿Mecánica o dinámica?', '⚙️', 'Separa las reglas del juego de lo que pasa cuando la '
                                    'gente lo juega.', [
        ('Mecánica (regla)', '⚙️', ['Cada clic suma 1 perla', 'Tienes 30 segundos para jugar',
                                    'La mejora cuesta 10 perlas', 'Si un tiburón te toca, pierdes una vida',
                                    'El botón A sirve para saltar', 'Un dron suma 1 punto cada segundo',
                                    'En fútbol no se puede tocar el balón con la mano',
                                    'Necesitas 500 puntos para ganar']),
        ('Dinámica (lo que pasa)', '🔁', ['Los jugadores ahorran para comprar la mejora grande',
                                         'Todos presionan rapidísimo en los últimos segundos',
                                         'Dos amigos compiten por romper el récord',
                                         'Un equipo de fútbol ensaya jugadas de tiro de esquina',
                                         'En Minecraft construyes refugio antes de que anochezca',
                                         'Alguien descubre un truco y todos lo copian',
                                         'Un jugador espera para comprar varias mejoras juntas',
                                         'El grupo se pone de acuerdo para defender la base']),
    ], rondas=14),
    'clasifica_clicker': clasifica('Anatomía de un clicker', '👆', 'Cada pieza de un clicker tiene su trabajo: ¿es acción, '
                                   'mejora o producción automática?', [
        ('Acción del jugador', '👆', ['Presionar el botón A para sacar una perla', 'Hacer clic en el cofre',
                                      'Tocar la pantalla para bucear más hondo', 'Presionar B para abrir la tienda']),
        ('Mejora', '⬆️', ['Ahora cada clic vale 2 perlas', 'Aletas nuevas: el doble de puntos por clic',
                          'La mejora cuesta el doble cada vez que la compras', 'Lámpara potente: +3 por clic']),
        ('Producción automática', '🤖', ['Un dron recoge 1 perla cada segundo', 'Un submarino junta tesoros solo',
                                         'Ganas puntos aunque no hagas clic', 'Cada robot suma 5 puntos por segundo']),
    ], rondas=12),
    'clasifica_bloques_arcade': clasifica('¿De qué cajón es el bloque?', '🧰', 'En MakeCode Arcade cada bloque vive en '
                                          'una categoría. ¿Dónde lo buscas?', [
        ('Sprites', '🧍', ['establecer buzo como objeto de tipo Player', 'buzo decir "¡A explorar!"',
                           'buzo empieza burbujas efecto', 'fijar buzo rebotar en la pared',
                           'destruir todos los objetos de tipo Enemy']),
        ('Controles', '🎮', ['cuando el botón A sea presionado', 'cuando el botón B sea presionado',
                             'mover buzo con los botones', 'cuando el botón arriba sea presionado']),
        ('Información', '📊', ['cambiar puntaje por 1', 'marcar puntaje en 0', 'iniciar cuenta atrás 30 (s)',
                               'cuando termine de la cuenta regresiva', 'fijar vidas en 3']),
    ], rondas=12),
}

MUNDO = {
    'nombre': 'Estudio Abismo', 'tema': 'abismo',
    'descripcion': 'ES-DAT302 · Aventura submarina. Heracleion, una ciudad egipcia, pasó siglos bajo el agua hasta que '
                   'la encontraron en el año 2000. Tu equipo es un estudio de videojuegos: entenderás qué hace que un '
                   'juego enganche y programarás un clicker para explorar el fondo del mar. Pregunta guía: si nos '
                   'sumergimos en aguas profundas, ¿qué hay por descubrir?',
    'niveles': [
        {'nombre': 'Inmersión', 'cofre': 25, 'misiones': [
            mision('La ciudad que se hundió', 'texto', leccion(
                intro='Durante siglos, Heracleion fue una leyenda: un puerto egipcio lleno de templos y barcos que '
                      'simplemente «desapareció». En el año 2000, un equipo de arqueología submarina encontró sus '
                      'ruinas bajo el mar, en la bahía de Abukir, cerca de donde el río Nilo llega al Mediterráneo.',
                saber=['La ciudad se hundió poco a poco: terremotos, inundaciones y un suelo blando que se deshizo con '
                       'el agua.',
                       'Bajo el agua encontraron estatuas de más de 5 metros, barcos hundidos, monedas y joyas.',
                       'Más del 80 % del océano sigue sin explorarse: hay más mapas de la Luna que del fondo del mar.'],
                pasos=['¿Qué crees que todavía se puede descubrir en el fondo del mar? Escribe 3 cosas.',
                       '¿Por qué crees que es tan difícil explorar las profundidades?',
                       'Si hicieras un videojuego sobre esto, ¿qué haría el jugador? Descríbelo en 2 renglones.'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('Contrato del estudio', 'presencial', leccion(
                intro='Un estudio de videojuegos real no funciona con todos hablando al mismo tiempo: trabaja con '
                      'roles, tiempos cortos («sprints») y señales claras. Hoy firman el contrato de su estudio.',
                saber=['Sprint: un bloque de trabajo de 10 a 15 minutos con una sola meta.',
                       'Stand-up: una junta de 1 minuto, de pie, donde cada quien dice qué hizo y qué sigue.',
                       'Playtest: cuando otra persona prueba tu juego y tú solo observas y anotas.'],
                roles=['Piloto: maneja el mouse y el teclado.',
                       'Copiloto: lee las instrucciones y revisa cada bloque.',
                       'Tester: prueba el juego y anota los errores (bugs).',
                       'Productor: cuida el tiempo y que el equipo cumpla la meta del sprint.'],
                pasos=['Formen equipos de 4 y pónganle nombre a su estudio.',
                       'Repartan los 4 roles. Cambiarán cada mundo, así que todos pasarán por todos.',
                       'Acuerden las señales del grupo con su profe: «manos arriba» = silencio y mouse suelto; '
                       '«pantallas a 45°» = todos miran al frente.',
                       'Escriban 3 reglas propias del estudio (por ejemplo: «se critica el juego, no a la persona»).',
                       'Firmen el contrato y tómenle foto.'],
                logro=['Cada integrante sabe su rol y las señales del grupo.',
                       'El estudio tiene nombre y 3 reglas escritas.'],
                tip='El equipo que respeta las señales en todo el mundo puede ganar XP extra al final.'), xp=50),
            mision('Mecánicas y dinámicas', 'cuestionario', leccion(
                intro='Los diseñadores de videojuegos hablan de dos ideas clave. Si las entiendes, nunca vuelves a ver '
                      'un juego igual.',
                saber=['Mecánica: las reglas y acciones que el juego permite. Ejemplos: saltar, hacer clic, comprar '
                       'mejoras, tener 3 vidas, un tiempo límite.',
                       'Dinámica: lo que pasa cuando las personas juegan con esas reglas. Ejemplos: competir, ahorrar '
                       'para la mejora grande, presionar rapidísimo al final, cooperar.',
                       'El diseñador solo controla las mecánicas; las dinámicas aparecen cuando la gente juega.',
                       'Ejemplo en fútbol: la mecánica es «no tocar el balón con la mano»; la dinámica es el equipo '
                       'ensayando jugadas de tiro de esquina.']), xp=60, preguntas=[
                ('¿Qué es una mecánica de juego?', 'Una regla o acción que el juego permite',
                 ['Lo que sienten los jugadores', 'El nombre del juego', 'La consola donde se juega']),
                ('¿Qué es una dinámica de juego?', 'Lo que pasa cuando las personas juegan con las reglas',
                 ['Una regla escrita por el diseñador', 'El precio del juego', 'La música del juego']),
                ('«Cada clic suma 1 punto» es…', 'Una mecánica', ['Una dinámica', 'Una emoción', 'Un error']),
                ('«Los jugadores ahorran para comprar la mejora más cara» es…', 'Una dinámica',
                 ['Una mecánica', 'Un bloque de código', 'Un sprite']),
                ('¿Quién controla directamente las mecánicas?', 'El diseñador del juego',
                 ['Los jugadores', 'Nadie', 'El público que mira']),
                ('En Minecraft, construir un refugio antes de que anochezca es…', 'Una dinámica',
                 ['Una mecánica', 'Un sprite', 'Un tipo de bloque']),
            ]),
            mision('¿Mecánica o dinámica?', 'juego', leccion(
                intro='Pon a prueba tu ojo de diseñador: separa las reglas del juego de lo que hacen los jugadores.',
                tip='Pregúntate: «¿esto lo escribió el diseñador o lo decidió el jugador?».'), juego='clasifica_mecanica'),
        ]},
        {'nombre': 'El género clicker', 'cofre': 30, 'misiones': [
            mision('Anatomía de un clicker', 'cuestionario', leccion(
                intro='Los juegos clicker (o incrementales) parecen simples: haces clic y ganas puntos. Pero tienen un '
                      'diseño muy pensado para que no puedas dejar de jugar.',
                saber=['El ciclo central: haces clic → ganas recursos → compras mejoras → ganas recursos más rápido.',
                       'Recurso: lo que juntas (perlas, monedas, galletas, energía).',
                       'Mejora: hace que cada clic valga más.',
                       'Producción automática (autoclicker): genera recursos aunque no hagas clic.',
                       'Balance: las mejoras cuestan cada vez más para que el juego no se acabe en un minuto.',
                       'Meta: un puntaje, un tiempo límite o un tesoro final.']), xp=60, preguntas=[
                ('¿Cuál es el ciclo central de un clicker?',
                 'Clic → recursos → mejoras → recursos más rápido',
                 ['Correr → saltar → disparar', 'Leer → escribir → borrar', 'Ganar → perder → reiniciar']),
                ('¿Qué hace una mejora en un clicker?', 'Hace que cada clic valga más',
                 ['Borra tus puntos', 'Termina el juego', 'Cambia el idioma']),
                ('¿Qué es la producción automática?', 'Ganar recursos sin hacer clic',
                 ['Un clic muy rápido', 'Un error del juego', 'La pantalla de inicio']),
                ('¿Por qué las mejoras suben de precio cada vez?', 'Para balancear el juego y que dure más',
                 ['Para que nadie pueda comprarlas', 'Por un error de programación', 'Para que el juego sea más corto']),
                ('En un clicker del fondo del mar, ¿qué podría ser el recurso?', 'Perlas o tesoros',
                 ['Las vidas del enemigo', 'El botón B', 'El fondo de pantalla']),
            ]),
            mision('Clicker humano', 'presencial', leccion(
                intro='Antes de programarlo, lo juegan con papel y lápiz. Así descubren qué dinámicas aparecen cuando '
                      'cambias una sola regla.',
                material=['Una hoja por equipo', 'Un lápiz por equipo', 'El cronómetro del profe'],
                dinamica=['Equipos de 4. Solo el Piloto escribe; los demás observan y aconsejan en voz baja.',
                          'Cada ronda dura 60 segundos. Cuando el profe dice «¡alto!», lápices arriba.',
                          'Regla del estudio: el equipo que grita pierde 10 perlas. El ruido también es una mecánica.'],
                pasos=['Ronda 1: cada palomita (✓) que haga el Piloto vale 1 perla. Al final, cuenten.',
                       'Ronda 2, con tienda: al juntar 20 perlas pueden «comprar» la mejora x2 (tachan 20 perlas y '
                       'desde ahí cada palomita vale 2).',
                       'Ronda 3, con dron: por 40 perlas compran un dron; cada vez que el profe dice «tic» (cada 10 '
                       'segundos), el dron les da 5 perlas gratis.',
                       'Comparen: ¿en qué ronda juntaron más? ¿Qué estrategia usó el equipo ganador?',
                       'Anoten 2 dinámicas que aparecieron (por ejemplo: «ahorramos para el dron»).'],
                logro=['Explicas qué mecánica nueva cambió la forma de jugar de tu equipo.'],
                tip='Fíjense en quién compró la mejora muy pronto o muy tarde: ahí está la dinámica.'), xp=50),
            mision('Anatomía de un clicker: tarjetas', 'juego', leccion(
                intro='Clasifica cada pieza: ¿es algo que hace el jugador, una mejora o algo que trabaja solo?'),
                juego='clasifica_clicker'),
            mision('Analiza tu juego favorito', 'texto', leccion(
                intro='Ahora analiza como diseñador un juego que ya conoces (Minecraft, Fortnite, Roblox, Mario Kart, '
                      'Among Us, Subway Surfers…).',
                pasos=['Nombre del juego y su género (carreras, construcción, clicker, disparos, plataformas…).',
                       'Escribe 3 mecánicas (reglas o acciones que permite el juego).',
                       'Escribe 2 dinámicas que hayas visto al jugarlo con amigos.',
                       '¿Qué emoción te provoca: tensión, risa, competencia, calma? ¿Qué mecánica la causa?',
                       'Si pudieras cambiar UNA regla, ¿cuál sería y cómo cambiaría el juego?'],
                logro=['Tus mecánicas son reglas, no opiniones («se ve bonito» no es una mecánica).'],
                entrega='escribe tu análisis aquí abajo.'), xp=60),
        ]},
        {'nombre': 'Laboratorio MakeCode', 'cofre': 30, 'misiones': [
            mision('Entra a MakeCode Arcade', 'link', leccion(
                intro='MakeCode Arcade es el editor de Microsoft para crear videojuegos retro con bloques (y también con '
                      'JavaScript o Python). Es gratis y funciona en el navegador.',
                saber=['Simulador (izquierda): la consolita donde se prueba tu juego al instante.',
                       'Categorías de bloques (centro): Sprites, Controles, Juego, Música, Escenario, Información, '
                       'Ciclos, Lógica, Variables, Matemáticas…',
                       'Espacio de trabajo (derecha): donde armas el programa. Empieza con el bloque «al inicio».',
                       'Teclas del simulador: flechas o W A S D para moverte, Espacio (o Z) es el botón A e Intro '
                       '(o X) es el botón B.'],
                pasos=['Abre el enlace de abajo.',
                       'Si sale en inglés: ⚙️ (engrane) → Language → Español (México).',
                       'Clic en «Nuevo proyecto» y llámalo Abismo_TuNombre.',
                       'Abre cada categoría y busca el bloque «al inicio».',
                       'Prueba el buscador de bloques: escribe «puntaje».'],
                ojo=['Tu proyecto se guarda en el navegador de esta computadora. Para no perderlo, descárgalo o '
                     'compártelo con un enlace al final de cada clase.'],
                tip='Usa siempre la misma computadora o guarda tu enlace para encontrar tu proyecto.'),
                xp=40, monedas=10, link=MAKECODE),
            makecode('Tu primer sprite', leccion(
                intro='Un sprite es cualquier personaje u objeto del juego. Crea al explorador de tu juego.',
                saber=['Para dibujar el sprite haz clic en el cuadro gris del bloque: se abre el editor de imágenes '
                       '(lápiz, bote de pintura, borrador y colores). También puedes elegir uno de la Galería.',
                       'Player es el «tipo» del sprite: le dice al juego que es el jugador.',
                       LEYENDA_MAKECODE],
                dinamica=PAREJAS,
                pasos=['Del cajón Escenario, arrastra «establecer color de fondo a» dentro de «al inicio» y elige un azul '
                       'oscuro.',
                       'Del cajón Sprites, arrastra «establecer mySprite como objeto de tipo Player».',
                       'Cambia el nombre: clic en mySprite → Renombrar variable → buzo.',
                       'Dibuja tu buzo (o un submarino, un robot de exploración…).',
                       'Agrega «buzo decir» y escribe una frase de inicio.',
                       'Mira el simulador: tu buzo debe aparecer hablando.'],
                logro=['Tu sprite aparece en el simulador sobre fondo azul y dice su frase.'],
                entrega='sube una captura de tus bloques y del simulador.'), '''
al inicio
    establecer color de fondo a [azul oscuro]
    establecer buzo como objeto [dibuja tu buzo] de tipo Player
    buzo decir "¡A explorar el abismo!"
''', xp=80, monedas=20),
            mision('¿De qué cajón es el bloque?', 'juego', leccion(
                intro='Programar rápido es saber dónde buscar. Manda cada bloque a su categoría.',
                tip='El color del bloque te da la pista: cada categoría tiene su color.'), juego='clasifica_bloques_arcade'),
        ]},
        {'nombre': 'Sprints de programación', 'cofre': 35, 'misiones': [
            makecode('Sprint 1: cada clic cuenta', leccion(
                intro='Meta del sprint (15 minutos): que cada vez que presiones A ganes una perla y que el juego dure '
                      '30 segundos.',
                saber=['Un evento es algo que pasa mientras juegas (presionar un botón, que se acabe el tiempo). Los '
                       'bloques de evento no van dentro de «al inicio»: se ponen sueltos.',
                       'El puntaje vive en el cajón Información y se muestra solo, arriba a la derecha.',
                       'Cuenta regresiva: un reloj que baja; cuando llega a 0 se dispara su evento.'],
                dinamica=PAREJAS,
                pasos=['Abre tu proyecto Abismo_TuNombre.',
                       'Dentro de «al inicio» agrega «marcar puntaje en 0» e «iniciar cuenta atrás 30 (s)».',
                       'Del cajón Controles, saca «cuando el botón A sea presionado».',
                       'Adentro pon «cambiar puntaje por 1» y «buzo empieza burbujas efecto para 200 ms».',
                       'Agrega el evento «cuando termine de la cuenta regresiva» con «game over GANASTE».',
                       'Prueba con la tecla Espacio: cuenta cuántas perlas juntas en 30 segundos.'],
                logro=['Cada vez que presionas A sube el puntaje y salen burbujas.',
                       'A los 30 segundos termina el juego y muestra tu puntaje.'],
                entrega='sube una captura de tus bloques y escribe en el comentario tu récord.'), '''
al inicio
    establecer color de fondo a [azul oscuro]
    establecer buzo como objeto [tu buzo] de tipo Player
    marcar puntaje en 0
    iniciar cuenta atrás 30 (s)

cuando el botón A sea presionado
    cambiar puntaje por 1
    buzo empieza [burbujas] efecto para 200 ms

cuando termine de la cuenta regresiva
    game over GANASTE
'''),
            makecode('Sprint 2: la tienda de mejoras', leccion(
                intro='Meta del sprint: con el botón B compras una mejora que hace que cada clic valga más. Pero cada '
                      'mejora cuesta el doble que la anterior: eso es balancear un juego.',
                saber=['Una variable es una cajita con nombre que guarda un número que puede cambiar: porClic guarda '
                       'cuántas perlas da cada clic; costo guarda el precio de la mejora.',
                       'Crea las variables en el cajón Variables → «Crear una variable…».',
                       'Ojo con la traducción: el bloque «cambiar porClic a 1» en realidad SUMA 1 a la variable.',
                       'El bloque «si … entonces … si no» revisa una condición: si tienes perlas suficientes compras; '
                       'si no, el buzo te avisa.'],
                dinamica=PAREJAS,
                pasos=['Crea las variables porClic y costo.',
                       'En «al inicio»: «establecer porClic como 1» y «establecer costo como 10».',
                       'En el evento del botón A, cambia el 1 por la variable porClic.',
                       'Saca «cuando el botón B sea presionado» y arma el «si … entonces … si no» como en el código.',
                       'La condición «puntuación ≥ costo» se arma con el bloque de comparación de Lógica y «puntuación» '
                       'de Información.',
                       'Prueba: junta 10 perlas, presiona Intro (botón B) y revisa que ahora cada clic dé 2.'],
                logro=['Con B compras la mejora solo si te alcanzan las perlas, y cada vez cuesta el doble.'],
                entrega='sube una captura de tus bloques.'), '''
al inicio
    establecer porClic como 1
    establecer costo como 10
    (… lo que ya tenías …)

cuando el botón A sea presionado
    cambiar puntaje por porClic
    buzo empieza [burbujas] efecto para 200 ms

cuando el botón B sea presionado
    si puntuación ≥ costo entonces
        cambiar puntaje por 0 - costo
        cambiar porClic a 1          ← suma 1 a porClic
        establecer costo como costo × 2
        buzo decir "¡Mejora!" por 500 ms
    si no
        buzo decir "Te faltan perlas" por 500 ms
''', xp=110, monedas=30),
            makecode('Sprint 3: dron autoclicker', leccion(
                intro='Meta del sprint: un dron que junta perlas solo, cada segundo. Y una meta para ganar: 500 perlas '
                      'antes de que se acabe el tiempo.',
                saber=['«actualizar juego cada 1000 ms» repite lo que tiene adentro cada segundo (1000 milisegundos = '
                       '1 segundo).',
                       'Si drones vale 0, el dron no da nada. Cada dron que compras suma 1 perla por segundo.',
                       '«en puntaje 500» es un evento: se dispara cuando llegas a ese puntaje.'],
                dinamica=PAREJAS,
                pasos=['Crea la variable drones y en «al inicio» pon «establecer drones como 0».',
                       'Cambia la cuenta atrás a 60 segundos: la meta ahora es más difícil.',
                       'Saca «cuando el botón arriba sea presionado»: si tienes 50 perlas o más, resta 50 y suma 1 a '
                       'drones.',
                       'Del cajón Juego, saca «actualizar juego cada 500 ms», cámbialo a 1000 y pon adentro «cambiar '
                       'puntaje por drones».',
                       'Del cajón Información, saca «en puntaje 100» y cámbialo a 500, con «game over GANASTE».',
                       'Cambia el final de la cuenta regresiva a «game over PERDER»: ahora sí hay reto.'],
                logro=['Al comprar drones el puntaje sube solo cada segundo.',
                       'Ganas al llegar a 500 y pierdes si se acaba el tiempo antes.'],
                entrega='sube una captura de tus bloques.'), '''
al inicio
    establecer drones como 0
    iniciar cuenta atrás 60 (s)
    (… lo que ya tenías …)

cuando el botón arriba sea presionado
    si puntuación ≥ 50 entonces
        cambiar puntaje por -50
        cambiar drones a 1          ← suma 1 dron

actualizar juego cada 1000 ms
    cambiar puntaje por drones

en puntaje 500
    game over GANASTE

cuando termine de la cuenta regresiva
    game over PERDER
''', xp=110, monedas=30),
            makecode('Personaliza tu abismo', leccion(
                intro='Un juego con los colores por defecto se ve de prueba. Dale identidad: este es el juego de tu '
                      'estudio y tiene un mensaje para cuidar el océano (ODS 14: vida submarina).',
                pasos=['Cambia el fondo por una imagen: Escenario → «establecer imagen de fondo a» y dibuja el fondo del '
                       'mar (arena, algas, ruinas de Heracleion…).',
                       'Ponle nombre a tu recurso: perlas, fósiles, monedas antiguas… y úsalo en los mensajes.',
                       'Del cajón Juego, agrega al inicio un bloque «mostrar» con el título de tu juego.',
                       'Del cajón Música, agrega un sonido cuando compras una mejora.',
                       'Agrega un evento «en puntaje 100» donde el buzo diga un dato real: «Más del 80 % del océano no '
                       'se ha explorado».',
                       'Comparte tu juego: botón de compartir (arriba) → copia el enlace y guárdalo.'],
                logro=['Tu juego tiene título, fondo dibujado, sonido y un dato sobre el océano.'],
                tip='Un juego se siente mejor con «retroalimentación»: un sonido, un efecto o un mensaje cada vez que '
                    'pasa algo importante.',
                entrega='sube una captura de tu juego y pega el enlace para jugarlo en el comentario.'), '''
al inicio
    mostrar "ABISMO: la ciudad perdida"
    establecer imagen de fondo a [dibuja el fondo del mar]
    (… lo que ya tenías …)

cuando el botón B sea presionado
    si puntuación ≥ costo entonces
        (… la mejora …)
        reproducir sound [power up] hasta que termine

en puntaje 100
    buzo decir "Más del 80 % del océano no se ha explorado" por 2000 ms
''', xp=110, monedas=30),
        ]},
        {'nombre': 'Playtest', 'cofre': 40, 'misiones': [
            mision('Playtest cruzado', 'presencial', leccion(
                intro='En los estudios de verdad, otros prueban tu juego mientras tú solo observas. Duele un poco, pero '
                      'así se encuentran los errores.',
                dinamica=['Cada estudio se cambia a la computadora de otro estudio (el profe dice a cuál).',
                          '2 minutos de juego por persona, cronometrados por el Productor.',
                          'El creador NO explica nada: si el jugador se confunde, eso es información valiosa.'],
                pasos=['Juega el juego del otro estudio sin que te expliquen.',
                       'Anota en una hoja: 2 mecánicas que encontraste y 1 dinámica que te pasó al jugar.',
                       'Anota un bug (error) o algo que te confundió.',
                       'Escribe tu retroalimentación con la fórmula «Me gustó… / Me confundió… / Te sugiero…».',
                       'Entrega la hoja al estudio dueño del juego.'],
                logro=['Tu retroalimentación es concreta y amable: habla del juego, no de la persona.']), xp=50),
            mision('Notas del parche', 'evidencia', leccion(
                intro='Cuando un juego se actualiza, el estudio publica sus «notas del parche» (patch notes): qué se '
                      'arregló y qué se balanceó. Hoy sacas la versión 1.1 de tu juego.',
                saber=['Balancear: ajustar los números (precios, tiempo, puntos por clic) para que el juego no sea ni '
                       'imposible ni aburrido.',
                       'Una buena nota de parche dice qué cambió y por qué.'],
                pasos=['Lee la retroalimentación que te dejaron en el playtest.',
                       'Elige 2 cambios y hazlos en tu juego (por ejemplo: la mejora cuesta 15 en vez de 10; el dron '
                       'cuesta 40).',
                       'Prueba de nuevo: ¿se puede ganar? ¿Es demasiado fácil?',
                       'Escribe tus notas del parche v1.1 en el comentario con este formato: «Cambio: … / Por qué: …».'],
                logro=['Hiciste al menos 2 cambios basados en lo que dijeron los testers y explicas por qué.'],
                entrega='sube una captura de los bloques que cambiaste y escribe tus notas del parche en el comentario.'),
                xp=100, monedas=30, link=MAKECODE),
            jefe('Jefe: Leviatán del Abismo', leccion(
                intro='El Leviatán custodia la ciudad perdida. Solo un verdadero diseñador de videojuegos puede pasar.',
                tip='Repasa mecánicas, dinámicas, el ciclo de un clicker y los bloques de MakeCode.'), [
                ('¿Qué es una mecánica?', 'Una regla o acción que el juego permite',
                 ['Lo que hacen los jugadores al competir', 'La música del juego', 'Un tipo de consola']),
                ('Los jugadores se organizan para comprar el dron entre todos. Eso es…', 'Una dinámica',
                 ['Una mecánica', 'Un sprite', 'Un error']),
                ('¿Cuál es el ciclo central de un clicker?', 'Clic → recursos → mejoras → recursos más rápido',
                 ['Saltar → correr → caer', 'Iniciar → pausar → salir', 'Dibujar → colorear → guardar']),
                ('En MakeCode Arcade, ¿qué tecla funciona como botón A en el simulador?', 'Espacio (o Z)',
                 ['Intro', 'La flecha de arriba', 'Esc']),
                ('¿En qué categoría está «cambiar puntaje por 1»?', 'Información', ['Sprites', 'Escenario', 'Música']),
                ('¿Para qué sirve la variable porClic?', 'Para guardar cuántos puntos da cada clic',
                 ['Para cambiar el fondo', 'Para dibujar el sprite', 'Para terminar el juego']),
                ('¿Qué hace «actualizar juego cada 1000 ms»?', 'Repite lo que tiene adentro cada segundo',
                 ['Termina el juego en un segundo', 'Borra el puntaje', 'Cambia de nivel']),
                ('¿Por qué la mejora cuesta el doble cada vez?', 'Para balancear el juego',
                 ['Porque MakeCode lo obliga', 'Para que nadie la compre', 'Para que el juego sea más corto']),
                ('¿Dónde se encontró Heracleion?', 'Bajo el mar, cerca de donde el Nilo llega al Mediterráneo',
                 ['En la cima de una montaña', 'Bajo el hielo del Polo Sur', 'En el desierto de Sonora']),
            ]),
        ]},
    ],
}
