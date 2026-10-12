"""
Reglas de los minijuegos: configuración de cada plantilla, calificación de las partidas
y premios. Los juegos corren en el navegador (static/js/juegos.js); aquí se valida el
resultado y se entrega el botín a través del motor de gamificación.
"""
import unicodedata
from datetime import datetime, time, timedelta

from django.db import transaction
from django.db.models import Max, Q
from django.utils import timezone

from . import gamificacion as motor
from .models import Alumno, Juego, Mision, PartidaJuego, ProgresoMision

PLANTILLAS_INFO = {
    'meteoros': {
        'emoji': '☄️', 'nombre': 'Mecanografía de meteoros', 'color': '#7c3aed',
        'corto': 'Escribe las palabras para destruir los meteoros',
        'como': 'Los meteoros caen con palabras. Escríbelas para destruirlos antes de que toquen tu base.',
        'meta': 'meteoros',
    },
    'teclado': {
        'emoji': '⌨️', 'nombre': 'Teclado misterioso', 'color': '#0891b2',
        'corto': 'Encuentra cada tecla en tu teclado',
        'como': 'Aparece una letra misteriosa. Encuéntrala en tu teclado y presiónala lo más rápido que puedas.',
        'meta': 'teclas',
    },
    'clasifica': {
        'emoji': '🕵️', 'nombre': 'Detective digital', 'color': '#db2777',
        'corto': 'Clasifica cada tarjeta en su grupo',
        'como': 'Aparece una tarjeta. Mándala a su grupo correcto: tócalo, arrastra la tarjeta o usa las flechas del teclado.',
        'meta': 'tarjetas',
    },
    'robot': {
        'emoji': '🤖', 'nombre': 'Robot programador', 'color': '#ea580c',
        'corto': 'Programa al robot para llegar a la batería',
        'como': 'Arma una secuencia de instrucciones y presiona ▶ para que el robot llegue a la batería sin chocar.',
        'meta': 'laberintos',
    },
    'atajos': {
        'emoji': '🥷', 'nombre': 'Atajos ninja', 'color': '#4f46e5',
        'corto': 'Usa el atajo de teclado correcto',
        'como': 'Aparece una situación. Presiona en tu teclado el atajo que la resuelve, como Ctrl + C para copiar.',
        'meta': 'atajos',
    },
    'mensaje': {
        'emoji': '🔐', 'nombre': 'Mensaje secreto', 'color': '#059669',
        'corto': 'Descifra palabras con una tabla de códigos',
        'como': 'Cada símbolo es una letra. Usa la tabla de pistas para descifrar la palabra secreta y escríbela.',
        'meta': 'mensajes',
    },
    'rutas': {
        'emoji': '📁', 'nombre': 'Explorador de rutas', 'color': '#ca8a04',
        'corto': 'Encuentra el archivo navegando carpetas',
        'como': 'Abre carpetas en el explorador hasta encontrar el archivo que te piden, con la menor cantidad de clics.',
        'meta': 'archivos',
    },
    'formato': {
        'emoji': '🎨', 'nombre': 'Copia el formato', 'color': '#2563eb',
        'corto': 'Iguala el formato del texto modelo',
        'como': 'Selecciona palabras y usa la barra de herramientas (negrita, cursiva, color…) para que tu texto quede igual al modelo.',
        'meta': 'textos',
    },
}

# Segundos entre meteoros y lo que tarda uno en caer, según la velocidad elegida
VELOCIDADES = {
    'lenta': {'intervalo': 2.8, 'caida': 10.0},
    'normal': {'intervalo': 2.1, 'caida': 7.5},
    'rapida': {'intervalo': 1.6, 'caida': 5.8},
}

CONJUNTOS_TECLAS = {
    'central': 'ASDFGHJKLÑ',
    'superior': 'QWERTYUIOP',
    'inferior': 'ZXCVBNM',
    'letras': 'QWERTYUIOPASDFGHJKLÑZXCVBNM',
    'numeros': '1234567890',
    'todo': 'QWERTYUIOPASDFGHJKLÑZXCVBNM1234567890',
}
TECLAS_VALIDAS = set(CONJUNTOS_TECLAS['todo'])

