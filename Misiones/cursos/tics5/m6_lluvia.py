"""Mundo 6 · ES-DAT306 Rescatador de lluvia: la escuela sin agua y las inundaciones, cómo funciona un captador,
factores internos y externos, la entrevista al usuario, una calculadora de lluvia con fórmulas, el modelo 3D del
captador con su filtro de capas y una noticia que lo explica."""
from .base import KIDDLE, PAREJAS, clasifica, jefe, leccion, mision, tinkercad

PAREJAS_3D = ['Cada quien modela en su computadora. Todo el captador se arma en un solo diseño: Captador_TuNombre.',
              'Tu dupla revisa tu modelo al terminar cada paso, y tú el suyo.',
              'Semáforo de voz en 🟡. ¿Atorados? Primero entre los dos; después, mano arriba.']

JUEGOS = {
    'clasifica_usos_lluvia': clasifica('¿Para qué sirve el agua de lluvia?', '💧', 'El agua de lluvia con un filtro '
                                       'sencillo sirve para muchas cosas, pero no para todo. ¿Esta actividad se puede '
                                       'hacer con ella?', [
        ('Sirve con filtro sencillo', '🪣', ['Regar las plantas del jardín', 'El depósito del baño (WC)',
                                             'Lavar el patio', 'Trapear los pasillos', 'Lavar el coche',
                                             'Llenar una cubeta para limpiar']),
        ('Necesita potabilizarse', '🚱', ['Beberla', 'Cocinar una sopa', 'Lavarte los dientes',
                                          'Preparar agua de sabor', 'Lavar biberones', 'Hacer hielos']),
    ], rondas=12),
    'clasifica_factores': clasifica('¿Factor interno o externo?', '🏫', 'Un problema grande tiene muchas causas. '
                                    '¿Esta causa depende de la escuela o viene de fuera?', [
        ('Interno (la escuela)', '🏫', ['Una llave del baño que gotea todo el día', 'El tinaco de la escuela es pequeño',
                                        'Nadie revisa si hay fugas', 'Se riega el patio con manguera a mediodía',
                                        'No hay letreros para cuidar el agua', 'Las canaletas del techo están tapadas']),
        ('Externo (fuera de ella)', '🌎', ['En temporada de secas casi no llueve',
                                           'La ciudad reparte el agua por tandeo', 'Las presas están bajas',
                                           'Cada año vive más gente en el municipio',
                                           'Las tuberías de la ciudad tienen fugas',
                                           'Lluvias muy intensas que inundan las calles']),
    ], rondas=12),
}

