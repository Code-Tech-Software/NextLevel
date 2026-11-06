"""Mundo 4 · ES-SEA206 Secreto plantástico: lo que una planta necesita y una maceta 3D en Tinkercad que facilite
su cuidado (medidas, huecos, alinear, agrupar y texto 3D)."""
from .base import KIDDLE, clasifica, jefe, leccion, mision

JUEGOS = {
    'clasifica_partes': clasifica('¿Raíz, tallo u hoja?', '🌿', '¿Qué parte de la planta hace cada trabajo?', [
        ('Raíz', '🥕', ['Absorbe agua y minerales del suelo', 'Sujeta la planta a la tierra', 'Crece hacia abajo',
                       'La zanahoria es una de estas', 'Guarda alimento bajo tierra, como el camote']),
        ('Tallo', '🪵', ['Sostiene a la planta', 'Lleva el agua de la raíz a las hojas', 'En los árboles se llama tronco',
                        'El apio que comemos es uno de estos', 'Mantiene las hojas cerca de la luz']),
        ('Hoja', '🍃', ['Fabrica el alimento con la luz del sol', 'Tiene clorofila que la hace verde',
                       'Hace la fotosíntesis', 'Por aquí la planta suelta oxígeno', 'La lechuga que comemos es una de estas']),
    ], rondas=14),
    'clasifica_cuidados': clasifica('¿Ayuda o daña a Enriqueta?', '🪴', '¿Esto ayuda a que la planta crezca o la daña?', [
        ('Ayuda', '💚', ['Una maceta con agujeros de drenaje', 'Un plato debajo para el agua que sobra',
                        'Ponerla cerca de una ventana con luz', 'Tierra con abono', 'Regarla cuando la tierra está seca',
                        'Una maceta del tamaño adecuado', 'Quitarle las hojas secas']),
        ('Daña', '🥀', ['Una maceta sin agujeros', 'Regarla hasta que se encharque', 'Dejarla en un cuarto oscuro',
                       'Ponerla junto a un calentador', 'Una maceta muy pequeña para sus raíces',
                       'Olvidar regarla por semanas', 'Tierra dura que no deja pasar el agua']),
    ]),
}