TEMAS_PALABRAS = {
    'computadora': ('🖥️', 'Partes de la PC', ['monitor', 'teclado', 'mouse', 'bocina', 'cpu', 'memoria', 'disco',
                                              'puerto', 'cable', 'pantalla', 'audifonos', 'impresora', 'camara']),
    'internet': ('🌐', 'Internet', ['correo', 'navegador', 'enlace', 'pagina', 'buscar', 'red', 'wifi', 'nube',
                                     'descarga', 'usuario', 'archivo', 'servidor', 'router']),
    'programacion': ('🧩', 'Programación', ['codigo', 'bucle', 'variable', 'funcion', 'algoritmo', 'bloque', 'evento',
                                             'repetir', 'sensor', 'condicion', 'error', 'scratch', 'orden']),
    'robotica': ('🤖', 'Robótica', ['robot', 'motor', 'led', 'arduino', 'circuito', 'sensor', 'bateria', 'rueda',
                                     'servo', 'boton', 'resistencia', 'energia', 'chip']),
    'seguridad': ('🔒', 'Seguridad digital', ['contraseña', 'privado', 'respeto', 'virus', 'antivirus', 'cuidado',
                                               'secreto', 'bloquear', 'reportar', 'seguro', 'perfil', 'candado']),
    'office': ('📄', 'Word y Excel', ['negrita', 'fuente', 'tabla', 'celda', 'fila', 'columna', 'formula', 'guardar',
                                      'imprimir', 'imagen', 'titulo', 'copiar', 'pegar']),
}

# Detective digital: grupos listos para usar (nombre, emoji y sus tarjetas)
TEMAS_CLASIFICA = {
    'seguridad': ('🛡️', '¿Seguro o peligroso?', [
        ('Seguro', '✅', ['Pedir permiso antes de descargar un juego', 'Usar una contraseña difícil de adivinar',
                         'Contarle a un adulto si algo te incomoda', 'Cerrar sesión en una compu compartida',
                         'Abrir el enlace que tu maestro comparte en clase', 'Preguntar antes de publicar una foto de alguien',
                         'Tapar la cámara cuando no la usas', 'Mantener actualizado el antivirus']),
        ('Peligroso', '⚠️', ['Darle tu contraseña a un amigo', 'Abrir un correo que dice «¡Ganaste un celular!»',
                            'Aceptar a desconocidos en un videojuego', 'Mandar tu dirección a alguien que no conoces',
                            'Descargar programas de páginas raras', 'Usar 1234 como contraseña',
                            'Escribir los datos de la tarjeta de tus papás', 'Platicar en secreto con un desconocido']),
    ]),
    'privacidad': ('🔒', '¿Público o privado?', [
        ('Lo puedo compartir', '🌍', ['Mi color favorito', 'Mi caricatura favorita', 'Mi deporte favorito',
                                      'Mi comida favorita', 'Un dibujo que hice', 'Mi animal favorito', 'Mi canción favorita']),
        ('Es privado', '🔒', ['Mi contraseña', 'Mi dirección', 'Mi número de teléfono', 'Mi fecha de nacimiento completa',
                              'El nombre de mi escuela', 'Dónde estoy ahora mismo', 'Una foto de mi casa']),
    ]),
    'dispositivos': ('🖥️', 'Entrada, salida o almacenamiento', [
        ('Entrada', '⌨️', ['Teclado', 'Mouse', 'Micrófono', 'Cámara web', 'Escáner', 'Control de videojuegos']),
        ('Salida', '🔊', ['Monitor', 'Bocinas', 'Impresora', 'Audífonos', 'Proyector']),
        ('Almacenamiento', '💾', ['Memoria USB', 'Disco duro', 'Tarjeta SD', 'Disco SSD', 'La nube']),
    ]),
    'hardware': ('💿', '¿Hardware o software?', [
        ('Hardware', '🔧', ['Teclado', 'Monitor', 'Procesador', 'Memoria RAM', 'Mouse', 'Impresora', 'Tarjeta madre']),
        ('Software', '💿', ['Word', 'Scratch', 'Windows', 'Navegador web', 'Antivirus', 'Paint', 'Un videojuego']),
    ]),
    'robotica': ('🤖', '¿Sensor o actuador?', [
        ('Sensor', '👀', ['Sensor ultrasónico', 'Botón', 'Sensor de luz', 'Sensor de temperatura', 'Sensor de movimiento',
                         'Sensor de humedad']),
        ('Actuador', '⚙️', ['Motor', 'LED', 'Buzzer', 'Servomotor', 'Pantalla LCD', 'Ventilador']),
    ]),
}

