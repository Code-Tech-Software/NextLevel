"""Mundo 8 · ES-DAT304 Respira hondo: el polvo del Sahara y la salud de los pulmones, el usuario, el árbol de
problemas y el de decisión, diagrama de flujo y pseudocódigo, y un entrenador de soplido con micro:bit que cuenta
repeticiones (circuito que se cierra al soplar).

Se usan tonos y no los sonidos de la V2 para que el programa funcione en cualquier micro:bit."""
from .base import DUPLA_MAKER, LEYENDA_MICROBIT, PAREJAS, clasifica, jefe, leccion, microbit, mision

JUEGOS = {
    'clasifica_pulmones': clasifica('¿Ayuda o daña a tus pulmones?', '🫁', 'Algunas cosas fortalecen tus pulmones y '
                                    'otras los lastiman. ¿Qué hace cada una?', [
        ('Ayuda', '💪', ['Nadar', 'Correr o andar en bici', 'Respirar profundo por la nariz',
                         'Tocar un instrumento de viento', 'Ventilar el salón', 'Tener árboles cerca de casa']),
        ('Daña', '🚭', ['El humo del cigarro, aunque sea de otros', 'Quemar basura', 'Respirar polvo del Sahara',
                        'El humo de los coches en el tráfico', 'Vapear', 'Cohetes y fogatas en lugares cerrados']),
    ], rondas=12),
    'clasifica_simbolos': clasifica('Símbolos del diagrama de flujo', '🔷', 'Cada forma del diagrama tiene un trabajo. '
                                    '¿En qué forma va cada paso del entrenador?', [
        ('Óvalo (inicio o fin)', '⬭', ['INICIO', 'FIN', 'Empieza el entrenamiento', 'Termina el programa']),
        ('Rectángulo (acción)', '▭', ['Sumar 1 a repeticiones', 'Mostrar el número en la pantalla',
                                      'Reproducir un tono de festejo', 'Poner segundos en 0']),
        ('Rombo (decisión)', '🔶', ['¿El circuito está cerrado?', '¿segundos = 3?', '¿Se presionó el botón A?',
                                   '¿Ya hiciste 5 repeticiones?']),
    ], rondas=12),
}

DIAGRAMA = '''
( INICIO )
    ↓
[ segundos ← 0 · repeticiones ← 0 ]
    ↓
◇ ¿El circuito está cerrado? ◇ ── No ──→ [ segundos ← 0 ] ──→ (regresa al rombo)
    ↓ Sí
[ sumar 1 a segundos · esperar 1 segundo ]
    ↓
◇ ¿segundos = 3? ◇ ── No ──→ (regresa al primer rombo)
    ↓ Sí
[ sumar 1 a repeticiones · sonar · mostrar repeticiones ]
    ↓
[ segundos ← 0 ] ──→ (regresa al primer rombo)
'''

CODIGO_ENTRENADOR = '''
al iniciar
    fijar [segundos] a 0
    fijar [repeticiones] a 0
    mostrar ícono [corazón]
para siempre
    si (pin [P1] está presionado) entonces
        cambiar [segundos] por 1
        trazar gráfico de barras (segundos) hasta 3
        pausa (ms) 1000
    si no
        fijar [segundos] a 0
        borrar la pantalla
    si ((segundos) = 3) entonces
        cambiar [repeticiones] por 1
        reproduce secuencia (tono [Do alto] durante [1 pulso]) en modo [hasta que termine]
        mostrar número (repeticiones)
        fijar [segundos] a 0
al presionarse el botón A
    mostrar número (repeticiones)
al presionarse el botón A+B
    fijar [repeticiones] a 0
    mostrar número 0
'''

