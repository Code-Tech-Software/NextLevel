"""Mundo 9 · Gran final: algoritmos, depuración, el portafolio del año y una animación científica en Scratch que une
todo lo aprendido."""
from .base import LEYENDA_SCRATCH, jefe, leccion, mision, scratch

JUEGOS = {
    'robot_bucles': {'nombre': 'Robot programador: usa ciclos', 'icono': '🔁', 'plantilla': 'robot', 'en_arcade': True,
                     'descripcion': 'Caminos más largos: usa el bloque de repetir para programar menos.',
                     'configuracion': {'dificultad': 'media', 'niveles': 6, 'modo': 'flechas', 'bucles': True}},
}

CODIGO_BUGS = '''
OBJETO: Gato
al hacer clic en la bandera verde
    ir a x: 0 y: 0
    por siempre
        si <¿tecla flecha derecha presionada?> entonces
            cambiar x en -10
        si <¿tocando "Manzana"?> entonces
            cambiar "puntos" en 1
    fijar "puntos" a 0

OBJETO: Manzana
al hacer clic en la bandera verde
    ir a x: 150 y: 0
'''

CODIGO_FINAL = '''
OBJETO: Científico
al hacer clic en la bandera verde
    cambiar fondo a "Laboratorio"   (usa los nombres de tus fondos)
    decir "¡Hola! Hoy te explicaré el secreto de Gastón" durante 3 segundos
    enviar "escena2" y esperar
    preguntar "¿En qué se convierte el agua a 100 °C?" y esperar
    si <(respuesta) = "vapor"> entonces
        decir "¡Correcto! Eres un gran científico" durante 2 segundos
    si no
        decir "Casi: se convierte en vapor" durante 2 segundos

OBJETO: Gota
al hacer clic en la bandera verde
    esconder
al recibir "escena2"
    cambiar fondo a "Cocina"
    mostrar
    repetir 10
        cambiar tamaño en 5
        esperar 0.2 segundos
    decir "¡Con calor me evaporo!" durante 2 segundos
    esconder
'''

