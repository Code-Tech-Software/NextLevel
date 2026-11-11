import re
from urllib.parse import parse_qs, urlparse

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from Misiones import batallas
from Misiones.gamificacion import TEMA_INFO, TIPO_INFO
from Misiones.minijuegos import juegos_arcade
from Misiones.models import ArticuloTienda, Clase, CompraAlumno, ProgresoMision

register = template.Library()

COLORES_CLASE = {
    'indigo': ('#6366f1', '#4338ca'),
    'esmeralda': ('#10b981', '#047857'),
    'coral': ('#fb7185', '#e11d48'),
    'ambar': ('#f59e0b', '#d97706'),
    'cielo': ('#38bdf8', '#0284c7'),
    'uva': ('#a855f7', '#7e22ce'),
    'rosa': ('#f472b6', '#db2777'),
}

# Patrón en zigzag para los nodos del mapa (multiplicador del desplazamiento horizontal)
ZIGZAG = [0, 0.9, 1.4, 0.9, 0, -0.9, -1.4, -0.9]


# Imágenes de Cloudinary: tamaño máximo (en píxeles reales, el doble de lo que se ve, para pantallas nítidas)
TAMANOS_IMAGEN = {
    'avatar': 300,    # avatares (se ven de 26 a 150 px)
    'mini': 480,      # tienda, miniaturas de evidencias y vistas previas
    'mision': 1200,   # la imagen de la misión
    'grande': 1920,   # imagen ampliada (para leer bien una evidencia)
}
_SUBIDA_CLOUDINARY = '/image/upload/'


def imagen_optimizada(url, tamano='mini'):
    """La misma imagen de Cloudinary, en el formato más ligero que acepte el navegador (WebP/AVIF), con calidad
    automática y nunca más grande que `tamano`. No la recorta ni la agranda: se ve igual, pero pesa mucho menos.
    Cualquier otra dirección (DiceBear, archivos locales) se devuelve tal cual."""
    if not url or 'res.cloudinary.com' not in url or _SUBIDA_CLOUDINARY not in url:
        return url
    base, resto = url.split(_SUBIDA_CLOUDINARY, 1)
    if not re.match(r'v\d+/', resto):   # ya trae ajustes de Cloudinary: no se tocan
        return url
    lado = TAMANOS_IMAGEN.get(tamano, TAMANOS_IMAGEN['mini'])
    return f'{base}{_SUBIDA_CLOUDINARY}f_auto,q_auto,c_limit,w_{lado},h_{lado}/{resto}'


@register.filter
def imagen_web(archivo, tamano='mini'):
    """{{ mision.imagen|imagen_web:'mision' }} → dirección optimizada de una imagen subida ('' si no hay)."""
    try:
        url = archivo.url if archivo else ''
    except (ValueError, AttributeError):
        url = archivo if isinstance(archivo, str) else ''
    return imagen_optimizada(url, tamano)


@register.filter
def avatar_url(alumno):
    try:
        if alumno.avatar:
            return imagen_optimizada(alumno.avatar.url, 'avatar')
    except (ValueError, AttributeError):
        pass
    return (f'https://api.dicebear.com/9.x/bottts/svg?seed=nextlevel-{alumno.pk}'
            f'&backgroundColor=b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf,c7f9cc')


@register.filter
def tipo_info(tipo):
    return TIPO_INFO.get(tipo, TIPO_INFO['link'])


@register.filter
def tema_info(tema):
    return TEMA_INFO.get(tema, TEMA_INFO['bosque'])


@register.filter
def zigzag(indice):
    try:
        return ZIGZAG[int(indice) % len(ZIGZAG)]
    except (TypeError, ValueError):
        return 0


@register.filter
def calif10(puntuacion):
    try:
        return f'{int(puntuacion) / 10:.1f}'
    except (TypeError, ValueError):
        return '-'


@register.filter
def estrellas(cantidad):
    """[True, True, False] para pintar 2 de 3 estrellas."""
    try:
        cantidad = int(cantidad)
    except (TypeError, ValueError):
        cantidad = 0
    return [i < cantidad for i in range(3)]