MUNDO = {
    'nombre': 'Misión Respira Hondo', 'tema': 'desierto',
    'descripcion': 'ES-DAT304 · Respira hondo. Turistas y vecinos del Caribe han tenido problemas para respirar: la causa '
                   'es el polvo del desierto del Sahara, que cruza el océano. No se puede evitar del todo, pero unos '
                   'pulmones fuertes ayudan a prevenir enfermedades como el asma o la bronquitis. Analiza el problema con '
                   'árboles, diseña el diagrama de flujo y construye con la micro:bit un entrenador de soplido. Pregunta '
                   'guía: ¿cómo podemos fortalecer nuestros pulmones?',
    'niveles': [
        {'nombre': 'Polvo del Sahara', 'cofre': 25, 'misiones': [
            mision('Polvo que cruza el océano', 'texto', leccion(
                intro='Cada verano, el viento levanta enormes nubes de polvo en el desierto del Sahara, en África. El '
                      'polvo viaja unos 8,000 kilómetros sobre el océano Atlántico y llega al Caribe, al Golfo de México y '
                      'a la península de Yucatán. El cielo se ve amarillento y el polvo, muy fino, puede irritar los ojos '
                      'y la garganta y empeorar el asma.',
                pasos=['¿Has visto el cielo amarillento o con mucho polvo o humo? ¿Cómo te sentiste?',
                       '¿Qué crees que les pasa a los pulmones cuando respiran polvo muchos días?',
                       '¿Qué podrías construir con lo que aprendiste de circuitos para ayudar a alguien a fortalecer sus '
                       'pulmones?'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('Diagnóstico: circuitos y micro:bit', 'cuestionario', leccion(
                intro='Este proyecto usa todo lo del mundo de Sombra Veloz. Revisa qué tan listo estás.',
                saber=['Circuito cerrado: la electricidad circula. Abierto: está cortado.',
                       'Cerrar un circuito con la micro:bit: unir un pin con GND.',
                       '«pin P1 está presionado» responde verdadero si el circuito está cerrado.',
                       'Una variable guarda un dato que cambia.']), xp=50, preguntas=[
                ('Unes el pin 1 con GND. El circuito está…', 'Cerrado', ['Abierto', 'Apagado', 'Roto']),
                ('¿Qué bloque responde verdadero o falso?', 'pin P1 está presionado',
                 ['mostrar número', 'al iniciar', 'borrar la pantalla']),
                ('¿Qué material sirve para cerrar un circuito?', 'Papel aluminio', ['Cartulina', 'Plástico',
                                                                                   'Hule']),
                ('¿Para qué sirve una variable?', 'Para guardar un dato que cambia', ['Para encender la tarjeta',
                                                                                     'Para cortar el cable',
                                                                                     'Para dibujar']),
                ('¿Qué bloque se ejecuta sin parar?', 'para siempre', ['al iniciar', 'al presionarse el botón A',
                                                                       'mostrar ícono']),
            ]),
            mision('Carta de intención', 'texto', leccion(
                intro='Antes de un proyecto importante, los ingenieros escriben una carta de intención: qué se '
                      'comprometen a hacer y para qué.',
                pasos=['Escribe la misión con tus palabras: «Nuestra misión es…».',
                       'Escribe tu compromiso: «Yo, (tu nombre), me comprometo a…» (por ejemplo, cumplir mi papel en la '
                       'dupla y cuidar el material).',
                       'Escribe tu meta personal para este proyecto.'],
                entrega='escribe tu carta aquí abajo.'), xp=50),
        ]},
        {'nombre': 'Pulmones y problemas', 'cofre': 30, 'misiones': [
            mision('Pulmones en riesgo', 'cuestionario', leccion(
                intro='Para ayudar a alguien, primero hay que entender qué le pasa.',
                saber=['Asma: las vías por donde pasa el aire se inflaman y se cierran; cuesta trabajo respirar.',
                       'Bronquitis: se inflaman los bronquios, los tubos que llevan el aire a los pulmones.',
                       'Partículas finas: polvo y humo tan pequeños que entran hasta el fondo de los pulmones.',
                       'Cómo protegerse: no estar cerca del humo de cigarro, ventilar, usar cubrebocas cuando el aire está '
                       'muy contaminado y hacer ejercicio.',
                       'Los ejercicios de respiración fortalecen los músculos que te ayudan a respirar, como el '
                       'diafragma.']), xp=60, preguntas=[
                ('¿Qué pasa en un ataque de asma?', 'Las vías del aire se inflaman y se cierran',
                 ['Los pulmones crecen', 'El corazón se detiene', 'La nariz se tapa con agua']),
                ('¿Qué se inflama en la bronquitis?', 'Los bronquios', ['El estómago', 'Los músculos de las piernas',
                                                                       'Los ojos']),
                ('¿Por qué son peligrosas las partículas finas?', 'Porque entran hasta el fondo de los pulmones',
                 ['Porque son de colores', 'Porque hacen ruido', 'Porque pesan mucho']),
                ('¿Qué te protege cuando el aire está muy contaminado?', 'Usar cubrebocas y evitar el ejercicio afuera',
                 ['Correr más rápido', 'Abrir todas las ventanas', 'Respirar por la boca']),
                ('¿Qué fortalecen los ejercicios de respiración?', 'Los músculos que ayudan a respirar',
                 ['Los huesos de los pies', 'El cabello', 'Las uñas']),
            ]),
            mision('¿Ayuda o daña a tus pulmones?', 'juego', leccion(
                intro='Clasifica cada cosa según lo que les hace a tus pulmones.',
                tip='Todo lo que hace que respires humo o polvo los daña; lo que los pone a trabajar con aire limpio '
                    'los fortalece.'), juego='clasifica_pulmones'),
            mision('Conoce a tu usuario', 'texto', leccion(
                intro='Un buen invento piensa en una persona concreta. Elige al usuario de tu entrenador de soplido.',
                saber=['Ejemplos de usuarios: un abuelo que se cansa al subir escaleras, una niña con asma, un '
                       'deportista que quiere mejorar, un músico de banda, alguien que vive donde llega el polvo del '
                       'Sahara.'],
                pasos=['Describe a tu usuario: edad, qué hace y qué problema tiene al respirar (sin nombres reales).',
                       '¿Qué necesita tu entrenador para que tu usuario lo pueda usar? Escribe 3 necesidades (por ejemplo: '
                       'fácil de limpiar, que muestre su avance, que no sea muy difícil al principio).',
                       '¿Cómo sabrá tu usuario que va mejorando?'],
                logro=['Tu usuario tiene un problema claro y 3 necesidades que tu diseño debe cumplir.'],
                entrega='escribe tu usuario y sus necesidades aquí abajo.'), xp=60),
            mision('Árbol de problemas', 'evidencia', leccion(
                intro='Un árbol de problemas organiza un problema como un árbol: las raíces son las causas, el tronco es '
                      'el problema y las ramas son las consecuencias.',
                saber=['Tronco: «Muchas personas tienen pulmones débiles o enfermos».',
                       'Raíces (causas): por ejemplo, el polvo del Sahara, el humo del tráfico, poco ejercicio…',
                       'Ramas (consecuencias): por ejemplo, asma, cansancio, faltar a la escuela…',
                       'Se puede hacer a mano o en una presentación con formas (Insertar → Formas).'],
                dinamica=PAREJAS,
                pasos=['Dibuja el árbol con el problema en el tronco.',
                       'Escribe al menos 4 causas en las raíces.',
                       'Escribe al menos 4 consecuencias en las ramas.',
                       'Encierra en un círculo la causa que tu entrenador puede ayudar a combatir.'],
                logro=['Tu árbol tiene problema, 4 causas, 4 consecuencias y la causa que atacará tu invento.'],
                entrega='sube una foto o una captura de tu árbol.'), xp=80, monedas=25),
            mision('Árbol de decisión', 'texto', leccion(
                intro='Un árbol de decisión hace preguntas de sí o no, una tras otra, hasta llegar a una decisión. Las '
                      'computadoras toman decisiones así.',
                saber=['Ejemplo: «¿El cielo está amarillento o con humo?» → Sí: «¿Tienes asma?» → Sí: quedarte adentro. '
                       'No: usar cubrebocas y no correr. → No: salir a jugar.'],
                pasos=['Copia el ejemplo y agrégale una pregunta más en alguna rama.',
                       'Inventa tu propio árbol de 2 preguntas para decidir algo de tu entrenador (por ejemplo, si subir '
                       'la dificultad).',
                       'Escríbelo con flechas: Pregunta → Sí: … / No: …'],
                logro=['Tu árbol tiene 2 preguntas de sí o no y una decisión al final de cada camino.'],
                entrega='escribe tus dos árboles aquí abajo.'), xp=60),
        ]},
        {'nombre': 'Diagrama y pseudocódigo', 'cofre': 30, 'misiones': [
            mision('Diagramas de flujo', 'cuestionario', leccion(
                intro='Antes de programar, los programadores dibujan el camino de su programa con un diagrama de flujo.',
                saber=['Óvalo: INICIO y FIN.',
                       'Rectángulo: una acción («sumar 1 a repeticiones»).',
                       'Rombo: una decisión con dos salidas, Sí y No («¿el circuito está cerrado?»).',
                       'Flechas: el orden en que se siguen los pasos. Una flecha que regresa forma un ciclo.',
                       'Pseudocódigo: el mismo programa escrito con palabras, como receta: INICIO, SI … ENTONCES, SI NO, '
                       'FIN SI, REPETIR PARA SIEMPRE, FIN.']), xp=60, preguntas=[
                ('¿Qué forma se usa para una decisión?', 'El rombo', ['El óvalo', 'El rectángulo', 'La flecha']),
                ('¿Qué forma se usa para INICIO y FIN?', 'El óvalo', ['El rombo', 'El rectángulo', 'El círculo de '
                                                                                                 'colores']),
                ('«Sumar 1 a repeticiones» va en un…', 'Rectángulo', ['Rombo', 'Óvalo', 'Triángulo']),
                ('¿Cuántas salidas tiene un rombo?', 'Dos: Sí y No', ['Una', 'Ninguna', 'Cinco']),
                ('Una flecha que regresa a un paso anterior forma…', 'Un ciclo', ['Un error', 'El fin',
                                                                                  'Una variable']),
                ('¿Qué es el pseudocódigo?', 'El programa escrito con palabras, como una receta',
                 ['Un código secreto', 'Un virus', 'Un tipo de micro:bit']),
            ]),
            mision('Símbolos del diagrama de flujo', 'juego', leccion(
                intro='Cada paso del entrenador va en su forma. Clasifícalos.',
                tip='Si es una pregunta, va en rombo.'), juego='clasifica_simbolos'),
            mision('Dibuja el diagrama', 'evidencia', leccion(
                intro='Con esta información, dibuja el diagrama de flujo del entrenador de soplido.',
                saber=['Al empezar, los segundos y las repeticiones valen 0.',
                       'El programa revisa todo el tiempo si el circuito está cerrado (alguien está soplando).',
                       'Si está cerrado, suma 1 a los segundos y espera 1 segundo. Si no, los segundos vuelven a 0.',
                       'Cuando los segundos llegan a 3, suma 1 a las repeticiones, suena, muestra las repeticiones y '
                       'regresa los segundos a 0.',
                       'Después de cada paso, vuelve a revisar el circuito.'],
                material=['Una hoja', 'Lápiz y regla'],
                pasos=['Dibuja el óvalo de INICIO y el rectángulo donde todo vale 0.',
                       'Dibuja el primer rombo con sus dos salidas.',
                       'Dibuja el segundo rombo: ¿segundos = 3?',
                       'Une todo con flechas, incluyendo las que regresan.'],
                logro=['Tu diagrama usa óvalo, rectángulos y 2 rombos con salidas Sí y No, y tiene flechas que '
                       'regresan.'],
                entrega='sube una foto de tu diagrama.'), xp=80, monedas=25),
            mision('Del diagrama al pseudocódigo', 'texto', leccion(
                intro='Compara tu diagrama con el de abajo y tradúcelo a pseudocódigo: el puente entre el dibujo y los '
                      'bloques.',
                saber=['Palabras del pseudocódigo: INICIO, FIN, REPETIR PARA SIEMPRE, SI … ENTONCES, SI NO, FIN SI.',
                       '«←» significa «ahora vale». «segundos ← 0» se lee «segundos ahora vale 0».',
                       'Lo que está dentro de un SI o de un REPETIR se escribe con sangría (un poco a la derecha).'],
                pasos=['Compara el diagrama de abajo con el tuyo: ¿qué te faltó o qué hiciste distinto?',
                       'Escribe el pseudocódigo completo empezando con INICIO.',
                       'Revisa: cada rombo debe convertirse en un SI … ENTONCES / SI NO.'],
                logro=['Tu pseudocódigo tiene el ciclo, los dos SI y la sangría correcta.'],
                entrega='escribe tu pseudocódigo aquí abajo.'), xp=70, monedas=20, codigo=DIAGRAMA.strip('\n')),
        ]},
        {'nombre': 'Construye el entrenador', 'cofre': 35, 'misiones': [
            mision('Parte maker: el tubo de soplido', 'presencial', leccion(
                intro='Así funciona: soplas por un tubo, el aire empuja una aleta con aluminio y la pega contra otra tira '
                      'de aluminio. Mientras soples fuerte, el circuito está cerrado.',
                roles=['Constructor: arma el tubo, la aleta y la pared de contacto.',
                       'Electricista: pega el aluminio, conecta los caimanes y prueba que la aleta cierre el circuito.'],
                material=['Un tubo de cartón (de papel de cocina)', 'Cartulina delgada', 'Papel aluminio',
                          'Cinta adhesiva', 'Una tapa o pedazo de cartón como base', '2 cables con caimanes',
                          'Un popote o boquilla de papel PARA CADA PERSONA'],
                dinamica=['En duplas, en su lugar. Semáforo en 🟡.',
                          'Higiene: cada quien sopla solo por su propia boquilla. Nunca se comparte.',
                          'Si alguien se marea al soplar, para y respira normal.'],
                pasos=['Pega el tubo acostado sobre la base.',
                       'Aleta: un rectángulo de cartulina un poco más grande que la salida del tubo, con aluminio por '
                       'fuera. Pégala solo de su orilla de arriba, como puerta de perro.',
                       'Pared de contacto: un cartón parado frente a la aleta, a 1 o 2 cm, con aluminio del lado que mira '
                       'a la aleta.',
                       'Caimán de la aleta → pin 1. Caimán de la pared → GND. Deja los cables flojos para que la aleta '
                       'se mueva.',
                       'Prueba con el detector de conductores: al soplar fuerte, ¿aparece la palomita?'],
                logro=['Al soplar fuerte la aleta toca la pared y el circuito se cierra; al dejar de soplar, se '
                       'abre.']), xp=60),
            microbit('Programa el entrenador', leccion(
                intro='Ahora el programa que diseñaste: cuenta los segundos de soplido, muestra el avance en barras y '
                      'festeja cada repetición.',
                saber=['«trazar gráfico de barras (segundos) hasta 3» (LED) llena la pantalla poco a poco: con 3 '
                       'segundos se llena toda.',
                       '«si … entonces / si no» es el primer rombo de tu diagrama; el segundo «si» es el rombo de '
                       '«¿segundos = 3?».',
                       'Botón A: muestra las repeticiones. A+B: empieza de nuevo.',
                       LEYENDA_MICROBIT],
                dinamica=DUPLA_MAKER,
                pasos=['Crea las variables «segundos» y «repeticiones» y arma el código.',
                       'Pruébalo en el simulador: mantén presionado el pin 1 tres segundos.',
                       'Descárgalo a la micro:bit y conecta tu tubo de soplido.',
                       'Prueba soplando: ¿se llenan las barras? ¿Suena al llegar a 3?',
                       'Si tu micro:bit es V1 y no suena, conecta audífonos o una bocina a P0 y GND.'],
                logro=['Al soplar 3 segundos seguidos se llenan las barras, suena el tono y suben las repeticiones.'],
                entrega='sube un video corto o una foto de tu entrenador funcionando y una captura de tus bloques.'),
                CODIGO_ENTRENADOR, xp=110, monedas=30),
            mision('Pruebas y mejoras', 'evidencia', leccion(
                intro='Los ingenieros prueban, miden y mejoran. Haz 5 pruebas y regístralas en una hoja de cálculo.',
                saber=['Variable a probar: la distancia entre la aleta y la pared. Más lejos = más difícil.',
                       'Mide cuántas repeticiones logras en 1 minuto con cada distancia.',
                       'Reto V2: si tu micro:bit tiene micrófono, cambia la condición por «nivel de sonido > 120» (de '
                       'Entrada y Lógica) y sopla cerca del micrófono. ¿Qué funciona mejor?'],
                dinamica=DUPLA_MAKER,
                pasos=['En una hoja de cálculo: columna A «Distancia (cm)» y columna B «Repeticiones en 1 minuto».',
                       'Prueba 5 distancias (por ejemplo 0.5, 1, 1.5, 2 y 2.5 cm) y anota los resultados.',
                       'Haz una gráfica de columnas con tus datos.',
                       'Escribe en la hoja: ¿qué distancia recomendarías para un principiante y cuál para un deportista?',
                       'Propón una mejora para tu entrenador.'],
                logro=['Tu hoja tiene 5 pruebas, una gráfica y tu recomendación para cada usuario.'],
                entrega='sube una captura de tu tabla con su gráfica y escribe tu mejora en el comentario.'),
                xp=90, monedas=25),
        ]},
        {'nombre': 'Feria de la salud', 'cofre': 40, 'misiones': [
            mision('Defiende tu prototipo', 'presencial', leccion(
                intro='Feria de la salud: cada dupla presenta su entrenador como si quisiera convencer a un hospital de '
                      'usarlo.',
                dinamica=['Cada dupla tiene 2 minutos al frente: uno explica y el otro hace la demostración.',
                          'El público escucha con el semáforo en 🔴 y al final hace 1 pregunta.'],
                pasos=['Presenten a su usuario y su problema.',
                       'Hagan la demostración: soplen hasta lograr una repetición.',
                       'Expliquen el circuito y el programa con su diagrama.',
                       'Respondan la pregunta del público defendiendo su diseño.'],
                logro=['Explicaron usuario, circuito y programa, y respondieron la pregunta con argumentos.']), xp=60),
            mision('Evaluación final', 'texto', leccion(
                intro='Cierra el proyecto revisando tu trabajo y el de tu dupla.',
                pasos=['Relee tu carta de intención: ¿cumpliste tu compromiso y tu meta? ¿Por qué?',
                       'Del 1 al 5, califica tu entrenador en: funciona, ayuda a tu usuario y está bien construido.',
                       '¿Qué parte fue más difícil: la maker o la programación? ¿Cómo la resolvieron?',
                       '¿Qué le dirías a alguien para que cuide sus pulmones?'],
                entrega='escribe tu evaluación aquí abajo.'), xp=60),
            jefe('Jefe: La Tormenta de Arena', leccion(
                intro='La Tormenta de Arena cruzó el océano y viene directo hacia ti. Solo la detiene quien entiende los '
                      'pulmones, los diagramas y la micro:bit.'), [
                ('¿De dónde viene el polvo que llega al Caribe y a Yucatán?', 'Del desierto del Sahara',
                 ['Del Polo Norte', 'De los volcanes de México', 'De la Luna']),
                ('En un árbol de problemas, ¿qué son las raíces?', 'Las causas', ['Las consecuencias', 'El problema',
                                                                                 'Las soluciones']),
                ('¿Qué forma del diagrama de flujo representa una decisión?', 'El rombo', ['El óvalo',
                                                                                         'El rectángulo',
                                                                                         'La flecha']),
                ('En pseudocódigo, un rombo se convierte en…', 'Un SI … ENTONCES / SI NO', ['Un INICIO', 'Un FIN',
                                                                                           'Una variable']),
                ('¿Qué cierra el circuito del entrenador?', 'La aleta con aluminio al tocar la pared de contacto',
                 ['El botón A', 'El cable USB', 'La pantalla']),
                ('¿Qué hace «trazar gráfico de barras (segundos) hasta 3»?', 'Llena la pantalla según los segundos',
                 ['Borra la pantalla', 'Toca un sonido', 'Cuenta repeticiones']),
                ('¿Por qué cada persona usa su propia boquilla?', 'Por higiene, para no compartir gérmenes',
                 ['Para que suene más fuerte', 'Porque es más barato', 'Para que no se moje el aluminio']),
                ('¿Qué enfermedad hace que las vías del aire se inflamen y se cierren?', 'El asma',
                 ['La gripe del estómago', 'La caries', 'La miopía']),
            ]),
        ]},
    ],
}