# Robot programador: tamaño del laberinto, obstáculos y largo del camino más corto
DIFICULTADES_ROBOT = {
    'facil': {'tam': 5, 'obstaculos': [3, 5], 'camino': [3, 6]},
    'media': {'tam': 6, 'obstaculos': [6, 9], 'camino': [5, 9]},
    'dificil': {'tam': 7, 'obstaculos': [11, 15], 'camino': [8, 13]},
}

# Atajos ninja: solo atajos que el navegador deja atrapar (nunca Ctrl+W, Ctrl+T ni Ctrl+N)
ATAJOS = {
    'copiar': ('C', 'Copiar', '📋', ['Quieres copiar el texto que seleccionaste', 'Vas a duplicar una imagen para tu presentación']),
    'pegar': ('V', 'Pegar', '📌', ['Ya copiaste el texto: ahora ponlo en tu documento', 'Quieres poner aquí la imagen que copiaste']),
    'cortar': ('X', 'Cortar', '✂️', ['Quieres mover este párrafo a otra página', 'Quieres quitar una frase y ponerla más abajo']),
    'deshacer': ('Z', 'Deshacer', '↩️', ['¡Ups! Borraste un párrafo sin querer', 'Pintaste de rojo todo el dibujo por error']),
    'rehacer': ('Y', 'Rehacer', '↪️', ['Deshiciste algo y te arrepentiste', 'Quieres recuperar el cambio que acabas de deshacer']),
    'todo': ('A', 'Seleccionar todo', '🔲', ['Necesitas seleccionar todo el documento', 'Quieres cambiar la letra de todo el texto de un jalón']),
    'guardar': ('S', 'Guardar', '💾', ['Terminaste tu tarea y no quieres perderla', 'Se va a ir la luz y no has guardado']),
    'imprimir': ('P', 'Imprimir', '🖨️', ['Quieres tu trabajo en papel para entregarlo', 'Necesitas sacar una copia de tu diploma']),
    'buscar': ('F', 'Buscar', '🔍', ['Necesitas encontrar la palabra «robot» en una página larga', 'Buscas tu nombre en la lista del grupo']),
    'negrita': ('B', 'Negrita', '🅱️', ['Quieres que el título se vea más grueso', 'Quieres resaltar una palabra importante']),
    'cursiva': ('I', 'Cursiva', '📐', ['Quieres inclinar las letras de una frase', 'Escribes el nombre de un libro y va inclinado']),
    'subrayado': ('U', 'Subrayado', '〰️', ['Quieres poner una línea debajo del título', 'La maestra pidió subrayar las palabras clave']),
}
GRUPOS_ATAJOS = {
    'texto': ('✏️', 'Editar texto', ['copiar', 'pegar', 'cortar', 'deshacer', 'rehacer', 'todo']),
    'archivo': ('💾', 'Archivo', ['guardar', 'imprimir', 'buscar']),
    'formato': ('🅱️', 'Formato', ['negrita', 'cursiva', 'subrayado']),
}

# Mensaje secreto
ALFABETO = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
CIFRADOS = {
    'simbolos': ('🔣', 'Símbolos', 'Cada letra es un dibujo. Ideal para los más pequeños.'),
    'cesar': ('🏛️', 'César', 'Cada letra se recorre unos lugares en el abecedario, como lo hacía Julio César.'),
    'morse': ('📡', 'Morse', 'Puntos y rayas, como los telegrafistas y los barcos.'),
    'binario': ('💻', 'Binario', 'Cada letra es un número escrito con ceros y unos, como lo guarda la computadora.'),
}

# Explorador de rutas y Copia el formato
DIFICULTADES_RUTAS = {'facil': 'Carpetas cerca, pocas opciones', 'media': 'Más carpetas y subcarpetas', 'dificil': 'Rutas largas con distractores'}
DIFICULTADES_FORMATO = {'facil': 'Un formato a todo el texto', 'media': 'Formato en algunas palabras', 'dificil': 'Varias palabras, color, tamaño y alineación'}
FRASES_FORMATO = [
    'Mi robot tiene dos motores', 'El teclado sirve para escribir', 'Guarda tu trabajo cada rato',
    'Arduino es una placa programable', 'La nube guarda mis archivos', 'Nunca compartas tu contraseña',
    'El monitor muestra la imagen', 'Scratch usa bloques de colores', 'Un sensor mide el mundo real',
    'Los LED encienden con poca energía',
]