@register.filter
def youtube_embed(url):
    if not url:
        return ''
    parsed = urlparse(url)
    video_id = ''
    if parsed.hostname in ('youtu.be',):
        video_id = parsed.path.lstrip('/')
    elif parsed.hostname and 'youtube.com' in parsed.hostname:
        if parsed.path == '/watch':
            video_id = parse_qs(parsed.query).get('v', [''])[0]
        else:
            match = re.match(r'^/(embed|shorts|live)/([^/?]+)', parsed.path)
            if match:
                video_id = match.group(2)
    if video_id and re.match(r'^[\w-]{6,20}$', video_id):
        return f'https://www.youtube-nocookie.com/embed/{video_id}?rel=0'
    return ''


@register.filter
def get_item(diccionario, clave):
    try:
        return diccionario.get(clave)
    except AttributeError:
        return None


@register.filter
def color_clase(color, indice=0):
    return COLORES_CLASE.get(color, COLORES_CLASE['indigo'])[int(indice)]


@register.filter
def porcentaje(valor, total):
    try:
        return int(int(valor) * 100 / int(total)) if int(total) else 0
    except (TypeError, ValueError):
        return 0


@register.filter
def restar(valor, otro):
    try:
        return int(valor) - int(otro)
    except (TypeError, ValueError):
        return valor


@register.filter
def multiplicar(valor, otro):
    try:
        return float(valor) * float(otro)
    except (TypeError, ValueError):
        return 0


@register.filter
def iniciales(alumno):
    return f'{(alumno.nombre or "?")[:1]}{(alumno.apellido or "")[:1]}'.upper()


@register.simple_tag
def notificaciones_alumno(alumno):
    if not alumno:
        return {'no_leidas': 0, 'recientes': [], 'celebraciones': []}
    no_leidas = alumno.notificaciones.filter(leida=False)
    celebraciones = [
        {'id': n.id, 'tipo': n.tipo, 'titulo': n.titulo, 'mensaje': n.mensaje, 'icono': n.icono}
        for n in no_leidas.filter(celebrar=True).order_by('fecha')[:5]
    ]
    return {
        'no_leidas': no_leidas.count(),
        'recientes': list(alumno.notificaciones.all()[:12]),
        'celebraciones': celebraciones,
    }


@register.simple_tag
def contadores_profesor():
    return {
        'revisiones': ProgresoMision.objects.filter(estado='pendiente').count(),
        'pedidos': CompraAlumno.objects.filter(estado='pendiente').count(),
        'stock_bajo': ArticuloTienda.objects.filter(activo=True, stock__isnull=False, stock__lte=3).count(),
    }


SECCIONES_MISION = ('📘', '🧰', '🛠️', '✅', '🧩', '⏱️', '👥', '⚠️')
ETIQUETAS_MISION = ('💡 Tip:', '📤 Entrega:')


@register.filter
def titulo_codigo(mision):
    """El nombre del recuadro de código de una misión: el sketch de Arduino, los bloques de Scratch o MakeCode o un
    diagrama de flujo."""
    codigo, link = mision.codigo or '', mision.link or ''
    if mision.tipo == 'arduino' or 'void setup' in codigo:
        return 'sketch.ino'
    if codigo.startswith('( INICIO )'):
        return 'diagrama de flujo'
    if 'makecode' in link:      # Arcade (arcade.makecode.com) y micro:bit (makecode.microbit.org)
        return 'bloques de MakeCode'
    if 'scratch.mit.edu' in link or '🏁' in codigo or 'OBJETO:' in codigo:
        return 'bloques de Scratch'
    return 'código'


