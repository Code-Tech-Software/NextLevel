"""Mundo 1 · ES-SEA202 ¡Intenta, aprende, avanza!: la computadora, el error como pista y un videojuego de
obstáculos en Scratch con ciclos y mensajes."""
from .base import LEYENDA_SCRATCH, SCRATCH, clasifica, jefe, leccion, mision, scratch

JUEGOS = {
    'clasifica_es': clasifica('Detective digital: ¿entrada o salida?', '🕵️', '¿Le da información a la compu o la saca?', [
        ('Entrada', '⌨️', ['Teclado', 'Mouse', 'Micrófono', 'Cámara web', 'Escáner', 'Control de videojuegos', 'Lápiz digital']),
        ('Salida', '🖥️', ['Monitor', 'Bocinas', 'Impresora', 'Audífonos', 'Proyector']),
        ('Entrada y salida', '🔄', ['Pantalla táctil', 'Audífonos con micrófono', 'Impresora que también escanea']),
    ]),
    'clasifica_bloques': clasifica('¿Qué tipo de bloque es?', '🧩', 'Cada familia de bloques de Scratch tiene su color.', [
        ('Eventos', '🟨', ['al hacer clic en la bandera verde', 'al presionar tecla espacio', 'al hacer clic en este objeto',
                          'al recibir mensaje', 'enviar mensaje', 'cuando el fondo cambie a…']),
        ('Control', '🟧', ['por siempre', 'repetir 10', 'esperar 1 segundos', 'si … entonces', 'repetir hasta que…',
                          'detener todos', 'crear clon de mí mismo']),
        ('Movimiento', '🟦', ['mover 10 pasos', 'girar 15 grados', 'ir a x: 0 y: 0', 'deslizar en 1 segs a…',
                             'cambiar x en 10', 'rebotar si toca un borde']),
    ], rondas=14),
    'robot_piloto': {'nombre': 'Robot piloto: prueba y corrige', 'icono': '🤖', 'plantilla': 'robot', 'en_arcade': True,
                     'descripcion': 'Programa al robot con flechas. Si choca, corrige y vuelve a intentar.',
                     'configuracion': {'dificultad': 'facil', 'niveles': 5, 'modo': 'flechas', 'bucles': False}},
}

CODIGO_DESPEGUE = '''
OBJETO: Cohete
al hacer clic en la bandera verde
    ir a x: 0 y: -120
    decir "3" durante 1 segundos
    decir "2" durante 1 segundos
    decir "1" durante 1 segundos
    decir "¡Despegue!" durante 1 segundos
    iniciar sonido (el que tú elijas)
    deslizar en 2 segs a x: 0 y: 150
'''

CODIGO_ASTEROIDE = '''
OBJETO: Asteroide
al hacer clic en la bandera verde
    ir a x: 240 y: (número aleatorio entre -150 y 150)
    por siempre
        cambiar x en -5
        girar ↻ 5 grados
        si <(posición en x) < -230> entonces
            ir a x: 240 y: (número aleatorio entre -150 y 150)
'''

CODIGO_MENSAJES = '''
OBJETO: Botón
al hacer clic en este objeto
    decir "¡Iniciando motores!" durante 1 segundos
    enviar "despegar"

OBJETO: Cohete
al hacer clic en la bandera verde
    ir a x: 0 y: -120
    mostrar
al recibir "despegar"
    repetir 30
        cambiar y en 10
    esconder

ESCENARIO
al hacer clic en la bandera verde
    cambiar fondo a "Stars"
al recibir "despegar"
    esperar 2 segundos
    cambiar fondo a (tu segundo fondo)
'''

CODIGO_BUGS = '''
OBJETO: Botón
al hacer clic en este objeto
    enviar "Despega"

OBJETO: Cohete
al recibir "despegar"
    repetir 30
    cambiar y en -10
    esconder
'''

CODIGO_NAVE = '''
OBJETO: Nave
al hacer clic en la bandera verde
    ir a x: -180 y: 0
    por siempre
        si <¿tecla flecha arriba presionada?> entonces
            cambiar y en 8
        si <¿tecla flecha abajo presionada?> entonces
            cambiar y en -8
'''

CODIGO_OBSTACULOS = '''
OBJETO: Asteroide
al hacer clic en la bandera verde
    esconder
    por siempre
        crear clon de "mí mismo"
        esperar 1 segundos

al comenzar como clon
    ir a x: 240 y: (número aleatorio entre -160 y 160)
    mostrar
    repetir hasta que <(posición en x) < -230>
        cambiar x en -6
    eliminar este clon
'''

