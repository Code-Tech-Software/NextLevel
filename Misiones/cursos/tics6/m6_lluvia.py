"""Mundo 6 · Rescatador de lluvia: el problema del agua (factores internos y externos), cómo funciona un sistema de
captación pluvial, soluciones que ya existen, diagnóstico de la escuela, cálculo de litros en hoja de cálculo, el
captador modelado en Tinkercad y una noticia redactada en el procesador de textos."""
from .base import TINKERCAD, clasifica, jefe, leccion, mision, tinkercad

PAREJAS_3D = ['Cada quien modela en su computadora; tu dupla revisa tus medidas al terminar cada paso, y tú las suyas.',
              'Meta del día escrita en el pizarrón: al final de la clase todos muestran su avance.',
              'Señal «manos arriba»: sueltan el mouse y miran al frente.']

JUEGOS = {
    'clasifica_factores_agua': clasifica('¿Factor interno o externo?', '💧', '¿El problema del agua viene de dentro de '
                                         'la escuela o de fuera?', [
        ('Interno (en la escuela)', '🏫', ['Una llave del baño que gotea todo el día', 'No hay cisterna para guardar agua',
                                           'Lavar el patio con manguera', 'Los tinacos no reciben mantenimiento',
                                           'Nadie revisa si hay fugas', 'El agua de lluvia del techo se va al drenaje']),
        ('Externo (fuera)', '🌎', ['Hay sequía y llueve menos que antes', 'Los pozos de la ciudad se están secando',
                                   'Las calles pavimentadas no dejan que el agua se filtre',
                                   'La red de tuberías de la ciudad tiene fugas',
                                   'Cada año vive más gente en la zona', 'La basura tapa las coladeras y hay inundaciones']),
    ], rondas=12),
    'clasifica_captador': clasifica('El viaje de la gota', '🌧️', 'Cada parte del captador hace un trabajo: captar, '
                                    'limpiar o guardar y usar.', [
        ('Captar', '🏠', ['El techo o la azotea donde cae la lluvia', 'La canaleta que recoge el agua del techo',
                          'El bajante: el tubo que lleva el agua hacia abajo', 'La inclinación del techo hacia la canaleta']),
        ('Limpiar', '🧽', ['La malla que detiene hojas y basura', 'El separador que desecha las primeras lluvias',
                           'Las capas de grava y arena', 'El carbón activado que quita olores']),
        ('Guardar y usar', '🛢️', ['La cisterna o el tanque con tapa', 'El rebosadero que saca el agua que sobra',
                                  'La llave para sacar el agua', 'Usar el agua para los baños y la limpieza']),
    ], rondas=12),
}

