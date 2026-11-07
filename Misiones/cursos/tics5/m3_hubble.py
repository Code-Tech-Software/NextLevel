"""Mundo 3 · ES-DAT301 Programación estelar: la historia del espejo del Hubble, conceptos de programación
(algoritmo, evento, ciclo, condicional, variable), prácticas de Scratch y el rompecabezas del Hubble: piezas que se
arrastran y encajan mientras la foto borrosa se vuelve nítida."""
from .base import LEYENDA_SCRATCH, PAREJAS, SCRATCH, clasifica, jefe, leccion, mision, scratch

JUEGOS = {
    'clasifica_evento_ciclo': clasifica('¿Evento, ciclo o condicional?', '🔭', 'Los programas se arman con eventos '
                                        '(cuándo empieza algo), ciclos (qué se repite) y condicionales (qué se decide). '
                                        '¿Qué es cada uno?', [
        ('Evento', '⚡', ['al presionar bandera verde', 'al hacer clic en este objeto', 'al recibir «pieza lista»',
                          'Cuando suena el timbre, salimos al recreo']),
        ('Ciclo', '🔁', ['por siempre', 'repetir 10', 'repetir hasta que <…>', 'Dar 5 vueltas a la cancha']),
        ('Condicional', '🔀', ['si <…> entonces', 'si <…> entonces / si no', 'Si llueve, llevo paraguas',
                               'Si la pieza toca su lugar, encaja']),
    ], rondas=12),
    'clasifica_categorias_scratch': clasifica('¿De qué categoría es el bloque?', '🧩', 'Para armar el rompecabezas '
                                              'vas a usar bloques de tres categorías. ¿Dónde vive cada uno?', [
        ('Movimiento', '🟦', ['ir a x: 0 y: 0', 'cambiar x en 10', 'ir a «puntero del ratón»',
                              'desplazar en 1 segs a x: 0 y: 0']),
        ('Apariencia', '🟪', ['fijar efecto pixelar a 100', 'quitar efectos gráficos', 'siguiente disfraz',
                              'decir ¡Hola! durante 2 segundos']),
        ('Sensores', '🩵', ['¿tocando «Ranura espejo»?', '¿ratón presionado?', 'fijar modo de arrastre a arrastrable',
                            'reiniciar cronómetro']),
    ], rondas=12),
}

CODIGO_CAZADOR = '''
ESCENARIO
al presionar bandera verde
    cambiar fondo a "Stars"
    fijar "puntos" a 0
    reiniciar cronómetro
    esperar hasta que <(cronómetro) > 30>
    detener "todos"

OBJETO: Estrella
al presionar bandera verde
    por siempre
        ir a x: (elegir número al azar entre -200 y 200) y: (elegir número al azar entre -140 y 140)
        esperar 1.5 segundos
al recibir "atrapada"
    ir a x: (elegir número al azar entre -200 y 200) y: (elegir número al azar entre -140 y 140)

OBJETO: Mira
al presionar bandera verde
    por siempre
        ir a "puntero del ratón"
        si <<¿tocando "Estrella"?> y <¿ratón presionado?>> entonces
            cambiar "puntos" en 1
            iniciar sonido (el que tú elijas)
            enviar "atrapada"
            esperar hasta que <no <¿ratón presionado?>>
'''

CODIGO_ENFOQUE = '''
OBJETO: Foto (el objeto «Planet2»)
al presionar bandera verde
    fijar tamaño a 200 %
    fijar efecto "pixelar" a 60
    decir "Usa las flechas para enfocarme" durante 2 segundos
al presionar tecla "flecha arriba"
    cambiar el efecto "pixelar" en -10
al presionar tecla "flecha abajo"
    cambiar el efecto "pixelar" en 10
al presionar tecla "espacio"
    quitar efectos gráficos
    decir "¡Enfocado!" durante 2 segundos
'''