MUNDO = {
    'nombre': 'Rescatadores de Lluvia', 'tema': 'tormenta',
    'descripcion': 'ES-DAT306 · Rescatador de lluvia. En abril de 2024, una escuela del Estado de México llevaba 6 '
                   'meses sin agua y los papás tenían que llevar cubetas. Dos meses después, muy cerca de ahí, las '
                   'lluvias intensas provocaron inundaciones. Investiga cómo funciona un captador de agua de lluvia, '
                   'diagnostica tu escuela, calcula cuánta agua se podría juntar y modela tu captador en 3D. Pregunta '
                   'guía: ¿cómo podemos aprovechar mejor el agua de lluvia?',
    'niveles': [
        {'nombre': 'Sin agua, con inundaciones', 'cofre': 25, 'misiones': [
            mision('La escuela sin agua', 'texto', leccion(
                intro='En abril de 2024, en una escuela de un municipio del Estado de México, se pidió a los papás que '
                      'al llevar a sus hijos llevaran también una cubeta con agua limpia: la escuela llevaba 6 meses sin '
                      'agua. En junio, a unos kilómetros de ahí, llovió tanto que hubo inundaciones graves.',
                pasos=['¿Cómo sería un día en tu escuela sin agua? Menciona 3 problemas.',
                       '¿Por qué crees que en el mismo lugar puede faltar agua y después sobrar?',
                       '¿Qué se te ocurre hacer con el agua que cae cuando llueve?'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('¿Qué recuerdo del 3D?', 'cuestionario', leccion(
                intro='Ya modelaste un inspirómetro. Antes de diseñar el captador, revisa qué tanto recuerdas.',
                saber=['Ejes: X izquierda-derecha, Y adelante-atrás, Z arriba-abajo.',
                       'Tubo: forma prediseñada hueca. Alinear: tecla L. Duplicar: Ctrl + D. Agrupar: Ctrl + G.',
                       'Hueco: convierte una forma en «molde» que, al agrupar, recorta a la otra.',
                       'Transparente: en el panel de color.']), xp=50, preguntas=[
                ('¿Qué eje es la altura?', 'Z', ['X', 'Y', 'Ninguno']),
                ('¿Qué hace Ctrl + G?', 'Agrupa las piezas seleccionadas', ['Las duplica', 'Las borra',
                                                                            'Las vuelve transparentes']),
                ('¿Qué hace la opción Hueco?', 'Convierte la forma en un molde que recorta al agrupar',
                 ['Pinta la pieza de negro', 'La hace más grande', 'La sube en el eje Z']),
                ('¿Qué tecla abre Alinear?', 'L', ['D', 'F', 'G']),
                ('¿Qué forma prediseñada ya viene hueca?', 'El tubo', ['La caja', 'La esfera', 'El techo']),
            ]),
            mision('Mis metas del proyecto', 'texto', leccion(
                intro='Los equipos profesionales escriben sus metas antes de empezar un proyecto largo. Así saben si lo '
                      'lograron.',
                saber=['Una buena meta dice QUÉ vas a lograr y CÓMO sabrás que lo lograste. Ejemplo: «Mi captador tendrá '
                       'filtro de 3 capas y lo explicaré en 1 minuto sin leer».'],
                pasos=['Escribe una meta sobre tu modelo 3D.',
                       'Escribe una meta sobre lo que vas a aprender del agua.',
                       'Escribe una meta sobre cómo vas a trabajar en clase (por ejemplo, con el semáforo de voz).'],
                entrega='escribe tus 3 metas aquí abajo.'), xp=50),
        ]},
        {'nombre': 'El camino de la lluvia', 'cofre': 30, 'misiones': [
            mision('Cómo funciona un captador', 'cuestionario', leccion(
                intro='Un sistema de captación de agua de lluvia lleva el agua del techo a un tanque y la limpia en el '
                      'camino.',
                saber=['1. Techo (área de captación): donde cae la lluvia.',
                       '2. Canaleta y bajante: tubos que juntan el agua del techo y la bajan.',
                       '3. Separador de primeras lluvias: aparta el agua de los primeros minutos, que lava el polvo del '
                       'techo.',
                       '4. Filtro: quita hojas, tierra y basura (malla, grava, arena, carbón).',
                       '5. Tanque o tinaco: guarda el agua tapada, sin luz, para que no crezcan algas ni mosquitos.',
                       'Regla de oro: 1 mm de lluvia sobre 1 m² de techo = 1 litro de agua.',
                       'Con filtro sencillo sirve para riego, baños y limpieza. Para beberla necesita potabilizarse.']),
                xp=60, preguntas=[
                ('¿Dónde cae la lluvia que se va a captar?', 'En el techo', ['En el tinaco', 'En el filtro',
                                                                            'En la llave']),
                ('¿Para qué sirve el separador de primeras lluvias?', 'Para apartar el agua que lava el polvo del techo',
                 ['Para calentar el agua', 'Para que llueva más', 'Para pintar el techo']),
                ('¿Qué quita el filtro?', 'Hojas, tierra y basura', ['La sal del mar', 'El color del cielo',
                                                                    'La lluvia']),
                ('¿Por qué el tanque debe estar tapado y sin luz?', 'Para que no crezcan algas ni mosquitos',
                 ['Para que el agua se enfríe', 'Para que pese menos', 'Para que se vea bonito']),
                ('Si caen 10 mm de lluvia sobre 1 m² de techo, ¿cuántos litros se juntan?', '10 litros',
                 ['1 litro', '100 litros', '1000 litros']),
                ('¿Se puede beber el agua de lluvia con un filtro sencillo?', 'No, necesita potabilizarse',
                 ['Sí, siempre', 'Sí, si está fría', 'Solo si es de noche']),
            ]),
            mision('¿Para qué sirve el agua de lluvia?', 'juego', leccion(
                intro='Usar la tecnología de forma responsable también es saber sus límites. Clasifica cada uso.',
                tip='Todo lo que entra a tu boca necesita agua potable.'), juego='clasifica_usos_lluvia'),
            mision('¿Factor interno o externo?', 'juego', leccion(
                intro='La falta de agua en una escuela tiene causas de adentro y de afuera. Clasifícalas.',
                tip='Si la escuela lo puede arreglar por su cuenta, es interno.'), juego='clasifica_factores'),
            mision('Entrevista al usuario', 'texto', leccion(
                intro='Un diseño es bueno si funciona para quien lo va a usar. Entrevista a alguien que usaría el captador '
                      'en tu escuela o en tu casa: el conserje, una maestra, la directora o un familiar.',
                pasos=['Pregunta 1: ¿Para qué usaría el agua de lluvia?',
                       'Pregunta 2: ¿Dónde se podría poner el tanque sin estorbar?',
                       'Pregunta 3: ¿Quién lo limpiaría y cada cuánto?',
                       'Pregunta 4: ¿Qué le preocupa de tener un captador?',
                       'Escribe 3 necesidades del usuario que tu diseño debe cumplir.'],
                ojo=['Pide permiso antes de entrevistar y no escribas datos personales: solo su puesto (por ejemplo, '
                     '«el conserje»).'],
                logro=['Tienes 4 respuestas y 3 necesidades claras del usuario.'],
                entrega='escribe las respuestas y las 3 necesidades aquí abajo.'), xp=70, monedas=20),
        ]},
        {'nombre': 'Diagnóstico de la escuela', 'cofre': 30, 'misiones': [
            mision('Recorrido de diagnóstico', 'presencial', leccion(
                intro='Salen como ingenieros a diagnosticar dónde se podría instalar un captador en la escuela.',
                roles=['Medidor: cuenta los pasos para medir el largo y el ancho de un techo o una pared.',
                       'Cartógrafo: dibuja el croquis con los techos, los bajantes y dónde podría ir el tanque.'],
                dinamica=['En duplas y en fila detrás del profe. Nadie se separa del grupo ni se sube a ningún lado.',
                          'Semáforo en 🟡 durante el recorrido: hay otros grupos en clase.',
                          '15 minutos de recorrido y 10 de trabajo en el salón.'],
                pasos=['Recorran el patio y ubiquen los techos más grandes y por dónde baja el agua cuando llueve.',
                       'Midan con pasos un techo (o su pared más larga): 1 paso de un alumno de 5.º mide unos 0.5 m.',
                       'Dibujen el croquis y marquen con una X el mejor lugar para el tanque.',
                       'En el salón, calculen el área del techo: largo × ancho, en metros.'],
                logro=['Tienen un croquis con el techo medido, su área y el lugar del tanque.']), xp=50),
            mision('Calculadora de lluvia', 'evidencia', leccion(
                intro='¿Cuánta agua podría juntar tu escuela en un año? Una hoja de cálculo hace la cuenta por ti con una '
                      'fórmula.',
                saber=['Las fórmulas empiezan con =. Ejemplo: =B1*B2 multiplica lo que hay en B1 por lo que hay en B2.',
                       'Si cambias un dato, la fórmula se recalcula sola.',
                       'Regla de oro: litros = área del techo (m²) × lluvia del año (mm).',
                       'Ejemplo de lluvia: unos 700 mm al año, más o menos lo que llueve en la Ciudad de México.',
                       'Un tinaco común guarda 1,100 litros.'],
                dinamica=PAREJAS,
                pasos=['Abre una hoja de cálculo: Lluvia_TuNombre, en tu carpeta Lluvia.',
                       'A1 «Área del techo (m²)» y en B1 el área que calcularon en el recorrido.',
                       'A2 «Lluvia al año (mm)» y en B2 escribe 700.',
                       'A3 «Litros al año» y en B3 la fórmula =B1*B2.',
                       'A4 «Tinacos que se llenan» y en B4 la fórmula =B3/1100.',
                       'Experimenta: cambia el área del techo por el doble. ¿Qué pasa con los litros?'],
                logro=['Tu hoja calcula sola los litros y los tinacos, y cambia al modificar un dato.'],
                tip='Si sale #¡VALOR!, revisa que en B1 y B2 haya solo números, sin letras.',
                entrega='sube una captura de tu hoja y escribe cuántos tinacos se llenarían.'), xp=100, monedas=30),
            mision('Soluciones que ya existen', 'texto', leccion(
                intro='Antes de diseñar, los ingenieros investigan cómo se ha resuelto el problema en otros lugares.',
                saber=['Hace más de 2,000 años, los mayas guardaban agua de lluvia en depósitos bajo tierra llamados '
                       'chultunes.',
                       'En la Ciudad de México, el proyecto Isla Urbana ha instalado miles de captadores en casas y '
                       'escuelas.',
                       'Busca con Kiddle o con fuentes confiables y anota de dónde sacas cada dato.'],
                pasos=['Investiga una solución antigua y una actual para aprovechar la lluvia.',
                       'Escribe cómo funciona cada una en 2 renglones.',
                       '¿Qué idea de esas soluciones usarías en tu captador?',
                       'Anota tus fuentes.'],
                logro=['Explicas 2 soluciones, una idea para tu diseño y tus fuentes.'],
                entrega='escribe tu investigación aquí abajo.'), xp=60, link=KIDDLE),
        ]},
        {'nombre': 'Modela el captador', 'cofre': 35, 'misiones': [
            tinkercad('Base y tinaco', leccion(
                intro='Empieza por la pieza principal: el tinaco donde se guarda el agua.',
                saber=['El Tubo puesto sobre la base forma un tanque: la base le sirve de fondo.',
                       'Para que una pieza quede justo encima de otra, arrástrala sobre ella: Tinkercad la pone en su '
                       'superficie.'],
                dinamica=PAREJAS_3D,
                pasos=['Diseño nuevo: Captador_TuNombre.',
                       'Base: una caja de 120 × 80 × 5 mm, gris.',
                       'Tinaco: un Tubo con radio 20 y 50 mm de alto, sobre la base, del lado derecho.',
                       'Tapa: un cilindro de 40 × 40 × 3 mm encima del tinaco; céntralo con L.',
                       'Llave: un cilindro de 4 × 4 × 10 mm acostado, pegado abajo al frente del tinaco.',
                       'Pinta el tinaco de negro o azul oscuro: así no le entra luz.'],
                logro=['El tinaco está sobre la base, con su tapa centrada y su llave.'],
                entrega='sube una captura en perspectiva.')),
            tinkercad('Techo, canaleta y bajante', leccion(
                intro='Ahora el camino del agua: el techo la junta, la canaleta la recoge y el bajante la lleva hacia '
                      'abajo.',
                dinamica=PAREJAS_3D,
                pasos=['Edificio: una caja de 50 × 50 × 40 mm del lado izquierdo de la base.',
                       'Techo: la forma «Techo», de 50 × 50 mm, encima del edificio.',
                       'Canaleta: un Tubo con radio 4 y 50 mm de largo, acostado, justo debajo de la orilla del techo que '
                       'mira al tinaco.',
                       'Bajante: un Tubo con radio 3, vertical, que baje desde una punta de la canaleta.',
                       'Revisa desde varios ángulos que el agua tenga un camino continuo: techo → canaleta → bajante.'],
                logro=['Se ve el camino completo del agua desde el techo hasta abajo.'],
                entrega='sube una captura donde se vea el camino del agua.')),
            tinkercad('Filtro de 3 capas', leccion(
                intro='El filtro es el corazón del captador. Lo harás transparente para que se vean sus capas.',
                saber=['Malla (arriba): detiene hojas y basura grande.',
                       'Grava (piedritas): detiene la tierra.',
                       'Arena: detiene partículas finas.',
                       'Carbón: quita olores y colores.'],
                dinamica=PAREJAS_3D,
                pasos=['Contenedor: un Tubo con radio 10 y 35 mm de alto, transparente, entre el bajante y el tinaco.',
                       'Capas: 3 cilindros de 18 × 18 mm y 8 mm de alto, uno encima del otro dentro del contenedor: '
                       'carbón (negro) abajo, arena (amarillo) en medio y grava (gris) arriba.',
                       'Malla: un cilindro de 18 × 18 × 1 mm verde encima de la grava.',
                       'Centra todas las capas con el contenedor (selecciónalas → L → centra en X y Y).',
                       'Conecta el filtro con el tinaco con un Tubo delgado acostado.'],
                logro=['El filtro es transparente, se ven sus 4 capas en orden y está conectado al tinaco.'],
                entrega='sube una captura de cerca del filtro.')),
            tinkercad('Mejoras para el usuario', leccion(
                intro='Un diseño se mejora escuchando al usuario. Revisa tu entrevista y mejora tu captador.',
                pasos=['Relee las 3 necesidades de tu usuario.',
                       'Haz al menos 2 mejoras. Ideas: un separador de primeras lluvias (un tubo vertical con una esfera '
                       'adentro), un letrero «AGUA NO POTABLE» con la forma Texto, una escalera para limpiar el tinaco, '
                       'una tapa con candado o una base más alta.',
                       'Agrupa las piezas de cada parte para que no se muevan por accidente.',
                       'Toma 3 capturas: de frente, desde arriba y en perspectiva.'],
                logro=['Tu captador tiene 2 mejoras que responden a las necesidades de tu usuario.'],
                entrega='sube tus 3 capturas y escribe en el comentario qué mejoraste y por qué.'), xp=110,
                monedas=30),
        ]},
        {'nombre': 'Noticia del agua', 'cofre': 40, 'misiones': [
            mision('Redacta la noticia', 'evidencia', leccion(
                intro='Ahora eres periodista: escribe una noticia que explique cómo funciona tu captador y por qué le '
                      'serviría a tu escuela.',
                saber=['Una noticia responde 6 preguntas: qué, quién, cuándo, dónde, cómo y por qué.',
                       'Partes: titular (corto y llamativo), entrada (lo más importante en 2 renglones), cuerpo (los '
                       'detalles), una cita (lo que dijo alguien entre comillas) e imagen con pie de foto.',
                       'Se escribe en tercera persona: «Los alumnos de 5.º diseñaron…».'],
                dinamica=['20 minutos de escritura con el semáforo en 🔴.',
                          'Los últimos 5 minutos, tu dupla lee tu noticia y te dice si responde las 6 preguntas.'],
                pasos=['Abre un documento: Noticia_TuNombre.',
                       'Escribe el titular en letra grande y la entrada en negritas.',
                       'En el cuerpo explica el camino del agua y para qué se usaría. Incluye un dato de tu calculadora de '
                       'lluvia.',
                       'Agrega una cita de tu entrevista (sin nombres: «dijo el conserje de la escuela»).',
                       'Inserta una captura de tu captador con su pie de foto.'],
                logro=['Tu noticia responde las 6 preguntas y tiene titular, entrada, cita, dato e imagen.'],
                entrega='sube tu noticia en PDF o una captura.'), xp=100, monedas=30),
            mision('Noticiero de 1 minuto', 'presencial', leccion(
                intro='Presenta tu captador como reportero de noticiero: 1 minuto, sin leer todo.',
                dinamica=['Por turnos, al frente, con tu modelo proyectado. El profe cronometra.',
                          'El público escucha con el semáforo en 🔴 y al final puede hacer 1 pregunta.'],
                pasos=['Empieza con el titular de tu noticia.',
                       'Explica el camino del agua señalando tu modelo.',
                       'Di cuántos litros podría juntar la escuela.',
                       'Cierra con una frase para convencer al público.'],
                logro=['Explicaste tu captador en 1 minuto, con tu dato y sin leer.']), xp=50),
            jefe('Jefe: La Gran Inundación', leccion(
                intro='La Gran Inundación llega cada temporada de lluvias… y luego deja todo seco. Solo un rescatador '
                      'de lluvia que entienda el agua y el diseño 3D puede aprovecharla.'), [
                ('¿Qué parte del captador aparta el agua sucia de los primeros minutos?',
                 'El separador de primeras lluvias', ['El tinaco', 'La llave', 'El techo']),
                ('¿Cuántos litros junta 1 mm de lluvia sobre 1 m² de techo?', '1 litro', ['10 litros', '100 litros',
                                                                                       '1000 litros']),
                ('En una hoja de cálculo, ¿cómo empieza una fórmula?', 'Con =', ['Con #', 'Con una letra',
                                                                               'Con un espacio']),
                ('¿Qué hace la fórmula =B1*B2?', 'Multiplica B1 por B2', ['Suma B1 y B2', 'Borra B1 y B2',
                                                                          'Copia B1 en B2']),
                ('¿Qué capa del filtro quita olores y colores?', 'El carbón', ['La grava', 'La malla', 'El tinaco']),
                ('«La llave del baño gotea todo el día» es un factor…', 'Interno', ['Externo', 'Climático',
                                                                                   'Imposible de arreglar']),
                ('¿Para qué NO sirve el agua de lluvia con filtro sencillo?', 'Para beberla',
                 ['Para regar', 'Para el baño', 'Para lavar el patio']),
                ('¿Qué 6 preguntas responde una noticia?', 'Qué, quién, cuándo, dónde, cómo y por qué',
                 ['Solo qué y quién', 'Cuánto cuesta y quién paga', 'Ninguna, solo opina']),
            ]),
        ]},
    ],
}
