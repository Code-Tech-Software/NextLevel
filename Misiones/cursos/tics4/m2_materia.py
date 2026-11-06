"""Mundo 2 · ES-SEA202 Materia misteriosa: estados y cambios de la materia, diagramas de flujo, operadores de
comparación y un videojuego en Scratch con condicionales."""
from .base import LEYENDA_SCRATCH, clasifica, jefe, leccion, mision, scratch

JUEGOS = {
    'clasifica_estados': clasifica('¿Sólido, líquido o gas?', '🧊', 'Clasifica cada sustancia según su estado de la materia.', [
        ('Sólido', '🧊', ['Hielo', 'Piedra', 'Lápiz', 'Cuchara', 'Sal', 'Madera', 'Moneda', 'Plastilina']),
        ('Líquido', '💧', ['Agua', 'Leche', 'Jugo de naranja', 'Aceite', 'Miel', 'Vinagre', 'Gotas de lluvia']),
        ('Gas', '💨', ['Vapor de agua', 'Aire', 'Oxígeno', 'Helio de un globo', 'Burbujas del refresco',
                      'Aire dentro de una llanta', 'Lo que exhalas al respirar']),
    ]),
    'clasifica_calor': clasifica('¿Gana o pierde calor?', '🌡️', '¿La materia se está calentando o enfriando?', [
        ('Gana calor', '🔥', ['Un helado que se derrite al sol', 'El agua de un charco que desaparece',
                             'La ropa mojada que se seca', 'Chocolate que se derrite en tu mano',
                             'Mantequilla en un sartén caliente', 'Agua hirviendo que se vuelve vapor',
                             'Hielo que se derrite en la limonada']),
        ('Pierde calor', '❄️', ['Gotitas afuera de un vaso con agua fría', 'Agua que se vuelve hielo en el congelador',
                               'El espejo del baño que se empaña', 'Lava que se enfría y se vuelve roca',
                               'Cera de una vela que se endurece', 'Rocío en el pasto por la mañana',
                               'Gelatina que cuaja en el refrigerador']),
    ]),
    'clasifica_comparaciones': clasifica('¿Verdadero o falso?', '⚖️', 'Así «piensan» los bloques verdes de Scratch.', [
        ('Verdadero', '✅', ['100 > 50', '0 = 0', '25 < 30', '-5 < 0', '7 + 3 = 10',
                            'Si temperatura = 120, temperatura > 100', 'Si temperatura = -2, temperatura < 0']),
        ('Falso', '❌', ['50 > 100', '30 < 25', '10 = 100', '0 > 5', '8 < 8',
                        'Si temperatura = 20, temperatura > 100', 'Si temperatura = 50, temperatura < 0']),
    ], rondas=14),
}

CODIGO_TERMOMETRO = '''
OBJETO: Agua
al hacer clic en la bandera verde
    fijar "temperatura" a 20
    cambiar disfraz a "agua"
    decir "¡Soy agua! Usa las flechas para calentarme o enfriarme" durante 3 segundos

al presionar tecla "flecha arriba"
    cambiar "temperatura" en 10

al presionar tecla "flecha abajo"
    cambiar "temperatura" en -10
'''

CODIGO_ESTADOS = '''
OBJETO: Agua (agrega este programa)
al hacer clic en la bandera verde
    por siempre
        si <(temperatura) < 1> entonces
            cambiar disfraz a "hielo"
        si no
            si <(temperatura) > 99> entonces
                cambiar disfraz a "vapor"
            si no
                cambiar disfraz a "agua"
'''

