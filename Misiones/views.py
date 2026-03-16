import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from .models import Clase, Alumno


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
    alumnos = clase.alumnos.filter(activo=True)
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

    # Obtiene la URL de la página anterior
    return_url = request.META.get('HTTP_REFERER', '/')
    return redirect(return_url)

# Asegúrate de tener importado get_object_or_404, redirect, render y messages

def ver_mision(request, clase_id, mision_id):
    alumno_id = request.session.get('alumno_id')
    if not alumno_id:
        return redirect('lista_alumnos', clase_id=clase_id)

    alumno = get_object_or_404(Alumno, id=alumno_id)
    clase = get_object_or_404(Clase, id=clase_id)
    mision = get_object_or_404(Mision, id=mision_id, clase=clase)

    # Buscamos si el alumno ya tiene un progreso registrado en esta misión
    progreso = ProgresoMision.objects.filter(alumno=alumno, mision=mision).first()

    return render(request, 'Alumnos/mision_detalle.html', {
        'alumno': alumno,
        'clase': clase,
        'mision': mision,
        'progreso': progreso
    })


def marcar_completada(request, clase_id, mision_id):
    alumno_id = request.session.get('alumno_id')
    if not alumno_id or request.method != 'POST':
        return redirect('lista_alumnos', clase_id=clase_id)

    alumno = get_object_or_404(Alumno, id=alumno_id)
    mision = get_object_or_404(Mision, id=mision_id)

    # get_or_create busca el registro; si no existe, lo crea con estado 'pendiente'
    progreso, creado = ProgresoMision.objects.get_or_create(
        alumno=alumno,
        mision=mision,
        defaults={'estado': 'pendiente'}
    )

    # Si el registro ya existía (por ejemplo, si tú se la habías rechazado para que la corrigiera),
    # la volvemos a poner en 'pendiente' para una nueva revisión.
    if not creado and progreso.estado == 'rechazado':
        progreso.estado = 'pendiente'
        progreso.revisado = False
        progreso.save()

    messages.success(request, f"¡Excelente! La misión '{mision.nombre}' fue enviada a revisión.")
    return redirect('dashboard_alumno', clase_id=clase_id)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction  # Importante para actualizar los puntos de forma segura
from .models import Clase, ProgresoMision


def panel_profesor(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)

    # Obtenemos solo los progresos que están pendientes de revisión para esta clase en específico
    entregas_pendientes = ProgresoMision.objects.filter(
        mision__clase=clase,
        estado='pendiente'
    ).select_related('alumno', 'mision').order_by('fecha')

    return render(request, 'Profesor/panel_profesor.html', {
        'clase': clase,
        'entregas_pendientes': entregas_pendientes
    })


def aprobar_mision(request, progreso_id):
    progreso = get_object_or_404(ProgresoMision, id=progreso_id)

    # Aseguramos que solo procesamos misiones que estaban pendientes
    if progreso.estado == 'pendiente':
        with transaction.atomic():
            # 1. Actualizar el estado de la misión
            progreso.estado = 'aprobado'
            progreso.revisado = True
            # Opcional: registrar la puntuación ganada en ese momento
            progreso.puntuacion = progreso.mision.xp_recompensa
            progreso.save()

            # 2. Sumar recompensas al alumno
            alumno = progreso.alumno
            alumno.xp_total += progreso.mision.xp_recompensa
            alumno.monedas += progreso.mision.monedas_recompensa
            alumno.save()

            messages.success(request,
                             f"¡Misión aprobada! {alumno.nombre} ha ganado {progreso.mision.xp_recompensa} XP.")

    return redirect('panel_profesor', clase_id=progreso.mision.clase.id)


def rechazar_mision(request, progreso_id):
    progreso = get_object_or_404(ProgresoMision, id=progreso_id)

    if progreso.estado == 'pendiente':
        progreso.estado = 'rechazado'
        progreso.revisado = True
        progreso.save()
        messages.warning(request, f"Misión de {progreso.alumno.nombre} rechazada. Deberá corregirla.")

    return redirect('panel_profesor', clase_id=progreso.mision.clase.id)