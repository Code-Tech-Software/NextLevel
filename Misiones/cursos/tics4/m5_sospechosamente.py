"""Mundo 5 · ES-SEA207 SospechosaMente: la memoria y el sistema nervioso, y el procesador de textos (escribir,
dar formato, listas, imágenes, ortografía y PDF)."""
from Misiones.minijuegos import TEMAS_CLASIFICA

from .base import clasifica, jefe, leccion, mision

JUEGOS = {
    'teclado_central': {'nombre': 'Teclado misterioso: fila guía', 'icono': '⌨️', 'plantilla': 'teclado', 'en_arcade': True,
                        'descripcion': 'Encuentra las teclas A S D F – J K L Ñ sin mirar.',
                        'configuracion': {'conjunto': 'central', 'rondas': 20, 'modo': 'guiado'}},
    'clasifica_teclas': clasifica('¿Qué tecla uso?', '⌨️', 'Cada tecla especial tiene su trabajo.', [
        ('Enter', '↩️', ['Empezar un párrafo nuevo', 'Bajar el cursor a la siguiente línea',
                        'Separar el título del texto', 'Terminar una lista (presionándola dos veces)']),
        ('Retroceso', '⬅️', ['Borrar la letra que está a la izquierda del cursor', 'Corregir la última letra que escribiste',
                            'Quitar un espacio que sobra antes del cursor', 'Borrar una palabra hacia atrás, letra por letra']),
        ('Shift', '⬆️', ['Escribir una sola letra mayúscula', 'Escribir los dos puntos (:)', 'Escribir el signo de pesos ($)',
                        'Escribir el paréntesis que abre (', 'Escribir el signo de interrogación que cierra ?']),
    ]),
    'clasifica_memoria': clasifica('¿Ayuda o daña a tu memoria?', '🧠', 'Hábitos que fortalecen o debilitan tu memoria.', [
        ('Ayuda', '🧠', ['Dormir de 9 a 11 horas', 'Repasar un poco cada día', 'Hacer ejercicio', 'Desayunar fruta y cereal',
                        'Tomar agua', 'Explicarle a alguien lo que aprendiste', 'Hacer dibujos o esquemas para estudiar']),
        ('Daña', '😵', ['Desvelarse jugando videojuegos', 'Estudiar toda la noche antes del examen', 'Saltarse el desayuno',
                       'Ver el celular mientras haces la tarea', 'Comer muchos dulces y refrescos',
                       'Estudiar con la tele prendida', 'No descansar nunca']),
    ]),
    'clasifica_seguridad': clasifica('¿Seguro o peligroso?', '🛡️', 'Una mente sospechosa también se cuida en internet.',
                                     TEMAS_CLASIFICA['seguridad'][2]),
}