CODIGO_CHOQUES = '''
OBJETO: Nave (agrega este programa a lo que ya tenías)
al hacer clic en la bandera verde
    esperar hasta que <¿tocando "Asteroide"?>
    enviar "perdiste"

ESCENARIO
al hacer clic en la bandera verde
    cambiar fondo a "Stars"
    fijar "puntos" a 0
    repetir hasta que <(puntos) = 30>
        esperar 1 segundos
        cambiar "puntos" en 1
    enviar "ganaste"

al recibir "perdiste"
    cambiar fondo a "GAME OVER"
    detener "todos"

al recibir "ganaste"
    cambiar fondo a "GANASTE"
    detener "todos"
'''

MUNDO = {
    'nombre': 'Estación Despegue', 'tema': 'espacio',
    'descripcion': 'ES-SEA202 · ¡Intenta, aprende, avanza! Cleo quería hacer el mejor avión de papel y descubrió que '
                   'cada error es una pista. Conoce tu computadora, aprende Scratch y programa un videojuego de '
                   'obstáculos con ciclos y mensajes. Pregunta guía: ¿cómo sabes si vas por el camino correcto?',
    'niveles': [
        {'nombre': 'Conoce tu nave', 'cofre': 25, 'misiones': [
            mision('Reglas de la estación', 'presencial', leccion(
                intro='Antes de despegar, la tripulación hace sus acuerdos del laboratorio de cómputo. Una nave bien '
                      'cuidada dura muchos años.',
                saber=['La computadora es una herramienta de todo el grupo: lo que le pase nos afecta a todos.',
                       'Los líquidos y las migajas descomponen el teclado; los jalones dañan cables y audífonos.',
                       'Apagar desde el menú Inicio deja que la computadora cierre todo bien; desconectarla de golpe '
                       'puede dañar archivos.'],
                pasos=['Escucha con tu equipo los acuerdos: manos limpias, nada de comida ni bebida, cuidar cables y '
                       'audífonos y no cambiar la configuración de la compu.',
                       'Enciende la computadora con el botón de encendido y espera a que aparezca el escritorio.',
                       'Siéntate como piloto: espalda recta, pies en el piso, hombros relajados y la pantalla a la '
                       'altura de tus ojos, a un brazo de distancia.',
                       'Al terminar la clase: guarda tu trabajo, cierra los programas y apaga desde Inicio → '
                       'Encendido → Apagar.'],
                logro=['Puedes decir 3 acuerdos del laboratorio sin verlos.',
                       'Enciendes y apagas la computadora correctamente.'],
                entrega='tu profe marca esta misión cuando la tripulación la complete.'), xp=40, monedas=10),
            mision('Partes de la nave', 'cuestionario', leccion(
                intro='Toda nave tiene piezas que trabajan en equipo. Repasa y demuestra que conoces tu computadora.',
                saber=['Hardware: las partes que puedes tocar (monitor, teclado, mouse, CPU, bocinas).',
                       'Software: los programas que no se tocan, como Scratch, Word o el navegador.',
                       'El procesador (CPU) es el «cerebro»: hace todos los cálculos.',
                       'Entrada: le da información a la compu (teclado, mouse, micrófono, cámara).',
                       'Salida: saca información de la compu (monitor, bocinas, impresora, audífonos).',
                       'El almacenamiento (disco duro) guarda tus archivos aunque apagues la compu.']), xp=60, preguntas=[
                ('¿Qué parte de la computadora muestra las imágenes?', 'El monitor', ['El teclado', 'Las bocinas', 'El mouse']),
                ('¿Qué parte es el «cerebro» que hace los cálculos?', 'El procesador (CPU)',
                 ['El mouse', 'La pantalla', 'El cable de luz']),
                ('¿Cuál de estos es software?', 'Scratch', ['El teclado', 'El monitor', 'Las bocinas']),
                ('¿Cuál es un dispositivo de entrada?', 'El micrófono', ['La impresora', 'Las bocinas', 'El monitor']),
                ('¿Dónde se quedan tus archivos cuando apagas la computadora?', 'En el almacenamiento (disco duro)',
                 ['En el monitor', 'En el mouse', 'Se borran siempre']),
                ('¿Cuál es la postura correcta frente a la computadora?',
                 'Espalda recta, pies en el piso y pantalla a la altura de los ojos',
                 ['Acostado en la silla', 'Con la cara pegada a la pantalla', 'Hincado sobre la silla']),
                ('Para apagar la computadora correctamente debes…', 'Apagarla desde el menú Inicio',
                 ['Desconectar el cable', 'Apretar todas las teclas', 'Cerrar la tapa sin guardar']),
            ]),
            mision('Detective digital: ¿entrada o salida?', 'juego', leccion(
                intro='¿El dispositivo le da información a la computadora o la saca? Clasifica cada tarjeta antes de '
                      'que se acabe el tiempo.',
                tip='Piensa hacia dónde viaja la información: de ti a la compu es entrada; de la compu a ti es salida.'),
                juego='clasifica_es'),
            mision('Pilotos del escritorio', 'presencial', leccion(
                intro='El escritorio es la cabina de tu nave: desde ahí abres programas, archivos y ventanas.',
                saber=['Escritorio: la pantalla principal con íconos (dibujitos que abren programas o carpetas).',
                       'Barra de tareas: la franja de abajo con el botón Inicio, los programas abiertos y el reloj.',
                       'Cada programa trabaja en una ventana. Arriba a la derecha tiene 3 botones: — minimizar (la '
                       'esconde en la barra de tareas), □ maximizar (la hace grande) y ✕ cerrar.',
                       'Mouse: clic (seleccionar), doble clic (abrir), clic derecho (menú de opciones), arrastrar '
                       '(mantener presionado y mover) y rueda (subir y bajar).'],
                pasos=['Abre el menú Inicio y escribe «Paint» para buscarlo. Ábrelo.',
                       'Minimiza la ventana. Búscala en la barra de tareas y vuelve a abrirla con un clic.',
                       'Maximiza la ventana y luego regrésala a su tamaño normal.',
                       'Arrastra la ventana desde su barra de título (la franja de arriba) a otro lugar.',
                       'Abre la calculadora y cambia entre los dos programas con Alt + Tab (mantén Alt y presiona Tab).',
                       'Cierra las dos ventanas con la ✕.'],
                logro=['Minimizas, maximizas, mueves y cierras ventanas sin ayuda.',
                       'Usas el clic derecho y el doble clic en el momento correcto.'],
                entrega='muéstrale a tu profe la secuencia completa.'), xp=50),
            mision('Mi carpeta de piloto', 'evidencia', leccion(
                intro='Un piloto ordenado nunca pierde sus mapas. Hoy crearás la carpeta donde guardarás TODO tu '
                      'trabajo del año.',
                saber=['Un archivo es un trabajo guardado: un dibujo, un texto, un proyecto de Scratch.',
                       'Una carpeta guarda y ordena archivos, como un fólder.',
                       'La ruta dice dónde está un archivo, por ejemplo: Documentos › TIC_4A_Ana › Scratch.'],
                pasos=['Abre el Explorador de archivos (la carpeta amarilla de la barra de tareas).',
                       'Entra a «Documentos» (o a donde te indique tu profe).',
                       'Clic derecho en un espacio vacío → Nuevo → Carpeta.',
                       'Escribe el nombre TIC_4A_TuNombre (por ejemplo: TIC_4A_Ana) y presiona Enter.',
                       'Entra a tu carpeta y crea adentro tres carpetas: Scratch, Documentos y Presentaciones.',
                       'Si te equivocaste en un nombre: clic derecho → Cambiar nombre.'],
                logro=['Tu carpeta tiene tu nombre y las 3 subcarpetas.', 'Sabes decir la ruta de tu carpeta.'],
                tip='Nunca uses nombres como «asdf» o «nuevo1»: en un mes no sabrás qué hay adentro.',
                entrega='sube una foto o captura donde se vean tu carpeta y sus 3 subcarpetas.'), xp=70, monedas=20),
        ]},
        {'nombre': 'El misterio del avión de papel', 'cofre': 30, 'misiones': [
            mision('El caso de Cleo', 'texto', leccion(
                intro='Cleo quería hacer el mejor avión de papel, pero ninguno volaba bien: unos chocaban y otros '
                      'caían en picada. Se puso sus gafas de detective y empezó a investigar. Notó pistas en los '
                      'dobleces, en el peso y en otros detalles. Aunque fallaba, cada intento lo acercaba más a la '
                      'respuesta.\n\nPregunta del caso: ¿cómo sabes si vas por el camino correcto?',
                saber=['Una hipótesis es una idea que crees que explica algo y que puedes poner a prueba.',
                       'En un buen experimento cambias UNA sola cosa a la vez; así sabes qué causó el cambio.'],
                pasos=['Escribe 2 hipótesis sobre qué hace que un avión de papel vuele más lejos (por ejemplo: «Si '
                       'la punta pesa más, volará más recto»).',
                       'Para cada hipótesis, escribe qué cambiarías en el avión para comprobarla.',
                       'Responde con tus palabras: ¿cómo sabes si vas por el camino correcto?'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('Laboratorio de aviones', 'evidencia', leccion(
                intro='Hoy eres Cleo: vas a probar, medir y mejorar tu avión hasta encontrar el mejor diseño.',
                material=['3 hojas tamaño carta', 'Un clip', 'Cinta métrica (o mide con tus pasos)', 'Tu cuaderno'],
                pasos=['Dobla un avión clásico de punta. Lánzalo 3 veces desde la misma línea y anota cuánto voló.',
                       'Cambia UNA cosa: ponle un clip en la punta. Lánzalo 3 veces y anota.',
                       'Cambia otra cosa: dobla hacia arriba las puntas de las alas. Lánzalo 3 veces y anota.',
                       'Haz una tabla: Versión · ¿Qué cambié? · Distancia 1 · Distancia 2 · Distancia 3.',
                       'Encierra la versión ganadora y escribe por qué crees que voló mejor.'],
                logro=['Probaste 3 versiones cambiando una cosa a la vez.', 'Tu tabla tiene todas las mediciones.'],
                tip='Lanza siempre con la misma fuerza y desde el mismo lugar; si no, la prueba no es justa.',
                entrega='sube una foto de tu tabla junto a tu avión ganador.'), xp=90, monedas=25),
            mision('Bitácora: el día que no me rendí', 'texto', leccion(
                intro='Los ingenieros dicen: «Intenta, aprende, avanza». Los errores no son el final: son pistas.',
                pasos=['Piensa en algo que al principio no te salía y que lograste con práctica (andar en bici, un '
                       'truco, una tabla de multiplicar, un nivel de un videojuego).',
                       'Escribe: ¿qué era?, ¿qué hiciste diferente en cada intento? y ¿qué te enseñó el error?',
                       'Termina con una frase que empiece con «Todavía no sé…, pero…».'],
                entrega='escribe tu bitácora aquí abajo (mínimo 5 renglones).'), xp=60),
            mision('¿Error o pista?', 'cuestionario', leccion(
                intro='Demuestra que piensas como un detective que aprende de sus errores.',
                saber=['Ciclo del ingeniero: Preguntar → Imaginar → Planear → Crear → Probar → Mejorar (y otra vez).',
                       'Un error te dice qué NO funciona: eso ya es información.',
                       'En un experimento justo cambias una sola cosa y mides igual cada vez.',
                       '«Todavía no» significa que con práctica sí podrás.']), xp=60, preguntas=[
                ('Cuando algo no te sale a la primera, lo mejor es…', 'Intentarlo otra vez cambiando algo',
                 ['Rendirte', 'Culpar a alguien más', 'Copiarle al de junto']),
                ('Un error sirve para…', 'Saber qué cambiar en el siguiente intento',
                 ['Sentirte mal', 'Dejar de intentarlo', 'Nada']),
                ('¿Cuál es el orden del ciclo del ingeniero?', 'Preguntar → Imaginar → Planear → Crear → Probar y mejorar',
                 ['Crear → Rendirse → Imaginar', 'Probar → Terminar sin mejorar', 'Mejorar → Crear → Preguntar']),
                ('Cleo quiere saber si el clip ayuda a su avión. ¿Qué debe hacer?',
                 'Probar el mismo avión con clip y sin clip, sin cambiar nada más',
                 ['Cambiar el papel, las alas y el clip al mismo tiempo', 'Lanzarlo una sola vez', 'Adivinar']),
                ('¿Por qué Cleo lanza cada avión 3 veces?', 'Para comparar y no confiarse de un solo intento',
                 ['Porque le aburre', 'Para romperlo', 'No sirve de nada']),
                ('Decir «todavía no lo sé hacer» significa que…', 'Puedo aprenderlo con práctica',
                 ['Nunca lo voy a lograr', 'No sirvo para eso', 'Otro lo debe hacer por mí']),
            ]),
        ]},
        {'nombre': 'Cabina de Scratch', 'cofre': 30, 'misiones': [
            mision('Conoce Scratch', 'link', leccion(
                intro='Scratch es un programa para crear juegos, historias y animaciones encajando bloques de colores, '
                      'como piezas de rompecabezas.',
                saber=['Escenario: el rectángulo donde pasa todo (ahí se ve tu juego).',
                       'Objetos: los personajes y cosas que programas. El gato es el objeto que viene de inicio.',
                       'Categorías de bloques: Movimiento (azul), Apariencia (morado), Sonido (rosa), Eventos '
                       '(amarillo), Control (naranja), Sensores (azul claro), Operadores (verde) y Variables.',
                       'Área de programación: el espacio de en medio donde arrastras y encajas los bloques.',
                       'Bandera verde: inicia el programa. Señal roja: lo detiene.'],
                pasos=['Abre el enlace. Si está en inglés, da clic en el globo terráqueo (arriba a la izquierda) y '
                       'elige «Español».',
                       'En Movimiento, arrastra el bloque «mover (10) pasos» al área de programación y dale clic. '
                       '¿Qué hizo el gato?',
                       'Cambia el 10 por 50 y vuelve a darle clic.',
                       'En Apariencia busca «decir ¡Hola! durante 2 segundos», encájalo debajo y dale clic a los dos.',
                       'Explora: cambia el fondo («Elige un fondo», abajo a la derecha) y agrega un objeto nuevo.'],
                logro=['Señalas el escenario, los objetos, las categorías y el área de programación.',
                       'Hiciste que el gato se moviera y hablara.'],
                entrega='en el comentario, escribe para qué sirven 3 categorías de bloques.'),
                xp=60, link=SCRATCH),
            scratch('Mi primer programa: ¡despegue!', leccion(
                intro='Vas a programar tu primer cohete: al presionar la bandera verde hará la cuenta regresiva y '
                      'despegará.',
                saber=['Todo programa empieza con un bloque de Eventos (los amarillos con la parte de arriba redonda). '
                       'Sin él, nada se mueve solo.',
                       'El escenario es como un plano: x va de izquierda (−) a derecha (+) y y de abajo (−) a arriba '
                       '(+). El centro es x: 0, y: 0.',
                       'Scratch hace los bloques de arriba hacia abajo, uno por uno: eso es una secuencia.',
                       LEYENDA_SCRATCH],
                pasos=['Borra el gato (clic derecho → borrar), agrega el objeto «Rocketship» y el fondo «Stars».',
                       'Arma en el cohete los bloques del código de abajo.',
                       'Presiona la bandera verde. Si no despega, compara bloque por bloque con el código.',
                       'Cambia los números para que suba más lento o más rápido.',
                       'Guarda: Archivo → Guardar en tu computadora → en TIC_4A_TuNombre › Scratch, con el nombre '
                       'Despegue_TuNombre.'],
                logro=['El cohete regresa a su lugar, cuenta 3, 2, 1 y sube hasta arriba.',
                       'Tu proyecto quedó guardado en tu carpeta.'],
                entrega='sube una captura de tus bloques y del cohete en el escenario.'), CODIGO_DESPEGUE),
            mision('¿Qué tipo de bloque es?', 'juego', leccion(
                intro='Clasifica cada bloque en su familia: Eventos (amarillo), Control (naranja) o Movimiento (azul).',
                tip='Los Eventos arrancan los programas; Control decide cuántas veces o cuándo; Movimiento mueve al objeto.'),
                juego='clasifica_bloques'),
            mision('Robot piloto: prueba y corrige', 'juego', leccion(
                intro='Programa al robot con flechas para llegar a la batería. Si choca, no borres todo: revisa paso a '
                      'paso dónde se equivocó y corrige solo ese paso.',
                saber='Así trabajan los programadores: prueban, encuentran el error (el «bug») y lo corrigen. A eso se '
                      'le llama depurar.'), xp=60, juego='robot_piloto'),
            mision('Scratch a la vista', 'cuestionario', leccion(
                intro='Demuestra que ya sabes moverte en la cabina de Scratch.',
                saber=['Los bloques de Eventos inician los programas, por ejemplo «al hacer clic en la bandera verde».',
                       'Scratch hace los bloques de arriba hacia abajo.',
                       'x mueve a izquierda y derecha; y mueve arriba y abajo. El centro es (0, 0).',
                       'Para guardar en tu compu: Archivo → Guardar en tu computadora.',
                       'Un error en un programa se llama bug; arreglarlo se llama depurar.']), xp=60, preguntas=[
                ('¿Cómo se llama el lugar donde se ve lo que programas en Scratch?', 'El escenario',
                 ['La paleta', 'El disfraz', 'La carpeta']),
                ('¿Qué bloque sirve para que un programa empiece?', 'Al hacer clic en la bandera verde',
                 ['Mover 10 pasos', 'Decir ¡Hola!', 'Girar 15 grados']),
                ('Si quieres que un objeto suba, ¿qué cambias?', 'La coordenada y (la hago más grande)',
                 ['La coordenada x', 'El color del fondo', 'El volumen']),
                ('¿En qué orden hace Scratch los bloques de un programa?', 'De arriba hacia abajo',
                 ['De abajo hacia arriba', 'Al azar', 'Todos a la vez sin orden']),
                ('A los personajes y cosas que programas en Scratch se les llama…', 'Objetos',
                 ['Ventanas', 'Celdas', 'Diapositivas']),
                ('¿Cómo guardas tu proyecto en tu carpeta?', 'Archivo → Guardar en tu computadora',
                 ['Cerrando la ventana', 'Presionando la bandera verde', 'Apagando la compu']),
            ]),
        ]},
        {'nombre': 'Ciclos y mensajes', 'cofre': 35, 'misiones': [
            mision('Baila el ciclo', 'presencial', leccion(
                intro='Antes de programar ciclos en la compu, ¡los vas a bailar!',
                saber=['Un ciclo (o bucle) repite instrucciones. En vez de decir «aplaude» 10 veces, dices «repite 10 '
                       'veces: aplaude».',
                       'Scratch tiene 3 ciclos: «repetir (10)» repite un número exacto de veces; «por siempre» repite '
                       'sin parar hasta la señal roja; «repetir hasta que…» repite hasta que pasa algo.'],
                pasos=['Tu profe dicta un programa SIN ciclos: «paso adelante, aplaude, paso adelante, aplaude, paso '
                       'adelante, aplaude…». ¡Qué largo!',
                       'Ahora con ciclo: «repetir 4 veces: paso adelante, aplaude». ¿Cuál fue más fácil?',
                       '«Por siempre: salta», hasta que el profe diga ¡ALTO! (la señal roja).',
                       '«Repetir hasta que el profe levante la mano: gira».',
                       'En equipos, inventen un baile con al menos un ciclo; el grupo adivina qué ciclo usaron.'],
                logro=['Explicas la diferencia entre repetir, por siempre y repetir hasta que.'],
                entrega='tu profe marca la misión cuando tu equipo presente su baile.'), xp=50),
            scratch('El asteroide infinito', leccion(
                intro='En tu videojuego, los asteroides deben pasar una y otra vez. En lugar de programarlos mil veces, '
                      'usarás el ciclo «por siempre».',
                saber=['«por siempre» repite todo lo que tiene adentro sin detenerse.',
                       '«número aleatorio entre -150 y 150» (Operadores) elige un número distinto cada vez: así el '
                       'asteroide aparece a alturas diferentes.',
                       '«si … entonces» revisa una condición: si se cumple, hace lo de adentro.',
                       LEYENDA_SCRATCH],
                pasos=['Proyecto nuevo con el fondo «Stars». Agrega el objeto «Rocks» y llámalo Asteroide.',
                       'Arma el código. «posición en x» está al final de Movimiento y el signo «<» en Operadores.',
                       'Presiona la bandera: el asteroide debe cruzar de derecha a izquierda y volver a aparecer.',
                       'Experimenta: cambia el -5 por -10. ¿Qué pasa? Cambia también el giro.',
                       'Guarda como Asteroide_TuNombre en tu carpeta.'],
                logro=['El asteroide cruza la pantalla sin parar y aparece a diferentes alturas.'],
                entrega='sube una captura de tus bloques.'), CODIGO_ASTEROIDE),
            scratch('Mensajes entre objetos', leccion(
                intro='Los objetos de Scratch se hablan con mensajes, como walkie-talkies: uno «envía» y los demás '
                      '«reciben».',
                saber=['«enviar [mensaje]» (Eventos) avisa a todos los objetos al mismo tiempo.',
                       '«al recibir [mensaje]» se activa cuando llega ese aviso. Puede estar en cualquier objeto o en '
                       'el escenario.',
                       'Para crear un mensaje: abre la flechita del bloque «enviar» → «Nuevo mensaje» → escribe el nombre.',
                       'El nombre debe ser EXACTAMENTE igual al enviar y al recibir.',
                       LEYENDA_SCRATCH],
                pasos=['Proyecto nuevo con fondo «Stars». Agrega los objetos «Button2» (botón) y «Rocketship».',
                       'En el escenario, pestaña Fondos, agrega un segundo fondo del espacio (por ejemplo «Nebula»).',
                       'Arma el código del botón (crea el mensaje «despegar»), luego el del cohete y el del escenario.',
                       'Presiona la bandera y da clic en el botón: los tres deben reaccionar al mismo mensaje.',
                       'Guarda como Mensajes_TuNombre.'],
                logro=['Al dar clic en el botón, el cohete despega y el fondo cambia.',
                       'Explicas quién envía y quién recibe el mensaje.'],
                entrega='sube una captura de los bloques del botón o del cohete.'), CODIGO_MENSAJES),
            mision('Cazadores de bugs', 'texto', leccion(
                intro='Este programa tiene 3 bugs. El cohete debería subir poco a poco cuando llega el mensaje '
                      '«despegar», pero no funciona.',
                saber=['Depurar es buscar y arreglar errores revisando el programa paso a paso.',
                       'Pistas: revisa si los nombres de los mensajes son iguales, si los bloques están dentro del '
                       'ciclo correcto y si los números tienen sentido.'],
                pasos=['Lee el código del botón y del cohete renglón por renglón.',
                       'Encuentra los 3 bugs. Si quieres, ármalo en Scratch para probarlo.',
                       'Escribe cada bug y cómo lo arreglarías.'],
                entrega='escribe aquí: «Bug 1: … · Arreglo: …» (los tres).'), xp=70, monedas=20, codigo=CODIGO_BUGS.strip('\n')),
            mision('Ciclos y mensajes', 'cuestionario', leccion(
                intro='Repasa los ciclos y los mensajes antes de construir tu videojuego.',
                saber=['«repetir (10)»: repite un número exacto de veces.', '«por siempre»: repite sin parar.',
                       '«repetir hasta que <condición>»: repite hasta que la condición se cumple.',
                       '«enviar» manda un mensaje y «al recibir» lo escucha.',
                       'El nombre del mensaje debe ser igual al enviar y al recibir.']), xp=60, preguntas=[
                ('¿Para qué sirve un ciclo?', 'Para repetir instrucciones sin escribirlas muchas veces',
                 ['Para borrar el programa', 'Para cambiar el idioma', 'Para guardar el proyecto']),
                ('Quieres que un asteroide se mueva durante todo el juego. ¿Qué ciclo usas?', 'Por siempre',
                 ['Repetir 2', 'Ninguno', 'Esperar 1 segundo']),
                ('Quieres que un personaje salte exactamente 3 veces. ¿Qué usas?', 'Repetir 3',
                 ['Por siempre', 'Repetir hasta que se acabe el juego', 'Ningún ciclo']),
                ('«Repetir hasta que ¿tocando Meta?» significa que…', 'Repite hasta que el objeto toque la meta',
                 ['Repite 10 veces', 'Nunca repite', 'Repite solo si presionas espacio']),
                ('¿Qué bloque escucha un mensaje?', 'Al recibir', ['Enviar', 'Mover 10 pasos', 'Por siempre']),
                ('El botón envía «despegar» y el cohete espera «Despegar». ¿Qué pasa?',
                 'El cohete no se mueve porque los nombres no son iguales',
                 ['El cohete despega dos veces', 'Scratch se apaga', 'Funciona perfecto']),
                ('Un error en un programa se llama…', 'Bug', ['Sprite', 'Fondo', 'Disfraz']),
            ]),
        ]},
        {'nombre': '¡Caso resuelto! Mi videojuego', 'cofre': 50, 'misiones': [
            scratch('Videojuego paso 1: la nave piloto', leccion(
                intro='Vas a construir un videojuego de obstáculos en 3 pasos. En el paso 1 programas la nave que el '
                      'jugador controla con las flechas.',
                saber=['«¿tecla flecha arriba presionada?» (Sensores) es una pregunta: su respuesta es sí o no.',
                       'Va dentro de un «si … entonces», y ese «si» dentro de «por siempre»: así Scratch revisa las '
                       'teclas todo el tiempo.',
                       LEYENDA_SCRATCH],
                pasos=['Proyecto nuevo con fondo «Stars». Borra el gato y agrega el objeto «Rocketship» (o la nave que '
                       'quieras); llámalo Nave.',
                       'Hazla más chica: en la casilla «Tamaño» escribe 50.',
                       'Arma el código de la nave y pruébalo con las flechas arriba y abajo.',
                       'Reto extra: agrega las flechas derecha e izquierda (cambiar x en 8 y en -8).',
                       'Guarda como Videojuego_TuNombre.'],
                logro=['La nave se mueve con las flechas y siempre empieza en el mismo lugar.'],
                entrega='sube una captura de los bloques de tu nave.'), CODIGO_NAVE),
            scratch('Videojuego paso 2: lluvia de obstáculos', leccion(
                intro='Ahora los obstáculos. En lugar de agregar 20 asteroides, usarás clones: copias que Scratch crea '
                      'mientras juegas.',
                saber=['«crear clon de mí mismo» (Control) hace una copia del objeto.',
                       '«al comenzar como clon» dice qué hace cada copia.',
                       '«eliminar este clon» borra la copia cuando ya no sirve (si no, ¡el juego se pone lento!).',
                       'El objeto original se esconde: solo es la «fábrica» de clones.',
                       LEYENDA_SCRATCH],
                pasos=['Abre tu Videojuego. Agrega el objeto «Rocks», llámalo Asteroide y ponle tamaño 60.',
                       'Arma los dos programas del asteroide.',
                       'Prueba: deben salir asteroides por la derecha, a diferentes alturas, cada segundo.',
                       'Ajusta la dificultad: cambia «esperar 1 segundos» por 0.7 o la velocidad de -6 por -9.',
                       'Guarda tu proyecto.'],
                logro=['Aparecen asteroides sin parar y cada uno desaparece al llegar a la izquierda.'],
                entrega='sube una captura de los bloques del asteroide.'), CODIGO_OBSTACULOS, xp=100, monedas=30),
            scratch('Videojuego paso 3: choques, puntos y mensajes', leccion(
                intro='El último paso une todo: si la nave choca se envía «perdiste»; si aguanta 30 segundos, se envía '
                      '«ganaste». ¡Ciclos y mensajes trabajando juntos!',
                saber=['Una variable guarda un dato que cambia, como los puntos. Créala en Variables → «Crear una '
                       'variable» → «puntos».',
                       '«¿tocando Asteroide?» (Sensores) revisa si la nave choca, también con los clones.',
                       '«detener todos» (Control) termina el juego.',
                       LEYENDA_SCRATCH],
                pasos=['En el escenario, pestaña Fondos, pinta dos fondos nuevos con la herramienta Texto: uno que se '
                       'llame y diga «GAME OVER» y otro «GANASTE». El fondo «Stars» debe seguir ahí.',
                       'Crea la variable «puntos» (para todos los objetos).',
                       'Agrega a la nave su segundo programa y crea los mensajes «perdiste» y «ganaste».',
                       'Arma el código del escenario.',
                       'Juega 3 veces. ¿Se puede ganar? ¿Es muy fácil o muy difícil? Ajusta los números hasta que '
                       'sea divertido.'],
                logro=['Los puntos suben cada segundo.', 'Al chocar aparece GAME OVER y al llegar a 30 aparece GANASTE.'],
                tip='Si al chocar no pasa nada, revisa que en «¿tocando…?» diga exactamente Asteroide.',
                entrega='sube una captura de tu juego funcionando y otra de tus bloques.'), CODIGO_CHOQUES,
                xp=110, monedas=30),
            mision('Prueba de pilotos', 'presencial', leccion(
                intro='Los videojuegos de verdad se prueban muchas veces antes de salir. Hoy tus compañeros serán tus '
                      'probadores.',
                pasos=['Deja tu juego abierto. Cambia de lugar y juega el videojuego de 3 compañeros.',
                       'A cada uno déjale «2 estrellas y 1 deseo»: dos cosas que te gustaron y una que mejorarías.',
                       'Regresa, lee tus notas y haz al menos una mejora (velocidad, sonido, fondo, más puntos para '
                       'ganar…).',
                       'Cuéntale a tu profe qué error te ayudó a mejorar tu juego.'],
                logro=['Probaste 3 juegos y dejaste comentarios amables y útiles.',
                       'Mejoraste tu juego con lo que te dijeron.'],
                entrega='tu profe marca la misión al ver tu mejora.'), xp=60, monedas=20),
            jefe('Jefe: Capitán Rendirse-Jamás',
                 'El Capitán Rendirse-Jamás custodia la salida de la estación. Solo deja pasar a quien domina los '
                 'ciclos, los mensajes y el arte de aprender de los errores. ¡Responde todo para conquistar la estación!', [
                     ('Tu asteroide debe moverse durante todo el juego. ¿Qué bloque lo logra?', 'Por siempre',
                      ['Repetir 1', 'Esperar 1 segundos', 'Decir ¡Hola!']),
                     ('¿Qué hace el bloque «enviar perdiste»?', 'Avisa a todos los objetos que el jugador perdió',
                      ['Borra el juego', 'Cambia de color la nave', 'Guarda el proyecto']),
                     ('¿Qué bloque se activa cuando llega el mensaje «ganaste»?', 'Al recibir ganaste',
                      ['Al hacer clic en este objeto', 'Por siempre', 'Mover 10 pasos']),
                     ('Para que los puntos suban de 1 en 1 usas…', 'Cambiar puntos en 1',
                      ['Fijar puntos a 1', 'Mover 1 paso', 'Esperar 1 segundo']),
                     ('¿Qué hace «crear clon de mí mismo»?', 'Hace una copia del objeto mientras el juego corre',
                      ['Borra el objeto', 'Cambia el fondo', 'Copia el proyecto en tu carpeta']),
                     ('Tu nave no se mueve con las flechas. ¿Qué haces primero?',
                      'Reviso paso a paso si los bloques están dentro de «por siempre» y del «si»',
                      ['Borro todo y me rindo', 'Digo que la compu está mal', 'Apago la compu']),
                     ('Un dispositivo de entrada es…', 'El que le da información a la compu, como el teclado',
                      ['El que saca información, como las bocinas', 'Un programa', 'Un cable de luz']),
                     ('Cleo cambió el papel, las alas y el clip al mismo tiempo y su avión voló mejor. ¿Qué problema '
                      'tiene su experimento?', 'No sabe cuál de los cambios lo mejoró',
                      ['Ninguno, es perfecto', 'Que voló demasiado', 'Que usó papel']),
                 ]),
        ]},
    ],
}