CODIGO_REY = '''
OBJETO: Rey
al hacer clic en la bandera verde
    fijar "puntos" a 0
    repetir 5
        fijar "pedido" a (número aleatorio entre 1 y 2)
        si <(pedido) = 1> entonces
            decir "¡Quiero HIELO para mi limonada! Presiona espacio cuando esté listo"
        si no
            decir "¡Quiero VAPOR para mi baño! Presiona espacio cuando esté listo"
        esperar hasta que <¿tecla espacio presionada?>
        enviar "revisar" y esperar
        esperar 1 segundos
    decir (unir "Puntos finales: " (puntos))

OBJETO: Agua (agrega este programa)
al recibir "revisar"
    si <<(pedido) = 1> y <(temperatura) < 1>> entonces
        cambiar "puntos" en 1
        decir "¡Hielo perfecto!" durante 1 segundos
    si no
        si <<(pedido) = 2> y <(temperatura) > 99>> entonces
            cambiar "puntos" en 1
            decir "¡Vapor perfecto!" durante 1 segundos
        si no
            decir "¡Ups! Ese no es el estado que pidió el Rey" durante 1 segundos
'''

MUNDO = {
    'nombre': 'Laboratorio de la Materia Misteriosa', 'tema': 'hielo',
    'descripcion': 'ES-SEA202 · Materia misteriosa. Gastón Olvidón, el mago del Rey, convierte el agua en hielo o en '
                   'vapor… ¿con magia? Descubre su secreto con experimentos y prográmalo en un videojuego con '
                   'condicionales y operadores de comparación. Pregunta guía: ¿cuál es el secreto de Gastón?',
    'niveles': [
        {'nombre': 'El castillo de Gastón Olvidón', 'cofre': 25, 'misiones': [
            mision('Expediente del caso', 'texto', leccion(
                intro='En un castillo vive Gastón Olvidón, un mago que siempre tiene la cabeza en otro lado. Es el mago '
                      'personal del Rey porque es el único del reino que sabe convertir el agua en hielo para enfriar '
                      'las limonadas de la corte… ¡o en vapor para el baño de su majestad! Guarda el secreto en su '
                      'laboratorio mágico y no deja entrar a nadie.\n\nPregunta del caso: ¿cuál es el secreto de Gastón?',
                saber='Un expediente es donde un detective anota lo que sabe, lo que sospecha y lo que necesita averiguar.',
                pasos=['Escribe 3 cosas que SABEMOS por la historia.',
                       'Escribe 2 cosas que SOSPECHAS: ¿cómo crees que Gastón convierte el agua en hielo o en vapor?',
                       'Escribe tu meta para este proyecto: ¿qué te gustaría lograr en tu videojuego?'],
                entrega='escribe tu expediente aquí abajo.'), xp=60),
            mision('¿Qué es la materia?', 'cuestionario', leccion(
                intro='Todo lo que te rodea es materia… ¿o no? Repasa y compruébalo.',
                saber=['Materia es todo lo que tiene masa (se puede pesar) y ocupa un lugar (tiene volumen).',
                       'El aire es materia: no lo ves, pero infla un globo.',
                       'La luz, las sombras y los sonidos NO son materia.',
                       'Sólido: forma fija. Líquido: toma la forma del recipiente. Gas: se expande y llena todo.',
                       'La masa se mide con una balanza o báscula.']), xp=60, preguntas=[
                ('La materia es…', 'Todo lo que tiene masa y ocupa un lugar',
                 ['Solo lo que podemos comer', 'Solo lo que es sólido', 'Solo los seres vivos']),
                ('¿Cuál de estos NO es materia?', 'Una sombra', ['El aire', 'El agua', 'Una piedra']),
                ('Los tres estados de la materia que más vemos son…', 'Sólido, líquido y gaseoso',
                 ['Frío, tibio y caliente', 'Grande, mediano y chico', 'Duro, blando y suave']),
                ('Un líquido…', 'Toma la forma del recipiente que lo contiene',
                 ['Siempre tiene la misma forma', 'No ocupa espacio', 'No tiene masa']),
                ('Un gas…', 'Se expande y ocupa todo el espacio que tiene',
                 ['Tiene forma fija como una piedra', 'Siempre se puede ver', 'Se puede cortar con tijeras']),
                ('¿Con qué instrumento medimos la masa de un objeto?', 'Con una balanza o báscula',
                 ['Con un termómetro', 'Con una regla', 'Con un reloj']),
            ]),
            mision('Cazadores de materia', 'presencial', leccion(
                intro='Hoy el salón es el laboratorio de Gastón. ¡Todo lo que ves es materia… o casi todo!',
                material=['Una balanza o báscula de cocina', 'Un globo', 'Tu cuaderno'],
                pasos=['En equipos, busquen 5 sólidos y 3 líquidos (del salón, del lavabo o de su lonchera). Anótenlos '
                       'en una tabla: Objeto · Estado · ¿Cómo lo sé?',
                       'Inflen un globo: ¿qué hay adentro? ¡Aire! Anoten 2 gases que conozcan.',
                       'Pesen el globo desinflado y luego inflado. ¿Cambió? (Pista: el aire también tiene masa, '
                       'aunque muy poquita.)',
                       'Escriban algo que NO sea materia (la sombra, la luz, un sonido) y expliquen por qué.'],
                logro=['Su tabla tiene sólidos, líquidos y gases con su explicación.'],
                entrega='tu profe revisa la tabla del equipo.'), xp=50),
            mision('¿Sólido, líquido o gas?', 'juego', leccion(
                intro='Clasifica cada sustancia según su estado de la materia.',
                tip='¿Tiene forma propia (sólido), toma la forma del recipiente (líquido) o se escapa y llena todo (gas)?'),
                juego='clasifica_estados'),
        ]},
        {'nombre': '¿De qué está hecha la materia?', 'cofre': 30, 'misiones': [
            mision('Partículas bailarinas', 'presencial', leccion(
                intro='La materia está hecha de partículas tan pequeñas que no se ven ni con lupa. Hoy tú serás una '
                      'partícula.',
                saber=['Sólido: partículas muy juntas que solo vibran en su lugar.',
                       'Líquido: partículas juntas que se deslizan unas sobre otras.',
                       'Gas: partículas muy separadas que se mueven rápido en todas direcciones.',
                       'El calor les da energía: con más calor, se mueven más rápido.'],
                pasos=['Todo el grupo se pone hombro con hombro y solo «tiembla» en su lugar: ¡son un sólido!',
                       'El profe dice «calor»: ahora caminan despacio rozándose: ¡son un líquido!',
                       'Más calor: se separan y caminan rápido por todo el salón: ¡son un gas!',
                       'El profe dice «frío»: ¿qué tienen que hacer para volver a ser sólido?',
                       'Dibuja en tu cuaderno 3 cajitas con las partículas de cada estado.'],
                logro=['Explicas cómo se mueven las partículas en cada estado y qué hace el calor.']), xp=50),
            mision('Simulador de estados de la materia', 'link', leccion(
                intro='Los científicos usan simuladores para ver lo que el ojo no alcanza. Vas a calentar y enfriar '
                      'partículas en la computadora.',
                pasos=['Abre el enlace, presiona el botón de reproducir y entra a la pantalla «Estados».',
                       'Elige el agua y presiona el botón «Sólido». Observa cómo se mueven las moléculas.',
                       'Usa el control de calor (la flama) para calentar poco a poco. Mira el termómetro: ¿cuándo '
                       'empieza a moverse como líquido?',
                       'Sigue calentando hasta que sea gas. Luego enfría con el control de hielo.',
                       'Prueba con otra sustancia y compara.'],
                logro=['Observaste los tres estados y cómo cambian con la temperatura.'],
                entrega='en el comentario, escribe qué pasó con las moléculas al calentarlas y al enfriarlas.'),
                xp=60, link='https://phet.colorado.edu/es/simulations/states-of-matter-basics'),
            mision('Experimento: la materia misteriosa', 'evidencia', leccion(
                intro='¿Puede algo ser sólido y líquido a la vez? Esta mezcla parece salida del laboratorio de Gastón.',
                material=['2 tazas de maicena', '1 taza de agua', 'Un recipiente', 'Colorante (opcional)'],
                pasos=['Con ayuda de tu profe, mezcla la maicena con el agua poco a poco, con la mano.',
                       'Toca la mezcla despacio: ¿qué pasa?', 'Ahora golpéala rápido con el dedo: ¿qué pasa?',
                       'Toma un puño, apriétalo y luego abre la mano.', 'Anota tus observaciones.'],
                tip='⚠️ No la tires al lavabo porque lo tapa: tírala a la basura.',
                entrega='sube una foto de tu experimento.'), xp=90, monedas=25),
            mision('¿Sólido o líquido? Tú decides', 'texto', leccion(
                intro='Después del experimento, ¡eres el científico que decide!',
                pasos=['Explica con tus palabras: ¿la materia misteriosa es sólida, líquida o las dos cosas?',
                       'Da al menos dos evidencias de lo que observaste (lo que pasó al tocarla despacio y al golpearla).',
                       'Escribe una pregunta nueva que te gustaría investigar.'],
                entrega='escribe tu respuesta aquí abajo.'), xp=60),
        ]},
        {'nombre': 'La varita de la temperatura', 'cofre': 30, 'misiones': [
            mision('El termómetro de Gastón', 'cuestionario', leccion(
                intro='El secreto de Gastón tiene que ver con algo que se mide… Repasa y descúbrelo.',
                saber=['La temperatura mide qué tan caliente o frío está algo. Se mide con un termómetro en grados '
                       'Celsius (°C).',
                       'El agua se congela a 0 °C y hierve a 100 °C (al nivel del mar).',
                       'Fusión: sólido → líquido (el hielo se derrite).',
                       'Solidificación: líquido → sólido (el agua se congela).',
                       'Evaporación: líquido → gas (el charco se seca).',
                       'Condensación: gas → líquido (el vapor forma gotitas).']), xp=60, preguntas=[
                ('¿Con qué instrumento medimos la temperatura?', 'Con un termómetro',
                 ['Con una balanza', 'Con una regla', 'Con un reloj']),
                ('¿A qué temperatura se congela el agua?', 'A 0 °C', ['A 100 °C', 'A 50 °C', 'A 20 °C']),
                ('¿A qué temperatura hierve el agua al nivel del mar?', 'A 100 °C', ['A 0 °C', 'A 37 °C', 'A 10 °C']),
                ('El hielo se derrite y se vuelve agua. ¿Qué cambio es?', 'Fusión',
                 ['Condensación', 'Solidificación', 'Evaporación']),
                ('Las gotitas que aparecen afuera de un vaso con hielo se forman por…', 'Condensación',
                 ['Fusión', 'Evaporación', 'Magia']),
                ('Para convertir el agua de la limonada en hielo, Gastón debe…', 'Bajar su temperatura a menos de 0 °C',
                 ['Calentarla a 100 °C', 'Ponerle azúcar', 'Moverla de lugar']),
                ('¿Cuál es el verdadero secreto de Gastón?', 'Cambiar la temperatura del agua',
                 ['Una varita mágica de verdad', 'Pintar el agua', 'Gritarle al agua']),
            ]),
            mision('¿Gana o pierde calor?', 'juego', leccion(
                intro='Cuando la materia gana calor se derrite o se evapora; cuando lo pierde se condensa o se '
                      'solidifica. Clasifica cada situación.'), juego='clasifica_calor'),
            mision('Evaporación en acción', 'evidencia', leccion(
                intro='¿A dónde se va el agua de un charco? Vas a comprobarlo con un experimento de dos días.',
                saber='El agua no desaparece: se convierte en vapor (gas) y se va al aire. Con más calor se evapora '
                      'más rápido.',
                material=['2 platos iguales', 'Agua', 'Un plumón', 'Un vaso para medir'],
                pasos=['Pon la misma cantidad de agua en los dos platos (por ejemplo, medio vaso en cada uno).',
                       'Marca con plumón el nivel del agua en cada plato.',
                       'Deja un plato al sol y el otro en la sombra.',
                       'Escribe tu hipótesis: ¿en cuál desaparecerá más rápido el agua? ¿Por qué?',
                       'Al día siguiente revisa los niveles y compáralos con tu hipótesis.'],
                entrega='sube una foto de tus platos con las marcas y escribe en el comentario qué pasó.'),
                xp=80, monedas=20),
            mision('Lluvia en un frasco', 'presencial', leccion(
                intro='El vapor de agua, al enfriarse, vuelve a ser líquido. ¡Así se forman las nubes y la lluvia!',
                saber='Esto es condensación: el vapor caliente sube, toca el plato frío, pierde calor y se vuelve gotitas.',
                material=['Un frasco de vidrio', 'Agua caliente (la sirve tu profe)', 'Un plato', 'Cubos de hielo'],
                pasos=['Tu profe sirve agua caliente en el frasco (⚠️ solo el profe toca el agua caliente).',
                       'Tapen el frasco con el plato y pongan hielos encima.',
                       'Observen 3 minutos la parte de abajo del plato.',
                       '¿Qué aparece? ¿De dónde salió? Anoten su explicación.'],
                logro=['Explicas con tus palabras la evaporación y la condensación del frasco.']), xp=50),
            mision('Carrera de cubos de hielo', 'presencial', leccion(
                intro='En equipos, cada uno recibe un cubo de hielo. Gana el equipo que lo derrita más rápido… ¡sin '
                      'meterlo a la boca!',
                saber='Para derretir el hielo hay que darle calor: la fusión ocurre cuando el sólido gana calor.',
                pasos=['Antes de empezar, escriban su hipótesis: ¿qué método funcionará mejor y por qué?',
                       'Elijan su método (frotarlo entre las manos, ponerlo al sol, envolverlo en una servilleta…).',
                       'Midan con un reloj cuánto tarda en derretirse.',
                       'Comparen con los demás equipos: ¿acertaron? ¿Qué método dio más calor?']), xp=50),
        ]},
        {'nombre': 'Trazo mis pistas: el plan del juego', 'cofre': 35, 'misiones': [
            mision('El mapa del juego: diagrama de flujo', 'evidencia', leccion(
                intro='Antes de programar, los programadores dibujan el plan del juego. Ese plano se llama diagrama de '
                      'flujo y te ayuda a ordenar tus ideas.',
                saber=['Óvalo: inicio o fin.',
                       'Rectángulo: una acción (por ejemplo, «subir la temperatura 10 grados»).',
                       'Rombo: una pregunta de sí o no (por ejemplo, «¿la temperatura es menor que 1?»).',
                       'Flechas: el camino que sigue el programa. Del rombo salen dos: una para «sí» y otra para '
                       '«no». ¡Eso es una condicional!'],
                pasos=['En una hoja, dibuja el óvalo «Inicio».',
                       'Dibuja un rectángulo: «Leer la temperatura del agua».',
                       'Dibuja un rombo: «¿Temperatura menor que 1?». Si SÍ → rectángulo «Mostrar hielo».',
                       'Si NO → otro rombo: «¿Temperatura mayor que 99?». Si SÍ → «Mostrar vapor». Si NO → «Mostrar '
                       'agua líquida».',
                       'Une todo con flechas y regresa al inicio (¡eso es un ciclo!).'],
                logro=['Tu diagrama tiene inicio, acciones, dos preguntas con sí y no, y flechas claras.'],
                entrega='sube una foto de tu diagrama de flujo.'), xp=80, monedas=20),
            mision('Mayor que, menor que, igual que', 'cuestionario', leccion(
                intro='Para que tu juego sepa si el agua es hielo o vapor, debe comparar números.',
                saber=['> significa «mayor que»: 100 > 50 se lee «cien es mayor que cincuenta».',
                       '< significa «menor que»: 3 < 8.', '= significa «igual que»: 0 = 0.',
                       'Truco: la boca abierta del cocodrilo siempre se come al número más grande.',
                       'En Scratch están en Operadores (verdes), responden verdadero o falso y se usan dentro de '
                       '«si … entonces».']), xp=60, preguntas=[
                ('¿Qué significa el símbolo >?', 'Mayor que', ['Menor que', 'Igual que', 'Más']),
                ('¿Cuál comparación es verdadera?', '100 > 99', ['5 > 9', '0 = 10', '7 < 2']),
                ('Si la temperatura es 120, ¿cuál comparación es verdadera?', 'temperatura > 100',
                 ['temperatura < 0', 'temperatura = 0', 'temperatura < 100']),
                ('En el juego, el agua debe verse como hielo cuando…', 'temperatura < 1',
                 ['temperatura > 99', 'temperatura = 50', 'temperatura > 1000']),
                ('¿En qué categoría de Scratch están los bloques >, < e =?', 'Operadores',
                 ['Movimiento', 'Sonido', 'Apariencia']),
                ('Una condicional («si … entonces») sirve para…', 'Hacer algo solo cuando se cumple una condición',
                 ['Repetir por siempre', 'Cambiar el idioma', 'Guardar el proyecto']),
            ]),
            mision('¿Verdadero o falso?', 'juego', leccion(
                intro='Revisa cada comparación: ¿es verdadera o falsa?',
                tip='Léelas en voz alta: > «mayor que», < «menor que», = «igual que».'), juego='clasifica_comparaciones'),
        ]},
        {'nombre': 'DTectives en acción: el juego de Gastón', 'cofre': 50, 'misiones': [
            scratch('Juego paso 1: el termómetro mágico', leccion(
                intro='Vas a programar el laboratorio de Gastón: un poco de agua cuya temperatura subes y bajas con '
                      'las flechas.',
                saber=['Una variable guarda un número que cambia; aquí guardará la temperatura.',
                       '«fijar temperatura a 20» pone el valor inicial; «cambiar temperatura en 10» le suma 10 (o le '
                       'resta, si es -10).',
                       LEYENDA_SCRATCH],
                pasos=['Proyecto nuevo con un fondo de castillo (por ejemplo «Castle 2») o pinta el tuyo.',
                       'Pinta un objeto nuevo llamado Agua con 3 disfraces: «hielo» (cubo azul claro), «agua» (gota '
                       'azul) y «vapor» (nube gris). Pestaña Disfraces → pincel.',
                       'Crea la variable «temperatura» y deja visible su casilla en el escenario.',
                       'Arma el código en el objeto Agua y pruébalo con las flechas.',
                       'Guarda como Gaston_TuNombre en tu carpeta.'],
                logro=['La temperatura empieza en 20 y sube o baja de 10 en 10 con las flechas.'],
                entrega='sube una captura de tus bloques y de los 3 disfraces.'), CODIGO_TERMOMETRO),
            scratch('Juego paso 2: el agua cambia de estado', leccion(
                intro='Ahora el secreto de Gastón: el agua cambia de disfraz según la temperatura, con condicionales y '
                      'operadores.',
                saber=['«si … entonces / si no» (Control) elige entre dos caminos, como el rombo de tu diagrama.',
                       'Un «si» dentro del «si no» da 3 caminos: hielo, vapor o agua.',
                       'Todo va dentro de «por siempre» para revisar la temperatura a cada momento.',
                       LEYENDA_SCRATCH],
                pasos=['Abre Gaston_TuNombre y agrega el nuevo programa al objeto Agua.',
                       'Compáralo con tu diagrama de flujo: ¿es el mismo camino?',
                       'Prueba: baja a 0 o menos (hielo), sube a 100 o más (vapor) y regresa a 50 (agua).',
                       'Reto: agrega «decir» en cada caso: «¡Brrr, soy hielo!», «¡Soy vapor!», «Soy agua líquida».'],
                logro=['El agua cambia al disfraz correcto con las tres temperaturas.'],
                entrega='sube una captura de tus bloques.'), CODIGO_ESTADOS),
            scratch('Juego paso 3: los pedidos del Rey', leccion(
                intro='El Rey pide hielo para su limonada o vapor para su baño. El jugador debe preparar el estado '
                      'correcto y presionar espacio. ¡5 pedidos para ganar puntos!',
                saber=['«número aleatorio entre 1 y 2» decide qué pide el Rey cada vez.',
                       '«esperar hasta que ¿tecla espacio presionada?» pausa al Rey hasta que el jugador presione espacio.',
                       '«enviar revisar y esperar» avisa al Agua y espera a que termine de revisar.',
                       '«y» (Operadores) une dos condiciones: las dos deben cumplirse.',
                       '«unir» (Operadores) junta un texto y un número en una sola frase.',
                       LEYENDA_SCRATCH],
                pasos=['Agrega un objeto para el Rey (por ejemplo «Prince») o dibújalo.',
                       'Crea las variables «puntos» y «pedido».',
                       'Arma el código del Rey y crea el mensaje «revisar».',
                       'Agrega al Agua el programa «al recibir revisar».',
                       'Juega: sube o baja la temperatura y presiona espacio cuando esté lista. Guarda la versión final.'],
                logro=['El Rey hace 5 pedidos al azar y los puntos suben solo cuando aciertas.'],
                entrega='sube una captura de tu juego funcionando y de tus bloques.'), CODIGO_REY, xp=110, monedas=30),
            mision('Feria de videojuegos de Gastón', 'presencial', leccion(
                intro='Revelo mis hallazgos: el laboratorio abre sus puertas. Prueba los juegos de tus compañeros y '
                      'compite por el mejor marcador.',
                pasos=['Deja tu juego listo en la pantalla.',
                       'Rota por 3 computadoras: juega y anota tu puntaje.',
                       'Cuando alguien visite tu juego, explícale con tus palabras el secreto de Gastón.',
                       'Con el grupo elijan: el juego más divertido, el más difícil y el más creativo.'],
                logro=['Tu juego funciona y explicas los cambios de estado que usa.']), xp=60, monedas=20),
            jefe('Jefe: La Gelatina Mutante',
                 'Una gelatina mutante cambia de estado a su antojo. Solo podrás vencerla si dominas los cambios de '
                 'estado, los operadores y las condicionales.', [
                     ('Cuando el hielo se derrite pasa de sólido a líquido. A eso se le llama…', 'Fusión',
                      ['Evaporación', 'Condensación', 'Solidificación']),
                     ('El agua de un charco desaparece con el sol porque se…', 'Evapora',
                      ['Congela', 'Solidifica', 'Condensa']),
                     ('Si metes agua al congelador se convierte en hielo. Eso es…', 'Solidificación',
                      ['Evaporación', 'Fusión', 'Condensación']),
                     ('¿Qué hace que la materia cambie de estado?', 'Subir o bajar su temperatura',
                      ['Cambiarla de color', 'Ponerle nombre', 'Moverla de lugar']),
                     ('¿Cómo se mueven las partículas de un gas?', 'Muy separadas y rápido en todas direcciones',
                      ['Muy juntas, sin moverse', 'Pegadas en fila', 'Los gases no tienen partículas']),
                     ('En tu juego, ¿qué condición hace que el agua se vea como vapor?', 'temperatura > 99',
                      ['temperatura < 1', 'temperatura = 20', 'puntos > 99']),
                     ('En un diagrama de flujo, el rombo representa…', 'Una pregunta de sí o no',
                      ['El inicio', 'Una acción', 'El fin']),
                     ('¿Qué bloque de Scratch elige entre dos caminos?', 'Si … entonces / si no',
                      ['Por siempre', 'Mover 10 pasos', 'Cambiar disfraz']),
                 ]),
        ]},
    ],
}