MUNDO = {
    'nombre': 'Galaxia del Código', 'tema': 'espacio',
    'descripcion': 'El gran final: algoritmos, ciclos y bugs. Ordena tu portafolio del año y crea en Scratch una '
                   'animación científica con todo lo que aprendiste.',
    'niveles': [
        {'nombre': 'Algoritmos', 'cofre': 30, 'misiones': [
            mision('Algoritmos en todas partes', 'cuestionario', leccion(
                intro='Un algoritmo es una receta de pasos. ¿Los sabes ordenar?',
                saber=['Un algoritmo es una serie de pasos ordenados para resolver algo, como una receta.',
                       'El orden importa: si cambias los pasos, el resultado cambia.',
                       'Un ciclo repite pasos; una condicional decide qué hacer según una pregunta.',
                       'Un bug es un error; depurar es encontrarlo y arreglarlo.']), xp=60, preguntas=[
                ('Un algoritmo es…', 'Una serie de pasos ordenados para resolver algo',
                 ['Un tipo de robot', 'Un virus', 'Una tecla']),
                ('¿Cuál es el orden correcto para lavarte los dientes?', 'Poner pasta → cepillar → enjuagar',
                 ['Enjuagar → guardar el cepillo → poner pasta', 'Cepillar → poner pasta → comprar el cepillo',
                  'Guardar el cepillo → cepillar → poner pasta']),
                ('Un ciclo (bucle) sirve para…', 'Repetir instrucciones varias veces',
                 ['Borrar el programa', 'Apagar la compu', 'Cambiar el color del teclado']),
                ('En programación, un «bug» es…', 'Un error en el programa',
                 ['Un insecto dentro de la compu', 'Un premio', 'Un juego']),
                ('Encontrar y arreglar los errores de un programa se llama…', 'Depurar',
                 ['Imprimir', 'Descargar', 'Dibujar']),
                ('«Si llueve, llevo paraguas» es un ejemplo de…', 'Una condicional', ['Un ciclo', 'Un bug', 'Una variable']),
            ]),
            mision('Robot humano', 'presencial', leccion(
                intro='Las computadoras hacen exactamente lo que les dices, ni más ni menos. ¡Compruébalo!',
                pasos=['En parejas: uno es el robot y el otro el programador.',
                       'El programador escribe en una hoja las instrucciones exactas para que el robot llegue a un objeto '
                       'del salón (avanza 3 pasos, gira a la derecha, repite 2 veces…).',
                       'El robot sigue la hoja AL PIE DE LA LETRA, sin adivinar.',
                       'Si el robot no llega, ¡busquen el bug, corríjanlo y vuelvan a probar!',
                       'Cambien de papel y usen al menos un «repetir».'],
                logro=['Su algoritmo lleva al robot a la meta y usa un ciclo.']), xp=50),
            mision('Robot programador: usa ciclos', 'juego', leccion(
                intro='Ahora los caminos son más largos. Usa el bloque de repetir para programar menos y llegar más lejos.'),
                xp=70, monedas=20, juego='robot_bucles'),
        ]},
        {'nombre': 'Laboratorio de bugs', 'cofre': 30, 'misiones': [
            mision('Depura el juego del gato', 'texto', leccion(
                intro='Este juego tiene 3 bugs. El gato debería moverse a la derecha con la flecha, empezar con 0 puntos '
                      'y ganar UN punto cada vez que toca la manzana.',
                saber=['Pista 1: revisa hacia dónde se mueve el gato con la flecha derecha.',
                       'Pista 2: hay un bloque que nunca se ejecuta. ¿Por qué? (Recuerda: «por siempre» nunca termina.)',
                       'Pista 3: la manzana nunca se mueve… ¿qué pasa con los puntos mientras el gato la sigue tocando?'],
                pasos=['Lee el código renglón por renglón (si quieres, ármalo en Scratch).',
                       'Encuentra los 3 bugs.',
                       'Escribe cada bug y cómo lo arreglarías.'],
                entrega='escribe aquí: «Bug 1: … · Arreglo: …» (los tres).'), xp=70, monedas=20,
                codigo=CODIGO_BUGS.strip('\n')),
            mision('La Hora del Código', 'link', leccion(
                intro='Millones de estudiantes del mundo programan en la Hora del Código. ¡Únete!',
                pasos=['Entra a code.org y busca la Hora del Código.',
                       'Elige una actividad en español para tu edad (por ejemplo, de Minecraft o de baile).',
                       'Complétala. Si te atoras, lee la pista y prueba de nuevo: ¡intenta, aprende, avanza!'],
                entrega='en el comentario, escribe qué fue lo más difícil y cómo lo resolviste.'),
                xp=70, monedas=20, link='https://code.org/'),
        ]},
        {'nombre': 'Mi portafolio del año', 'cofre': 30, 'misiones': [
            mision('Ordena tu carpeta del año', 'evidencia', leccion(
                intro='Un año de trabajo merece estar en orden. Revisa tu carpeta como un archivista profesional.',
                saber=['Mover un archivo: arrástralo a otra carpeta (o Cortar y Pegar).',
                       'Copiar: Ctrl + C y Ctrl + V. El archivo queda en los dos lugares.',
                       'Cambiar nombre: clic derecho → Cambiar nombre (o F2).',
                       'Eliminar lo manda a la Papelera de reciclaje; de ahí se puede recuperar.',
                       'Ordenar por nombre, fecha o tipo: clic derecho en un espacio vacío → Ordenar por.'],
                pasos=['Abre tu carpeta TIC_4A_TuNombre.',
                       'Revisa que cada trabajo esté en su subcarpeta (Scratch, Documentos, Presentaciones). Si no, muévelo.',
                       'Cambia el nombre de los archivos que no digan qué son.',
                       'Crea una subcarpeta Proyecto_final.',
                       'Ordena por fecha para ver tu primer y tu último trabajo del año.'],
                logro=['Cada archivo está en su carpeta y con un nombre que dice qué es.'],
                entrega='sube una captura de tu carpeta ordenada.'), xp=80, monedas=20),
        ]},
        {'nombre': 'Proyecto final', 'cofre': 50, 'misiones': [
            mision('Planea tu proyecto final', 'texto', leccion(
                intro='Tu proyecto final es una animación en Scratch que explique tu tema favorito del año.',
                pasos=['Elige un tema: el avión de Cleo, la materia misteriosa, las montañas, Enriqueta, la memoria, los '
                       'árboles, el helecho o la foto familiar.',
                       'Decide qué harás: una animación que explique el tema o un juego de preguntas.',
                       'Escribe tus personajes, tus fondos y qué pasa al inicio, en medio y al final.',
                       'Escribe qué usarás: ¿un ciclo?, ¿un mensaje?, ¿una condicional?, ¿una variable?'],
                entrega='escribe tu plan aquí abajo.'), xp=70, monedas=20),
            scratch('Proyecto final: animación científica en Scratch', leccion(
                intro='Crea en Scratch una animación que explique tu tema favorito del año con lo que aprendiste: '
                      'secuencias, ciclos, mensajes y condicionales.',
                saber=['Una animación cuenta una historia en escenas: cambia de fondo con «cambiar fondo a» y avisa a los '
                       'personajes con mensajes.',
                       'Usa «decir … durante … segundos» para los diálogos y «esperar» para que no hablen a la vez.',
                       'Puedes terminar con una pregunta: «preguntar … y esperar» y revisa la «respuesta» con un «si».',
                       LEYENDA_SCRATCH],
                pasos=['Sigue tu plan. Usa al menos 2 personajes y 2 fondos.',
                       'Usa el código de ejemplo como base y cámbialo a tu tema.',
                       'Agrega al menos un ciclo y un mensaje.',
                       'Pide a un compañero que la pruebe y corrige los bugs.',
                       'Guárdala en tu carpeta › Proyecto_final.'],
                logro=['Tu animación explica un tema del año con 2 personajes, 2 fondos, un ciclo y un mensaje.'],
                entrega='sube una captura de tu animación y de tus bloques.'), CODIGO_FINAL, xp=120, monedas=35),
            mision('Estreno en la galaxia', 'presencial', leccion(
                intro='¡Noche de estreno! Presenta tu animación al grupo.',
                pasos=['Proyecta tu animación (o déjala abierta para el recorrido).',
                       'Explica qué tema elegiste y qué bloques usaste.',
                       'Cuenta un bug que encontraste y cómo lo arreglaste.',
                       'Voten por la animación más clara, la más divertida y la más creativa.'],
                logro=['Explicaste tu proyecto y un bug que resolviste.']), xp=70, monedas=20),
            jefe('Jefe final: El Glitch Supremo',
                 '¡El Glitch Supremo quiere borrar todo lo que aprendiste este año! Demuestra que dominas la ciencia y la '
                 'tecnología para vencerlo de una vez por todas.', [
                     ('Cuando el chocolate se derrite con el calor ocurre una…', 'Fusión',
                      ['Condensación', 'Evaporación', 'Solidificación']),
                     ('¿Qué forma las cordilleras como los Andes?', 'El choque de placas tectónicas',
                      ['La lluvia', 'El viento de un día', 'Los ríos']),
                     ('¿Por qué una maceta necesita agujeros de drenaje?', 'Para que salga el agua que sobra',
                      ['Para decorar', 'Para que entre luz', 'Para que pese menos']),
                     ('Recordar tu primer día de escuela usa la memoria…', 'De largo plazo',
                      ['Sensorial', 'De corto plazo', 'De la computadora']),
                     ('Un objetivo bien escrito empieza con…', 'Un verbo en infinitivo, como «reducir» o «plantar»',
                      ['Un saludo', 'Una fecha', 'Un dibujo']),
                     ('¿Qué combinación de letra y fondo se lee mejor en una diapositiva?', 'Letra oscura sobre fondo claro',
                      ['Amarillo sobre blanco', 'Verde sobre verde', 'Gris claro sobre blanco']),
                     ('«Creo que la foto es de un cumpleaños.» Esto es…', 'Una hipótesis',
                      ['Un hecho', 'Un dato comprobado', 'Una evidencia']),
                     ('En Scratch, ¿qué bloque repite instrucciones sin parar?', 'Por siempre',
                      ['Esperar 1 segundos', 'Decir ¡Hola!', 'Ir a x: 0 y: 0']),
                     ('En Tinkercad, ¿qué herramienta sube una figura?', 'Elevar (el cono negro)',
                      ['Rotar', 'Hueco', 'Agrupar']),
                     ('Cuando tu programa falla, lo mejor es…', 'Buscar el error paso a paso y volver a intentarlo',
                      ['Rendirte', 'Culpar a la compu', 'Borrar todo el proyecto']),
                 ], xp=200, monedas=80),
        ]},
    ],
}