CODIGO_PASO1 = '''
ESCENARIO
al presionar bandera verde
    cambiar fondo a "Galaxy"
    fijar "piezas" a 0
    fijar efecto "pixelar" a 100
    reiniciar cronómetro
al recibir "pieza lista"
    cambiar "piezas" en 1
    cambiar el efecto "pixelar" en -25
    si <(piezas) = 4> entonces
        quitar efectos gráficos
        enviar "Hubble reparado"

al presionar tecla "espacio"      (solo para probar: lo borras en el paso 2)
    enviar "pieza lista"
'''

CODIGO_PASO2 = '''
OBJETO: Espejo
al presionar bandera verde
    ir a la capa "de adelante"
    fijar modo de arrastre a "arrastrable"
    ir a x: (elegir número al azar entre -220 y -150) y: (elegir número al azar entre -140 y 140)
    esperar hasta que <<¿tocando "Ranura espejo"?> y <no <¿ratón presionado?>>>
    ir a "Ranura espejo"
    fijar modo de arrastre a "no arrastrable"
    iniciar sonido (el que tú elijas)
    enviar "pieza lista"

(Las otras 3 piezas llevan el mismo programa: solo cambia «Ranura espejo» por su propia ranura, en los dos lugares.)
'''

CODIGO_PASO3 = '''
OBJETO: Guía (el personaje que tú elijas)
al presionar bandera verde
    decir "La foto del Hubble salió borrosa. Arrastra cada pieza a su lugar." durante 4 segundos
al recibir "Hubble reparado"
    iniciar sonido (el que tú elijas)
    decir (unir "¡Foto nítida! Segundos: " (redondear (cronómetro))) durante 5 segundos

OBJETO: Telescopio (reto: con un segundo disfraz «reparado»)
al presionar bandera verde
    cambiar disfraz a "dañado"
al recibir "Hubble reparado"
    cambiar disfraz a "reparado"
'''

CODIGO_BUGS = '''
OBJETO: Cámara
al presionar bandera verde
    fijar modo de arrastre a "arrastrable"
    ir a x: (elegir número al azar entre -220 y -150) y: (elegir número al azar entre -140 y 140)
    esperar hasta que <<¿tocando "Ranura espejo"?> y <no <¿ratón presionado?>>>
    ir a "Ranura cámara"
    enviar "pieza lista"

ESCENARIO
al recibir "pieza lista"
    cambiar "piezas" en 1
    cambiar el efecto "pixelar" en 25
    si <(piezas) = 5> entonces
        quitar efectos gráficos
        enviar "Hubble reparado"
'''