MUNDO = {
    'nombre': 'Agencia SospechosaMente', 'tema': 'ciudad',
    'descripcion': 'ES-SEA207 · SospechosaMente. Si tu cerebro viajara en el tiempo, ¿nunca olvidarías nada? '
                   'Investiga la memoria y el sistema nervioso, y registra tus descubrimientos en un expediente hecho '
                   'en el procesador de textos. Pregunta guía: ¿cuál es el secreto para viajar en el tiempo?',
    'niveles': [
        {'nombre': 'El caso de la memoria', 'cofre': 25, 'misiones': [
            mision('¿Se puede viajar en el tiempo?', 'texto', leccion(
                intro='«Me encanta leer historias sobre viajes en el tiempo y otros mundos. Así puedo volver al pasado '
                      'cada vez que quiero recordar algo importante. Si mi cerebro hiciera viajes en el tiempo, ¡nunca '
                      'más olvidaría nada! …¿O sí?»\n\nPregunta del caso: ¿cuál es el secreto para viajar en el tiempo?',
                pasos=['Escribe tu recuerdo más antiguo: ¿cuántos años tenías?, ¿qué veías, oías u olías?',
                       '¿Por qué crees que ese recuerdo se quedó contigo y otros no?',
                       'Escribe tu hipótesis: ¿qué le ayuda a tu cerebro a recordar?'],
                entrega='escribe tus respuestas aquí abajo.'), xp=60),
            mision('El juego de Kim', 'presencial', leccion(
                intro='Pon a prueba tu memoria con el juego que usan los detectives para entrenar su atención.',
                saber='La memoria funciona mejor cuando organizas la información o le das un significado.',
                material=['15 objetos pequeños (lápiz, goma, llave, moneda…)', 'Un trapo para taparlos', 'Un reloj'],
                pasos=['Tu profe pone 15 objetos en la mesa. Obsérvalos 30 segundos sin escribir.',
                       'Se tapan. Escribe todos los que recuerdes en 1 minuto.',
                       'Segunda ronda con objetos nuevos, pero ahora usa un truco: agrúpalos (cosas de escritorio, de '
                       'cocina…) o inventa una historia que los una.',
                       'Compara: ¿en qué ronda recordaste más? ¿Por qué?'],
                logro=['Explicas qué truco te ayudó a recordar más.']), xp=50),
            mision('¿Cómo funciona la memoria?', 'cuestionario', leccion(
                intro='Tu cerebro guarda recuerdos en diferentes «cajones». Repasa y demuestra que los conoces.',
                saber=['La memoria es la capacidad del cerebro de guardar y recordar información.',
                       'Memoria sensorial: dura menos de un segundo; es lo que captan tus sentidos.',
                       'Memoria de corto plazo: guarda algo unos segundos o minutos, como un número que acabas de oír.',
                       'Memoria de largo plazo: guarda recuerdos por años, como tu nombre o tu primer día de escuela.',
                       'Repasar, dormir bien y relacionar lo nuevo con lo que ya sabes ayuda a que un recuerdo pase a '
                       'largo plazo.']), xp=60, preguntas=[
                ('¿Qué es la memoria?', 'La capacidad del cerebro de guardar y recordar información',
                 ['Una parte del estómago', 'Un tipo de computadora', 'Un sentido como el olfato']),
                ('¿Cuánto dura la memoria sensorial?', 'Menos de un segundo', ['Toda la vida', 'Una semana', 'Un año']),
                ('Oyes un número de teléfono y lo recuerdas solo un ratito. ¿Qué memoria usaste?', 'De corto plazo',
                 ['De largo plazo', 'Ninguna', 'La de la computadora']),
                ('Recuerdas tu primer día de escuela. ¿Qué memoria es?', 'De largo plazo',
                 ['Sensorial', 'De corto plazo', 'De la computadora']),
                ('¿Qué ayuda a guardar un recuerdo por mucho tiempo?', 'Repasar y dormir bien',
                 ['Desvelarse', 'No repasar nunca', 'Comer muchos dulces']),
                ('En el juego de Kim, ¿qué truco ayuda a recordar más objetos?', 'Agruparlos o inventar una historia con ellos',
                 ['Cerrar los ojos', 'Verlos solo un segundo', 'No intentarlo']),
            ]),
        ]},
        {'nombre': 'Mi primer documento', 'cofre': 30, 'misiones': [
            mision('Conoce tu procesador de textos', 'presencial', leccion(
                intro='Un procesador de textos (Word, Google Docs o LibreOffice Writer) sirve para escribir, corregir y '
                      'dar formato a documentos. Es la libreta del detective digital.',
                saber=['Barra de título: muestra el nombre de tu documento.',
                       'Cinta de opciones: las pestañas de arriba (Archivo, Inicio, Insertar, Diseño…) con las herramientas.',
                       'Pestaña Inicio: fuente, tamaño, negrita, cursiva, subrayado, color, alineación y viñetas.',
                       'Hoja: donde escribes. El cursor es la rayita que parpadea: ahí aparece lo que escribes.',
                       'Barra de estado (abajo): número de páginas, palabras y zoom.'],
                pasos=['Abre Word → Documento en blanco.',
                       'Tu profe señala cada parte en el proyector y tú la encuentras en tu pantalla.',
                       'Escribe tu nombre y mueve el cursor con las flechas del teclado.',
                       'Haz zoom con el control de abajo a la derecha (o Ctrl + rueda del mouse).',
                       'Busca en la pestaña Inicio la negrita, el color de letra y el botón de centrar.'],
                logro=['Señalas la cinta de opciones, la pestaña Inicio, el cursor y la barra de estado.']), xp=50),
            mision('Teclado misterioso: fila guía', 'juego', leccion(
                intro='Los detectives escriben rápido y sin mirar. Coloca tus dedos en la fila guía (A S D F – J K L Ñ) '
                      'y encuentra cada tecla.',
                saber=['Los índices descansan en la F y en la J: tienen una rayita para encontrarlas sin mirar.',
                       'Cada dedo tiene sus teclas: así escribes más rápido y con menos errores.']), juego='teclado_central'),
            mision('¿Qué tecla uso?', 'juego', leccion(
                intro='Enter, Retroceso o Shift: decide qué tecla resuelve cada situación.',
                tip='Suprimir también borra, pero hacia adelante (la letra a la derecha del cursor).'),
                juego='clasifica_teclas'),
            mision('Escribe tu viaje en el tiempo', 'evidencia', leccion(
                intro='Tu primer documento será el expediente de la memoria: empieza contando un recuerdo como si '
                      'viajaras en el tiempo.',
                saber=['Mayúscula: Shift + letra (para una sola) o Bloq Mayús (para varias; ¡apágala después!).',
                       'Acentos: primero presiona la tecla del acento ( ´ ) y luego la vocal: á, é, í, ó, ú.',
                       'La ñ tiene su propia tecla, junto a la L.',
                       'Enter: párrafo nuevo. Retroceso: borra hacia atrás. Suprimir: borra hacia adelante.'],
                pasos=['Abre Word → Documento en blanco.', 'Escribe el título: Mi viaje en el tiempo.',
                       'Presiona Enter y escribe un párrafo de al menos 5 renglones sobre tu recuerdo favorito: ¿cuántos '
                       'años tenías?, ¿qué veías, oías u olías?, ¿por qué lo recuerdas?',
                       'Revisa tus acentos y mayúsculas.',
                       'Guarda: Archivo → Guardar como → TIC_4A_TuNombre › Documentos → nombre: Memoria_TuNombre.'],
                logro=['Tu texto tiene título, un párrafo de 5 renglones y acentos correctos.',
                       'Está guardado en tu carpeta con el nombre correcto.'],
                entrega='sube una captura de tu documento.'), xp=90, monedas=25),
            mision('Edita como detective', 'evidencia', leccion(
                intro='Dale formato a tu documento para que parezca un expediente profesional.',
                saber=['Para dar formato primero se SELECCIONA: doble clic selecciona una palabra; triple clic, un '
                       'párrafo; también puedes arrastrar con el mouse.',
                       'Fuente: el tipo de letra. Tamaño: qué tan grande es (títulos de 20 a 28; texto de 12 a 14).',
                       'Negrita (N), cursiva (K) y subrayado (S) están en la pestaña Inicio.',
                       'Alineación: izquierda, centrado, derecha o justificado (parejo de los dos lados).'],
                pasos=['Abre Memoria_TuNombre.',
                       'Selecciona el título: tamaño 24, negrita, centrado y de un color.',
                       'Selecciona el párrafo: fuente fácil de leer (Calibri, Arial o Verdana), tamaño 14 y justificado.',
                       'Pon en cursiva una palabra importante de tu recuerdo.',
                       'Guarda los cambios (ícono del disquete o Archivo → Guardar).'],
                logro=['El título es grande, centrado y en negrita; el texto se lee fácil y está justificado.'],
                entrega='sube una captura de tu documento con formato.'), xp=90, monedas=25),
        ]},
        {'nombre': 'Memoria de los sentidos', 'cofre': 30, 'misiones': [
            mision('Los sentidos guardan recuerdos', 'cuestionario', leccion(
                intro='Tus sentidos son la puerta de entrada de los recuerdos.',
                saber=['La memoria sensorial guarda por un instante lo que captan tus 5 sentidos: vista, oído, olfato, '
                       'gusto y tacto.',
                       'Si pones atención, esa información pasa a la memoria de corto plazo.',
                       'El olfato está muy conectado con los recuerdos: un olor puede llevarte a tu infancia en un segundo.',
                       'Mientras más sentidos uses al aprender (ver, oír, tocar), más fácil es recordar.']), xp=60, preguntas=[
                ('¿Cuáles son los 5 sentidos?', 'Vista, oído, olfato, gusto y tacto',
                 ['Vista, memoria, sueño, gusto y tacto', 'Oído, risa, olfato, frío y tacto', 'Solo vista y oído']),
                ('El olor a pan recién hecho te recuerda la casa de tu abuela. ¿Qué sentido se conectó con tu recuerdo?',
                 'El olfato', ['El tacto', 'El oído', 'La vista']),
                ('¿Qué hace que la información de los sentidos pase a la memoria de corto plazo?', 'Poner atención',
                 ['Cerrar los ojos', 'Dormirse', 'Ignorarla']),
                ('Para aprender sobre los volcanes, ¿qué ayuda más a recordar?', 'Verlo, escucharlo y hacer una maqueta',
                 ['Leerlo una sola vez', 'No verlo', 'Escucharlo con la tele prendida']),
                ('Sientes lo áspero de una lija. ¿Qué sentido usaste?', 'El tacto', ['El gusto', 'El olfato', 'El oído']),
            ]),
            mision('Lista de recuerdos sensoriales', 'evidencia', leccion(
                intro='Agrega a tu expediente una lista de recuerdos guardados por tus sentidos. Aprenderás a usar '
                      'viñetas y listas numeradas.',
                saber=['Viñetas: puntos o figuras al inicio de cada elemento, cuando el orden no importa (botón de '
                       'viñetas de la pestaña Inicio).',
                       'Numeración: listas con 1, 2, 3, cuando el orden sí importa (como los pasos de una receta).',
                       'Al presionar Enter en una lista aparece la siguiente viñeta. Presiona Enter dos veces para terminarla.',
                       'La tecla Tab hace una sublista (un nivel más adentro).'],
                pasos=['Abre Memoria_TuNombre y escribe el subtítulo Recuerdos de mis sentidos (en negrita).',
                       'Activa las viñetas y escribe 5 renglones, uno por sentido. Ejemplo: Olfato: el olor a tierra '
                       'mojada cuando llueve.',
                       'Escribe otro subtítulo: Mis trucos para recordar.',
                       'Activa la numeración y escribe 3 trucos (ejemplo: 1. Hacer un dibujo).',
                       'Cambia el estilo de la viñeta (flechita junto al botón de viñetas) y guarda.'],
                logro=['Tienes una lista con viñetas de 5 sentidos y una lista numerada de 3 trucos.'],
                entrega='sube una captura de tus dos listas.'), xp=90, monedas=25),
        ]},
        {'nombre': 'El centro de control', 'cofre': 30, 'misiones': [
            mision('El sistema nervioso', 'cuestionario', leccion(
                intro='Tu cuerpo tiene un centro de control que nunca descansa. Repasa cómo funciona.',
                saber=['El sistema nervioso es el centro de control del cuerpo: recibe información, la procesa y da órdenes.',
                       'Cerebro: piensa, siente, recuerda y aprende. Lo protege el cráneo.',
                       'Médula espinal: un «cable» dentro de la columna que lleva mensajes entre el cerebro y el cuerpo.',
                       'Nervios: ramas que llegan a todo el cuerpo.',
                       'Neuronas: las células del sistema nervioso; se pasan mensajes eléctricos muy rápido. Cuando '
                       'aprendes, ¡hacen nuevas conexiones!',
                       'El casco protege tu cerebro: úsalo en bici, patines o patineta.']), xp=60, preguntas=[
                ('¿Cuál es el centro de control del cuerpo?', 'El sistema nervioso',
                 ['El sistema digestivo', 'Los huesos', 'La piel']),
                ('¿Qué órgano piensa, siente y guarda tus recuerdos?', 'El cerebro',
                 ['El corazón', 'El estómago', 'Los pulmones']),
                ('La médula espinal está protegida por…', 'La columna vertebral', ['Las costillas', 'El cabello', 'Las uñas']),
                ('Las células del sistema nervioso se llaman…', 'Neuronas', ['Glóbulos rojos', 'Huesos', 'Píxeles']),
                ('¿Qué pasa en tu cerebro cuando aprendes algo nuevo?', 'Las neuronas hacen nuevas conexiones',
                 ['Se borra lo anterior', 'Se hace más chico', 'Nada']),
                ('¿Cómo cuidas tu cerebro al andar en bicicleta?', 'Usando casco',
                 ['Yendo más rápido', 'Sin agarrar el manubrio', 'Con los ojos cerrados']),
            ]),
            mision('Mensajeros veloces', 'presencial', leccion(
                intro='Las neuronas se pasan mensajes en milésimas de segundo. ¡Mide tu velocidad de reacción!',
                saber='Tus ojos ven caer la regla → el mensaje viaja al cerebro → el cerebro manda la orden por la médula '
                      'y los nervios → tus dedos se cierran. ¡Todo en menos de un segundo!',
                material=['Una regla de 30 cm', 'Tu cuaderno'],
                pasos=['En parejas: uno sostiene la regla colgando desde el número 30; el otro pone el pulgar y el índice '
                       'abiertos a la altura del 0, sin tocarla.',
                       'Sin avisar, el primero suelta la regla y el otro la atrapa lo más rápido posible.',
                       'Anota en qué número la atrapó: mientras más bajo, más rápido fue el mensaje.',
                       'Hagan 3 intentos cada uno. ¿Mejoró con la práctica?'],
                logro=['Explicas el camino del mensaje: ojos → cerebro → médula y nervios → mano.']), xp=50),
            mision('Imágenes en tu expediente', 'evidencia', leccion(
                intro='Un buen expediente tiene imágenes. Agrega una imagen del cerebro o del sistema nervioso.',
                saber=['Insertar → Imágenes → «Este dispositivo» (una imagen guardada) o «Imágenes en línea» (buscarla '
                       'en internet).',
                       'Para cambiar el tamaño sin deformarla, arrastra desde una ESQUINA, no desde los lados.',
                       'Ajustar texto (el ícono junto a la imagen): «Cuadrado» acomoda el texto alrededor.',
                       'Escribe de dónde tomaste la imagen.'],
                pasos=['Abre Memoria_TuNombre. Escribe el subtítulo El centro de control y un párrafo de 3 renglones '
                       'sobre el cerebro y las neuronas.',
                       'Coloca el cursor al inicio del párrafo e inserta una imagen del cerebro.',
                       'Hazla más pequeña desde una esquina.',
                       'Elige Ajustar texto → Cuadrado y acomódala a la derecha del párrafo.',
                       'Debajo escribe: Imagen tomada de: (nombre de la página). Guarda.'],
                logro=['La imagen no está deformada y el texto la rodea.'],
                entrega='sube una captura de tu página con la imagen.'), xp=90, monedas=25),
        ]},
        {'nombre': '¡Caso resuelto! Memoria de acero', 'cofre': 50, 'misiones': [
            mision('¿Ayuda o daña a tu memoria?', 'juego', leccion(
                intro='¿Cada hábito fortalece tu memoria o la debilita? Clasifícalos.'), juego='clasifica_memoria'),
            mision('Cierra el expediente', 'evidencia', leccion(
                intro='Termina tu documento con los hábitos para una memoria de acero y revísalo como un profesional.',
                saber=['Revisión ortográfica: las palabras con subrayado rojo pueden estar mal escritas. Da clic derecho '
                       'sobre ellas para ver sugerencias, o presiona F7 para revisar todo el documento.',
                       'Estilos (pestaña Inicio): «Título 1» en los subtítulos hace que todo el documento se vea ordenado.',
                       'Guardar como PDF: Archivo → Guardar como → Tipo: PDF. Así nadie desacomoda tu formato.'],
                pasos=['Agrega el subtítulo Hábitos para una memoria de acero y una lista con viñetas de 5 hábitos.',
                       'Escribe una conclusión: ¿cuál es el secreto para «viajar en el tiempo» con la memoria?',
                       'Aplica el estilo «Título 1» a todos tus subtítulos.',
                       'Revisa la ortografía con F7 o con clic derecho en cada palabra subrayada.',
                       'Guarda tu documento y también una copia en PDF.'],
                logro=['Tu expediente tiene título, recuerdo, listas, imagen, hábitos y conclusión, sin palabras '
                       'subrayadas en rojo.'],
                entrega='sube una captura de tu documento terminado.'), xp=100, monedas=30),
            mision('Mente sospechosa en internet', 'juego', leccion(
                intro='Una mente sospechosa también se cuida en internet. ¿Cada situación es segura o peligrosa?',
                saber=['Nunca compartas tu contraseña, tu dirección ni tu escuela con desconocidos.',
                       'Si algo te incomoda o te asusta en internet, cuéntaselo a un adulto de confianza.']),
                juego='clasifica_seguridad'),
            jefe('Jefe: El Ladrón de Recuerdos',
                 'El Ladrón de Recuerdos quiere borrar la memoria de toda la agencia. Demuestra que conoces tu cerebro y '
                 'que dominas el procesador de textos para detenerlo.', [
                     ('Recuerdas tu cumpleaños de hace 3 años. ¿Qué memoria usas?', 'De largo plazo',
                      ['Sensorial', 'De corto plazo', 'Ninguna']),
                     ('¿Qué parte del sistema nervioso lleva los mensajes entre el cerebro y el cuerpo?', 'La médula espinal',
                      ['El estómago', 'El cabello', 'Los dientes']),
                     ('¿Qué hábito ayuda a tu memoria?', 'Dormir bien',
                      ['Desvelarse', 'Saltarse el desayuno', 'Estudiar con la tele prendida']),
                     ('Para dar formato a una palabra, primero debes…', 'Seleccionarla',
                      ['Borrarla', 'Imprimirla', 'Cerrar el documento']),
                     ('¿Qué tecla usas para empezar un párrafo nuevo?', 'Enter', ['Retroceso', 'Shift', 'Esc']),
                     ('¿Cuándo usas una lista numerada en lugar de viñetas?',
                      'Cuando el orden importa, como los pasos de una receta', ['Siempre', 'Nunca', 'Cuando hay imágenes']),
                     ('Para agrandar una imagen sin deformarla la arrastras desde…', 'Una esquina',
                      ['El centro', 'Un lado', 'La barra de título']),
                     ('¿Qué significa una palabra con subrayado rojo en el procesador de textos?',
                      'Que puede estar mal escrita', ['Que es importante', 'Que es un enlace', 'Que se va a borrar']),
                 ]),
        ]},
    ],
}
