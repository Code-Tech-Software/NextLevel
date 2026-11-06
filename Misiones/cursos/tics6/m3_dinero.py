"""Mundo 3 · ES-DAT314 Mini-historia del dinero: del trueque al dinero digital, investigación con fuentes confiables,
procesador de textos avanzado (estilos, imágenes, notas al pie, índice) trabajado en dupla en la nube y una hoja de
cálculo con precios en granos de cacao."""
from .base import KIDDLE, clasifica, jefe, leccion, mision

JUEGOS = {
    'clasifica_eras_dinero': clasifica('La línea del tiempo del dinero', '⏳', '¿En qué época va cada forma de pagar?', [
        ('Antes de las monedas', '🫘', ['Cambiar una gallina por maíz (trueque)', 'Pagar con granos de cacao',
                                        'Pagar con mantas de algodón', 'Usar conchas cauri como dinero',
                                        'Recibir sal como parte del pago']),
        ('Monedas y billetes', '🪙', ['Las primeras monedas de Lidia, hechas de electro',
                                      'El papel moneda de la antigua China', 'El real de a ocho de plata',
                                      'Un billete de 500 pesos', 'Una moneda de 10 pesos']),
        ('Dinero digital', '💳', ['Pagar con tarjeta de débito', 'Una transferencia desde el celular',
                                  'Pagar escaneando un código QR', 'Las criptomonedas',
                                  'Comprar una skin con saldo de una tarjeta de regalo']),
    ], rondas=14),
    'clasifica_fuentes': clasifica('¿Fuente confiable o dudosa?', '🔎', 'Un buen investigador revisa de dónde viene la '
                                   'información.', [
        ('Confiable', '✅', ['La página del Banco de México', 'Un museo de economía', 'Una enciclopedia con autores',
                             'Un libro de historia de la biblioteca', 'Un artículo con autor, fecha y fuentes',
                             'La página de una universidad']),
        ('Dudosa', '⚠️', ['Un video sin autor ni fecha', 'Una página llena de anuncios y ventanas',
                          'Un comentario en redes sociales', 'Un blog que no dice de dónde sacó los datos',
                          'Un mensaje reenviado muchas veces', 'Una página que promete hacerte rico rápido']),
    ], rondas=12),
    'atajos_editor': {'nombre': 'Atajos ninja del editor', 'icono': '🥷', 'plantilla': 'atajos', 'en_arcade': True,
                      'descripcion': 'Copiar, pegar, cortar, deshacer y rehacer sin tocar el mouse.',
                      'configuracion': {'atajos': ['copiar', 'pegar', 'cortar', 'deshacer', 'rehacer', 'todo'],
                                        'rondas': 12, 'modo': 'ninja'}},
}

