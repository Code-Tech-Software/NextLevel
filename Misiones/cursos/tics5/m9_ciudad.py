"""Mundo 9 · Cierre del año: ciudadanía digital para 5.º (datos personales, contraseñas de 3 palabras, ciberacoso y
verificar información) y el portafolio del año con el jefe final de todo el curso."""
from .base import KIDDLE, LLAVERO, PAREJAS, clasifica, jefe, leccion, mision

JUEGOS = {
    'clasifica_datos_cuido': clasifica('¿Lo comparto o lo cuido?', '🔐', 'Algunos datos se pueden compartir en '
                                       'internet y otros te ponen en riesgo. ¿Qué haces con cada uno?', [
        ('Lo puedo compartir', '🙂', ['Tu color favorito', 'Tu personaje de videojuego favorito',
                                      'Un dibujo tuyo sin tu nombre completo', 'Tu opinión de una película',
                                      'Un dato curioso de los planetas', 'Tu apodo de juego, sin tu nombre real']),
        ('Lo cuido', '🔒', ['Tu dirección', 'Tu contraseña', 'El nombre de tu escuela', 'Una foto con tu uniforme',
                            'Tu número de teléfono', 'Dónde vas a estar el sábado']),
    ], rondas=12),
    'clasifica_contrasenas': clasifica('¿Contraseña fuerte o débil?', '🗝️', 'Las contraseñas fuertes son largas, '
                                       'raras y no tienen nada que ver contigo. ¿Cómo es cada una?', [
        ('Fuerte', '💪', ['Pato!Volcan7Tacos', 'Rio-Nube-Tenis-58', '8Jirafas#Bailan.Mar', 'SolDeMarte!Pizza3',
                          'Trompo.Verde.Cielo9', 'Cactus_Lunar_Bici_42']),
        ('Débil', '🥀', ['123456', 'contraseña', 'qwerty', 'abc123', 'firulais2015', 'maria2014']),
    ], rondas=12),
    'clasifica_reaccion': clasifica('Ciberacoso: ¿buena o mala idea?', '🛡️', 'Alguien está molestando a un '
                                    'compañero en internet. ¿Esta reacción ayuda o empeora las cosas?', [
        ('Buena idea', '✅', ['Guardar una captura del mensaje', 'Bloquear a quien te molesta',
                              'Contarle a un adulto de confianza', 'Reportar la cuenta en la app',
                              'Apoyar al compañero que lo sufre', 'No reenviar un meme que se burla de alguien']),
        ('Mala idea', '❌', ['Responder con insultos', 'Reenviarlo para que todos lo vean',
                             'Quedarte callado y no contarle a nadie', 'Burlarte en los comentarios',
                             'Publicar la foto de otro sin permiso', 'Hacerte pasar por otra persona']),
    ], rondas=12),
}

