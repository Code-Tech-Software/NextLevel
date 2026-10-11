from django.db import migrations

COMPORTAMIENTOS = [
    # (nombre, icono, monedas, xp)
    ('Participación', '🙋', 5, 5),
    ('Ayudó a un compañero', '🤝', 5, 10),
    ('Trabajo en equipo', '👥', 5, 5),
    ('Creatividad', '💡', 10, 10),
    ('Buena conducta', '😇', 5, 0),
    ('Trabajo terminado', '✅', 5, 10),
    ('Habló sin turno', '🗣️', -3, 0),
    ('Distracción', '📵', -3, 0),
    ('Sin material', '🎒', -2, 0),
]


def sembrar(apps, schema_editor):
    Comportamiento = apps.get_model('Misiones', 'Comportamiento')
    if Comportamiento.objects.exists():
        return
    for orden, (nombre, icono, monedas, xp) in enumerate(COMPORTAMIENTOS, start=1):
        Comportamiento.objects.create(nombre=nombre, icono=icono, monedas=monedas, xp=xp, orden=orden)


class Migration(migrations.Migration):

    dependencies = [
        ('Misiones', '0013_modo_clase_equipos_metas'),
    ]

    operations = [
        migrations.RunPython(sembrar, migrations.RunPython.noop),
    ]