MUNDO = {
    'nombre': 'Jardín Plantástico', 'tema': 'dulces',
    'descripcion': 'ES-SEA206 · Secreto plantástico. Enriqueta, la planta de la casa, no crece aunque le hablen '
                   'bonito. ¿Existe una fórmula mágica? Descubre lo que una planta necesita y diseña en 3D una maceta '
                   'inteligente que facilite su cuidado.',
    'niveles': [
        {'nombre': '¿Existe una fórmula mágica?', 'cofre': 25, 'misiones': [
            mision('El misterio de Enriqueta', 'texto', leccion(
                intro='«Intenté muchas veces hacer crecer una planta en casa, pero no lo logro. Mi mamá dice que no todos '
                      'tenemos ese poder especial. Le puse nombre a mi planta, Enriqueta, y le hablo bonito, pero sé '
                      'que no basta. Mi tío Pepe también cree que cuidar plantas es una habilidad especial.»\n\n'
                      'Pregunta del caso: ¿existe una fórmula mágica para hacer crecer las plantas?',
                pasos=['Escribe 5 cosas que crees que Enriqueta necesita para crecer.',
                       'Escribe tu hipótesis: ¿por qué crees que Enriqueta no crece?',
                       '¿Crees que existe una fórmula mágica? Explica por qué sí o por qué no.'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('Lo que una planta necesita', 'cuestionario', leccion(
                intro='Repasa la «fórmula» de las plantas y descubre qué le pasaba a Enriqueta.',
                saber=['Luz: las plantas fabrican su alimento con la luz del sol (fotosíntesis).',
                       'Agua: la justa. Si le falta, se seca; si le sobra y no puede salir, las raíces se pudren.',
                       'Aire: toman dióxido de carbono y sueltan oxígeno.',
                       'Suelo con nutrientes: la tierra con abono les da minerales.',
                       'Espacio: las raíces necesitan lugar para crecer.',
                       'La fórmula no es magia: luz + agua justa + aire + nutrientes + espacio.']), xp=60, preguntas=[
                ('¿Qué necesita una planta para fabricar su alimento?', 'Luz del sol',
                 ['Oscuridad total', 'Refresco', 'Música fuerte']),
                ('¿Qué les pasa a las raíces si la maceta se llena de agua que no puede salir?', 'Se pudren',
                 ['Crecen más rápido', 'Se vuelven flores', 'Nada']),
                ('¿Cómo se llama el proceso con el que las plantas fabrican su alimento?', 'Fotosíntesis',
                 ['Digestión', 'Evaporación', 'Respiración']),
                ('Durante la fotosíntesis, las plantas sueltan al aire…', 'Oxígeno', ['Humo', 'Plástico', 'Arena']),
                ('¿Para qué sirve el abono en la tierra?', 'Para darle nutrientes a la planta',
                 ['Para que no le dé luz', 'Para que pese más', 'Para pintarla']),
                ('¿Cuál es la «fórmula» para que Enriqueta crezca?', 'Luz, agua justa, aire, nutrientes y espacio',
                 ['Hablarle bonito y ya', 'Mucha agua todos los días', 'Guardarla en un cajón']),
            ]),
            mision('¿Raíz, tallo u hoja?', 'juego', leccion(
                intro='Cada parte de la planta tiene un trabajo. Clasifica cada tarjeta en la parte correcta.'),
                juego='clasifica_partes'),
            mision('Germinador: mi frijol mágico', 'evidencia', leccion(
                intro='Vas a ver crecer una planta desde la semilla. ¡Tu frijol será tu Enriqueta de laboratorio!',
                material=['Un vaso transparente', 'Algodón', '2 o 3 frijoles', 'Agua'],
                pasos=['Pon algodón húmedo dentro del vaso.',
                       'Coloca los frijoles pegados a la pared del vaso para poder verlos.',
                       'Déjalo cerca de una ventana y mantén el algodón húmedo (no encharcado).',
                       'Dibuja o fotografía tu germinador cada 2 días.'],
                entrega='sube una foto del primer día. ¡En las siguientes clases verás qué pasa!'), xp=80, monedas=20),
        ]},
        {'nombre': 'Científicos de plantas', 'cofre': 30, 'misiones': [
            mision('Experimento: luz contra oscuridad', 'evidencia', leccion(
                intro='¿De verdad la luz es tan importante? Compruébalo con dos germinadores gemelos.',
                saber='Para que el experimento sea justo, los dos germinadores deben tener lo mismo (agua, frijoles, '
                      'algodón). Solo cambia UNA cosa: la luz.',
                pasos=['Prepara dos germinadores iguales.',
                       'Pon uno junto a la ventana y el otro dentro de una caja cerrada o un cajón.',
                       'Escribe tu hipótesis: ¿qué pasará con cada uno?',
                       'Riégalos igual durante una semana.',
                       'Compara el color, la altura y la forma de las plantitas.'],
                logro=['Comparas los dos germinadores y explicas qué hizo la luz.'],
                entrega='sube una foto de los dos germinadores juntos al final de la semana.'), xp=90, monedas=25),
            mision('Diario de mi frijol', 'texto', leccion(
                intro='Los científicos registran lo que observan con fecha y medidas.',
                pasos=['Durante 5 días, mide tu plantita con una regla (en centímetros).',
                       'Escribe aquí tu tabla: Día · ¿Qué observo? · Altura (cm).',
                       'Al final escribe: ¿en qué día creció más? ¿Qué crees que la ayudó?'],
                entrega='escribe tu diario aquí abajo.'), xp=70, monedas=20),
            mision('Partes de la planta', 'cuestionario', leccion(
                intro='Raíz, tallo, hojas, flor, fruto y semilla: ¿para qué sirve cada una?',
                saber=['Raíz: absorbe agua y minerales y sujeta la planta.',
                       'Tallo: la sostiene y lleva el agua a las hojas.',
                       'Hojas: fabrican el alimento con la luz (fotosíntesis).',
                       'Flor: de ella se forma el fruto.', 'Fruto: protege las semillas.',
                       'Semilla: guarda una nueva planta y su primer alimento.']), xp=60, preguntas=[
                ('¿Qué parte de la planta absorbe el agua del suelo?', 'La raíz', ['La flor', 'La hoja', 'El fruto']),
                ('El tallo sirve para…', 'Sostener la planta y llevar el agua a las hojas',
                 ['Producir semillas', 'Atraer abejas', 'Nada']),
                ('¿En qué parte de la planta se fabrica su alimento?', 'En las hojas',
                 ['En la raíz', 'En la semilla', 'En la maceta']),
                ('¿Qué se forma a partir de la flor?', 'El fruto, con semillas adentro', ['La raíz', 'El tallo', 'Las hojas']),
                ('La semilla…', 'Guarda una nueva planta y su primer alimento',
                 ['Es una hoja seca', 'Es una piedra', 'Es una raíz muerta']),
                ('Las abejas ayudan a las plantas porque…', 'Llevan el polen de flor en flor',
                 ['Se comen sus raíces', 'Les dan sombra', 'Las riegan']),
            ]),
            mision('¿Ayuda o daña a Enriqueta?', 'juego', leccion(
                intro='¿Cada situación ayuda a la planta a crecer o la daña? ¡Piensa en la fórmula!'),
                juego='clasifica_cuidados'),
        ]},
        {'nombre': 'Diseño la maceta perfecta', 'cofre': 30, 'misiones': [
            mision('Macetas inteligentes', 'link', leccion(
                intro='Una buena maceta ayuda a cuidar la planta. Investiga qué características tienen las macetas '
                      'inteligentes.',
                saber=['Agujeros de drenaje: dejan salir el agua que sobra.',
                       'Plato: atrapa el agua que sale para no mojar la mesa.',
                       'Autorriego: un depósito de agua abajo y una mecha que sube el agua poco a poco.',
                       'Etiqueta: dice qué planta es y cómo cuidarla.',
                       'Tamaño correcto: espacio para que crezcan las raíces.'],
                pasos=['Abre Kiddle y busca con palabras clave: «maceta autorriego» o «drenaje plantas».',
                       'Anota 3 características que ayudan a cuidar una planta.',
                       'Piensa en Enriqueta: ¿qué problema tenía? ¿Qué característica de la maceta la ayudaría?'],
                entrega='en el comentario, escribe tus 3 características y cuál pondrás en tu maceta.'),
                xp=60, link=KIDDLE),
            mision('Boceto con medidas', 'evidencia', leccion(
                intro='Antes de modelar, dibuja tu maceta con medidas, como un diseñador de verdad.',
                saber=['Tinkercad mide en milímetros (mm): 10 mm = 1 cm.',
                       'Una maceta pequeña puede medir 70 mm de ancho y 60 mm de alto.',
                       'La pared tiene grosor: si el hueco de adentro mide 64 mm, la pared mide 3 mm de cada lado.'],
                pasos=['Dibuja tu maceta vista de lado y vista desde arriba.',
                       'Escribe las medidas: ancho, alto, grosor de la pared y tamaño de los agujeros.',
                       'Marca dónde irán los agujeros de drenaje, el plato y la etiqueta.',
                       'Agrega una característica especial (asas, depósito de agua, decoración…).'],
                logro=['Tu boceto tiene 2 vistas, medidas en mm y las partes señaladas.'],
                entrega='sube una foto de tu boceto.'), xp=80, monedas=20),
            mision('Medidas y huecos en Tinkercad', 'cuestionario', leccion(
                intro='Repasa las herramientas que usarás para construir tu maceta.',
                saber=['Al seleccionar una figura, los cuadritos blancos muestran sus medidas; da clic en el número para '
                       'escribir la medida exacta.',
                       'Regla (arriba a la derecha): mide distancias desde un punto.',
                       'Hueco: convierte una figura en espacio vacío; al agrupar, quita esa parte.',
                       'Alinear (tecla L): centra varias figuras entre sí.',
                       'Agrupar: Ctrl + G. Duplicar: Ctrl + D.']), xp=60, preguntas=[
                ('¿En qué unidad mide Tinkercad?', 'Milímetros (mm)', ['Kilómetros', 'Litros', 'Kilos']),
                ('¿Cuántos milímetros tiene un centímetro?', '10', ['100', '1', '1000']),
                ('Para hacer el espacio de adentro de la maceta usas un cilindro…', 'Hueco',
                 ['Rojo', 'Más grande que la maceta', 'Acostado']),
                ('¿Qué herramienta centra el hueco dentro de la maceta?', 'Alinear', ['Borrar', 'Imprimir', 'Zoom']),
                ('Si la maceta mide 70 mm y el hueco 64 mm, ¿cuánto mide la pared de cada lado?', '3 mm',
                 ['6 mm', '64 mm', '70 mm']),
                ('¿Para qué sirven los agujeros de drenaje?', 'Para que salga el agua que sobra',
                 ['Para que entren hormigas', 'Para decorar', 'Para que pese menos']),
            ]),
        ]},
        {'nombre': 'Mi maceta en 3D', 'cofre': 50, 'misiones': [
            mision('Maceta paso 1: el cuerpo', 'evidencia', leccion(
                intro='Construye el cuerpo de tu maceta: un vaso hueco con paredes y piso.',
                pasos=['Diseño nuevo en Tinkercad: Maceta_TuNombre.',
                       'Arrastra un cilindro y dale 70 × 70 mm de ancho y 60 mm de alto. Ponle tu color favorito.',
                       'Arrastra otro cilindro de 64 × 64 mm y 60 mm de alto. Conviértelo en Hueco.',
                       'Elévalo 3 mm para que la maceta tenga piso.',
                       'Selecciona los dos, presiona L (Alinear) y da clic en los puntos del centro para centrarlos.',
                       'Agrupa con Ctrl + G. ¡Ya es un vaso hueco!'],
                tip='Si el hueco quedó chueco, deshaz con Ctrl + Z y vuelve a alinear.',
                logro=['Tu maceta es hueca por dentro, con paredes y piso de 3 mm.'],
                entrega='sube una captura de tu maceta vista desde arriba (debe verse el hueco).'), xp=90, monedas=25),
            mision('Maceta paso 2: agujeros de drenaje', 'evidencia', leccion(
                intro='Sin agujeros de drenaje el agua se estanca y las raíces se pudren: ese pudo ser el problema de '
                      'Enriqueta.',
                pasos=['Arrastra un cilindro de 5 × 5 mm y 10 mm de alto. Conviértelo en Hueco.',
                       'Colócalo en el piso de la maceta, cerca de la orilla.',
                       'Duplícalo con Ctrl + D y mueve la copia al otro lado. Haz 4 agujeros en total.',
                       'Revisa desde abajo (cubo de vista → cara de abajo) que atraviesen el piso.',
                       'Selecciona todo y agrupa con Ctrl + G.'],
                logro=['Se ven 4 agujeros que atraviesan el piso.'],
                entrega='sube una captura desde abajo donde se vean los 4 agujeros.'), xp=90, monedas=25),
            mision('Maceta paso 3: plato y etiqueta', 'evidencia', leccion(
                intro='Agrega el plato para el agua que sobra y una etiqueta con el nombre de tu planta.',
                pasos=['Plato: cilindro de 90 × 90 mm y 10 mm de alto. Agrega un cilindro hueco de 84 × 84 mm, elévalo '
                       '3 mm, alinéalos al centro y agrúpalos.',
                       'Pon el plato debajo de la maceta (eleva la maceta 3 mm para que quede encima).',
                       'Etiqueta: en las formas básicas busca «Texto», escribe el nombre de tu planta y hazlo de 3 mm de grosor.',
                       'Pega la etiqueta al frente: rótala 90° para que quede parada y acércala hasta que toque la pared.',
                       'Dale colores que combinen.'],
                logro=['La maceta está sobre su plato y la etiqueta se lee de frente.'],
                entrega='sube una captura de tu maceta con plato y etiqueta.'), xp=90, monedas=25),
            mision('Maceta paso 4: tu superpoder', 'evidencia', leccion(
                intro='Tu maceta necesita una característica especial que resuelva un problema de cuidado.',
                pasos=['Elige una: asas para moverla al sol, depósito de agua para autorriego, un soporte para colgarla, '
                       'un protector para que no se caiga la tierra o tu propia idea.',
                       'Constrúyela con figuras, huecos, rotar y elevar.',
                       'Revisa tu diseño desde todos los lados con el cubo de vista.',
                       'Si tu escuela tiene impresora 3D: Exportar → .STL para imprimirla.'],
                logro=['Tu maceta tiene una característica que ayuda a cuidar la planta y sabes explicar cómo.'],
                entrega='sube una captura de tu diseño final y escribe en el comentario qué problema resuelve tu superpoder.'),
                xp=100, monedas=30),
            mision('Feria de macetas inteligentes', 'presencial', leccion(
                intro='¡Abre la tienda de macetas inteligentes! Presenta tu diseño como si lo fueras a vender.',
                pasos=['Prepara un anuncio de 30 segundos: nombre de tu maceta, para qué planta es y qué problema resuelve.',
                       'Presenta tu diseño en 3D al grupo.',
                       'Escucha las presentaciones y vota por la maceta más útil y la más creativa.'],
                logro=['Explicas cómo tu maceta ayuda a cumplir la fórmula de las plantas.']), xp=60, monedas=20),
            jefe('Jefe: La Planta Carnívora Gigante',
                 '¡Una planta carnívora gigante custodia el invernadero! Solo se calmará si conoces la verdadera fórmula '
                 'de las plantas y diseñas como un experto.', [
                     ('¿Cómo se llama el proceso con el que las plantas fabrican su alimento con la luz?', 'Fotosíntesis',
                      ['Digestión', 'Evaporación', 'Germinación']),
                     ('El color verde de las hojas se debe a la…', 'Clorofila', ['Pintura', 'Tierra', 'Lluvia']),
                     ('¿Qué parte de la planta absorbe el agua del suelo?', 'La raíz', ['La flor', 'La hoja', 'El fruto']),
                     ('Una planta que pasa muchos días en un cuarto oscuro…', 'Se pone amarilla y débil',
                      ['Se pone más verde', 'Da más frutos', 'No le pasa nada']),
                     ('¿Por qué una maceta necesita agujeros de drenaje?',
                      'Para que el agua que sobra salga y no se pudran las raíces',
                      ['Para que se vea bonita', 'Para que entre luz', 'Para que pese menos']),
                     ('En Tinkercad, ¿cómo haces el espacio de adentro de la maceta?',
                      'Con un cilindro hueco agrupado con la maceta',
                      ['Pintándola de negro', 'Con el cubo de vista', 'Borrando la maceta']),
                     ('¿Qué tecla abre la herramienta Alinear en Tinkercad?', 'L', ['Z', 'Enter', 'Espacio']),
                     ('En el experimento de luz contra oscuridad, ¿qué fue lo ÚNICO que cambiaste?', 'La luz',
                      ['El agua', 'Los frijoles', 'Todo']),
                 ]),
        ]},
    ],
}