MUNDO = {
    'nombre': 'Ciudad Conectada', 'tema': 'ciudad',
    'descripcion': 'El cierre del año. Ya sabes programar, modelar en 3D, usar la IA y armar circuitos; ahora toca ser '
                   'un buen ciudadano digital: cuidar tus datos, crear contraseñas fuertes, saber qué hacer ante el '
                   'ciberacoso y distinguir lo real de lo inventado. Al final armas tu portafolio del año y enfrentas al '
                   'jefe final. Pregunta guía: ¿cómo me cuido y cuido a los demás en internet?',
    'niveles': [
        {'nombre': 'Tus datos, tu llave', 'cofre': 30, 'misiones': [
            mision('Datos personales', 'cuestionario', leccion(
                intro='En internet, tus datos personales son como las llaves de tu casa: no se le dan a cualquiera.',
                saber=['Datos personales: tu nombre completo, dirección, teléfono, escuela, fotos donde se te reconoce, '
                       'dónde estás y tus contraseñas.',
                       'Lo que se publica es muy difícil de borrar: alguien pudo copiarlo o tomarle captura.',
                       'Un perfil o apodo no debe revelar tu nombre real ni tu edad.',
                       'Si alguien que no conoces en persona te pide fotos o datos, no respondas y cuéntale a un adulto '
                       'de confianza.']), xp=60, preguntas=[
                ('¿Cuál es un dato personal?', 'Tu dirección', ['Tu color favorito', 'Tu película favorita',
                                                               'Un dato de los planetas']),
                ('¿Por qué hay que pensar antes de publicar algo?', 'Porque es muy difícil de borrar',
                 ['Porque se borra solo', 'Porque nadie lo ve', 'Porque cuesta dinero']),
                ('¿Cuál es un buen apodo para un juego en línea?', 'CometaVeloz', ['MariaLopez2015', 'Juan5toB',
                                                                                 'Ana_calle_Pino']),
                ('Alguien que no conoces te pide una foto. ¿Qué haces?', 'No respondo y le cuento a un adulto',
                 ['Se la mando', 'Le pido la suya primero', 'Le doy mi dirección']),
                ('¿Por qué una foto con tu uniforme es un riesgo?', 'Porque dice a qué escuela vas',
                 ['Porque sale fea', 'Porque gasta datos', 'Porque no tiene filtro']),
            ]),
            mision('¿Lo comparto o lo cuido?', 'juego', leccion(
                intro='Decide qué datos se pueden compartir y cuáles se cuidan.',
                tip='Si con ese dato alguien te puede encontrar o hacerse pasar por ti, se cuida.'),
                juego='clasifica_datos_cuido'),
            mision('Contraseñas de 3 palabras', 'texto', leccion(
                intro='Los expertos recomiendan el método de las 3 palabras: fácil de recordar para ti y muy difícil de '
                      'adivinar para los demás.',
                saber=['Elige 3 palabras al azar que no tengan que ver contigo (nada de tu nombre, tu mascota o tu '
                       'cumpleaños).',
                       'Únelas y agrega un número y un símbolo: Pato!Volcan7Tacos.',
                       'Mientras más larga, mejor: al menos 12 caracteres.',
                       'Una contraseña distinta para cada cuenta, y solo la conocen tú y tu papá, mamá o tutor.',
                       LLAVERO + ' No se las enseñes a nadie.'],
                ojo=['En esta misión NO escribas ninguna contraseña que uses de verdad: todo es de ejemplo.'],
                pasos=['Inventa 2 contraseñas DE EJEMPLO con el método de las 3 palabras.',
                       'Explica por qué «firulais2015» es débil.',
                       '¿Qué harías si un amigo te pide tu contraseña «para ayudarte» en un juego?'],
                logro=['Tus contraseñas de ejemplo tienen 3 palabras, número, símbolo y al menos 12 caracteres.'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('¿Contraseña fuerte o débil?', 'juego', leccion(
                intro='Clasifica cada contraseña como lo haría un experto en ciberseguridad.'),
                juego='clasifica_contrasenas'),
        ]},
        {'nombre': 'Convivencia digital', 'cofre': 30, 'misiones': [
            mision('Ciberacoso: qué hacer', 'cuestionario', leccion(
                intro='Detrás de cada pantalla hay una persona. El ciberacoso lastima de verdad, y todos podemos '
                      'ayudar a detenerlo.',
                saber=['Ciberacoso: molestar, amenazar, burlarse o excluir a alguien una y otra vez por internet.',
                       'Si te pasa a ti: no respondas, guarda capturas, bloquea, reporta y cuéntale a un adulto de '
                       'confianza.',
                       'Si lo ves: no reenvíes ni des «me gusta», apoya a la persona y avisa a un adulto.',
                       'Antes de publicar algo sobre otra persona, pregúntate: ¿le gustaría que lo viera todo el mundo?']),
                xp=60, preguntas=[
                ('¿Qué es el ciberacoso?', 'Molestar o burlarse de alguien una y otra vez por internet',
                 ['Jugar en línea con amigos', 'Mandar un mensaje de cumpleaños', 'Ver videos']),
                ('Alguien te manda mensajes que te molestan. ¿Qué haces primero?',
                 'No respondo, guardo capturas y le cuento a un adulto', ['Le contesto con insultos',
                                                                         'Borro todo sin decir nada',
                                                                         'Publico sus mensajes']),
                ('Ves un meme que se burla de un compañero. ¿Qué haces?', 'No lo reenvío y apoyo a mi compañero',
                 ['Lo reenvío porque es chistoso', 'Le doy me gusta', 'Escribo un comentario burlón']),
                ('¿Para qué sirve guardar capturas?', 'Para tener pruebas al reportar', ['Para presumirlas',
                                                                                         'Para reenviarlas',
                                                                                         'Para nada']),
                ('¿Qué pregunta te haces antes de publicar algo de otra persona?',
                 '¿Le gustaría que lo viera todo el mundo?', ['¿Cuántos «me gusta» tendrá?', '¿Es chistoso?',
                                                              '¿Lo verá el profe?']),
            ]),
            mision('Ciberacoso: ¿buena o mala idea?', 'juego', leccion(
                intro='Decide qué reacciones ayudan y cuáles empeoran las cosas.',
                tip='Ayuda todo lo que protege a la persona y deja pruebas; empeora todo lo que hace que más gente lo '
                    'vea.'), juego='clasifica_reaccion'),
            mision('Semáforo digital', 'presencial', leccion(
                intro='Una dinámica rápida: el profe lee situaciones de internet y cada quien decide con su semáforo.',
                dinamica=['Cada alumno tiene 3 tarjetas: 🟢 está bien, 🟡 pide ayuda a un adulto, 🔴 no lo hagas.',
                          'Todos levantan su tarjeta al mismo tiempo, cuando el profe cuenta 3. Nadie grita la '
                          'respuesta.',
                          'Después de cada situación, 2 voluntarios explican su color.'],
                pasos=['Situación 1: un desconocido te invita a un grupo de chat «solo para niños».',
                       'Situación 2: quieres subir un dibujo tuyo a la clase de Classroom.',
                       'Situación 3: un juego te pide la contraseña de tu mamá para comprar monedas.',
                       'Situación 4: un compañero te pide que le pases la tarea por mensaje para copiarla.',
                       'Situación 5: ves que en un grupo se burlan de alguien de tu salón.',
                       'Inventen en duplas una situación nueva para el grupo.'],
                logro=['Elegiste tu color en cada situación y explicaste al menos una con argumentos.']), xp=50),
        ]},
        {'nombre': '¿Real o inventado?', 'cofre': 35, 'misiones': [
            mision('Detecta lo falso', 'cuestionario', leccion(
                intro='En internet circulan noticias falsas, fotos editadas e imágenes hechas con IA. Un buen detective '
                      'no se cree todo: verifica.',
                saber=['Revisa la fuente: ¿quién lo publica? ¿Es un medio o una institución confiable?',
                       'Revisa la fecha: a veces circulan noticias viejas como si fueran nuevas.',
                       'Búscalo en otras fuentes confiables: si nadie más lo dice, desconfía.',
                       'Desconfía de títulos en MAYÚSCULAS, con muchos signos o que te piden reenviarlo «urgente».',
                       'Recuerda: la IA puede inventar datos y fabricar imágenes que parecen reales.',
                       'Primero haces inferencias («probablemente es falso porque…») y solo con pruebas llegas a una '
                       'conclusión.']), xp=60, preguntas=[
                ('Ves una noticia increíble. ¿Qué haces primero?', 'Reviso quién la publica y la busco en otras fuentes',
                 ['La reenvío rápido', 'Le creo porque tiene foto', 'La comento sin leerla']),
                ('¿Qué es una señal de noticia falsa?', 'Un título en mayúsculas que pide reenviarlo urgente',
                 ['Que tenga fecha', 'Que diga su fuente', 'Que otras fuentes la publiquen']),
                ('¿Por qué hay que revisar la fecha?', 'Porque circulan noticias viejas como si fueran nuevas',
                 ['Porque las noticias caducan', 'Para saber el clima', 'No hace falta revisarla']),
                ('Una imagen de un animal rarísimo se ve muy real. ¿Qué piensas?', 'Puede estar hecha con IA o editada',
                 ['Seguro es real', 'Las fotos nunca mienten', 'Si es bonita es verdad']),
                ('«Probablemente es falso porque ninguna otra fuente lo dice» es…', 'Una inferencia',
                 ['Una conclusión comprobada', 'Una pista', 'Un dato personal']),
            ]),
            mision('Verifica como detective', 'texto', leccion(
                intro='Pon a prueba tu radar. Algunas de estas frases son reales y otras son mitos famosos. Verifícalas.',
                saber=['1. Venus gira al revés que casi todos los planetas.',
                       '2. La Gran Muralla China se ve a simple vista desde la Luna.',
                       '3. Un día en Júpiter dura casi 10 horas.',
                       '4. El agua de lluvia filtrada con arena ya se puede beber.',
                       '5. Leonardo da Vinci construyó un avión que voló en el año 1500.',
                       '6. El polvo del Sahara puede llegar hasta el Caribe.'],
                dinamica=PAREJAS,
                pasos=['Para cada frase escribe primero tu inferencia: ¿real o falsa? ¿Por qué lo crees?',
                       'Verifícala con lo que aprendiste este año o búscala en Kiddle.',
                       'Escribe tu conclusión: REAL o FALSA, y la prueba o fuente que la respalda.'],
                logro=['Las 6 frases tienen inferencia, conclusión y prueba o fuente.'],
                entrega='escribe tus 6 verificaciones aquí abajo.'), xp=70, monedas=20, link=KIDDLE),
        ]},
        {'nombre': 'Mi año en TIC', 'cofre': 40, 'misiones': [
            mision('Portafolio del año', 'evidencia', leccion(
                intro='Un portafolio reúne tus mejores trabajos para mostrar de qué eres capaz. Te servirá para '
                      'presumir lo que aprendiste y para empezar 6.º con todo.',
                saber=['Busca tus capturas en tu carpeta del año: ahí está todo tu trabajo.',
                       'Una diapositiva por proyecto: título, una imagen y 2 renglones de lo que aprendiste.',
                       'Diseño: el mismo tema en todas las diapositivas, letra grande y poco texto.'],
                dinamica=PAREJAS,
                pasos=['Abre una presentación nueva: Portafolio_TuNombre.',
                       'Portada: tu nombre (sin apellidos si se va a publicar), «TIC 5.º» y una imagen tuya de AutoDraw.',
                       'Una diapositiva para cada uno de estos: gráfica de los planetas, historia de ciencia ficción, '
                       'ficha del invento, rompecabezas del Hubble, escape room, inspirómetro, captador de lluvia, alarma '
                       'de Sombra Veloz y entrenador de soplido.',
                       'Diapositiva final: «Lo que más me gustó» y «Mi meta para 6.º».',
                       'Revisa la ortografía y pide a tu dupla que la vea.'],
                logro=['Tu portafolio tiene portada, al menos 6 proyectos con imagen y la diapositiva final.'],
                entrega='sube tu portafolio en PDF o capturas de 3 diapositivas.'), xp=120, monedas=40),
            mision('Expo de portafolios', 'presencial', leccion(
                intro='El último día de laboratorio: cada quien presenta su mejor proyecto del año.',
                dinamica=['Por turnos, 1 minuto cada quien, con su portafolio proyectado.',
                          'El público escucha con el semáforo en 🔴. Se aplaude al terminar cada presentación.'],
                pasos=['Muestra tu proyecto favorito del año.',
                       'Explica qué aprendiste y qué fue lo más difícil.',
                       'Comparte tu meta para 6.º.'],
                logro=['Presentaste tu proyecto favorito en 1 minuto y escuchaste a tus compañeros con respeto.']),
                xp=60),
            jefe('Jefe final: El Virus Maestro', leccion(
                intro='El Virus Maestro se metió en la Ciudad Conectada y quiere borrar todo lo que aprendiste este año. '
                      'Este es el examen final: demuestra que eres un ciudadano digital de verdad.'), [
                ('¿Qué es la rotación de un planeta?', 'Su giro sobre sí mismo', ['Su vuelta al Sol', 'Su tamaño',
                                                                                    'Su color']),
                ('¿Cuáles son los 3 ingredientes de un prompt claro?', 'Qué quiero, detalles y lo que no debe hacer',
                 ['Saludo, pregunta y despedida', 'Nombre, edad y escuela', 'Mayúsculas, emojis y signos']),
                ('«Tal vez llovió anoche» es…', 'Una inferencia', ['Una conclusión', 'Una pista', 'Un hecho']),
                ('En Scratch, ¿qué bloque guarda lo que escribió el jugador?', 'respuesta',
                 ['cronómetro', 'puntos', 'disfraz']),
                ('¿Qué forma de Tinkercad ya viene hueca?', 'El tubo', ['La caja', 'La esfera', 'El cilindro']),
                ('¿Cuántos litros junta 1 mm de lluvia sobre 1 m² de techo?', '1 litro', ['10 litros', '100 litros',
                                                                                       'Medio litro']),
                ('Con la micro:bit, ¿cómo se cierra un circuito?', 'Uniendo un pin con GND',
                 ['Presionando el botón A', 'Agitándola', 'Desconectando el USB']),
                ('En un diagrama de flujo, una decisión va en…', 'Un rombo', ['Un óvalo', 'Un rectángulo',
                                                                              'Un círculo']),
                ('¿Cuál es la contraseña más fuerte?', 'Rio-Nube-Tenis-58', ['123456', 'firulais2015', 'qwerty']),
                ('Ves que se burlan de un compañero en un grupo. ¿Qué haces?', 'No lo reenvío, lo apoyo y aviso a un '
                 'adulto', ['Le doy me gusta', 'Lo reenvío', 'Escribo algo burlón']),
            ], xp=200, monedas=60),
        ]},
    ],
}
