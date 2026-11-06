"""Mundo 6 · ES-SEA207 La rebelión de los árboles: problemas ambientales de la comunidad y un plan de rescate en el
procesador de textos (portada, objetivo, tabla, acciones, encabezados y carta formal)."""
from .base import clasifica, jefe, leccion, mision

JUEGOS = {
    'clasifica_bosque': clasifica('¿Ayuda o daña al bosque?', '🌳', 'Clasifica cada acción: ¿cuida a los árboles o los daña?', [
        ('Ayuda al bosque', '🌱', ['Plantar un árbol', 'Reciclar papel', 'Usar las hojas por los dos lados',
                                  'Apagar por completo una fogata', 'Regar los árboles del parque',
                                  'Cuidar los nidos de los pájaros', 'Usar bolsas de tela']),
        ('Daña al bosque', '🪓', ['Tirar basura en el bosque', 'Talar árboles sin volver a plantar', 'Quemar pastizales',
                                 'Desperdiciar hojas de papel', 'Dejar vidrios tirados en el pasto',
                                 'Arrancar plantas pequeñas por diversión']),
    ]),
    'clasifica_plan': clasifica('¿Problema o solución?', '📝', 'Separa los problemas de las acciones que los resuelven.', [
        ('Problema', '⚠️', ['Basura tirada en el parque', 'Árboles talados sin volver a plantar', 'Plagas que secan los árboles',
                           'Incendios por fogatas mal apagadas', 'Ramas rotas por colgarse de ellas',
                           'Raíces cubiertas de cemento', 'Falta de riego en tiempo de calor']),
        ('Solución', '💡', ['Poner botes de basura y de reciclaje', 'Organizar una jornada para plantar árboles',
                           'Pedir ayuda a un experto en plagas', 'Hacer un reglamento para fogatas',
                           'Colocar letreros para cuidar las ramas', 'Dejar un círculo de tierra alrededor del tronco',
                           'Hacer un calendario de riego por grupos']),
    ], rondas=14),
    'atajos_texto': {'nombre': 'Atajos ninja: copia y pega', 'icono': '🥷', 'plantilla': 'atajos', 'en_arcade': True,
                     'descripcion': 'Copiar, pegar, cortar y deshacer sin usar el mouse.',
                     'configuracion': {'atajos': ['copiar', 'pegar', 'cortar', 'deshacer', 'rehacer', 'todo'],
                                       'rondas': 10, 'modo': 'aprende'}},
}

