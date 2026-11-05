"""Robótica · Primaria Baja (1° a 3°): Dash con la app Blockly, abejitas Bee-Bot y muchas actividades sin pantalla.

Casi todo se hace en clase (el profe marca las misiones presenciales); solo hay dos minijuegos de la plataforma.
Los textos son cortos y con emojis para que el profe los lea en voz alta. Las preguntas tienen 3 opciones.
"""
from Misiones.cursos import mision


def jefe(nombre, descripcion, xp=130, monedas=40, **extra):
    """Los jefes de los más pequeños casi siempre son un reto en vivo con el robot."""
    return mision(nombre, extra.pop('tipo', 'presencial'), descripcion, xp, monedas, jefe=True, **extra)


JUEGOS = {
    'beebot_virtual': {'nombre': 'Bee-Bot virtual: gira y avanza', 'icono': '🐝', 'plantilla': 'robot', 'en_arcade': True,
                       'descripcion': 'Funciona como Bee-Bot: avanza hacia donde mira y gira sin moverse.',
                       'configuracion': {'dificultad': 'facil', 'niveles': 4, 'modo': 'giros', 'bucles': False}},
    'robot_repetidor': {'nombre': 'Robot repetidor', 'icono': '🔁', 'plantilla': 'robot', 'en_arcade': True,
                        'descripcion': 'Usa el bloque de repetir para llegar a la batería con menos flechas.',
                        'configuracion': {'dificultad': 'facil', 'niveles': 4, 'modo': 'flechas', 'bucles': True}},
}

