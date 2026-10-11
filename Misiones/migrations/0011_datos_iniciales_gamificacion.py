from django.db import migrations


MISIONES_DIARIAS = [
    # (titulo, descripcion, icono, objetivo, meta, monedas, xp)
    ('Reportándome', 'Entra a la plataforma hoy', '👋', 'login', 1, 5, 10),
    ('Aventurero del día', 'Completa 1 misión del mapa', '🗺️', 'misiones', 1, 15, 20),
    ('Imparable', 'Completa 2 misiones del mapa', '⚡', 'misiones', 2, 25, 30),
    ('Mente brillante', 'Responde un cuestionario', '🧠', 'cuestionarios', 1, 15, 15),
    ('¡Diez perfecto!', 'Saca 10 en un cuestionario', '💯', 'perfecto', 1, 30, 30),
    ('Cazador de XP', 'Gana 100 XP hoy', '🔋', 'xp', 100, 20, 0),
    ('Manos a la obra', 'Envía un trabajo para revisión', '🛠️', 'evidencias', 1, 20, 20),
    ('De compras', 'Visita la tienda', '🛍️', 'tienda', 1, 5, 5),
]

LOGROS = [
    # (nombre, descripcion, icono, condicion, valor, rareza, monedas, xp)
    ('Primer paso', 'Completa tu primera misión', '👣', 'misiones', 1, 'comun', 10, 0),
    ('En marcha', 'Completa 5 misiones', '🚲', 'misiones', 5, 'comun', 20, 0),
    ('Explorador incansable', 'Completa 15 misiones', '🧭', 'misiones', 15, 'raro', 50, 0),
    ('Héroe del mapa', 'Completa 30 misiones', '🦸', 'misiones', 30, 'epico', 100, 0),
    ('Chispa', 'Llega a 500 XP', '✨', 'xp', 500, 'comun', 20, 0),
    ('Supernova', 'Llega a 2,000 XP', '🌟', 'xp', 2000, 'epico', 80, 0),
    ('Alcancía', 'Gana 200 monedas en total', '🐷', 'monedas', 200, 'comun', 0, 30),
    ('Tesoro del dragón', 'Gana 1,000 monedas en total', '🐉', 'monedas', 1000, 'epico', 0, 100),
    ('En llamas', 'Mantén una racha de 3 días', '🔥', 'racha', 3, 'comun', 15, 0),
    ('Fuego eterno', 'Mantén una racha de 7 días', '☄️', 'racha', 7, 'raro', 40, 0),
    ('Cerebrito', 'Saca 10 en un cuestionario', '🧠', 'perfectos', 1, 'raro', 25, 0),
    ('Genio', 'Saca 10 en 5 cuestionarios', '🎓', 'perfectos', 5, 'epico', 60, 0),
    ('Cliente frecuente', 'Haz tu primera compra en la tienda', '🛒', 'compras', 1, 'comun', 0, 20),
    ('Conquistador', 'Completa un mundo entero', '🏰', 'mundos', 1, 'raro', 50, 50),
    ('Subiendo', 'Llega al nivel 5', '📈', 'nivel', 5, 'raro', 30, 0),
    ('Leyenda viviente', 'Llega al nivel 20', '👑', 'nivel', 20, 'legendario', 200, 0),
    ('Constante', 'Completa 10 misiones diarias', '📅', 'diarias', 10, 'raro', 40, 0),
    ('Cazajefes', 'Derrota a tu primer jefe', '⚔️', 'jefes', 1, 'epico', 50, 0),
    ('Estrella de la clase', 'Reconocimiento especial del profesor', '🌈', 'manual', 1, 'legendario', 50, 50),
]


def migrar_datos(apps, schema_editor):
    CompraAlumno = apps.get_model('Misiones', 'CompraAlumno')
    Clase = apps.get_model('Misiones', 'Clase')
    Mundo = apps.get_model('Misiones', 'Mundo')
    Nivel = apps.get_model('Misiones', 'Nivel')
    MisionDiaria = apps.get_model('Misiones', 'MisionDiaria')
    Logro = apps.get_model('Misiones', 'Logro')

    # 1. Las compras pasan de un booleano a un estado
    for compra in CompraAlumno.objects.select_related('articulo'):
        compra.estado = 'entregado' if compra.entregado_usado else 'pendiente'
        compra.costo_pagado = compra.articulo.costo_monedas
        compra.save(update_fields=['estado', 'costo_pagado'])

    # 2. Los niveles existentes se agrupan en un primer mundo por clase
    for clase in Clase.objects.all():
        niveles_sueltos = Nivel.objects.filter(clase=clase, mundo__isnull=True)
        if niveles_sueltos.exists():
            mundo = Mundo.objects.create(
                clase=clase, nombre='Mundo 1', tema='bosque', orden=1,
                descripcion='¡Aquí comienza la aventura!'
            )
            niveles_sueltos.update(mundo=mundo)

    # 3. Catálogo inicial de misiones del día y logros
    if not MisionDiaria.objects.exists():
        for titulo, desc, icono, objetivo, meta, monedas, xp in MISIONES_DIARIAS:
            MisionDiaria.objects.create(
                titulo=titulo, descripcion=desc, icono=icono, objetivo=objetivo, meta=meta,
                recompensa_monedas=monedas, recompensa_xp=xp
            )

    if not Logro.objects.exists():
        for orden, (nombre, desc, icono, condicion, valor, rareza, monedas, xp) in enumerate(LOGROS, start=1):
            Logro.objects.create(
                nombre=nombre, descripcion=desc, icono=icono, condicion=condicion, valor=valor,
                rareza=rareza, recompensa_monedas=monedas, recompensa_xp=xp, orden=orden
            )


def revertir(apps, schema_editor):
    CompraAlumno = apps.get_model('Misiones', 'CompraAlumno')
    for compra in CompraAlumno.objects.all():
        compra.entregado_usado = compra.estado == 'entregado'
        compra.save(update_fields=['entregado_usado'])


class Migration(migrations.Migration):

    dependencies = [
        ('Misiones', '0010_mundos_tienda_gamificacion'),
    ]

    operations = [
        migrations.RunPython(migrar_datos, revertir),
    ]