NOTA_MINIMA = 50  # Desde aquí la partida cuenta como superada (1 estrella)


def estrellas_de(calificacion):
    """Mismos cortes que ProgresoMision.estrellas: 50 → ⭐, 70 → ⭐⭐, 90 → ⭐⭐⭐."""
    if calificacion >= 90:
        return 3
    if calificacion >= 70:
        return 2
    if calificacion >= NOTA_MINIMA:
        return 1
    return 0


def _entero(valor, minimo, maximo, defecto):
    try:
        return max(minimo, min(maximo, int(valor)))
    except (TypeError, ValueError):
        return defecto


def meta_sugerida(duracion, velocidad):
    """Meteoros que un alumno promedio puede destruir: cerca del 70 % de los que caen."""
    intervalo = VELOCIDADES.get(velocidad, VELOCIDADES['normal'])['intervalo']
    return max(5, round(duracion / intervalo * 0.7))


def configuracion(juego):
    """Configuración completa y saneada (con valores por defecto) para mostrar y calificar."""
    datos = juego.configuracion or {}
    if juego.plantilla == 'atajos':
        atajos = [a for a in dict.fromkeys(datos.get('atajos') or []) if a in ATAJOS]
        return {
            'atajos': atajos if len(atajos) >= 2 else list(GRUPOS_ATAJOS['texto'][2]),
            'catalogo': {clave: {'tecla': t, 'nombre': n, 'emoji': e, 'situaciones': sit}
                         for clave, (t, n, e, sit) in ATAJOS.items()},
            'rondas': _entero(datos.get('rondas'), 5, 40, 10),
            'modo': 'ninja' if datos.get('modo') == 'ninja' else 'aprende',
        }
    if juego.plantilla == 'mensaje':
        palabras = [p for p in dict.fromkeys(normalizar_secreto(p) for p in datos.get('palabras') or []) if 2 <= len(p) <= 12]
        if len(palabras) < 3:
            palabras = [normalizar_secreto(p) for p in TEMAS_PALABRAS['computadora'][2] if 2 <= len(normalizar_secreto(p)) <= 12]
        return {
            'cifrado': datos.get('cifrado') if datos.get('cifrado') in CIFRADOS else 'simbolos',
            'palabras': palabras[:60],
            'rondas': min(_entero(datos.get('rondas'), 3, 20, 5), len(palabras)),
            'desplazamiento': _entero(datos.get('desplazamiento'), 1, 5, 3),
            'intentos': 3,
        }
    if juego.plantilla == 'rutas':
        return {
            'modo': 'buscar' if datos.get('modo') == 'buscar' else 'ruta',
            'dificultad': datos.get('dificultad') if datos.get('dificultad') in DIFICULTADES_RUTAS else 'facil',
            'rondas': _entero(datos.get('rondas'), 3, 20, 5),
        }
    if juego.plantilla == 'formato':
        frases = []
        for frase in datos.get('frases') or []:
            frase = ' '.join(str(frase).split())[:60]
            if len(frase.split()) >= 2 and frase not in frases:
                frases.append(frase)
        return {
            'dificultad': datos.get('dificultad') if datos.get('dificultad') in DIFICULTADES_FORMATO else 'facil',
            'rondas': _entero(datos.get('rondas'), 3, 20, 5),
            'frases': frases[:40] if len(frases) >= 3 else list(FRASES_FORMATO),
            'intentos': 3,
        }
    if juego.plantilla == 'clasifica':
        return configuracion_clasifica(datos)
    if juego.plantilla == 'robot':
        dificultad = datos.get('dificultad') if datos.get('dificultad') in DIFICULTADES_ROBOT else 'facil'
        return {
            'dificultad': dificultad,
            'niveles': _entero(datos.get('niveles'), 1, 12, 5),
            'modo': 'giros' if datos.get('modo') == 'giros' else 'flechas',
            'bucles': bool(datos.get('bucles')),
            'intentos': 3,
            'tablero': DIFICULTADES_ROBOT[dificultad],
        }
    if juego.plantilla == 'teclado':
        conjunto = datos.get('conjunto') if datos.get('conjunto') in CONJUNTOS_TECLAS or datos.get('conjunto') == 'personalizado' else 'central'
        teclas = ''.join(dict.fromkeys(c for c in str(datos.get('teclas', '')).upper() if c in TECLAS_VALIDAS))
        if conjunto != 'personalizado' or len(teclas) < 2:
            teclas = CONJUNTOS_TECLAS['central' if conjunto == 'personalizado' else conjunto]
        return {
            'conjunto': conjunto,
            'teclas': teclas,
            'rondas': _entero(datos.get('rondas'), 5, 60, 20),
            'modo': 'reto' if datos.get('modo') == 'reto' else 'guiado',
        }
    velocidad = datos.get('velocidad') if datos.get('velocidad') in VELOCIDADES else 'normal'
    duracion = _entero(datos.get('duracion'), 30, 300, 60)
    palabras = []
    for palabra in datos.get('palabras') or []:
        palabra = ' '.join(str(palabra).split())[:20]
        if palabra and palabra.lower() not in (p.lower() for p in palabras):
            palabras.append(palabra)
    if len(palabras) < 3:
        palabras = list(TEMAS_PALABRAS['computadora'][2])
    return {
        'palabras': palabras[:200],
        'duracion': duracion,
        'velocidad': velocidad,
        'vidas': _entero(datos.get('vidas'), 1, 10, 3),
        'meta': _entero(datos.get('meta'), 1, 300, meta_sugerida(duracion, velocidad)),
        'acentos': 'exactos' if datos.get('acentos') == 'exactos' else 'opcionales',
        **VELOCIDADES[velocidad],
    }