MUNDOS = [
    # ---------- ¿Qué es un robot? ----------
    {'nombre': 'Planeta Robot', 'tema': 'espacio',
     'descripcion': 'Aterriza en el planeta donde viven Dash y las abejitas Bee-Bot y descubre cómo piensan, sienten '
                    'y se mueven los robots.',
     'niveles': [
         {'nombre': 'Bienvenida a bordo', 'cofre': 20, 'misiones': [
             mision('¡Hola, robots!', 'presencial',
                    'Conoce a los robots de la academia: Dash 🤖 y las abejitas Bee-Bot 🐝.\n\n'
                    '1. Observa cómo se mueven.\n2. Cuéntale al grupo: ¿en qué se parecen a ti? ¿En qué son diferentes?\n'
                    '3. Ponle un apodo secreto a tu robot favorito.', xp=40, monedas=10),
             mision('Reglas para cuidar a los robots', 'presencial',
                    'Los robots son nuestros compañeros. Aprende las reglas:\n\n'
                    '🤲 Los cargamos con las dos manos.\n🚫 No se avientan ni se mojan.\n'
                    '🔋 Al terminar, los apagamos y los ponemos a cargar.\n🤝 Nos turnamos para usarlos.\n\n'
                    'Demuestra que sabes cargar y entregar un robot con cuidado.', xp=40, monedas=10),
             mision('¿Es un robot o no?', 'cuestionario', 'Escucha a tu profe y elige la respuesta correcta. 🤔', preguntas=[
                 ('¿Cuál de estos es un robot?', '🤖 Una máquina que sigue instrucciones', ['🪨 Una piedra', '🧸 Un osito de peluche']),
                 ('¿Qué necesita un robot para saber qué hacer?', '📋 Instrucciones (un programa)', ['🍕 Una pizza', '🛏️ Dormir mucho']),
                 ('¿Con qué siente un robot lo que pasa a su alrededor?', '👀 Con sus sensores', ['👃 Con perfume', '🎩 Con un sombrero']),
                 ('¿Qué hace que un robot se mueva?', '⚙️ Sus motores', ['🌧️ La lluvia', '🎨 Los colores']),
                 ('Dash y Bee-Bot funcionan con…', '🔋 Baterías', ['🥛 Leche', '🌱 Semillas']),
             ]),
         ]},
         {'nombre': 'Partes de un robot', 'cofre': 25, 'misiones': [
             mision('Soy un robot: cerebro, sentidos y motores', 'presencial',
                    '¡Juega a ser robot! 🧍🤖\n\n🧠 Tu cabeza es el cerebro (la computadora).\n'
                    '👀👂 Tus ojos y oídos son los sensores.\n💪 Tus brazos y piernas son los motores.\n\n'
                    'Tu profe da una orden y tú la haces como robot: ¡exactamente como te la dicen, ni más ni menos!'),
             mision('Dibuja tu robot soñado', 'evidencia',
                    'Dibuja el robot que te gustaría inventar. ✏️\n\n'
                    '• Colorea dónde están sus sensores (ojos, oídos), su cerebro y sus motores (ruedas, brazos).\n'
                    '• ¿Para qué te ayudaría?\n\nToma una foto de tu dibujo y súbela.', xp=70, monedas=20),
             jefe('Jefe: El Robot Gruñón',
                  '¡El Robot Gruñón no te deja entrar al planeta! Solo se pone feliz si sabes cómo funcionan los robots. 😤🤖',
                  tipo='cuestionario', xp=120, preguntas=[
                      ('Los sensores de un robot son como nuestros…', '👀 Ojos y oídos', ['🦶 Zapatos', '🍎 Dulces']),
                      ('El cerebro de un robot es su…', '💻 Computadora', ['🎈 Globo', '🧦 Calcetín']),
                      ('¿Cuál es una regla para cuidar a los robots?', '🤲 Cargarlos con las dos manos',
                       ['💦 Bañarlos con agua', '🏀 Aventarlos como pelota']),
                      ('¿Cuál de estos robots es una abejita?', '🐝 Bee-Bot', ['🤖 Dash', '🚗 Un carrito de juguete']),
                      ('Un robot hace las cosas…', '📋 Tal como lo programaste', ['🎲 Como él quiere', '😴 Solo cuando tiene sueño']),
                  ]),
         ]},
     ]},

    # ---------- Bee-Bot ----------
    {'nombre': 'Colmena de Miel', 'tema': 'dulces',
     'descripcion': 'Las abejitas Bee-Bot necesitan pilotos. Aprende sus botones, cuenta pasos y llévalas de flor en flor.',
     'niveles': [
         {'nombre': 'Los botones mágicos', 'cofre': 20, 'misiones': [
             mision('Conoce a Bee-Bot', 'presencial',
                    'Bee-Bot tiene 7 botones:\n\n⬆️ Avanza un paso\n⬇️ Retrocede un paso\n⬅️ ➡️ Gira sin avanzar\n'
                    '✖️ Borra su memoria\n⏸️ Hace una pausa\n🟢 GO: ¡hace tu programa!\n\n'
                    'Prueba cada botón y enséñale a un compañero lo que hace.', xp=40, monedas=10),
             mision('Abejas humanas', 'presencial',
                    '¡Sin robots! 🐝 En parejas: uno es la abejita y el otro es quien programa.\n\n'
                    'Con tarjetas de flechas, armen el camino hasta una flor de papel. La abejita solo puede hacer lo que '
                    'dicen las tarjetas, paso por paso.\n\n¡Después cambien de lugar!'),
             mision('¡Borra la memoria!', 'presencial',
                    'Bee-Bot recuerda TODO lo que le programaste antes. 🧠\n\n'
                    '1. Programa ⬆️⬆️ y presiona GO.\n2. Ahora programa ⬆️ SIN borrar y presiona GO: ¿cuántos pasos dio?\n'
                    '3. Presiona ✖️ y vuelve a intentarlo.\n\nExplícale a tu profe por qué hay que borrar antes de un programa nuevo.'),
         ]},
         {'nombre': 'De flor en flor', 'cofre': 25, 'misiones': [
             mision('¿Cuántos pasos hasta la flor?', 'presencial',
                    'Cada paso de Bee-Bot mide lo mismo que un cuadro del tapete (15 cm). 📏\n\n'
                    '1. Pon una flor en el tapete.\n2. ADIVINA: ¿cuántos pasos necesita la abejita?\n'
                    '3. Prográmala y comprueba.\n\n¿Acertaste? ¡Prueba con una flor más lejos!'),
             mision('Bee-Bot virtual: gira y avanza', 'juego',
                    'Esta abejita virtual funciona igual que Bee-Bot: ⬆️ avanza hacia donde mira y los giros la voltean '
                    'sin moverla. ¡Llévala hasta la batería! 🔋', juego='beebot_virtual'),
             mision('Mi tapete de Bee-Bot', 'evidencia',
                    'Con tu equipo, dibujen en una cartulina un tapete de 4 × 4 cuadros (cada cuadro de 15 cm). 🎨\n\n'
                    'Pongan una colmena en una esquina y flores, charcos y piedras en otros cuadros.\n\n'
                    'Toma una foto del tapete con Bee-Bot encima.', xp=80, monedas=20),
         ]},
         {'nombre': 'El jardín de la reina', 'cofre': 35, 'misiones': [
             jefe('Jefe: El reto de la Abeja Reina',
                  'La Abeja Reina 👑🐝 te pone a prueba:\n\nProgramar a Bee-Bot para que salga de la colmena, visite 3 '
                  'flores y regrese a casa SIN pisar las piedras.\n\nPuedes hacerlo en varios programas cortos (¡borra '
                  'entre cada uno!). Tu profe marca la misión cuando la abejita llegue a la colmena.', xp=120),
         ]},
     ]},

    # ---------- Dash y Blockly ----------
    {'nombre': 'Ciudad de Dash', 'tema': 'ciudad',
     'descripcion': 'Dash es el robot más famoso de la ciudad. Con la app Blockly le enseñarás a avanzar, girar, '
                    'brillar y hablar.',
     'niveles': [
         {'nombre': 'Hola, Dash', 'cofre': 20, 'misiones': [
             mision('Enciende y conecta a Dash', 'presencial',
                    '1. Enciende a Dash con su botón.\n2. Abre la app Blockly en la tableta.\n'
                    '3. Conecta a Dash: acerca la tableta y elige su nombre.\n'
                    '4. Pon el bloque de inicio y un bloque de sonido para que diga «Hola». ¡Presiona ▶️!\n\n🎉 ¡Dash te saludó!'),
             mision('Adelante, atrás… ¡alto!', 'presencial',
                    'Con los bloques de movimiento, programa a Dash para:\n\n⬆️ Avanzar\n⬇️ Regresar a donde empezó\n\n'
                    'Prueba distintas distancias (10, 20 y 50 cm). ¿Cuál llega más lejos?'),
             mision('Dash gira como trompo', 'presencial',
                    'Usa los bloques de girar. 🔄\n\n• ¿Qué pasa si gira 90°? (un cuarto de vuelta)\n'
                    '• ¿Y si gira 180°? (media vuelta)\n• ¿Y 360°? (¡una vuelta completa!)\n\n'
                    'Primero imita cada giro con tu cuerpo y luego prográmalo.'),
         ]},
         {'nombre': 'Luces y sonidos', 'cofre': 25, 'misiones': [
             mision('Show de luces', 'presencial',
                    'Programa a Dash para que cambie el color de sus luces. 🔴🟡🟢\n\n'
                    '¡Conviértelo en semáforo! Rojo → amarillo → verde, esperando un ratito entre cada color.'),
             mision('Dash, ¿cómo hace el perro?', 'presencial',
                    'Dash conoce muchos sonidos: animales, saludos, risas… 🐶🐱🦁\n\n'
                    'Programa a Dash para contar un cuento corto: que avance, haga el sonido de un animal, gire y diga '
                    'otro sonido. Si tu app lo permite, ¡graba tu voz para que Dash la diga!'),
             mision('¿Qué hace este bloque?', 'cuestionario', 'Escucha a tu profe y elige la respuesta correcta. 🧩', preguntas=[
                 ('Para que Dash avance usamos un bloque de…', '🚗 Movimiento', ['🎵 Música', '💡 Luces']),
                 ('Si Dash gira 360°…', '🔄 Da una vuelta completa', ['⬆️ Avanza mucho', '😴 Se apaga']),
                 ('Para que Dash cambie de color usamos un bloque de…', '💡 Luces', ['🚗 Movimiento', '🔊 Sonido']),
                 ('¿Qué botón presionamos en la app para que Dash haga el programa?', '▶️ Iniciar', ['🗑️ Basura', '🔇 Silencio']),
             ]),
         ]},
         {'nombre': 'Desfile en la ciudad', 'cofre': 35, 'misiones': [
             mision('Dash cartero', 'evidencia',
                    'Armen una ciudad en el piso con cajas o bloques: casas, un parque y una escuela. 🏘️\n\n'
                    'Programa a Dash para entregar una carta 💌 de la oficina de correos a una casa (pégale la carta con cinta).\n\n'
                    'Toma una foto de Dash entregando la carta.', xp=80, monedas=25),
             jefe('Jefe: El Gran Desfile de Dash',
                  '¡Hoy es el desfile de la ciudad! 🎉 Programa a Dash para que:\n\n1. Avance por la calle del desfile.\n'
                  '2. Cambie sus luces de colores.\n3. Le diga algo al público.\n4. Gire para saludar y termine en la meta.\n\n'
                  'Presenta tu desfile a todo el grupo.'),
         ]},
     ]},

    # ---------- Bucles y patrones ----------
    {'nombre': 'Bosque de los Bucles', 'tema': 'bosque',
     'descripcion': 'En este bosque todo se repite: el canto de los pájaros, los pasos del baile… Aprende a usar bucles '
                    'para programar menos y lograr más.',
     'niveles': [
         {'nombre': 'Patrones del bosque', 'cofre': 20, 'misiones': [
             mision('Collar de patrones', 'presencial',
                    'Haz un collar o una pulsera con cuentas, sopa de pasta o papelitos siguiendo un patrón:\n'
                    '🔴🔵🔴🔵… o 🟡🟡🟢🟡🟡🟢…\n\n¿Cuántas veces repetiste tu patrón? ¡Eso es un bucle!'),
             mision('El baile que se repite', 'presencial',
                    'Inventen en equipo un baile de 3 pasos: aplauso 👏, salto 🦘 y giro 🔄.\n\n'
                    'Ahora REPÍTANLO 4 veces sin decir cada paso: solo digan «¡repite 4 veces!». Así funciona un bucle.'),
             mision('¿Dónde está el bucle?', 'cuestionario', '¡Encuentra lo que se repite! 🔁', preguntas=[
                 ('🔴🔵🔴🔵🔴… ¿Qué sigue?', '🔵', ['🔴', '🟢']),
                 ('👏🦘👏🦘👏… ¿Qué sigue?', '🦘', ['👏', '🔄']),
                 ('Un bucle sirve para…', '🔁 Repetir algo varias veces', ['🛑 Apagar al robot', '🎨 Pintar']),
                 ('Para que Bee-Bot avance 4 pasos, ¿qué es más corto decir?', '🔁 «Avanza, repite 4 veces»',
                  ['❓ «Avanza nada»', '🙈 «No hagas nada»']),
             ]),
         ]},
         {'nombre': 'Robots repetidores', 'cofre': 25, 'misiones': [
             mision('Bee-Bot dibuja un cuadrado', 'presencial',
                    'Programa a Bee-Bot para que recorra un cuadrado en el tapete y regrese a donde empezó. 🟩\n\n'
                    'Pista: avanza y gira… avanza y gira… ¿cuántas veces se repite?', xp=60),
             mision('Dash baila en bucle', 'presencial',
                    'En Blockly, usa el bloque de repetir 🔁 para que Dash haga un baile: avanza, gira, cambia de luz… ¡y repite 3 veces!\n\n'
                    'Compara: ¿cuántos bloques usaste con repetir y cuántos sin repetir?', xp=60),
             mision('Robot repetidor', 'juego',
                    'Ayuda al robot a llegar a la batería. 🔋 Usa el bloque de repetir para programar menos flechas.',
                    juego='robot_repetidor'),
         ]},
         {'nombre': 'El nido del búho', 'cofre': 35, 'misiones': [
             jefe('Jefe: El Búho Repetidor',
                  'El Búho Repetidor 🦉 solo entiende bucles. Para vencerlo, programa a Dash para que dé la vuelta '
                  'alrededor de su árbol (una silla o una caja) usando el bloque de repetir.\n\n'
                  'Pista: avanza y gira… ¡4 veces!\n\nAl terminar, que Dash diga «¡Uh-uh!» como búho.', xp=120),
         ]},
     ]},

    # ---------- Sensores y condiciones ----------
    {'nombre': 'Océano de los Sensores', 'tema': 'oceano',
     'descripcion': 'Bajo el mar los robots necesitan sentir para no chocar. Descubre los sentidos de Dash y enséñale '
                    'a reaccionar: «si pasa esto, entonces haz aquello».',
     'niveles': [
         {'nombre': 'Mis sentidos, sus sensores', 'cofre': 20, 'misiones': [
             mision('La caja de los sentidos', 'presencial',
                    'Con los ojos tapados 🙈, adivina qué hay en la caja usando tus otros sentidos: tocar ✋, oír 👂 y oler 👃.\n\n'
                    'Los robots también usan sensores para saber qué pasa a su alrededor.'),
             mision('Simón dice: si pasa esto, haz aquello', 'presencial',
                    'Juega con condiciones:\n\n• SI tu profe aplaude 👏, ENTONCES saltas.\n'
                    '• SI levanta una tarjeta roja 🟥, ENTONCES te sientas.\n• SI dice «pez» 🐟, ENTONCES nadas con los brazos.\n\n'
                    '¡Los robots usan el mismo «si… entonces» con sus sensores!'),
             mision('¿Qué sensor usa?', 'cuestionario', 'Escucha a tu profe y elige la respuesta correcta. 🐠', preguntas=[
                 ('Para no chocar con una pared, Dash usa su sensor de…', '👀 Obstáculos', ['👃 Olores', '🍬 Sabores']),
                 ('Cuando aplaudes 👏, Dash te escucha con sus…', '🎤 Micrófonos', ['🛞 Ruedas', '💡 Luces']),
                 ('«SI hay una pared, ENTONCES detente». Esto es una…', '🔀 Condición', ['🔁 Repetición', '🎨 Pintura']),
                 ('Dash tiene botones arriba de su cabeza. ¿Para qué sirven?', '🔘 Para que haga algo cuando los presionas',
                  ['🍔 Para comer', '💤 Para dormir para siempre']),
             ]),
         ]},
         {'nombre': 'Dash submarino', 'cofre': 25, 'misiones': [
             mision('Dash, ¡cuidado con la roca!', 'presencial',
                    'Pon una caja enfrente de Dash: es una roca del océano. 🪨\n\n'
                    'Programa en Blockly: cuando Dash vea un obstáculo enfrente → que se detenga y diga «¡Uy, una roca!».\n\n'
                    'Prueba moviendo la roca a otros lugares.', xp=60, monedas=20),
             mision('Aplaude y Dash baila', 'presencial',
                    'Usa el bloque que escucha aplausos 👏: cuando Dash escuche un aplauso, ¡que baile y cambie de color!\n\n'
                    'Prueba aplaudir fuerte, suave y desde lejos. ¿Siempre te escucha?', xp=60, monedas=20),
             mision('Mi robot con súper sensores', 'evidencia',
                    'Dibuja un robot submarino 🐠🤖 con 3 sensores inventados: uno que encuentra tesoros, otro que avisa si '
                    'viene un tiburón… ¡los que tú quieras!\n\nCuéntale a tu profe qué hace cada sensor y sube la foto de tu dibujo.',
                    xp=70, monedas=20),
         ]},
         {'nombre': 'La cueva del pulpo', 'cofre': 35, 'misiones': [
             jefe('Jefe: El Pulpo de los Ocho Sensores',
                  'El Pulpo 🐙 esconde un tesoro en su cueva. Programa a Dash para que:\n\n1. Avance por el túnel.\n'
                  '2. Se detenga solito si encuentra una roca (sensor de obstáculos).\n'
                  '3. Gire y siga su camino hasta el tesoro 💎.\n4. Celebre con luces y sonidos.\n\n¡Pruébalo frente al grupo!'),
         ]},
     ]},

    # ---------- Errores (bugs) ----------
    {'nombre': 'Volcán de los Bugs', 'tema': 'volcan',
     'descripcion': '¡Unos bichos traviesos (bugs) se metieron en los programas! Aprende a encontrar los errores y a '
                    'arreglarlos sin rendirte.',
     'niveles': [
         {'nombre': 'Cazadores de bugs', 'cofre': 20, 'misiones': [
             mision('La receta equivocada', 'presencial',
                    'Tu profe va a leer los pasos para hacer un sándwich 🥪… ¡pero en desorden y con errores!\n\n'
                    '• Escucha con atención.\n• Grita «¡BUG!» 🐞 cuando encuentres un error.\n'
                    '• Ayuda a acomodar los pasos en el orden correcto.'),
             mision('¿Dónde está el bug?', 'cuestionario', '¡Encuentra los errores! 🐞', preguntas=[
                 ('Para vestirte, ¿qué orden tiene un bug?', '🐞 Primero los zapatos y luego los calcetines',
                  ['🧦 Primero los calcetines y luego los zapatos', '👕 Primero la camiseta y luego la sudadera']),
                 ('Bee-Bot debía avanzar 3 pasos, pero avanzó 5. ¿Qué pasó?', '✖️ No le borraron la memoria',
                  ['🌧️ Estaba lloviendo', '🍯 Tenía hambre']),
                 ('Si tu programa no funciona, ¿qué haces?', '🔍 Busco el error y lo arreglo', ['😭 Me rindo', '🗑️ Tiro el robot']),
                 ('Un «bug» en un programa es…', '🐞 Un error', ['🍰 Un pastel', '🎁 Un premio']),
             ]),
         ]},
         {'nombre': 'Arreglando robots', 'cofre': 25, 'misiones': [
             mision('Bee-Bot perdida', 'presencial',
                    'Tu profe programó a Bee-Bot para llegar a la flor 🌼… ¡pero tiene un bug y se pierde!\n\n'
                    '1. Mira el programa con las tarjetas de flechas.\n2. Encuentra el paso equivocado.\n'
                    '3. Arréglalo y compruébalo con Bee-Bot.', xp=60),
             mision('Dash no llega a la meta', 'presencial',
                    'Abre el programa de Dash que preparó tu profe en Blockly. Dash debería llegar a la meta 🏁, pero algo falla.\n\n'
                    'Pruébalo, observa en qué momento se equivoca, cambia ese bloque y vuelve a probar. '
                    '¡Los programadores hacen esto todos los días!', xp=60),
             mision('Mi diario de bugs', 'evidencia',
                    'Dibuja el bug más difícil que encontraste 🐞 y cómo lo arreglaste: dibuja el «antes» y el «después».\n\n'
                    'Sube una foto de tu dibujo.', xp=70, monedas=20),
         ]},
         {'nombre': 'El cráter', 'cofre': 35, 'misiones': [
             jefe('Jefe: El Bicho Lava-Errores',
                  '¡El Bicho Lava-Errores 🐛🔥 llenó de bugs el laberinto! En equipo:\n\n'
                  '1. Su profe les da un laberinto de cinta en el piso y un programa con 3 bugs escondidos.\n'
                  '2. Encuentren los 3 bugs.\n3. Arreglen el programa hasta que el robot (Dash o Bee-Bot) salga del laberinto.\n\n'
                  '¡Una porra por cada bug que encuentren! 📣'),
         ]},
     ]},

    # ---------- Inventores (sin pantallas) ----------
    {'nombre': 'Taller Polar de Inventores', 'tema': 'hielo',
     'descripcion': 'En el taller de los inventores no se usan pantallas: se usan las manos, el cartón y la imaginación. '
                    '¡Construye tus propios robots!',
     'niveles': [
         {'nombre': 'Manos a la obra', 'cofre': 25, 'misiones': [
             mision('Robot de material reciclado', 'evidencia',
                    'Con cajas, tubos de papel, tapas y botellas construye tu propio robot. ♻️🤖\n\n'
                    '• Ponle ojos (sensores) y algo que parezca motor (ruedas o brazos).\n• Dale un nombre.\n\n'
                    'Toma una foto de tu robot.', xp=90, monedas=25),
             mision('Mano robótica con popotes', 'presencial',
                    '🧰 Material: cartón, popotes, hilo y cinta. Pide ayuda a tu profe para recortar.\n\n'
                    '1. Dibuja tu mano en el cartón y recórtala.\n2. Pega pedacitos de popote en cada dedo.\n'
                    '3. Pasa un hilo por los popotes de cada dedo.\n4. ¡Jala los hilos y los dedos se doblan!\n\n'
                    'Así se mueven las manos de algunos robots.', xp=80, monedas=20),
             mision('Disfraza a tu robot', 'presencial',
                    'Diseña un disfraz para Dash o para Bee-Bot con papel, plastilina o tela 🎭 (¡sin tapar sus ruedas ni sus sensores!).\n\n'
                    'Luego prográmalo para que actúe como su personaje: un dragón que ruge, una ambulancia con luces…'),
         ]},
         {'nombre': 'Ideas que ayudan', 'cofre': 30, 'misiones': [
             mision('Un robot que ayuda en casa', 'evidencia',
                    'Piensa: ¿qué tarea de tu casa podría hacer un robot? 🏠 Tender la cama, regar las plantas, cuidar a tu mascota…\n\n'
                    'Dibuja tu invento con sus partes y súbelo.', xp=70, monedas=20),
             mision('Feria de inventos', 'presencial',
                    'Presenta tu robot reciclado o tu invento al grupo 🎤:\n\n• ¿Cómo se llama?\n• ¿Qué hace?\n'
                    '• ¿Qué sensores y motores tiene?\n\nEscucha a tus compañeros y dile a cada uno algo que te gustó.', xp=60, monedas=20),
             jefe('Jefe: El Yeti Inventor',
                  'El Yeti Inventor 🦍❄️ solo comparte su taller con quien piensa como inventor. ¡Demuéstraselo!',
                  tipo='cuestionario', xp=120, preguntas=[
                      ('Reciclar sirve para…', '♻️ Darle otra vida a los materiales', ['🗑️ Hacer más basura', '🔥 Quemar cajas']),
                      ('La mano robótica dobla los dedos cuando…', '🧵 Jalamos los hilos', ['💧 Le echamos agua', '🎤 Le cantamos']),
                      ('Cuando su idea no funciona, un inventor…', '🔁 La mejora y vuelve a probar', ['🙅 Se rinde', '😡 Se enoja con todos']),
                      ('Para recortar con tijeras debemos…', '✂️ Usarlas con cuidado y con ayuda de un adulto',
                       ['🏃 Correr con ellas', '🤺 Jugar a las espadas']),
                      ('¿Qué parte de tu robot reciclado sería su sensor?', '👀 Los ojos', ['🦶 Los pies', '🎀 Un moño']),
                  ]),
         ]},
     ]},

    # ---------- Gran final ----------
    {'nombre': 'Arena de los Campeones', 'tema': 'desierto',
     'descripcion': '¡La gran final de los pequeños robotistas! Usa todo lo que aprendiste: secuencias, bucles, '
                    'sensores y cacería de bugs.',
     'niveles': [
         {'nombre': 'Entrenamiento', 'cofre': 30, 'misiones': [
             mision('Búsqueda del tesoro con Bee-Bot', 'presencial',
                    'Tu profe esconde tarjetas de tesoro 💎 en el tapete. Con un mapa y coordenadas (por ejemplo, B3), '
                    'programa a Bee-Bot para visitar los tesoros en orden.\n\n¿Quién lo logra con menos programas?',
                    xp=60, monedas=20),
             mision('Código de baile en equipo', 'presencial',
                    'En equipo, escriban con dibujos o flechas el código de un baile 💃: pasos, una repetición y una '
                    'condición («si suena el silbato, ¡congelados!»).\n\nOtro equipo debe bailarlo leyendo su código. '
                    '¿Les salió igual?', xp=60, monedas=20),
             mision('Pista de carreras', 'evidencia',
                    'En equipo, construyan en el piso una pista para Dash con cinta, conos o bloques 🏁: con curvas, '
                    'un túnel y una meta.\n\nToma una foto de su pista.', xp=80, monedas=20),
         ]},
         {'nombre': 'La gran final', 'cofre': 50, 'misiones': [
             mision('Carrera galáctica de Dash', 'presencial',
                    '¡Es hora de la carrera! 🏎️ Programa a Dash para recorrer la pista de tu equipo sin salirse:\n\n'
                    '• Usa movimientos y giros.\n• Usa repetir si puedes.\n• Celebra en la meta con luces y sonido.\n\n'
                    'Si falla, ¡busca el bug y vuelve a intentarlo!', xp=80, monedas=25),
             mision('Repaso de pequeños robotistas', 'cuestionario', '¿Listo para la final? Escucha y responde. 🏆',
                    xp=60, monedas=20, preguntas=[
                        ('Bee-Bot avanza un paso cuando presionas…', '⬆️', ['✖️', '⏸️']),
                        ('Antes de un programa nuevo, en Bee-Bot presionas…', '✖️ Borrar', ['🟢 GO', '⬇️ Atrás']),
                        ('Repetir varias veces lo mismo es un…', '🔁 Bucle', ['🐞 Bug', '🔋 Batería']),
                        ('«SI hay obstáculo, ENTONCES alto» es una…', '🔀 Condición', ['🔁 Repetición', '🎨 Pintura']),
                        ('Un error en un programa se llama…', '🐞 Bug', ['🌈 Arcoíris', '🍪 Galleta']),
                        ('Dash cambia de color con los bloques de…', '💡 Luces', ['🚗 Movimiento', '🔊 Sonido']),
                    ]),
             jefe('Jefe final: El Rey de los Robots',
                  'El Rey de los Robots 👑🤖 quiere conocer a los mejores robotistas de la galaxia. En equipo, preparen un show final:\n\n'
                  '🐝 Bee-Bot lleva una corona por un camino.\n🤖 Dash baila con bucles, luces y sonido.\n'
                  '🎤 Ustedes cuentan lo que aprendieron este año.\n\n¡Pregúntale a tu profe si pueden invitar a sus familias!',
                  xp=200, monedas=80),
         ]},
     ]},
]

CURSO = {
    'nombre': 'Robótica · Primaria Baja (Dash, Blockly y Bee-Bot)',
    'juegos': JUEGOS,
    'mundos': MUNDOS,
}
