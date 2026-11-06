from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from Misiones import cursos
from Misiones.models import Clase


class Command(BaseCommand):
    help = ('Carga un curso listo (mundos, niveles, misiones, jefes y minijuegos) al final del mapa de una clase. '
            'Con --actualizar pone al día un curso que ya estaba cargado.')

    def add_arguments(self, parser):
        parser.add_argument('curso', choices=sorted(cursos.CURSOS), help='Clave del curso, p. ej. tics4')
        parser.add_argument('--clase', type=int, required=True, help='Id de la clase que recibe el curso')
        parser.add_argument('--simular', action='store_true', help='Muestra lo que se haría sin guardar nada')
        parser.add_argument('--actualizar', action='store_true',
                            help='Corrige y completa un curso ya cargado: conserva el avance de los alumnos, retira lo '
                                 'de la versión anterior y no toca lo que creó el profe')

    def handle(self, *args, **opciones):
        clase = Clase.objects.filter(pk=opciones['clase']).first()
        if not clase:
            raise CommandError(f'No existe la clase con id {opciones["clase"]}.')

        curso = cursos.obtener(opciones['curso'])
        with transaction.atomic():
            if opciones['actualizar']:
                resumen = cursos.actualizar(clase, curso)
            else:
                resumen = cursos.cargar(clase, curso)
            if opciones['simular']:
                transaction.set_rollback(True)

        nombre = cursos.CURSOS[opciones['curso']][1]
        destino = f'{clase.nombre} {clase.grado} {clase.grupo}'
        if opciones['actualizar']:
            accion = 'Se actualizaría' if opciones['simular'] else 'Se actualizó'
            self.stdout.write(self.style.SUCCESS(
                f'{accion} «{nombre}» en {destino}: {resumen["actualizadas"]} misiones puestas al día, '
                f'{resumen["nuevas"]} nuevas, {resumen["retiradas"]} retiradas, {resumen["ocultas"]} ocultas (ya tenían '
                f'avance), {resumen["niveles"]} niveles nuevos, {resumen["preguntas"]} preguntas escritas, '
                f'{resumen["juegos"]} minijuegos nuevos y {resumen["juegos_retirados"]} retirados.'))
            for mundo in resumen['actualizados']:
                self.stdout.write(f'  ~ {mundo}')
            for mundo in resumen['mundos']:
                self.stdout.write(f'  + {mundo}')
            return

        accion = 'Se cargaría' if opciones['simular'] else 'Se cargó'
        self.stdout.write(self.style.SUCCESS(
            f'{accion} «{nombre}» en {destino}: {len(resumen["mundos"])} mundos, '
            f'{resumen["niveles"]} niveles, {resumen["misiones"]} misiones ({resumen["jefes"]} jefes), '
            f'{resumen["preguntas"]} preguntas y {resumen["juegos"]} minijuegos nuevos.'))
        for mundo in resumen['mundos']:
            self.stdout.write(f'  + {mundo}')
        for mundo in resumen['omitidos']:
            self.stdout.write(self.style.WARNING(f'  = {mundo} (ya existía, no se tocó)'))