MUNDO = {
    'nombre': 'Operación Lluvia', 'tema': 'tormenta',
    'descripcion': 'Rescatador de lluvia. En 2024, una escuela del Estado de México pasó 6 meses sin agua, mientras a '
                   'unos kilómetros las lluvias provocaban inundaciones. Diagnostica tu escuela, calcula cuánta lluvia se '
                   'podría juntar, modela en 3D un captador con filtro y publica una noticia sobre cómo funciona. '
                   'Pregunta guía: ¿cómo podemos aprovechar mejor el agua de lluvia?',
    'niveles': [
        {'nombre': 'Alerta: agua', 'cofre': 25, 'misiones': [
            mision('Sin agua y con inundaciones', 'texto', leccion(
                intro='En abril de 2024, en una escuela de un municipio del Estado de México, se pidió a los padres '
                      'llevar una cubeta de agua limpia al dejar a sus hijos: la escuela llevaba 6 meses sin agua. En '
                      'junio, a unos kilómetros, las lluvias intensas provocaron inundaciones severas. Mucha agua en un '
                      'lugar y nada en otro.',
                pasos=['¿Cómo crees que se puede pasar de no tener agua a tener inundaciones en la misma región?',
                       '¿Qué pasaría en tu escuela si no hubiera agua una semana? Menciona 3 problemas.',
                       '¿A dónde se va el agua de lluvia que cae en el techo de tu escuela?'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('¿Por qué falta el agua?', 'cuestionario', leccion(
                intro='Un problema grande casi nunca tiene una sola causa. Hay factores internos (que dependen de la '
                      'escuela) y externos (que vienen de fuera).',
                saber=['Factores internos: fugas, llaves abiertas, falta de cisterna, falta de mantenimiento, desperdicio.',
                       'Factores externos: sequías, pozos que se secan por sacar más agua de la que entra, redes de '
                       'tubería con fugas, crecimiento de la población, lluvias cada vez más irregulares.',
                       'En las ciudades, el pavimento no deja que la lluvia se filtre al suelo: el agua se va al drenaje '
                       'y puede inundar las calles.',
                       'Captar la lluvia ataca los dos problemas: guarda agua para cuando falta y saca agua de las '
                       'calles cuando llueve fuerte.']), xp=60, preguntas=[
                ('¿Cuál es un factor interno de la falta de agua en una escuela?', 'Una llave que gotea todo el día',
                 ['Una sequía en el país', 'Que llueva menos', 'Que la ciudad crezca']),
                ('¿Cuál es un factor externo?', 'Los pozos de la ciudad se están secando',
                 ['Lavar el patio con manguera', 'No cerrar la llave', 'No revisar los tinacos']),
                ('¿Por qué las calles pavimentadas causan inundaciones?', 'Porque el agua no puede filtrarse al suelo',
                 ['Porque atraen la lluvia', 'Porque son de color gris', 'Porque calientan el agua']),
                ('¿Qué dos problemas ataca la captación de lluvia?',
                 'Guarda agua para cuando falta y reduce inundaciones', ['Hace que llueva más',
                                                                         'Limpia el aire y quita el calor',
                                                                         'Ninguno']),
                ('¿Por qué un problema grande suele tener varias causas?',
                 'Porque intervienen factores internos y externos', ['Porque nadie lo estudia',
                                                                    'Porque siempre es culpa de una persona',
                                                                    'No es cierto, siempre hay una sola causa']),
            ]),
            mision('¿Factor interno o externo?', 'juego', leccion(
                intro='Clasifica cada causa: ¿depende de la escuela o viene de fuera?'), juego='clasifica_factores_agua'),
            mision('Mis metas del proyecto', 'texto', leccion(
                intro='Antes de empezar un proyecto largo, los equipos profesionales escriben sus metas. Así saben si '
                      'lo lograron.',
                saber=['Una buena meta dice qué quieres lograr, cómo sabrás que lo lograste y para cuándo.',
                       'Meta vaga: «hacer un buen captador». Meta clara: «terminar el modelo 3D con filtro y tanque en 3 '
                       'clases».'],
                pasos=['¿Qué sabes ya de modelado 3D? ¿Qué te gustaría aprender?',
                       'Escribe 2 metas claras para este proyecto (una de 3D y una de trabajo en dupla o de conducta).',
                       'Para cada meta: ¿cómo sabrás que la cumpliste?'],
                entrega='escribe tus metas aquí abajo. Al final del mundo las vas a revisar.'), xp=50),
        ]},
        {'nombre': 'Cómo funciona un captador', 'cofre': 30, 'misiones': [
            mision('Anatomía de un captador', 'cuestionario', leccion(
                intro='Un sistema de captación de agua de lluvia lleva el agua del techo a un tanque, limpiándola en el '
                      'camino.',
                saber=['Superficie de captación: el techo o la azotea donde cae la lluvia.',
                       'Canaleta y bajante: recogen el agua del techo y la bajan.',
                       'Separador de primeras lluvias: desecha los primeros litros, que vienen sucios del polvo del techo.',
                       'Filtro: malla para hojas y capas de grava, arena y carbón activado.',
                       'Cisterna o tanque con tapa (para que no entren mosquitos), rebosadero para el agua que sobra y '
                       'llave para usarla.',
                       'El agua de lluvia captada sirve para baños, limpieza y riego. Para beberla necesita tratamiento '
                       'y análisis.']), xp=60, preguntas=[
                ('¿Para qué sirve el separador de primeras lluvias?', 'Para desechar el agua que viene sucia del techo',
                 ['Para hacer que llueva más', 'Para calentar el agua', 'Para medir la lluvia']),
                ('¿Qué parte detiene hojas y basura?', 'La malla del filtro', ['La llave', 'El rebosadero', 'La tapa']),
                ('¿Por qué el tanque debe tener tapa?', 'Para que no entren mosquitos ni basura',
                 ['Para que se vea bonito', 'Para que el agua se caliente', 'Para que pese más']),
                ('¿Qué hace el rebosadero?', 'Saca el agua que sobra cuando el tanque está lleno',
                 ['Filtra el agua', 'Recoge el agua del techo', 'Mide la temperatura']),
                ('¿Para qué se puede usar el agua de lluvia captada sin más tratamiento?', 'Para baños, limpieza y riego',
                 ['Para beberla directo', 'Para preparar biberones', 'Para cocinar sin hervir']),
            ]),
            mision('El viaje de la gota', 'juego', leccion(
                intro='Sigue a una gota desde el techo hasta la llave: ¿cada parte capta, limpia o guarda el agua?'),
                juego='clasifica_captador'),
            mision('Calculadora de lluvia', 'evidencia', leccion(
                intro='¿Cuánta agua podría juntar tu escuela? Hay una regla sencilla y una hoja de cálculo hace el resto.',
                saber=['Regla de oro: 1 milímetro de lluvia sobre 1 metro cuadrado de techo = 1 litro.',
                       'Litros = área del techo (m²) × lluvia (mm) × 0.8. El 0.8 es porque una parte del agua se pierde '
                       '(salpica o se evapora).',
                       'En la hoja de cálculo: =B2*C2*0.8',
                       'Un tinaco común guarda 1,100 litros; una cubeta, unos 19.'],
                pasos=['Abre una hoja de cálculo: Calculadora_Lluvia_TuNombre.',
                       'Columnas: A Mes · B Área del techo (m²) · C Lluvia del mes (mm) · D Litros · E Tinacos.',
                       'Escribe 4 meses de lluvia (tu profe da los datos de tu ciudad o usa: junio 150, julio 170, '
                       'agosto 160, septiembre 140) y el área que midan del techo (o 100 m²).',
                       'En D2: =B2*C2*0.8 · En E2: =D2/1100 · Arrastra las fórmulas hacia abajo.',
                       'Suma el total de litros con =SUMA(D2:D5) y haz una gráfica de barras por mes.'],
                logro=['Tu hoja calcula sola los litros y los tinacos de cada mes, y tiene gráfica.'],
                entrega='sube una captura de tu calculadora con la gráfica.'), xp=100, monedas=30),
            mision('Soluciones que ya existen', 'texto', leccion(
                intro='Antes de diseñar, investiga cómo se ha resuelto este problema en otros lugares y épocas.',
                saber=['Chultunes: los mayas excavaban cisternas en la roca de Yucatán para guardar el agua de lluvia '
                       'durante la temporada seca.',
                       'Isla Urbana: un proyecto mexicano que desde 2009 instala sistemas de captación de lluvia en '
                       'casas y escuelas.',
                       'Techos verdes y pozos de absorción: ayudan a que el agua se filtre en lugar de inundar.'],
                pasos=['Investiga 2 soluciones (pueden ser las de arriba u otras).',
                       'Para cada una: ¿dónde se usa?, ¿cómo funciona?, ¿qué tiene de bueno y qué limitación tiene?',
                       '¿Qué idea de esas soluciones podrías usar en tu captador?',
                       'Anota tus fuentes.'],
                logro=['Comparas 2 soluciones reales y tomas al menos una idea para tu diseño.'],
                entrega='escribe tu investigación aquí abajo.'), xp=70),
        ]},
        {'nombre': 'Diagnóstico', 'cofre': 30, 'misiones': [
            mision('Detectives del agua', 'presencial', leccion(
                intro='Un buen diseño empieza por conocer el lugar donde se va a instalar. Salen a diagnosticar la '
                      'escuela.',
                material=['Una cinta métrica o un metro', 'Una hoja de registro', 'El celular del profe para fotos'],
                roles=['Medidor/a: mide (o cuenta pasos: 1 paso ≈ 0.6 m).',
                       'Anotador/a: llena la hoja de registro y le dice al profe qué fotografiar.',
                       'En la segunda zona cambian de rol.'],
                dinamica=['Salen todos juntos en fila con el profe, cada quien junto a su dupla. Se habla en voz baja '
                          'fuera del salón.',
                          'Si no se puede salir, hagan el diagnóstico con fotos o el plano de la escuela.'],
                pasos=['Elijan un techo o una zona donde se podría captar la lluvia.',
                       'Midan su largo y ancho y calculen el área (largo × ancho).',
                       '¿Hacia dónde escurre el agua cuando llueve? ¿Hay canaletas? ¿Dónde se encharca?',
                       '¿Dónde cabría un tanque? ¿Hay sombra? ¿Quién lo cuidaría?',
                       'Regresen y pasen sus datos a la calculadora de lluvia.'],
                logro=['Tienen el área del techo, fotos y la ubicación propuesta para el tanque.']), xp=60),
            mision('¿Quién usará el captador?', 'texto', leccion(
                intro='Un diseño es bueno cuando funciona para quien lo va a usar. Piensa como diseñador.',
                pasos=['¿Quiénes usarían el agua? (conserjes, alumnos, maestros…)',
                       '¿Para qué la usarían? (baños, limpieza, regar el jardín…)',
                       'Escribe 3 necesidades del usuario: por ejemplo, «fácil de limpiar», «que los niños no puedan '
                       'abrirlo», «que no críe mosquitos».',
                       'Escribe 2 limitaciones: espacio, dinero, sol, peso del tanque…'],
                logro=['Tienes 3 necesidades y 2 limitaciones que tu diseño deberá respetar.'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
        ]},
        {'nombre': 'Modela el captador', 'cofre': 35, 'misiones': [
            tinkercad('Tanque y base', leccion(
                intro='Empieza por la pieza más importante: el tanque, hueco por dentro y con tapa.',
                dinamica=PAREJAS_3D,
                pasos=['Diseño nuevo en Tinkercad: Captador_TuNombre.',
                       'Base: caja de 120 × 120 × 6 mm.',
                       'Tanque: cilindro de 60 × 60 × 70 mm sobre la base (elévalo 6 mm).',
                       'Hueco: cilindro de 56 × 56 × 68 mm convertido en Hueco, centrado con Alinear y elevado 8 mm → '
                       'Agrupar con el tanque.',
                       'Tapa: cilindro de 64 × 64 × 4 mm de otro color, centrado arriba del tanque.',
                       'Llave: un cilindro de 6 mm acostado cerca del fondo del tanque y una cajita como manija.'],
                logro=['El tanque es hueco por dentro, tiene tapa y llave.'],
                entrega='sube una captura de tu tanque.'), xp=100, monedas=30),
            tinkercad('Techo, canaleta y bajante', leccion(
                intro='Ahora el camino del agua: el techo la junta, la canaleta la recoge y el bajante la lleva al tanque.',
                saber=['Canaleta: un tubo cortado a la mitad. Se hace con un cilindro hueco y una caja Hueco que le '
                       'quita la mitad de arriba.'],
                dinamica=PAREJAS_3D,
                pasos=['Techo: forma «Techo» de 100 × 60 × 30 mm sobre 4 columnas (cilindros de 4 mm y 60 mm de alto).',
                       'Canaleta: cilindro de 10 mm acostado, de 100 mm de largo; adentro un cilindro Hueco de 8 mm; '
                       'encima una caja Hueco que cubra la mitad de arriba → Agrupar.',
                       'Pon la canaleta pegada a la orilla baja del techo.',
                       'Bajante: cilindro de 8 mm vertical desde la punta de la canaleta hasta la tapa del tanque.',
                       'Gira la vista y revisa que el agua «pudiera» bajar sin huecos en el camino.'],
                logro=['El techo, la canaleta y el bajante forman un camino continuo hasta el tanque.'],
                entrega='sube una captura en perspectiva.'), xp=110, monedas=30),
            tinkercad('Diseña el filtro', leccion(
                intro='El filtro es el corazón del captador. Lo harás transparente para que se vean sus capas.',
                saber=['Capas de arriba hacia abajo: malla (detiene hojas) → grava (piedras) → arena → carbón activado '
                       '(quita olores y colores).',
                       'Truco de «Duplicar y repetir»: duplica una pieza (Ctrl + D), muévela y vuelve a presionar '
                       'Ctrl + D; Tinkercad repite el mismo movimiento. Así se hace una fila de agujeros en segundos.'],
                dinamica=PAREJAS_3D,
                pasos=['Contenedor: cilindro transparente de 30 × 30 × 40 mm entre el bajante y la tapa del tanque.',
                       'Capas: tres discos de 28 mm de diámetro y 8 mm de alto, uno sobre otro: gris (grava), amarillo '
                       '(arena) y negro (carbón).',
                       'Malla: un disco de 28 × 28 × 2 mm arriba de todo.',
                       'Agujeros de la malla: un cilindro Hueco de 3 mm; con Duplicar y repetir haz una fila de 5; '
                       'duplica la fila para hacer una cuadrícula → Agrupar con el disco.',
                       'Escribe con Texto el nombre de cada capa a un lado del filtro.'],
                logro=['Tu filtro es transparente y se ven sus 4 capas, con la malla llena de agujeros.'],
                entrega='sube una captura donde se vean las capas del filtro.'), xp=110, monedas=30),
            tinkercad('Mejora tu diseño', leccion(
                intro='Ningún diseño sale perfecto a la primera. Revisa las necesidades del usuario y mejóralo.',
                pasos=['Muestra tu modelo a tu dupla y pídele 2 sugerencias.',
                       'Agrega el rebosadero: un tubo pequeño acostado cerca de la parte alta del tanque.',
                       'Agrega el separador de primeras lluvias: un tubo vertical antes del filtro con una esfera adentro.',
                       'Haz al menos un cambio para cumplir una necesidad del usuario (candado, escalón, sombra…).',
                       'Escribe en el comentario qué cambiaste y por qué.'],
                logro=['Tu captador tiene rebosadero, separador y un cambio pensado en el usuario.'],
                entrega='sube una captura final y explica tus mejoras en el comentario.'), xp=100, monedas=30),
        ]},
        {'nombre': 'Reportaje del agua', 'cofre': 40, 'misiones': [
            mision('Redacta la noticia', 'evidencia', leccion(
                intro='Ahora eres periodista: escribe una noticia que explique cómo funciona tu captador y por qué la '
                      'escuela lo necesita.',
                saber=['Titular: corto y con verbo. Ejemplo: «Alumnos de 6.º diseñan un captador que podría juntar 12 '
                       'mil litros».',
                       'Entrada: el primer párrafo responde qué, quién, cuándo y dónde.',
                       'Cuerpo: explica cómo funciona y por qué es importante, de lo más importante a lo menos '
                       '(pirámide invertida).',
                       'Cita: lo que dijo alguien, entre comillas y con su nombre o cargo.',
                       'Foto con pie: una captura de tu modelo con una línea que explique qué se ve.'],
                pasos=['Abre un documento nuevo: Noticia_Lluvia_TuNombre.',
                       'Escribe el titular en grande y la entrada en negritas.',
                       'Escribe 3 párrafos: el problema, cómo funciona el captador y cuánta agua podría juntar (usa '
                       'tu calculadora).',
                       'Agrega una cita de un compañero o del conserje.',
                       'Inserta la captura de tu modelo con su pie de foto.',
                       'Pon el cuerpo de la noticia en 2 columnas para que parezca periódico.'],
                logro=['Tu noticia tiene titular, entrada, 3 párrafos con datos, una cita y una foto con pie.'],
                entrega='sube tu noticia en PDF o una captura.'), xp=110, monedas=30),
            mision('Galería del agua', 'presencial', leccion(
                intro='Presenta tu captador en 60 segundos, como en un concurso de innovación.',
                dinamica=['Cada dupla tiene 60 segundos exactos para presentar el mejor de sus dos captadores. Cuando '
                          'suena la alarma, se termina.',
                          'El público escucha en silencio y al final hace una sola pregunta por presentación.'],
                pasos=['Muestra tu modelo en el proyector.',
                       'Explica en orden: el problema, cómo funciona tu captador y cuántos litros podría juntar.',
                       'Responde la pregunta del público.',
                       'Revisa tus metas del inicio del mundo: ¿las cumpliste?'],
                logro=['Presentaste en 60 segundos con un dato de tu calculadora.']), xp=50),
            jefe('Jefe: La Gran Sequía', leccion(
                intro='La Gran Sequía secó los tinacos de la ciudad. Solo tu conocimiento puede traer el agua de vuelta.'), [
                ('¿Cuánta agua da 1 mm de lluvia sobre 1 m² de techo?', '1 litro',
                 ['10 litros', '1 mililitro', '100 litros']),
                ('¿Qué fórmula calcula los litros si el área está en B2 y la lluvia en C2?', '=B2*C2*0.8',
                 ['=B2+C2', '=SUMA(B2)', 'B2 por C2']),
                ('¿Cuál es un factor externo de la falta de agua?', 'Una sequía en la región',
                 ['Una llave que gotea en la escuela', 'No tener cisterna', 'Lavar el patio con manguera']),
                ('¿Qué parte del captador desecha el agua sucia de las primeras lluvias?', 'El separador',
                 ['El rebosadero', 'La llave', 'La tapa']),
                ('¿Para qué sirve el carbón activado en el filtro?', 'Para quitar olores y colores',
                 ['Para calentar el agua', 'Para detener hojas grandes', 'Para dar color']),
                ('En Tinkercad, ¿qué hace presionar otra vez Ctrl + D después de mover una copia?',
                 'Repite la copia con el mismo movimiento', ['Borra todo', 'Agrupa las piezas', 'Cambia el color']),
                ('¿Qué responde la entrada de una noticia?', 'Qué, quién, cuándo y dónde',
                 ['Solo el nombre del autor', 'El final de la historia', 'Una opinión personal']),
                ('¿Qué construían los mayas para guardar agua de lluvia?', 'Chultunes, cisternas excavadas en la roca',
                 ['Presas de concreto', 'Tinacos de plástico', 'Pozos de petróleo']),
            ]),
        ]},
    ],
}