MUNDO = {
    'nombre': 'Observatorio Hubble', 'tema': 'marte',
    'descripcion': 'ES-DAT301 · Programación estelar. En 1990, el telescopio espacial Hubble mandó sus primeras fotos… '
                   'y salieron borrosas por un defecto en su espejo. La perseverancia y la creatividad lo repararon, y '
                   'desde entonces nos ha dado imágenes increíbles del universo. Aprende los conceptos de programación '
                   'y programa en Scratch un rompecabezas que arma el Hubble y vuelve nítida su foto. Pregunta guía: '
                   '¿qué podemos hacer para que las fotos del Hubble sean de mejor calidad?',
    'niveles': [
        {'nombre': 'Misión Hubble', 'cofre': 25, 'misiones': [
            mision('La foto borrosa', 'texto', leccion(
                intro='El 24 de abril de 1990 despegó el telescopio espacial Hubble, del tamaño de un autobús escolar. '
                      'Semanas después llegaron sus primeras fotos… borrosas. Su espejo principal, de 2.4 metros, tenía '
                      'la orilla mal pulida por una diferencia más delgada que un cabello. En 1993, unos astronautas '
                      'subieron a repararlo en el espacio y le instalaron unas «lentes». Desde entonces sus fotos son '
                      'nítidas y lleva más de 30 años descubriendo el universo.',
                pasos=['¿Qué crees que sintieron los científicos al ver las fotos borrosas?',
                       '¿Qué te enseña esta historia sobre los errores en un proyecto?',
                       'Cuéntanos de una vez que algo te salió mal y lo arreglaste.'],
                entrega='escribe tus tres respuestas aquí abajo.'), xp=60),
            mision('Así funciona el Hubble', 'cuestionario', leccion(
                intro='Antes de programar su rompecabezas, conoce las piezas del telescopio.',
                saber=['Espejo principal: junta la luz de las estrellas y la refleja hacia un espejo más pequeño '
                       '(secundario), que la manda a las cámaras.',
                       'Cámaras e instrumentos: convierten la luz en imágenes y datos.',
                       'Paneles solares: le dan electricidad con la luz del Sol.',
                       'Antenas: mandan las fotos a la Tierra.',
                       'Está en órbita a unos 540 km de altura, arriba de la atmósfera que hace «temblar» la luz: por '
                       'eso sus fotos son tan claras.',
                       'Su defecto: el espejo estaba mal pulido. La solución: una misión de astronautas en 1993.']),
                xp=60, preguntas=[
                ('¿Qué hace el espejo principal del Hubble?', 'Junta la luz de las estrellas',
                 ['Le da electricidad', 'Manda las fotos a la Tierra', 'Lo hace girar']),
                ('¿Para qué sirven los paneles solares?', 'Para darle electricidad', ['Para tomar fotos',
                                                                                      'Para enfriarlo',
                                                                                      'Para hablar con la Tierra']),
                ('¿Qué pieza manda las fotos a la Tierra?', 'Las antenas', ['El espejo', 'Los paneles solares',
                                                                            'La cámara']),
                ('¿Por qué las primeras fotos salieron borrosas?', 'Porque el espejo estaba mal pulido',
                 ['Porque estaba de noche', 'Porque se acabaron las pilas', 'Porque la cámara era de juguete']),
                ('¿Por qué las fotos del Hubble son más claras que las de un telescopio en la Tierra?',
                 'Porque está arriba de la atmósfera', ['Porque es más bonito', 'Porque está más cerca de la Luna',
                                                        'Porque usa flash']),
                ('¿Cómo se arregló el Hubble?', 'Unos astronautas subieron a repararlo en 1993',
                 ['Lo bajaron a la Tierra', 'Se arregló solo', 'Lo cambiaron por otro']),
            ]),
        ]},
        {'nombre': 'Conceptos de programación', 'cofre': 30, 'misiones': [
            mision('Programa a tu dupla', 'presencial', leccion(
                intro='Sin computadora: tu dupla será un robot que solo entiende instrucciones exactas. Vas a escribir un '
                      'algoritmo para que dibuje una constelación.',
                saber=['Algoritmo: una lista de pasos en orden para resolver algo.',
                       'Instrucciones permitidas: → ← ↑ ↓ (avanza un cuadro) y ★ (pinta una estrella en ese cuadro).',
                       'Ciclo: «repite 3 veces [→ ★]» ahorra escribir lo mismo muchas veces.'],
                dinamica=['En duplas, cada quien con una cuadrícula de 6 × 6 cuadros. Empiezan en la esquina de abajo a '
                          'la izquierda.',
                          'El programador escribe su algoritmo en silencio (5 minutos, semáforo en 🔴) y lo entrega.',
                          'El robot lo ejecuta exactamente como está, sin preguntar nada. Después cambian de papel.'],
                pasos=['Dibuja en secreto una constelación de 5 estrellas en tu cuadrícula.',
                       'Escribe el algoritmo con flechas y estrellas. Usa al menos un ciclo «repite».',
                       'Entrégaselo a tu dupla: debe dibujar tu constelación sin ver la original.',
                       'Comparen: si no salió igual, encuentren el paso con el error (el bug) y corríjanlo.'],
                logro=['Tu algoritmo tiene al menos un ciclo y tu dupla dibujó tu constelación igual (o encontraron y '
                       'corrigieron el bug).']), xp=50),
            mision('Los conceptos clave', 'cuestionario', leccion(
                intro='Estas son las palabras que usan los programadores. Las vas a usar todo el mundo.',
                saber=['Programa: un algoritmo escrito para que una computadora lo ejecute.',
                       'Secuencia: los bloques se ejecutan en orden, de arriba hacia abajo.',
                       'Evento: lo que hace que un programa empiece, como «al presionar bandera verde».',
                       'Ciclo: repite bloques («por siempre», «repetir 10», «repetir hasta que»).',
                       'Condicional: decide qué hacer según una condición («si <…> entonces / si no»).',
                       'Variable: guarda un dato que cambia, como los puntos.',
                       'Bug: un error. Depurar: buscarlo y corregirlo.']), xp=60, preguntas=[
                ('¿Qué es un algoritmo?', 'Una lista de pasos en orden para resolver algo',
                 ['Un tipo de computadora', 'Un error del programa', 'Un dibujo']),
                ('«Al presionar bandera verde» es un…', 'Evento', ['Ciclo', 'Condicional', 'Bug']),
                ('Quieres que algo se repita todo el juego. ¿Qué usas?', 'Un ciclo «por siempre»',
                 ['Un evento', 'Una variable', 'Un fondo']),
                ('«Si la pieza toca su lugar, encaja» es un…', 'Condicional', ['Ciclo', 'Evento', 'Disfraz']),
                ('¿Para qué sirve una variable?', 'Para guardar un dato que cambia, como los puntos',
                 ['Para cambiar el fondo', 'Para borrar el programa', 'Para dibujar']),
                ('¿Qué es depurar?', 'Buscar y corregir errores', ['Borrar todo el proyecto', 'Guardar el programa',
                                                                   'Agregar más objetos']),
            ]),
            mision('¿Evento, ciclo o condicional?', 'juego', leccion(
                intro='Hay ejemplos de Scratch y de la vida diaria. Clasifícalos todos.',
                tip='Pregúntate: ¿esto hace que algo empiece, se repita o se decida?'), juego='clasifica_evento_ciclo'),
        ]},
        {'nombre': 'Práctica en Scratch', 'cofre': 30, 'misiones': [
            mision('Scratch en tu idioma', 'link', leccion(
                intro='Scratch es el lenguaje de bloques con el que vas a programar el rompecabezas del Hubble.',
                saber=['Idioma: globo terráqueo (arriba a la izquierda) → «Español Latinoamericano». Todas las misiones '
                       'usan los bloques con ese idioma.',
                       'Escenario: donde se ve el juego. Objetos: los personajes y cosas que programas.',
                       'Pestañas: Código (bloques), Disfraces (cómo se ve el objeto) y Sonidos.',
                       'Coordenadas: x va de -240 (izquierda) a 240 (derecha) y y de -180 (abajo) a 180 (arriba). El '
                       'centro es x: 0, y: 0.',
                       'Guardar: Archivo → Guardar en tu computador.'],
                dinamica=PAREJAS,
                pasos=['Abre el enlace y cambia el idioma a Español Latinoamericano.',
                       'Mueve al gato por el escenario y observa cómo cambian su x y su y abajo del escenario.',
                       'Agrega el fondo «Stars» (Elige un fondo, abajo a la derecha) y el objeto «Star» (Elegir un '
                       'objeto).',
                       'Haz un proyecto de prueba y guárdalo en tu carpeta Hubble como Prueba_TuNombre.'],
                logro=['Tu Scratch está en Español Latinoamericano y sabes dónde están las pestañas, las coordenadas y '
                       'cómo guardar.'],
                entrega='en el comentario, escribe las coordenadas de una esquina del escenario.'),
                xp=50, monedas=15, link=SCRATCH),
            scratch('Cazador de estrellas', leccion(
                intro='Un minijuego de 30 segundos para practicar todo junto: eventos, ciclos, condicionales y una '
                      'variable. Las estrellas aparecen y desaparecen; atrápalas con la mira del telescopio.',
                saber=['«elegir número al azar entre -200 y 200» (Operadores) hace que la estrella aparezca en un lugar '
                       'distinto cada vez.',
                       '«<¿tocando Estrella?> y <¿ratón presionado?>»: las DOS condiciones tienen que cumplirse.',
                       'Variable «puntos»: Variables → Crear una variable → «puntos» → Para todos los objetos.',
                       '«cronómetro» (Sensores) cuenta los segundos desde que lo reinicias.',
                       LEYENDA_SCRATCH],
                dinamica=PAREJAS,
                pasos=['Proyecto nuevo. Borra al gato (clic derecho → eliminar). Agrega el fondo «Stars» y el objeto '
                       '«Star»; llámalo Estrella.',
                       'Pinta un objeto nuevo (Pintar): un círculo sin relleno con una cruz. Llámalo Mira.',
                       'Crea la variable «puntos» y los mensajes que pide el código («atrapada»).',
                       'Arma el código del escenario, de la Estrella y de la Mira.',
                       'Juega: ¿cuántas estrellas atrapas en 30 segundos? Reto: haz que la estrella cambie de lugar más '
                       'rápido.',
                       'Guárdalo en tu carpeta Hubble como Cazador_TuNombre.'],
                logro=['Los puntos suben solo cuando haces clic sobre la estrella y el juego termina a los 30 '
                       'segundos.'],
                tip='Si cuenta muchos puntos de un clic, revisa el último bloque de la Mira: «esperar hasta que <no '
                    '<¿ratón presionado?>>».',
                entrega='sube una captura de tus bloques de la Mira y de tu mejor puntaje.'), CODIGO_CAZADOR),
            scratch('Foto borrosa, foto nítida', leccion(
                intro='El truco del rompecabezas es el efecto «pixelar»: hace que una imagen se vea en cuadritos, como '
                      'una foto borrosa. Aquí aprendes a controlarlo.',
                saber=['«fijar efecto pixelar a 60» pone el efecto en un valor exacto.',
                       '«cambiar el efecto pixelar en -10» le quita 10 cada vez: la imagen se aclara.',
                       '«quitar efectos gráficos» regresa la imagen a la normalidad.',
                       LEYENDA_SCRATCH],
                dinamica=PAREJAS,
                pasos=['Proyecto nuevo con el fondo «Stars». Agrega el objeto «Planet2» y llámalo Foto.',
                       'Arma el código y prueba las flechas arriba y abajo y la barra espaciadora.',
                       'Experimenta: cambia «pixelar» por «mosaico» o «brillo». ¿Qué hace cada uno?',
                       'Guárdalo como Enfoque_TuNombre.'],
                logro=['Con las flechas la foto se pixela y se aclara, y con la barra espaciadora queda nítida.'],
                entrega='sube una captura de tus bloques y de la foto pixelada.'), CODIGO_ENFOQUE, xp=80, monedas=25),
            mision('¿De qué categoría es el bloque?', 'juego', leccion(
                intro='Encuentra rápido cada bloque: clasifícalo en su categoría.',
                tip='Lo que mueve es Movimiento; lo que cambia cómo se ve es Apariencia; lo que «pregunta» o detecta '
                    'es Sensores.'), juego='clasifica_categorias_scratch'),
        ]},
        {'nombre': 'Rompecabezas del Hubble', 'cofre': 35, 'misiones': [
            mision('Plano del rompecabezas', 'texto', leccion(
                intro='Antes de programar, los equipos de la NASA planean. Escribe el plan de tu rompecabezas.',
                saber=['El juego: la foto de una galaxia empieza muy pixelada. Hay 4 piezas del Hubble (espejo, cámara, '
                       'panel solar y antena) y 4 ranuras en el cuerpo del telescopio. Cada pieza que encaja aclara la '
                       'foto. Con las 4, la foto queda nítida.',
                       'Objetos: Telescopio, 4 piezas, 4 ranuras y un Guía.',
                       'Variable: «piezas» (cuántas van). Mensajes: «pieza lista» y «Hubble reparado».'],
                pasos=['Escribe qué hace cada objeto en una línea.',
                       'Escribe la condición para que una pieza encaje (pista: tiene dos partes unidas con «y»).',
                       '¿Qué pasa si sueltas una pieza en la ranura equivocada?',
                       '¿Cuánto se aclara la foto con cada pieza si empieza en 100 de pixelado? (Pista: 4 piezas.)'],
                logro=['Tu plan explica cada objeto, la condición para encajar y cuánto se aclara la foto.'],
                entrega='escribe tu plan aquí abajo.'), xp=60),
            scratch('Rompecabezas paso 1: la foto borrosa', leccion(
                intro='Empieza por el escenario: la foto de la galaxia muy pixelada y el cuerpo del telescopio con sus 4 '
                      'ranuras.',
                saber=['El escenario también tiene efectos: si lo pixelas, se pixela el fondo completo.',
                       'Una ranura es solo el contorno de la pieza: así el jugador sabe dónde va cada una.',
                       'El último programa (tecla espacio) sirve para PROBAR antes de tener las piezas. Los '
                       'programadores hacen esto todo el tiempo.',
                       LEYENDA_SCRATCH],
                dinamica=PAREJAS,
                pasos=['Proyecto nuevo: Hubble_TuNombre. Borra al gato y agrega el fondo «Galaxy» (o «Nebula»).',
                       'Pinta el objeto Telescopio: un rectángulo gris grande del lado derecho.',
                       'Pinta 4 objetos de ranura con la herramienta Rectángulo o Círculo, solo con contorno (sin '
                       'relleno): Ranura espejo, Ranura cámara, Ranura panel y Ranura antena. Acomódalas sobre el '
                       'telescopio.',
                       'Crea la variable «piezas» y arma el código del escenario.',
                       'Prueba: bandera verde (la galaxia se pixela) y luego 4 veces la barra espaciadora (se aclara '
                       'poco a poco).',
                       'Guarda tu proyecto.'],
                logro=['La galaxia empieza pixelada y con 4 espacios queda nítida.'],
                entrega='sube una captura del escenario pixelado con el telescopio y sus ranuras.'), CODIGO_PASO1),
            scratch('Rompecabezas paso 2: piezas que encajan', leccion(
                intro='Ahora las piezas: aparecen a la izquierda, el jugador las arrastra y, si las suelta en su ranura, '
                      'encajan solas.',
                saber=['«fijar modo de arrastre a arrastrable» (Sensores) deja que el jugador mueva la pieza con el mouse '
                       'aunque el juego esté en pantalla completa.',
                       '«esperar hasta que <<¿tocando Ranura espejo?> y <no <¿ratón presionado?>>>»: espera a que la '
                       'pieza esté en su lugar Y el jugador la haya soltado. Esa es una decisión con dos condiciones.',
                       'Duplicar: clic derecho en el objeto → duplicar. Se copia con todo y su código.',
                       LEYENDA_SCRATCH],
                dinamica=PAREJAS,
                pasos=['Borra el programa de prueba de la tecla espacio.',
                       'Pinta la primera pieza: el Espejo (un círculo plateado) del tamaño de su ranura.',
                       'Arma el código del Espejo y pruébalo: arrástralo a su ranura y suéltalo. Debe encajar y aclarar '
                       'la foto.',
                       'Duplica el Espejo 3 veces. Llámalas Cámara, Panel y Antena, y redibuja su disfraz.',
                       'En cada una cambia «Ranura espejo» por su propia ranura (en los DOS bloques).',
                       'Prueba las 4 piezas y guarda.'],
                logro=['Cada pieza solo encaja en su propia ranura y cada una aclara un poco la foto.'],
                tip='Si una pieza no encaja, revisa que el nombre de la ranura sea exactamente el mismo en sus dos '
                    'bloques.',
                entrega='sube una captura del código de una pieza y del rompecabezas a la mitad.'), CODIGO_PASO2,
                xp=110, monedas=30),
            scratch('Rompecabezas paso 3: ¡Hubble reparado!', leccion(
                intro='El cierre: un Guía que explica el juego y festeja cuando la foto queda nítida, diciendo en cuántos '
                      'segundos lo lograste.',
                saber=['«unir» (Operadores) junta un texto con un número: «¡Foto nítida! Segundos: 23».',
                       '«redondear» (Operadores) quita los decimales del cronómetro.',
                       'Reto: dibuja un segundo disfraz del telescopio con brillos y llámalo «reparado» (y al primero, '
                       '«dañado»).',
                       LEYENDA_SCRATCH],
                dinamica=PAREJAS,
                pasos=['Agrega un personaje de la biblioteca como Guía y arma su código.',
                       'Juega el rompecabezas completo: ¿el Guía dice tu tiempo al final?',
                       'Reto: agrega el segundo disfraz del telescopio y su código.',
                       'Pon tu nombre como título del proyecto y guárdalo.'],
                logro=['Al encajar las 4 piezas, la foto queda nítida y el Guía dice en cuántos segundos lo lograste.'],
                entrega='sube una captura del final del juego con la foto nítida.'), CODIGO_PASO3, xp=100, monedas=30),
        ]},
        {'nombre': 'Control de calidad', 'cofre': 40, 'misiones': [
            mision('Bugs en órbita', 'texto', leccion(
                intro='Este código de otro alumno tiene 3 bugs: la cámara nunca encaja, la foto se pone más borrosa y el '
                      'juego nunca termina. Encuéntralos.',
                saber=['Depurar es revisar el programa renglón por renglón y preguntarte: ¿esto hace lo que debería?',
                       'Pistas: revisa los nombres de las ranuras, los signos de los números y cuántas piezas hay.'],
                pasos=['Lee el código de la Cámara y del escenario.',
                       'Encuentra los 3 bugs.',
                       'Escribe cómo arreglarías cada uno.'],
                entrega='escribe aquí: «Bug 1: … · Arreglo: …» (los tres).'), xp=70, monedas=20,
                codigo=CODIGO_BUGS.strip('\n'), link=SCRATCH),
            mision('Prueba cruzada', 'presencial', leccion(
                intro='Ningún programa sale sin probarse. Hoy tus compañeros serán tus probadores.',
                dinamica=['Cada quien deja su rompecabezas abierto. Cambian de lugar con su dupla.',
                          'El probador juega dos veces sin que el autor le diga nada. Semáforo en 🟡.',
                          'Después regresan a su lugar a corregir.'],
                pasos=['Juega el rompecabezas de tu dupla y revisa: ¿cada pieza encaja solo en su ranura? ¿La foto se '
                       'aclara con cada pieza? ¿El Guía dice el tiempo?',
                       'Escríbele en una nota: 2 cosas que funcionan y 1 bug o mejora.',
                       'Regresa a tu lugar y corrige lo que te encontraron.',
                       'Cuéntale al profe cuál fue el bug más difícil de encontrar.'],
                logro=['Probaste el juego de tu dupla, le dejaste tu nota y corregiste el tuyo.']), xp=50),
            jefe('Jefe: El Espejo Torcido', leccion(
                intro='El Espejo Torcido distorsiona todo lo que ve. Solo un programador que domine eventos, ciclos, '
                      'condicionales y variables puede enderezarlo.'), [
                ('¿Qué bloque hace que un programa empiece?', 'al presionar bandera verde',
                 ['por siempre', 'cambiar x en 10', 'quitar efectos gráficos']),
                ('¿Qué bloque repite algo durante todo el juego?', 'por siempre', ['si <…> entonces', 'enviar',
                                                                                   'fijar puntos a 0']),
                ('La pieza debe encajar solo si toca su ranura y el jugador ya la soltó. ¿Qué operador une las dos '
                 'condiciones?', 'y', ['o', 'unir', 'no']),
                ('La foto empieza con pixelar en 100 y hay 4 piezas. ¿Cuánto cambias el efecto con cada pieza?', '-25',
                 ['25', '-100', '-4']),
                ('¿Para qué sirve la variable «piezas»?', 'Para contar cuántas piezas ya encajaron',
                 ['Para cambiar el fondo', 'Para mover las piezas', 'Para dibujar las ranuras']),
                ('Una pieza no encaja nunca. ¿Qué revisas primero?', 'Que el nombre de su ranura esté bien escrito',
                 ['El color del fondo', 'El volumen', 'El tamaño del gato']),
                ('¿Qué hace «enviar Hubble reparado»?', 'Avisa a todos los objetos que el telescopio ya está completo',
                 ['Guarda el proyecto', 'Borra las piezas', 'Reinicia el juego']),
                ('¿Por qué las primeras fotos del Hubble salieron borrosas?', 'Por un defecto en su espejo',
                 ['Porque estaba nublado', 'Por falta de pilas', 'Porque era de noche']),
            ]),
        ]},
    ],
}