MUNDO = {
    'nombre': 'Bosque en Rebelión', 'tema': 'bosque',
    'descripcion': 'ES-SEA207 · La rebelión de los árboles. ¡Los árboles de Pinion City se fueron de viaje y dejaron '
                   'una nota! Investiga qué problemas los dañan y escribe en el procesador de textos un plan de '
                   'rescate para que regresen. Pregunta guía: ¿por qué se fueron los árboles?',
    'niveles': [
        {'nombre': 'La nota de los árboles', 'cofre': 25, 'misiones': [
            mision('¡Los árboles se fueron!', 'texto', leccion(
                intro='Los ciudadanos de Pinion City despertaron con una sorpresa: ¡no había ni un árbol! Solo una nota '
                      'del Consejo de Árboles Unidos: se fueron de viaje porque necesitan un respiro, y mientras tanto '
                      'piden que la ciudad resuelva los problemas que los dañan. Prometen dejar una pista y estar atentos '
                      'a la respuesta.\n\nPregunta del caso: ¿por qué se fueron los árboles?',
                pasos=['Escribe 3 hipótesis: ¿qué problemas crees que molestaron a los árboles?',
                       '¿Qué pasaría en tu ciudad si de verdad se fueran todos los árboles? Escribe 3 consecuencias.',
                       'Escribe tu meta: ¿qué te gustaría lograr con tu plan de rescate?'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('Lo que los árboles hacen por nosotros', 'cuestionario', leccion(
                intro='Oxígeno, sombra, hogar… ¿qué más nos dan los árboles? Repasa y contesta.',
                saber=['Producen el oxígeno que respiramos y absorben dióxido de carbono.',
                       'Dan sombra y refrescan la ciudad.',
                       'Sus raíces sostienen el suelo para que la lluvia no se lo lleve.',
                       'Son el hogar de aves, insectos y muchos animales.',
                       'Deforestación: cortar o destruir muchos árboles de un bosque o una selva.',
                       'Las 3 R: Reducir, Reutilizar y Reciclar (ahorrar papel salva árboles).']), xp=60, preguntas=[
                ('Los árboles producen…', 'El oxígeno que respiramos', ['Plástico', 'Humo', 'Gasolina']),
                ('Las raíces de los árboles ayudan a…', 'Sostener el suelo para que la lluvia no se lo lleve',
                 ['Hacer ruido', 'Atraer rayos', 'Secar los ríos']),
                ('¿Qué es la deforestación?', 'Cortar o destruir muchos árboles de un bosque o una selva',
                 ['Plantar árboles', 'Regar flores', 'Un tipo de fruta']),
                ('¿Quién pierde su hogar cuando se tala un bosque?', 'Aves, ardillas, insectos y muchos animales más',
                 ['Nadie', 'Solo los peces del mar', 'Solo las mascotas']),
                ('¿Qué puedes hacer para ahorrar papel?', 'Usar las hojas por los dos lados y reciclar',
                 ['Tirar hojas casi nuevas', 'Imprimir todo dos veces', 'Usar una hoja por cada palabra']),
                ('Las tres R significan…', 'Reducir, Reutilizar y Reciclar',
                 ['Romper, Rayar y Regalar', 'Reír, Rodar y Rugir', 'Rápido, Recto y Redondo']),
            ]),
            mision('¿Ayuda o daña al bosque?', 'juego', leccion(
                intro='Clasifica cada acción: ¿cuida a los árboles o los daña?',
                tip='Piensa qué le pasaría al árbol: ¿tendría más agua, sombra y espacio, o menos?'), juego='clasifica_bosque'),
        ]},
        {'nombre': 'Problemas en mi comunidad', 'cofre': 30, 'misiones': [
            mision('Patrulla verde', 'presencial', leccion(
                intro='¿Habrá problemas que molesten a los árboles cerca de ti? Hoy saldrás a investigar como patrulla.',
                pasos=['En equipos, recorran el patio y los alrededores de la escuela con su profe.',
                       'Observen árboles y plantas: ¿hay basura alrededor, ramas rotas, plagas, cemento sobre las raíces '
                       'o falta de agua?',
                       'Anoten cada problema: lugar, qué observaron y qué creen que lo causa.',
                       'Con permiso de su profe, tomen fotos (sin personas) que servirán para su plan.'],
                logro=['Su equipo registró al menos 3 problemas con lugar, observación y causa.']), xp=60, monedas=20),
            mision('Mapa de decisiones', 'evidencia', leccion(
                intro='No se puede resolver todo a la vez. Un mapa de decisiones ayuda a elegir el problema más importante.',
                saber=['Un mapa de decisiones compara opciones con preguntas (criterios) para elegir la mejor.',
                       'Criterios útiles: ¿qué tanto daña a los árboles?, ¿podemos hacer algo nosotros?, ¿es seguro?, '
                       '¿cuánto tiempo necesitamos?'],
                pasos=['En una hoja hagan una tabla: en la primera columna escriban los problemas que encontraron.',
                       'En las siguientes columnas escriban los criterios. Califiquen cada problema del 1 al 3 en cada criterio.',
                       'Sumen los puntos de cada problema.',
                       'Encierren el que tenga más puntos: ¡será el problema de su plan de rescate!'],
                logro=['El mapa compara al menos 3 problemas con 3 criterios y tiene un ganador claro.'],
                entrega='sube una foto del mapa de decisiones de tu equipo.'), xp=80, monedas=20),
            mision('¿Problema o solución?', 'juego', leccion(
                intro='Un buen plan distingue el problema de la acción que lo resuelve. Clasifica cada tarjeta.'),
                juego='clasifica_plan'),
        ]},
        {'nombre': 'Trazo mis pistas: el plan de rescate', 'cofre': 30, 'misiones': [
            mision('¿Qué es un plan de acción?', 'cuestionario', leccion(
                intro='Antes de escribir, conoce las partes del plan de rescate.',
                saber=['Un plan de acción es un documento que explica qué problema vamos a resolver y cómo.',
                       'Partes del plan de rescate: portada, objetivo, diagnóstico (el problema, sus causas y '
                       'consecuencias), acciones (qué, quién y cuándo) y carta a los árboles.',
                       'El objetivo se escribe con un verbo en infinitivo (terminado en -ar, -er, -ir) + qué + para qué. '
                       'Ejemplo: «Reducir la basura del parque para que los árboles crezcan sanos».',
                       'Una acción clara dice qué se hará, quién lo hará y cuándo.']), xp=60, preguntas=[
                ('Un plan de acción sirve para…', 'Explicar qué problema resolveremos y cómo',
                 ['Contar un chiste', 'Hacer un dibujo libre', 'Guardar fotos']),
                ('¿Cuál está bien escrito como objetivo?', 'Reducir la basura del parque para que los árboles crezcan sanos',
                 ['La basura', 'Me gustan los árboles', 'Ayer fuimos al parque']),
                ('El diagnóstico del plan explica…', 'El problema, sus causas y sus consecuencias',
                 ['Los nombres del equipo', 'La despedida de la carta', 'El color de la portada']),
                ('¿Qué debe decir una acción clara?', 'Qué se hará, quién lo hará y cuándo',
                 ['Solo «ayudar»', 'Solo el título', 'Nada, se improvisa']),
                ('¿Qué parte va al inicio del documento?', 'La portada', ['La carta', 'Las acciones', 'El diagnóstico']),
            ]),
            mision('La portada del plan', 'evidencia', leccion(
                intro='Una buena portada dice de qué trata el documento y quién lo hizo. ¡Es la primera impresión!',
                saber=['WordArt (Insertar → WordArt) o el estilo «Título» hacen títulos llamativos.',
                       'Salto de página (Insertar → Salto de página, o Ctrl + Enter) manda lo que sigue a una hoja nueva.',
                       'Una portada lleva: título, subtítulo, imagen, nombres del equipo, grupo y fecha.'],
                pasos=['Abre Word → Documento en blanco. Guárdalo de una vez como Plan_Rescate_Equipo en tu carpeta › '
                       'Documentos.',
                       'Escribe el título del plan con WordArt (ejemplo: «Operación Árbol Feliz»).',
                       'Agrega un subtítulo: Plan de rescate de los árboles de (tu escuela o colonia).',
                       'Inserta una imagen o una foto de la patrulla verde y céntrala.',
                       'Abajo escribe los nombres del equipo, el grupo y la fecha, alineados a la derecha.',
                       'Inserta un salto de página para empezar la hoja 2.'],
                logro=['La portada tiene título, subtítulo, imagen, equipo, grupo y fecha, y cabe en una hoja.'],
                entrega='sube una captura de tu portada.'), xp=90, monedas=25),
            mision('El objetivo de rescate', 'evidencia', leccion(
                intro='En la hoja 2 escribirás el objetivo: la meta de tu plan.',
                pasos=['Escribe el subtítulo Objetivo y aplícale el estilo «Título 1».',
                       'Redacta tu objetivo con la fórmula: verbo en infinitivo + qué + para qué.',
                       'Debajo escribe en 2 o 3 renglones por qué eligieron ese problema (usa tu mapa de decisiones).',
                       'Revisen que el objetivo sea algo que su equipo SÍ pueda lograr.'],
                logro=['El objetivo empieza con un verbo en infinitivo y dice qué y para qué.'],
                entrega='sube una captura de la hoja 2.'), xp=70, monedas=20),
        ]},
        {'nombre': 'DTectives en acción: diagnóstico y acciones', 'cofre': 35, 'misiones': [
            mision('Atajos ninja: copia y pega', 'juego', leccion(
                intro='Escribir un plan es más rápido con atajos: copiar, pegar, cortar y deshacer sin usar el mouse.',
                saber=['Ctrl + C copia, Ctrl + V pega, Ctrl + X corta y Ctrl + Z deshace.',
                       'Primero se selecciona el texto y luego se usa el atajo.']), juego='atajos_texto'),
            mision('Diagnóstico con tabla', 'evidencia', leccion(
                intro='El diagnóstico explica el problema con datos y evidencias. Una tabla lo ordena perfecto.',
                saber=['Insertar → Tabla → elige columnas y filas pasando el mouse por los cuadritos.',
                       'Tab te lleva a la siguiente celda; en la última celda, Tab agrega una fila nueva.',
                       'Diseño de tabla: elige un estilo o pinta la primera fila (Sombreado) para resaltar los encabezados.'],
                pasos=['En la hoja 3 escribe el subtítulo Diagnóstico (estilo «Título 1»).',
                       'Escribe un párrafo corto: ¿qué problema eligieron y dónde lo encontraron?',
                       'Inserta una tabla de 3 columnas y 4 filas. Encabezados: Problema · Causa · Consecuencia.',
                       'Llénala con lo que investigaron.',
                       'Inserta una foto del problema y usa Ajustar texto → Cuadrado.'],
                logro=['La tabla tiene encabezados resaltados y al menos 3 filas llenas.', 'Hay una foto como evidencia.'],
                entrega='sube una captura de tu diagnóstico.'), xp=100, monedas=30),
            mision('Acciones de rescate', 'evidencia', leccion(
                intro='¡Ahora las soluciones! Escribe las acciones que tu equipo propone para rescatar a los árboles.',
                saber=['Encabezado y pie de página: textos que se repiten en todas las hojas (Insertar → Encabezado / '
                       'Pie de página).',
                       'Número de página: Insertar → Número de página.'],
                pasos=['En una hoja nueva escribe el subtítulo Acciones de rescate.',
                       'Haz una lista numerada con 5 acciones. Cada una dice qué, quién y cuándo (ejemplo: Colocar dos '
                       'botes de reciclaje en el patio · Equipo Ceiba · primera semana de marzo).',
                       'Agrega una imagen o un ícono que represente una de las acciones.',
                       'Inserta un encabezado con el nombre del plan y un pie de página con el número de página.',
                       'Guarda.'],
                logro=['Las 5 acciones dicen qué, quién y cuándo.',
                       'Todas las hojas tienen encabezado y número de página.'],
                entrega='sube una captura de tus acciones donde se vea el encabezado.'), xp=100, monedas=30),
        ]},
        {'nombre': 'Carta a los árboles', 'cofre': 50, 'misiones': [
            mision('La carta a los árboles', 'evidencia', leccion(
                intro='Los árboles esperan su respuesta. Escríbanles una carta formal para convencerlos de volver.',
                saber=['Partes de una carta formal: lugar y fecha (alineados a la derecha), destinatario, saludo, cuerpo, '
                       'despedida y firma.',
                       'El cuerpo tiene 3 párrafos: 1) reconocer el problema y disculparse, 2) explicar su plan, '
                       '3) invitarlos a regresar con una promesa.',
                       'Texto justificado: queda parejo de los dos lados, como en los libros.'],
                pasos=['En una hoja nueva escribe el lugar y la fecha y alinéalos a la derecha.',
                       'Escribe: Al Consejo de Árboles Unidos de Pinion City, y un saludo.',
                       'Escribe los 3 párrafos del cuerpo y justifícalos.',
                       'Escribe la despedida y los nombres del equipo como firma.',
                       'Revisa la ortografía (F7) y guarda.'],
                logro=['La carta tiene todas sus partes y ninguna palabra subrayada en rojo.'],
                entrega='sube una captura de tu carta.'), xp=100, monedas=30),
            mision('Revisión final y PDF', 'evidencia', leccion(
                intro='Antes de entregar, los profesionales revisan todo con una lista de cotejo.',
                pasos=['Revisen: ☐ portada ☐ objetivo ☐ diagnóstico con tabla y foto ☐ acciones ☐ carta ☐ encabezado y '
                       'números de página ☐ sin faltas de ortografía.',
                       'Pidan a otro equipo que revise su plan con la misma lista y corrijan lo que falte.',
                       'Guarden una copia en PDF: Archivo → Guardar como → Tipo: PDF.',
                       'Abran el PDF para comprobar que se ve bien.'],
                logro=['El plan cumple toda la lista y existe su versión PDF.'],
                entrega='sube una captura del PDF abierto.'), xp=80, monedas=25),
            mision('Galería de planes', 'presencial', leccion(
                intro='Revelo mis hallazgos: los planes se exhiben como en un museo y el Consejo de Árboles leerá sus '
                      'respuestas.',
                pasos=['Dejen su plan abierto (o impreso) en su mesa.',
                       'Recorran la galería y lean al menos 3 planes de otros equipos.',
                       'Dejen en cada uno una nota: algo que les gustó y una idea para mejorarlo.',
                       'Al final, su profe lee la respuesta del Consejo de Árboles. ¿Regresarán?'],
                logro=['Leyeron 3 planes y dejaron comentarios útiles.']), xp=60, monedas=20),
            jefe('Jefe: El Leñador de Humo',
                 'El Leñador de Humo quiere talar todo el bosque. Demuestra lo que sabes de los árboles y de tu plan de '
                 'rescate para detenerlo.', [
                     ('Los árboles producen…', 'El oxígeno que respiramos', ['Plástico', 'Humo', 'Gasolina']),
                     ('Un incendio forestal puede empezar por…', 'Una fogata mal apagada o vidrios tirados',
                      ['Regar las plantas', 'Plantar árboles', 'Reciclar']),
                     ('¿Qué es la deforestación?', 'Cortar o destruir muchos árboles de un bosque o una selva',
                      ['Plantar árboles', 'Regar flores', 'Un tipo de fruta']),
                     ('¿Cuál es un buen objetivo para el plan de rescate?',
                      'Plantar 10 árboles en el patio para tener más sombra y aire limpio',
                      ['Árboles', 'Los árboles son verdes', 'No sé']),
                     ('¿Qué atajo pega un texto que copiaste?', 'Ctrl + V', ['Ctrl + C', 'Ctrl + Z', 'Ctrl + X']),
                     ('Para que lo que sigue empiece en una hoja nueva usas…', 'Un salto de página',
                      ['Muchos Enter', 'La barra espaciadora', 'Un color']),
                     ('El texto que se repite arriba de todas las hojas se llama…', 'Encabezado',
                      ['Pie de página', 'Viñeta', 'Celda']),
                     ('En una carta formal, ¿dónde van el lugar y la fecha?', 'Arriba, alineados a la derecha',
                      ['Al final, en la firma', 'En medio del cuerpo', 'No se escriben']),
                 ]),
        ]},
    ],
}
