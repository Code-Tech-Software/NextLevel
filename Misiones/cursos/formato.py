"""El formato común de los cursos: cada misión escrita como una pequeña clase, los jefes y los juegos de tarjetas.

Las secciones empiezan con un emoji fijo (📘, 🧰, ⏱️, 👥, 🛠️, ⚠️, ✅) para que la página de la misión las resalte
(ver el filtro «texto_mision»).
"""
from Misiones.cursos import mision

__all__ = ['leccion', 'jefe', 'clasifica']


def _lista(elementos, numerada=False):
    if isinstance(elementos, str):
        return elementos
    if numerada:
        return '\n'.join(f'{i}. {texto}' for i, texto in enumerate(elementos, start=1))
    return '\n'.join(f'• {texto}' for texto in elementos)


def leccion(intro=None, saber=None, pasos=None, logro=None, tip=None, entrega=None, material=None, extra=None,
            dinamica=None, roles=None, ojo=None):
    """Arma la descripción de una misión como una pequeña clase.

    intro: la situación o el objetivo · saber: lo que hay que entender (texto o lista) · material: lo que se necesita ·
    dinamica: cómo se organiza la clase (tiempos, parejas, reglas) · roles: quién hace qué en el equipo ·
    pasos: el paso a paso · extra: secciones adicionales [(título, texto o lista)] · ojo: cuidados y seguridad ·
    logro: cómo saber que salió bien · tip: un consejo · entrega: qué se sube o se muestra.
    """
    partes = []
    if intro:
        partes.append(intro)
    if saber:
        partes.append('📘 Lo que necesitas saber\n' + _lista(saber))
    if material:
        partes.append('🧰 Necesitas\n' + _lista(material))
    if dinamica:
        partes.append('⏱️ Así se trabaja hoy\n' + _lista(dinamica))
    if roles:
        partes.append('👥 Roles del equipo\n' + _lista(roles))
    if pasos:
        partes.append('🛠️ Paso a paso\n' + _lista(pasos, numerada=True))
    for titulo, contenido in extra or []:
        partes.append(f'{titulo}\n{_lista(contenido)}')
    if ojo:
        partes.append('⚠️ Ojo\n' + _lista(ojo))
    if logro:
        partes.append('✅ Lo lograste si…\n' + _lista(logro))
    if tip:
        partes.append(f'💡 Tip: {tip}')
    if entrega:
        partes.append(f'📤 Entrega: {entrega}')
    return '\n\n'.join(partes)


def jefe(nombre, descripcion, preguntas, xp=150, monedas=50):
    return mision(nombre, 'cuestionario', descripcion, xp, monedas, jefe=True, preguntas=preguntas)


def clasifica(nombre, icono, descripcion, categorias, rondas=12, tiempo=12):
    """Juego de tarjetas: de 2 a 3 grupos (nombre de máximo 30 letras); cada tarjeta mide máximo 70 letras."""
    return {'nombre': nombre, 'icono': icono, 'descripcion': descripcion, 'plantilla': 'clasifica', 'en_arcade': True,
            'configuracion': {'tema': 'personalizado', 'rondas': rondas, 'tiempo': tiempo, 'categorias': [
                {'nombre': n, 'emoji': e, 'tarjetas': list(t)} for n, e, t in categorias]}}