def normalizar_secreto(palabra):
    """Mayúsculas sin acentos (la Ñ se queda) y solo letras: así se puede cifrar con cualquier código."""
    palabra = str(palabra).upper().replace('Ñ', '\x00')
    palabra = unicodedata.normalize('NFD', palabra)
    palabra = ''.join(c for c in palabra if unicodedata.category(c) != 'Mn').replace('\x00', 'Ñ')
    return ''.join(c for c in palabra if c in ALFABETO)


def configuracion_clasifica(datos):
    """Entre 2 y 3 grupos con al menos una tarjeta cada uno; si no, se usa el tema «¿Seguro o peligroso?»."""
    categorias = []
    for categoria in (datos.get('categorias') or [])[:3]:
        if not isinstance(categoria, dict):
            continue
        nombre = ' '.join(str(categoria.get('nombre', '')).split())[:30]
        tarjetas = []
        for tarjeta in categoria.get('tarjetas') or []:
            tarjeta = ' '.join(str(tarjeta).split())[:70]
            if tarjeta and tarjeta not in tarjetas:
                tarjetas.append(tarjeta)
        if nombre and tarjetas:
            categorias.append({'nombre': nombre, 'emoji': str(categoria.get('emoji') or '📁')[:10], 'tarjetas': tarjetas[:40]})
    if len(categorias) < 2:
        categorias = [{'nombre': n, 'emoji': e, 'tarjetas': list(t)} for n, e, t in TEMAS_CLASIFICA['seguridad'][2]]
    total = sum(len(c['tarjetas']) for c in categorias)
    return {
        'tema': datos.get('tema') if datos.get('tema') in TEMAS_CLASIFICA else 'personalizado',
        'categorias': categorias,
        'rondas': min(_entero(datos.get('rondas'), 5, 40, 10), total),
        'tiempo': _entero(datos.get('tiempo'), 0, 30, 8),
    }


def descripcion_meta(juego, cfg=None):
    cfg = cfg or configuracion(juego)
    if juego.plantilla == 'atajos':
        return f"Resuelve {cfg['rondas']} situaciones con el atajo correcto"
    if juego.plantilla == 'mensaje':
        return f"Descifra {cfg['rondas']} mensajes secretos"
    if juego.plantilla == 'rutas':
        return f"Encuentra {cfg['rondas']} archivos con pocos clics"
    if juego.plantilla == 'formato':
        return f"Copia el formato de {cfg['rondas']} textos"
    if juego.plantilla == 'clasifica':
        return f"Clasifica {cfg['rondas']} tarjetas sin equivocarte"
    if juego.plantilla == 'robot':
        return f"Resuelve {cfg['niveles']} laberintos programando al robot"
    if juego.plantilla == 'teclado':
        return f"Encuentra {cfg['rondas']} teclas sin equivocarte"
    return f"Destruye {cfg['meta']} meteoros en {cfg['duracion']} segundos"


