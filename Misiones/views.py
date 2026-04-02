import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from .models import Clase, Alumno, ArticuloTienda, CompraAlumno
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


def home_redirect(request):
    return HttpResponseRedirect('/misiones/seleccionar-clase/')


# Vista para seleccionar la clase (ya la tienes)
def seleccionar_clase(request):
    clases = Clase.objects.all()
    return render(request, 'Alumnos/seleccionar_clase.html', {'clases': clases})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Clase, Alumno, Mision, ProgresoMision


# Vista original (solo le agregamos el request al render)
def lista_alumnos(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    alumnos = clase.alumnos.filter(activo=True).order_by('apellido', 'nombre')
    return render(request, 'Alumnos/lista_alumnos.html', {'clase': clase, 'alumnos': alumnos})


# 1. Vista para procesar el PIN
def ingresar_pin(request, clase_id, alumno_id):
    if request.method == 'POST':
        pin_ingresado = request.POST.get('pin')
        alumno = get_object_or_404(Alumno, id=alumno_id)

        if alumno.pin == pin_ingresado:
            # Guardamos el ID del alumno en la sesión de Django
            request.session['alumno_id'] = alumno.id
            return redirect('dashboard_alumno', clase_id=clase_id)
        else:
            messages.error(request, f"PIN incorrecto para {alumno.nombre}")

    return redirect('lista_alumnos', clase_id=clase_id)


# 2. Vista del Dashboard (Estilo Duolingo)
def dashboard_alumno(request, clase_id):
    alumno_id = request.session.get('alumno_id')
    if not alumno_id:
        return redirect('lista_alumnos', clase_id=clase_id)  # Si no hay sesión, regresa a la lista

    alumno = get_object_or_404(Alumno, id=alumno_id)
    clase = get_object_or_404(Clase, id=clase_id)

    # Traemos todas las misiones de la clase ordenadas por Nivel y luego por Misión
    misiones = Mision.objects.filter(clase=clase).select_related('nivel').order_by('nivel__orden', 'orden')

    # Traemos el progreso del alumno y lo convertimos en un diccionario para búsqueda rápida
    progresos = ProgresoMision.objects.filter(alumno=alumno)
    progreso_dict = {p.mision_id: p for p in progresos}

    misiones_ruta = []
    mision_desbloqueada = True  # La primera misión siempre debe estar desbloqueada

    for mision in misiones:
        progreso = progreso_dict.get(mision.id)
        estado_actual = progreso.estado if progreso else 'pendiente'

        misiones_ruta.append({
            'mision': mision,
            'progreso': progreso,
            'estado': estado_actual,
            'desbloqueada': mision_desbloqueada
        })

        # LA REGLA DE ORO: Si esta misión NO está 'aprobada', bloqueamos todas las que siguen
        if estado_actual != 'aprobado':
            mision_desbloqueada = False

    return render(request, 'Alumnos/dashboard.html', {
        'alumno': alumno,
        'clase': clase,
        'misiones_ruta': misiones_ruta
    })


# 3. Vista para cerrar sesión
def salir_alumno(request):
    if 'alumno_id' in request.session:
        del request.session['alumno_id']
    return_url = request.META.get('HTTP_REFERER', '/')
    return redirect(return_url)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Alumno, Clase, Mision, ProgresoMision, RespuestaAlumno, OpcionRespuesta


def ver_mision(request, clase_id, mision_id):
    alumno_id = request.session.get('alumno_id')
    if not alumno_id:
        return redirect('lista_alumnos', clase_id=clase_id)

    alumno = get_object_or_404(Alumno, id=alumno_id)
    clase = get_object_or_404(Clase, id=clase_id)
    mision = get_object_or_404(Mision, id=mision_id, clase=clase)
    progreso = ProgresoMision.objects.filter(alumno=alumno, mision=mision).first()

    # Si es cuestionario, enviamos las preguntas a la plantilla
    preguntas = mision.preguntas.all() if mision.tipo == "cuestionario" else None

    return render(request, 'Alumnos/mision_detalle.html', {
        'alumno': alumno,
        'clase': clase,
        'mision': mision,
        'progreso': progreso,
        'preguntas': preguntas  # <-- ¡Nuevo!
    })


def marcar_completada(request, clase_id, mision_id):
    alumno_id = request.session.get('alumno_id')
    if not alumno_id or request.method != 'POST':
        return redirect('lista_alumnos', clase_id=clase_id)

    alumno = get_object_or_404(Alumno, id=alumno_id)
    mision = get_object_or_404(Mision, id=mision_id)

    progreso, creado = ProgresoMision.objects.get_or_create(
        alumno=alumno,
        mision=mision,
        defaults={'estado': 'pendiente'}
    )

    # Lógica para CUESTIONARIOS
    if mision.tipo == "cuestionario":

        RespuestaAlumno.objects.filter(progreso=progreso).delete()
        puntuacion_obtenida = 0

        # 1. Calculamos los puntos totales posibles del cuestionario
        preguntas_mision = mision.preguntas.all()
        puntos_totales = sum(pregunta.puntos for pregunta in preguntas_mision)

        # Procesamos cada respuesta enviada
        for pregunta in preguntas_mision:
            opcion_id = request.POST.get(f'pregunta_{pregunta.id}')
            if opcion_id:
                opcion_seleccionada = get_object_or_404(OpcionRespuesta, id=opcion_id)
                RespuestaAlumno.objects.create(
                    progreso=progreso,
                    pregunta=pregunta,
                    opcion_seleccionada=opcion_seleccionada
                )

                if opcion_seleccionada.es_correcta:
                    puntuacion_obtenida += pregunta.puntos

        # 2. Calculamos la calificación en porcentaje (0 a 100)
        if puntos_totales > 0:
            calificacion_porcentaje = int((puntuacion_obtenida / puntos_totales) * 100)
        else:
            calificacion_porcentaje = 0

        # 3. Calculamos las monedas proporcionales (convertidas a entero)
        monedas_ganadas = int((calificacion_porcentaje / 100.0) * mision.monedas_recompensa)

        # 4. La XP se otorga completa, independientemente de la calificación
        xp_ganada = mision.xp_recompensa

        # Actualizamos el progreso con el porcentaje como puntuación
        progreso.puntuacion = calificacion_porcentaje
        progreso.estado = 'aprobado'
        progreso.revisado = True
        progreso.save()

        # 5. Otorgamos las recompensas al alumno
        # para evitar que los alumnos envíen el cuestionario varias veces para "farmear" XP.
        if creado:
            alumno.monedas += monedas_ganadas
            alumno.xp_total += xp_ganada
            alumno.save()

        calificacion_base_10 = calificacion_porcentaje / 10.0

        messages.success(
            request,
            f"¡Cuestionario completado! Calificación: {calificacion_base_10:.1f}. Ganaste {monedas_ganadas} monedas."
        )

    else:
        # Lógica para Misiones de Arduino o Link
        if not creado and progreso.estado == 'rechazado':
            progreso.estado = 'pendiente'
            progreso.revisado = False
            progreso.save()
        messages.success(request, f"¡Excelente! La misión '{mision.nombre}' fue enviada a revisión.")

    return redirect('dashboard_alumno', clase_id=clase_id)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Clase, ProgresoMision


def panel_profesor(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)

    # Obtenemos solo los progresos que están pendientes de revisión para esta clase en específico
    entregas_pendientes = ProgresoMision.objects.filter(
        mision__clase=clase,
        estado='pendiente'
    ).select_related('alumno', 'mision').order_by('fecha')

    return render(request, 'Profesor/panel_calificar.html', {
        'clase': clase,
        'entregas_pendientes': entregas_pendientes
    })


def aprobar_mision(request, progreso_id):
    progreso = get_object_or_404(ProgresoMision, id=progreso_id)

    if request.method == 'POST' and progreso.estado == 'pendiente':
        # Obtenemos la calificación del formulario (por defecto 100 si no se envía)
        puntuacion = int(request.POST.get('puntuacion', 100))

        with transaction.atomic():
            # 1. Actualizamos el progreso con la nota manual
            progreso.estado = 'aprobado'
            progreso.revisado = True
            progreso.puntuacion = puntuacion
            progreso.save()

            # 2. Calculamos recompensas (XP completa, Monedas proporcionales)
            xp_ganada = progreso.mision.xp_recompensa
            # Usamos la misma lógica que en el cuestionario: monedas según la nota
            monedas_ganadas = int((puntuacion / 100.0) * progreso.mision.monedas_recompensa)

            # 3. Sumar al alumno
            alumno = progreso.alumno
            alumno.xp_total += xp_ganada  # O el campo que uses para XP
            alumno.monedas += monedas_ganadas
            alumno.save()

            calif_display = puntuacion / 10.0
            messages.success(request,
                             f"Misión de {alumno.nombre} aprobada con {calif_display}. Otorgadas {monedas_ganadas} monedas.")

    return redirect('panel_profesor', clase_id=progreso.mision.clase.id)


def rechazar_mision(request, progreso_id):
    progreso = get_object_or_404(ProgresoMision, id=progreso_id)

    if progreso.estado == 'pendiente':
        progreso.estado = 'rechazado'
        progreso.revisado = True
        progreso.save()
        messages.warning(request, f"Misión de {progreso.alumno.nombre} rechazada. Deberá corregirla.")

    return redirect('panel_profesor', clase_id=progreso.mision.clase.id)


from django.db import transaction


def tienda_alumno(request, clase_id):
    alumno_id = request.session.get('alumno_id')
    if not alumno_id:
        return redirect('lista_alumnos', clase_id=clase_id)

    alumno = get_object_or_404(Alumno, id=alumno_id)
    clase = get_object_or_404(Clase, id=clase_id)

    # CAMBIO AQUÍ: Traemos absolutamente todos los artículos de la tienda
    articulos = ArticuloTienda.objects.all()

    # El inventario sigue siendo personal del alumno
    mis_compras = CompraAlumno.objects.filter(alumno=alumno).order_by('-fecha_compra')

    return render(request, 'Alumnos/tienda.html', {
        'alumno': alumno,
        'clase': clase,  # Lo pasamos para que el botón "Volver" sepa a qué clase regresar
        'articulos': articulos,
        'mis_compras': mis_compras
    })

def comprar_articulo(request, clase_id, articulo_id):
    alumno_id = request.session.get('alumno_id')
    if not alumno_id or request.method != 'POST':
        return redirect('lista_alumnos', clase_id=clase_id)

    alumno = get_object_or_404(Alumno, id=alumno_id)
    articulo = get_object_or_404(ArticuloTienda, id=articulo_id)

    # Verificamos si tiene suficientes monedas
    if alumno.monedas >= articulo.costo_monedas:
        with transaction.atomic():
            # Descontamos monedas
            alumno.monedas -= articulo.costo_monedas
            alumno.save()

            # Registramos la compra
            CompraAlumno.objects.create(
                alumno=alumno,
                articulo=articulo,
                entregado_usado=not articulo.requiere_validacion  # Si es digital, ya está "entregado"
            )

            messages.success(request, f"¡Compraste '{articulo.nombre}' con éxito! 🎉")
    else:
        messages.error(request, "¡Oh no! No tienes suficientes monedas para este artículo.")

    return redirect('tienda_alumno', clase_id=clase_id)


def dashboard_profesor(request):
    # Obtenemos todas las clases registradas
    clases = Clase.objects.all().order_by('anio', 'grado', 'grupo')

    # Enriquecemos cada clase con estadísticas útiles para el profesor
    for clase in clases:
        # Contamos cuántos alumnos hay en esta clase
        clase.total_alumnos = clase.alumnos.count()
        # Contamos cuántas misiones están esperando calificación en esta clase
        clase.misiones_pendientes = ProgresoMision.objects.filter(
            mision__clase=clase,
            estado='pendiente'
        ).count()

    # Extra: Obtenemos las compras de la tienda que requieren que el profe entregue algo físico
    entregas_tienda = CompraAlumno.objects.filter(
        articulo__requiere_validacion=True,
        entregado_usado=False
    ).select_related('alumno', 'articulo').order_by('fecha_compra')

    return render(request, 'Profesor/dashboard_principal.html', {
        'clases': clases,
        'entregas_tienda': entregas_tienda
    })


def entregar_articulo_tienda(request, compra_id):
    # Vista rápida para marcar que ya le diste su premio físico al alumno
    if request.method == 'POST':
        compra = get_object_or_404(CompraAlumno, id=compra_id)
        compra.entregado_usado = True
        compra.save()
        messages.success(request,
                         f"¡Recompensa '{compra.articulo.nombre}' entregada con éxito a {compra.alumno.nombre}!")

    # Redirigimos de vuelta al dashboard principal
    return redirect('dashboard_profesor')



def matriz_calificaciones(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)

    # Obtener alumnos de la clase y misiones ordenadas
    alumnos = clase.alumnos.filter(activo=True).order_by('apellido', 'nombre')
    misiones = Mision.objects.filter(clase=clase).select_related('nivel').order_by('nivel__orden', 'orden')

    # Obtener todos los progresos de esta clase en una sola consulta
    progresos = ProgresoMision.objects.filter(
        alumno__in=alumnos,
        mision__in=misiones
    )

    # Crear un diccionario para buscar rápido: {(alumno_id, mision_id): progreso}
    diccionario_progresos = {(p.alumno_id, p.mision_id): p for p in progresos}

    # Construir la matriz
    matriz = []
    for alumno in alumnos:
        fila = {
            'alumno': alumno,
            'calificaciones': []
        }
        for mision in misiones:
            # Buscar si el alumno tiene progreso en esta misión
            progreso = diccionario_progresos.get((alumno.id, mision.id))
            fila['calificaciones'].append({
                'mision': mision,
                'progreso': progreso
            })
        matriz.append(fila)

    context = {
        'clase': clase,
        'misiones_columnas': misiones,
        'matriz': matriz,
    }

    return render(request, 'Profesor/matriz_calificaciones.html', context)




def mi_progreso(request, clase_id):
    # 1. Obtener el alumno actual (Ajusta esto según cómo manejes tu login)
    alumno_id = request.session.get('alumno_id')
    alumno = get_object_or_404(Alumno, id=alumno_id)

    # 2. Obtener la clase actual
    clase = get_object_or_404(Clase, id=clase_id)

    # 3. Filtrar los progresos de este alumno específicamente para las misiones de esta clase
    progresos = ProgresoMision.objects.filter(
        alumno=alumno,
        mision__clase=clase
    ).select_related('mision', 'mision__nivel').order_by('mision__nivel__orden', 'mision__orden')

    context = {
        'alumno': alumno,
        'clase': clase,
        'progresos': progresos,
    }

    return render(request, 'Alumnos/mi_progreso.html', context)