MUNDO = {
    'nombre': 'La Ruta del Dinero', 'tema': 'desierto',
    'descripcion': 'ES-DAT314 · Mini-historia del dinero. ¿Qué tienen en común el cacao, la sal y las conchas cauri? '
                   'Investiga cómo se inventó el dinero y escribe con tu dupla, en un documento compartido en la nube, '
                   'una mini-historia con estilos, imágenes, notas al pie e índice automático. Pregunta guía: ¿cómo se '
                   'inventó el dinero?',
    'niveles': [
        {'nombre': 'Antes del dinero', 'cofre': 25, 'misiones': [
            mision('¿Cómo se inventó el dinero?', 'texto', leccion(
                intro='Hace miles de años, en todo el mundo, la gente tenía el mismo problema: ¿cómo conseguir lo que '
                      'necesitaba de forma práctica? Cada pueblo encontró su respuesta con lo que tenía alrededor: '
                      'cacao, sal, conchas, telas, metales…',
                pasos=['Si mañana desapareciera el dinero, ¿cómo conseguirías tu comida? Explica.',
                       '¿Por qué crees que el cacao o la sal servían para pagar?',
                       '¿Qué forma de pago usa tu familia más seguido: efectivo, tarjeta o celular?'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('Mercado de trueque', 'presencial', leccion(
                intro='Vas a vivir en carne propia por qué se inventó el dinero.',
                material=['Una tarjeta por alumno con lo que TIENE y lo que NECESITA (las prepara el profe)',
                          'Fichas o semillas que harán de «cacao»'],
                dinamica=['Ronda 1 (4 minutos): solo trueque. Se camina, no se corre; se habla en voz baja.',
                          'Ronda 2 (4 minutos): el profe reparte 10 granos de cacao por persona y ya se puede pagar con '
                          'cacao.',
                          'Señal «¡congelados!»: todos se detienen donde están y escuchan.'],
                pasos=['Ronda 1: consigue lo que necesitas cambiando lo que tienes. Solo vale cambiar cosa por cosa.',
                       'Anota si lo lograste y cuántas personas tuviste que buscar.',
                       'Ronda 2: ahora puedes vender lo tuyo por cacao y comprar con cacao.',
                       'Comparen en grupo: ¿en qué ronda fue más fácil? ¿Por qué?'],
                logro=['Explicas con tus palabras el problema del trueque: necesitas encontrar a alguien que tenga lo '
                       'que quieres Y quiera lo que tú tienes.']), xp=50),
            mision('Del trueque al cacao', 'cuestionario', leccion(
                intro='El trueque funcionaba… hasta que no. Repasa por qué las personas inventaron el dinero.',
                saber=['Trueque: cambiar una cosa por otra sin usar dinero.',
                       'Problema 1: necesitas que el otro quiera justo lo que tú ofreces (la «doble coincidencia»).',
                       'Problema 2: muchas cosas no se pueden dividir (¿media vaca?) ni guardar mucho tiempo (la fruta '
                       'se pudre).',
                       'Dinero mercancía: objetos que todos aceptaban porque tenían valor: cacao y mantas de algodón '
                       'entre los mexicas y los mayas, sal en el mundo romano, conchas cauri en África y Asia.',
                       'La palabra «salario» viene del latín salarium, relacionada con la sal.']), xp=60, preguntas=[
                ('¿Qué es el trueque?', 'Cambiar una cosa por otra sin usar dinero',
                 ['Pagar con tarjeta', 'Pedir prestado al banco', 'Ahorrar en una alcancía']),
                ('¿Cuál es el gran problema del trueque?',
                 'Hay que encontrar a alguien que quiera justo lo que tú ofreces', ['Que todo es gratis',
                                                                                    'Que no existían las cosas',
                                                                                    'Que no había mercados']),
                ('¿Qué usaban los mexicas y los mayas como dinero?', 'Granos de cacao y mantas de algodón',
                 ['Monedas de oro con la cara del rey', 'Tarjetas de crédito', 'Billetes de papel']),
                ('¿De dónde viene la palabra «salario»?', 'Del latín salarium, relacionada con la sal',
                 ['Del inglés «salary»', 'De la palabra «salir»', 'De una marca de bancos']),
                ('¿Por qué una vaca no era buen dinero?', 'Porque no se puede dividir para pagar cosas pequeñas',
                 ['Porque no tenía valor', 'Porque nadie comía carne', 'Porque era ilegal']),
                ('¿Qué son las conchas cauri?', 'Conchas de mar usadas como dinero en África y Asia',
                 ['Un tipo de billete', 'Una moneda mexicana', 'Una tarjeta de banco']),
            ]),
        ]},
        {'nombre': 'Monedas que cambiaron el mundo', 'cofre': 30, 'misiones': [
            mision('De la concha a la pantalla', 'cuestionario', leccion(
                intro='El dinero cambió de forma muchas veces. Cada cambio resolvió un problema del anterior.',
                saber=['Primeras monedas: en Lidia (hoy Turquía), hace unos 2,600 años, hechas de electro (una mezcla '
                       'natural de oro y plata). Eran fáciles de contar y de cargar.',
                       'Papel moneda: en China, hace unos mil años. Cargar miles de monedas de metal pesaba demasiado.',
                       'Real de a ocho: moneda de plata acuñada en la Casa de Moneda de México (fundada en 1535, la '
                       'primera de América). Circuló por Europa, Asia y Estados Unidos.',
                       'Dinero digital: tarjetas, transferencias, pagos con el celular y códigos QR. Hoy gran parte '
                       'del dinero solo existe como números en una computadora.']), xp=60, preguntas=[
                ('¿Dónde se hicieron las primeras monedas?', 'En Lidia, en la actual Turquía',
                 ['En México', 'En Japón', 'En Estados Unidos']),
                ('¿Por qué se inventó el papel moneda en China?', 'Porque cargar muchas monedas pesaba demasiado',
                 ['Porque no había metales', 'Porque el papel brilla', 'Porque lo pidió un banco extranjero']),
                ('¿Qué fue el real de a ocho?', 'Una moneda de plata hecha en México que circuló por el mundo',
                 ['Un billete chino', 'Una tarjeta de débito', 'Una concha de mar']),
                ('¿Cuál fue la primera Casa de Moneda de América?', 'La de México, fundada en 1535',
                 ['La de Nueva York', 'La de Lima en 1900', 'La de Madrid']),
                ('Hoy, ¿cómo existe gran parte del dinero?', 'Como números en computadoras de los bancos',
                 ['Como granos de cacao', 'Solo en monedas', 'En cofres enterrados']),
            ]),
            mision('La línea del tiempo del dinero', 'juego', leccion(
                intro='Ordena la historia: ¿esta forma de pagar es de antes de las monedas, de monedas y billetes o del '
                      'dinero digital?'), juego='clasifica_eras_dinero'),
            mision('Investiga como pro', 'texto', leccion(
                intro='Cada dupla investiga una parada de la ruta del dinero. Tu profe asigna el tema (varias duplas '
                      'pueden tener el mismo).',
                saber=['Temas: 1) Mexicas y mayas: cacao y mantas · 2) China: conchas cauri y papel moneda · 3) Lidia: '
                       'las primeras monedas · 4) Roma: la sal y los denarios · 5) Isla de Yap: las piedras rai gigantes '
                       '· 6) Nueva España: el real de a ocho · 7) Hoy: tarjetas, transferencias y criptomonedas.',
                       'Busca con palabras clave, no con preguntas largas: «piedras rai Yap dinero» funciona mejor que '
                       '«qué eran las piedras que usaban como dinero en una isla».',
                       'Confirma cada dato en 2 fuentes distintas.',
                       'Copia la dirección (URL) de cada página que uses: la necesitarás para citar.'],
                pasos=['Busca en Kiddle o en el buscador que indique tu profe.',
                       'Escribe 5 datos importantes de tu tema con tus propias palabras.',
                       'Escribe un dato curioso que sorprenda al lector.',
                       'Anota tus fuentes: nombre de la página, título del artículo y URL.'],
                logro=['Tus 5 datos están escritos con tus palabras y cada uno tiene su fuente.'],
                tip='Copiar y pegar párrafos completos no es investigar: lee, entiende y escribe con tus palabras.',
                entrega='escribe tus datos y tus fuentes aquí abajo.'), xp=70, link=KIDDLE),
            mision('¿Fuente confiable o dudosa?', 'juego', leccion(
                intro='Antes de usar un dato, revisa de dónde viene.',
                saber=['Señales de confianza: tiene autor o institución, fecha, fuentes y no te quiere vender nada.',
                       'Señales de alerta: sin autor, muchos anuncios, promete cosas increíbles o solo es una opinión.']),
                juego='clasifica_fuentes'),
        ]},
        {'nombre': 'Documento de nivel pro', 'cofre': 30, 'misiones': [
            mision('Estilos de título', 'evidencia', leccion(
                intro='Los profesionales no ponen los títulos «a mano» con negritas y tamaño: usan estilos. Así el '
                      'documento se ve parejo y después el índice se hace solo.',
                saber=['Un estilo es un formato guardado con nombre: Título, Título 1, Título 2, Normal…',
                       'Título 1: los temas grandes (El trueque). Título 2: los subtemas (El problema del trueque).',
                       'En Word: pestaña Inicio → grupo Estilos. En Google Docs: el menú que dice «Texto normal».',
                       'En algunos programas los estilos se llaman Encabezado 1, Encabezado 2.',
                       'Si cambias el diseño de un estilo, cambian todos los títulos que lo usan al mismo tiempo.'],
                pasos=['Abre un documento nuevo: Historia_Dinero_TuNombre.',
                       'Escribe el título del documento y aplícale el estilo Título.',
                       'Escribe 3 títulos de tu tema y aplícales Título 1.',
                       'Debajo de uno de ellos, escribe 2 subtítulos con Título 2.',
                       'Escribe un párrafo corto debajo de cada título.',
                       'Abre el panel de navegación (Word: Vista → Panel de navegación; Google Docs: Ver → Mostrar '
                       'esquema) y mira cómo aparecen tus títulos.'],
                logro=['Tus títulos usan estilos y aparecen en el panel de navegación.'],
                entrega='sube una captura con el panel de navegación abierto.'), xp=90, monedas=25),
            mision('Imágenes con pie de foto', 'evidencia', leccion(
                intro='Una imagen sin explicación confunde. Agrega imágenes como en un libro de historia: acomodadas y '
                      'con pie de foto.',
                saber=['Ajuste de texto: decide cómo se acomoda el texto alrededor de la imagen. «Cuadrado» deja el '
                       'texto a un lado; «En línea con el texto» la trata como una letra más.',
                       'Pie de foto: una línea debajo de la imagen que dice qué es y de dónde salió.',
                       'Las imágenes tienen autor: escribe la fuente en el pie de foto.'],
                pasos=['Inserta una imagen de tu tema (Insertar → Imágenes).',
                       'Cámbiale el tamaño desde una esquina para que no se deforme.',
                       'Clic en la imagen → Ajustar texto → Cuadrado. Muévela a la derecha del párrafo.',
                       'Agrega el pie de foto (Word: clic derecho → Insertar título; Google Docs: escribe una línea '
                       'debajo en tamaño 9 y cursiva).',
                       'Escribe en el pie qué es y la fuente. Ejemplo: «Piedra rai en la isla de Yap. Fuente: …».'],
                logro=['La imagen está al lado del texto, sin deformarse, y su pie de foto dice qué es y de dónde salió.'],
                entrega='sube una captura de tu documento.'), xp=90, monedas=25),
            mision('Notas al pie y fuentes', 'evidencia', leccion(
                intro='Los historiadores dicen de dónde sacaron cada dato. Tú también.',
                saber=['Nota al pie: un numerito en el texto que lleva a una aclaración al final de la página.',
                       'Word: Referencias → Insertar nota al pie. Google Docs: Insertar → Nota al pie (Ctrl + Alt + F).',
                       'Al final del documento va la sección «Fuentes» con cada página que usaste: sitio, título del '
                       'artículo, fecha en que lo consultaste y URL.'],
                pasos=['Elige un dato sorprendente de tu texto y agrégale una nota al pie que explique de dónde salió.',
                       'Agrega una segunda nota al pie que aclare una palabra difícil (por ejemplo, «electro»).',
                       'Al final escribe el título «Fuentes» con estilo Título 1.',
                       'Escribe tus fuentes en una lista con viñetas.'],
                logro=['Tu documento tiene 2 notas al pie numeradas y una sección de fuentes.'],
                entrega='sube una captura donde se vean las notas al pie.'), xp=90, monedas=25),
            mision('Atajos ninja del editor', 'juego', leccion(
                intro='Trabajar rápido en el editor es usar el teclado. Resuelve cada situación con el atajo correcto.',
                saber=['Ctrl + C copia, Ctrl + V pega, Ctrl + X corta, Ctrl + Z deshace y Ctrl + Y rehace.',
                       'Primero se selecciona y luego se usa el atajo.']), juego='atajos_editor'),
        ]},
        {'nombre': 'Edición en dupla', 'cofre': 35, 'misiones': [
            mision('El documento compartido', 'presencial', leccion(
                intro='En el trabajo real, varias personas escriben el mismo documento al mismo tiempo desde distintas '
                      'computadoras. Hoy lo arman tú y tu dupla en la nube, cada quien desde su computadora.',
                saber=['Documento en la nube: se guarda en internet (Google Drive u OneDrive) y todos ven los cambios al '
                       'instante.',
                       'Al compartir eliges el permiso: Editor (puede cambiar todo), Comentarista (solo comenta) o '
                       'Lector (solo ve).',
                       'Se comparte solo con el correo de tu dupla y el de tu profe, nunca «con cualquier persona que '
                       'tenga el enlace».'],
                roles=['Editor/a en jefe: crea el documento, lo comparte y arma la estructura de títulos.',
                       'Diseñador/a: cuida que las imágenes y los estilos se vean iguales en todo el documento.',
                       'Los dos son redactores: uno escribe trueque, mercancías y monedas; el otro billetes, dinero '
                       'digital y la parte de su investigación.'],
                pasos=['El editor en jefe crea «La ruta del dinero – Dupla X» y lo comparte como Editor con su dupla.',
                       'El editor en jefe escribe los Título 1 de cada sección para que nadie se encime.',
                       'Cada quien escribe SOLO en sus secciones.',
                       'Regla de oro: nunca borres el texto del otro; si algo está mal, comenta.'],
                logro=['Los dos escriben en el mismo documento y cada sección tiene dueño.']), xp=50),
            mision('Comentarios y sugerencias', 'evidencia', leccion(
                intro='Revisar el trabajo de otro sin pisarlo es una habilidad profesional. Para eso existen los '
                      'comentarios y el modo sugerencia.',
                saber=['Comentario: una nota al margen. Word: Revisar → Nuevo comentario. Google Docs: Insertar → '
                       'Comentario (Ctrl + Alt + M).',
                       'Modo sugerencia: lo que escribes aparece de otro color y el dueño decide si lo acepta. Word: '
                       'Revisar → Control de cambios. Google Docs: el lápiz de arriba a la derecha → Sugerencias.',
                       'Historial de versiones: guarda cada cambio. Si alguien borra algo, se puede recuperar (Archivo → '
                       'Historial de versiones).',
                       'Un buen comentario es concreto y amable: «Aquí falta la fecha de las primeras monedas».'],
                pasos=['Lee la sección de un compañero.',
                       'Deja 2 comentarios útiles.',
                       'Activa el modo sugerencia y corrige un error de ortografía de otra sección.',
                       'Revisa los comentarios que te dejaron en tu sección y resuélvelos (Resolver).',
                       'Abre el historial de versiones y busca quién escribió el primer párrafo.'],
                logro=['Dejaste 2 comentarios, hiciste una sugerencia y resolviste los comentarios que te dejaron.'],
                entrega='sube una captura donde se vean tus comentarios o sugerencias.'), xp=90, monedas=25),
            mision('Precios en granos de cacao', 'evidencia', leccion(
                intro='Una lista de precios de Tlaxcala del año 1545 dice cuánto costaban las cosas en granos de cacao. '
                      'Con una hoja de cálculo vas a hacer las cuentas como mercader.',
                saber=['Precios de 1545: una guajolota = 100 granos · un guajolote = 200 · un conejo de monte = 100 · un '
                       'conejo pequeño = 30 · un huevo de guajolota = 3 · un aguacate recién cortado = 3 · un jitomate '
                       'grande = 1.',
                       'Fórmula de multiplicar: =B2*C2 (el asterisco es «por»).',
                       '=SUMA(D2:D8) suma toda la columna de totales.',
                       'Arrastra el cuadrito de la esquina de una celda para copiar la fórmula hacia abajo.'],
                pasos=['Abre una hoja de cálculo nueva: Cacao_TuNombre.',
                       'Columnas: A Producto · B Precio en granos · C Cantidad · D Total.',
                       'Escribe los 7 productos con su precio y una cantidad para tu «lista del mercado».',
                       'En D2 escribe =B2*C2 y arrástrala hasta D8.',
                       'Debajo calcula el gasto total con =SUMA(D2:D8).',
                       'Reto: si tienes 1000 granos, ¿cuántos guajolotes puedes comprar? Calcúlalo con una fórmula.'],
                logro=['Los totales se calculan con fórmulas y el gasto total cambia solo si cambias una cantidad.'],
                entrega='sube una captura de tu hoja de cálculo con las fórmulas.'), xp=90, monedas=25),
            mision('Índice, encabezado y PDF', 'evidencia', leccion(
                intro='Último paso: que el documento parezca publicado de verdad.',
                saber=['Índice automático: se arma con los estilos de título. Word: Referencias → Tabla de contenido. '
                       'Google Docs: Insertar → Índice.',
                       'Si cambias un título, actualiza el índice (Word: Actualizar tabla; Google Docs: botón de '
                       'actualizar).',
                       'Encabezado: el texto de arriba que se repite en todas las páginas. Pie de página: el de abajo.',
                       'PDF: un formato que se ve igual en cualquier computadora y no se desacomoda.'],
                pasos=['Crea una portada: título, nombres de la dupla, grupo y una imagen.',
                       'Después de la portada, inserta el índice automático.',
                       'Agrega en el encabezado el nombre de la dupla y en el pie el número de página.',
                       'Revisa la ortografía (F7 en Word; Herramientas → Ortografía en Google Docs).',
                       'Descárgalo en PDF (Word: Archivo → Guardar como → PDF; Google Docs: Archivo → Descargar → PDF).'],
                logro=['El documento tiene portada, índice automático, encabezado, números de página y está en PDF.'],
                entrega='sube el PDF o una captura de la portada y el índice.'), xp=110, monedas=30),
        ]},
        {'nombre': 'Cierre de edición', 'cofre': 40, 'misiones': [
            mision('Revisión entre duplas', 'presencial', leccion(
                intro='Antes de publicar, otra dupla revisa su documento con una lista de cotejo.',
                dinamica=['Cada dupla comparte el enlace de su documento con otra dupla como Comentarista (el profe dice '
                          'con cuál). Nadie se mueve de su lugar.',
                          '10 minutos de revisión en silencio y 3 minutos para explicar lo que encontraron.'],
                pasos=['Revisen: ¿tiene portada, índice automático, estilos, imágenes con pie de foto, notas al pie y '
                       'fuentes?',
                       '¿Los datos tienen sentido? ¿Hay faltas de ortografía?',
                       'Dejen 2 comentarios de algo que funciona y 2 de algo que se puede mejorar.',
                       'Cada dupla corrige su documento con los comentarios recibidos.'],
                logro=['Su revisión es concreta y su documento quedó corregido.']), xp=50),
            jefe('Jefe: La Inflación', leccion(
                intro='La Inflación hace que todo cueste más y que el dinero valga menos. Derrótala demostrando que '
                      'conoces la historia del dinero y las herramientas de un documento profesional.'), [
                ('¿Cuál era el gran problema del trueque?', 'Encontrar a alguien que quisiera justo lo que ofrecías',
                 ['Que todo era muy barato', 'Que no había nada que cambiar', 'Que estaba prohibido']),
                ('¿Qué usaban los mexicas como dinero?', 'Granos de cacao y mantas de algodón',
                 ['Tarjetas de débito', 'Monedas de Lidia', 'Billetes chinos']),
                ('¿Dónde se hicieron las primeras monedas?', 'En Lidia, en la actual Turquía',
                 ['En la Casa de Moneda de México', 'En Roma', 'En la isla de Yap']),
                ('¿Para qué sirven los estilos de título en un documento?',
                 'Para dar formato parejo y crear el índice automático', ['Para cambiar el idioma',
                                                                         'Para borrar el texto', 'Para imprimir más rápido']),
                ('¿Qué herramienta deja tus cambios marcados para que el dueño los acepte?',
                 'El modo sugerencia o control de cambios', ['El corrector ortográfico', 'El zoom', 'La regla']),
                ('¿Qué es una nota al pie?', 'Una aclaración numerada al final de la página',
                 ['El número de página', 'El título del documento', 'Una imagen pequeña']),
                ('¿Qué fórmula multiplica el precio de B2 por la cantidad de C2?', '=B2*C2',
                 ['=B2+C2', 'B2xC2', '=SUMA(B2)']),
                ('¿Con qué permiso compartes el documento con tu dupla para que los dos escriban?', 'Editor',
                 ['Lector', 'Comentarista', 'Cualquier persona con el enlace']),
                ('¿Cuál es una señal de fuente confiable?', 'Tiene autor, fecha y dice de dónde saca sus datos',
                 ['Tiene muchos anuncios', 'Promete hacerte rico', 'Es un mensaje reenviado']),
            ]),
        ]},
    ],
}