def datos_juego(juego):
    """Lo que el motor de juegos (static/js/juegos.js) necesita para arrancar."""
    cfg = configuracion(juego)
    return {
        'id': juego.id, 'nombre': juego.nombre, 'icono': juego.icono, 'plantilla': juego.plantilla,
        'descripcion': juego.descripcion, 'config': cfg, 'meta': descripcion_meta(juego, cfg),
        'info': PLANTILLAS_INFO[juego.plantilla],
    }


def calificar_partida(juego, datos, segundos):
    """
    Convierte lo que reporta el navegador en una calificación de 0 a 100. Cada número se
    limita a lo que es posible en el tiempo jugado para que no se pueda inflar a mano.
    Devuelve None si la partida es imposible (por ejemplo, terminada en un instante).
    """
    cfg = configuracion(juego)
    if juego.plantilla in ('atajos', 'mensaje', 'rutas', 'formato'):
        return _calificar_rondas(cfg['rondas'], datos, segundos, {'atajos': 0.4, 'mensaje': 2, 'rutas': 1.5, 'formato': 2}[juego.plantilla])
    if juego.plantilla == 'clasifica':
        rondas = cfg['rondas']
        completadas = _entero(datos.get('completadas'), 0, rondas, 0)
        if completadas and segundos < completadas * 0.35:
            return None
        aciertos = _entero(datos.get('aciertos'), 0, completadas, 0)
        rapidas = _entero(datos.get('rapidas'), 0, aciertos, 0)
        calificacion = round(aciertos * 100 / rondas)
        return {
            'calificacion': calificacion, 'estrellas': estrellas_de(calificacion),
            'puntaje': aciertos * 100 + rapidas * 50, 'aciertos': aciertos, 'errores': completadas - aciertos,
            'precision': round(aciertos * 100 / completadas) if completadas else 0, 'ppm': 0, 'duracion': round(segundos),
        }
    if juego.plantilla == 'robot':
        niveles = cfg['niveles']
        resueltos = _entero(datos.get('resueltos'), 0, niveles, 0)
        if resueltos and segundos < resueltos * 1.5:
            return None
        perfectos = _entero(datos.get('perfectos'), 0, resueltos, 0)
        errores = _entero(datos.get('errores'), 0, niveles * cfg['intentos'], 0)
        calificacion = round(resueltos * 100 / niveles)
        intentos = resueltos + errores
        return {
            'calificacion': calificacion, 'estrellas': estrellas_de(calificacion),
            'puntaje': resueltos * 150 + perfectos * 75, 'aciertos': resueltos, 'errores': errores,
            'precision': round(resueltos * 100 / intentos) if intentos else 0, 'ppm': 0, 'duracion': round(segundos),
        }
    if juego.plantilla == 'teclado':
        rondas = cfg['rondas']
        completadas = _entero(datos.get('completadas'), 0, rondas, 0)
        if completadas and segundos < completadas * 0.2:
            return None
        aciertos = _entero(datos.get('aciertos'), 0, completadas, 0)
        errores = _entero(datos.get('errores'), 0, 5000, 0)
        rapidas = _entero(datos.get('rapidas'), 0, aciertos, 0)
        calificacion = round(aciertos * 100 / rondas)
        presionadas = completadas + errores
        return {
            'calificacion': calificacion,
            'estrellas': estrellas_de(calificacion),
            'puntaje': aciertos * 100 + (completadas - aciertos) * 40 + rapidas * 50,
            'aciertos': aciertos,
            'errores': errores,
            'precision': round(completadas * 100 / presionadas) if presionadas else 0,
            'ppm': 0,
            'duracion': round(segundos),
        }

    segundos = min(segundos, cfg['duracion'] + 15)
    maximos = int(segundos / (cfg['intervalo'] * 0.5)) + 3
    destruidos = _entero(datos.get('destruidos'), 0, maximos, 0)
    caracteres = _entero(datos.get('caracteres'), 0, destruidos * 20, 0)
    errores = _entero(datos.get('errores'), 0, 5000, 0)
    vidas = _entero(datos.get('vidas'), 0, cfg['vidas'], 0)
    calificacion = min(100, round(destruidos * 100 / cfg['meta']))
    teclas = caracteres + errores
    return {
        'calificacion': calificacion,
        'estrellas': estrellas_de(calificacion),
        'puntaje': caracteres * 10 + destruidos * 20 + vidas * 50,
        'aciertos': destruidos,
        'errores': errores,
        'precision': round(caracteres * 100 / teclas) if teclas else 0,
        'ppm': min(200, round((caracteres / 5) / (segundos / 60))) if segundos >= 5 else 0,
        'duracion': round(segundos),
    }


