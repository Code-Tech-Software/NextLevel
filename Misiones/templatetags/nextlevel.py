import re
from urllib.parse import parse_qs, urlparse

from django import template

from Misiones.gamificacion import TEMA_INFO, TIPO_INFO
from Misiones.minijuegos import juegos_arcade
from Misiones.models import ArticuloTienda, CompraAlumno, ProgresoMision

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


@register.filter
def avatar_url(alumno):
    try:
        if alumno.avatar:
            return alumno.avatar.url
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