@register.filter
def texto_mision(texto):
    """La descripción de una misión con sus secciones («📘 Lo que necesitas saber», «🛠️ Paso a paso»…) resaltadas."""
    bloques = []
    for parrafo in re.split(r'\n\s*\n', (texto or '').strip()):
        lineas = [escape(linea) for linea in parrafo.split('\n')]
        if len(lineas) > 1 and lineas[0].startswith(SECCIONES_MISION) and len(lineas[0]) <= 40:
            bloques.append(f'<div class="bloque-mision"><div class="seccion-mision">{lineas[0]}</div>'
                           f'<p>{"<br>".join(lineas[1:])}</p></div>')
            continue
        html = '<br>'.join(lineas)
        for etiqueta in ETIQUETAS_MISION:
            if html.startswith(etiqueta):
                html = f'<b>{etiqueta}</b>{html[len(etiqueta):]}'
        bloques.append(f'<p>{html}</p>')
    return mark_safe(''.join(bloques))


@register.simple_tag
def clases_vista_alumno():
    """Las clases que el profe puede recorrer como alumno desde el encabezado del panel."""
    return Clase.objects.filter(activa=True).order_by('anio', 'grado', 'grupo', 'nombre')


@register.filter
def sin_icono(texto):
    """'🌳 Bosque Encantado' -> 'Bosque Encantado'."""
    partes = str(texto).split(' ', 1)
    return partes[1] if len(partes) == 2 else texto


@register.filter
def nivel_calif(puntuacion):
    """Clase de color para una calificación de 0 a 100."""
    try:
        valor = float(puntuacion)
    except (TypeError, ValueError):
        return ''
    if valor > 10:
        valor = valor / 10
    if valor >= 9:
        return 'a'
    if valor >= 7:
        return 'b'
    if valor >= 6:
        return 'c'
    return 'd'


TIPOS_PRODUCTO = {
    'fisico': ('🎁', 'Físico', 'fisico'),
    'permiso': ('🎟️', 'Privilegio en clase', 'privilegio'),
    'avatar': ('💻', 'Digital · Avatar', 'digital'),
    'otro': ('💻', 'Digital', 'digital'),
}


@register.filter
def info_articulo(articulo):
    """Qué tipo de premio es y cómo lo recibe el alumno, para que no haya confusiones en la tienda."""
    emoji, texto, clase = TIPOS_PRODUCTO.get(articulo.tipo, TIPOS_PRODUCTO['otro'])
    if articulo.tipo == 'avatar':
        entrega = ('✨', 'Se equipa al instante')
    elif articulo.tipo == 'fisico':
        # Un objeto físico siempre pasa por las manos del profe, aunque no requiera validación
        entrega = ('🤝', 'Te lo entrega el profe')
    elif articulo.requiere_validacion:
        entrega = ('🤝', 'El profe lo autoriza') if articulo.tipo == 'permiso' else ('🤝', 'El profe lo activa')
    else:
        entrega = ('⚡', 'Lo recibes al instante')
    return {'emoji': emoji, 'texto': texto, 'clase': clase, 'entrega_emoji': entrega[0], 'entrega': entrega[1]}


@register.simple_tag
def hay_arcade(clase):
    """El menú del alumno muestra el Arcade solo si su clase tiene juegos ahí."""
    return juegos_arcade(clase).exists()


@register.simple_tag
def batalla_en_juego(clase):
    """La señal de la Batalla en vivo de la clase si hay una jugándose (para el aviso del alumno), o None."""
    if not clase:
        return None
    datos = batallas.senal(clase.id)
    return datos if batallas.en_juego(datos) else None


@register.simple_tag
def batallas_abiertas():
    """Batallas que siguen abiertas (para el aviso del panel del profesor)."""
    from Misiones.models import Batalla
    return [b for b in Batalla.objects.abiertas().select_related('clase')]


@register.filter
def hace(fecha):
    """'hace 3 días', 'hace 2 horas' o 'hace un momento' (sin el raro «hace 0 minutos»)."""
    from django.utils.timesince import timesince
    if not fecha:
        return ''
    texto = timesince(fecha, depth=1)
    return 'hace un momento' if texto.startswith(('0\xa0', '0 ')) else f'hace {texto}'