def _calificar_rondas(rondas, datos, segundos, minimo_por_ronda):
    """Juegos por rondas: cada acierto vale 100 y si salió perfecto (sin errores ni pistas) 50 más."""
    completadas = _entero(datos.get('completadas'), 0, rondas, 0)
    if completadas and segundos < completadas * minimo_por_ronda:
        return None
    aciertos = _entero(datos.get('aciertos'), 0, completadas, 0)
    perfectos = _entero(datos.get('perfectos'), 0, aciertos, 0)
    errores = _entero(datos.get('errores'), 0, 5000, 0)
    calificacion = round(aciertos * 100 / rondas)
    intentos = aciertos + errores
    return {
        'calificacion': calificacion, 'estrellas': estrellas_de(calificacion),
        'puntaje': aciertos * 100 + perfectos * 50, 'aciertos': aciertos, 'errores': errores,
        'precision': round(aciertos * 100 / intentos) if intentos else 0, 'ppm': 0, 'duracion': round(segundos),
    }


# ========================
# ARCADE
# ========================
def juegos_arcade(clase):
    return Juego.objects.filter(activo=True, en_arcade=True).filter(Q(clase=clase) | Q(clase__isnull=True))


def inicio_semana():
    hoy = timezone.localdate()
    return timezone.make_aware(datetime.combine(hoy - timedelta(days=hoy.weekday()), time.min))


def _premio_cobrado_hoy(alumno, juego, excluir=None):
    partidas = PartidaJuego.objects.filter(alumno=alumno, juego=juego, mision__isnull=True, terminada=True,
                                           monedas__gt=0, inicio__date=timezone.localdate())
    if excluir:
        partidas = partidas.exclude(pk=excluir)
    return partidas.exists()


def bloqueado_en_arcade(alumno, clase, juego):
    """Con desbloqueo «por misión», el juego se abre al aprobar su misión del mapa en esta clase."""
    if juego.desbloqueo != 'mision':
        return False
    misiones = Mision.objects.filter(clase=clase, juego=juego, activa=True)
    if not misiones.exists():
        return False
    return not ProgresoMision.objects.filter(alumno=alumno, mision__in=misiones, estado='aprobado').exists()


def ranking_juego(juego, clase, desde=None, limite=10):
    partidas = PartidaJuego.objects.filter(juego=juego, clase=clase, terminada=True, alumno__activo=True)
    if desde:
        partidas = partidas.filter(inicio__gte=desde)
    filas = (partidas.values('alumno_id', 'alumno__nombre', 'alumno__apellido')
             .annotate(mejor=Max('puntaje')).order_by('-mejor', 'alumno__nombre')[:limite])
    return [{'alumno_id': f['alumno_id'], 'nombre': f['alumno__nombre'], 'apellido': f['alumno__apellido'],
             'puntaje': f['mejor']} for f in filas]


def estado_arcade(alumno, clase):
    """Juegos del Arcade con lo que el alumno necesita ver en cada máquina."""
    lista = []
    semana = inicio_semana()
    for juego in juegos_arcade(clase):
        cfg = configuracion(juego)
        propias = PartidaJuego.objects.filter(alumno=alumno, juego=juego, terminada=True)
        top = ranking_juego(juego, clase, desde=semana, limite=1)
        lista.append({
            'juego': juego,
            'info': PLANTILLAS_INFO[juego.plantilla],
            'meta': descripcion_meta(juego, cfg),
            'bloqueado': bloqueado_en_arcade(alumno, clase, juego),
            'record': propias.aggregate(m=Max('puntaje'))['m'],
            'estrellas': propias.aggregate(m=Max('estrellas'))['m'] or 0,
            'partidas': propias.count(),
            'premio_hoy': bool(juego.monedas_arcade) and not _premio_cobrado_hoy(alumno, juego),
            'top': top[0] if top else None,
        })
    return lista


# ========================
# PARTIDAS
# ========================
def mision_jugable(alumno, clase, mision):
    """La misión de minijuego se puede jugar si está desbloqueada en el mapa (o ya aprobada)."""
    ruta = motor.construir_ruta(alumno, clase)
    _, _, item = motor.buscar_en_ruta(ruta, mision.id)
    return bool(item and (item['desbloqueada'] or item['estado'] == 'aprobado'))


def terminar_partida(partida, datos):
    """Califica la partida, entrega el botín y devuelve el resumen para la pantalla final."""
    with transaction.atomic():
        partida = PartidaJuego.objects.select_for_update().select_related('juego', 'mision', 'alumno').get(pk=partida.pk)
        if partida.terminada:
            return None
        segundos = (timezone.now() - partida.inicio).total_seconds()
        resultado = calificar_partida(partida.juego, datos, segundos)
        if resultado is None:
            partida.terminada = True
            partida.save(update_fields=['terminada'])
            return None
        for campo, valor in resultado.items():
            setattr(partida, campo, valor)
        partida.terminada = True
        partida.save()

    juego, alumno, clase = partida.juego, partida.alumno, partida.clase
    mejor_antes = PartidaJuego.objects.filter(alumno=alumno, juego=juego, terminada=True).exclude(
        pk=partida.pk).aggregate(m=Max('puntaje'))['m']
    resumen = {
        **resultado,
        'monedas': 0, 'xp': 0, 'mision': None,
        'record': partida.puntaje > (mejor_antes or 0) and partida.puntaje > 0,
        'mejor': max(partida.puntaje, mejor_antes or 0),
        'mejor_antes': mejor_antes,
    }

    if partida.mision:
        mision = partida.mision
        progreso = ProgresoMision.objects.filter(alumno=alumno, mision=mision).first()
        aprobada_antes = bool(progreso and progreso.estado == 'aprobado')
        nota_antes = progreso.puntuacion if aprobada_antes else None
        estado = {'aprobada': aprobada_antes, 'primera': False, 'mejoro': False, 'nota_antes': nota_antes,
                  'estrellas_antes': progreso.estrellas if aprobada_antes else 0}
        if resultado['calificacion'] >= NOTA_MINIMA and (nota_antes is None or resultado['calificacion'] > nota_antes):
            progreso = progreso or ProgresoMision(alumno=alumno, mision=mision)
            monedas_antes = progreso.monedas_obtenidas if aprobada_antes else 0
            monedas_total = motor.calificar(progreso, resultado['calificacion'], avisar=False)
            ganadas = monedas_total - monedas_antes
            resumen['monedas'] = max(0, ganadas)
            resumen['xp'] = 0 if aprobada_antes else mision.xp_recompensa
            estado.update(aprobada=True, primera=not aprobada_antes, mejoro=aprobada_antes)
            if not aprobada_antes:
                motor.registrar_evento(alumno, 'misiones', clase=clase)
        resumen['mision'] = estado
    elif resultado['estrellas'] and juego.monedas_arcade and not _premio_cobrado_hoy(alumno, juego, excluir=partida.pk):
        motor.otorgar(alumno, monedas=juego.monedas_arcade, tipo='juego', descripcion=f'Arcade: {juego.nombre}',
                      clase=clase)
        resumen['monedas'] = juego.monedas_arcade
        resumen['premio_diario'] = True

    if resumen['monedas']:
        PartidaJuego.objects.filter(pk=partida.pk).update(monedas=resumen['monedas'])
    motor.registrar_evento(alumno, 'juegos', clase=clase)
    motor.verificar_logros(alumno)

    ranking = ranking_juego(juego, clase, desde=inicio_semana(), limite=100)
    resumen['ranking'] = ranking[:5]
    resumen['posicion'] = next((i for i, f in enumerate(ranking, start=1) if f['alumno_id'] == alumno.id), None)
    resumen['total_monedas'] = Alumno.objects.values_list('monedas', flat=True).get(pk=alumno.pk)
    return resumen
