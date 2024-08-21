from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Asistencia, AsignacionCiclo
from django.contrib.auth.decorators import login_required

@login_required
def lista_asistencia(request):
    hoy = timezone.now().date()
    asignaciones = AsignacionCiclo.objects.filter(user=request.user, year=hoy.year)

    asistencias_hoy = Asistencia.objects.filter(fecha=hoy, asignacion_ciclo__in=asignaciones)

    asignaciones_sin_asistencia = asignaciones.exclude(id__in=asistencias_hoy.values_list('asignacion_ciclo_id', flat=True))

    context = {
        'asignaciones_sin_asistencia': asignaciones_sin_asistencia,
        'asistencias_hoy': asistencias_hoy,
        'hoy': hoy,
    }
    return render(request, 'lista_asistencia.html', context)

@login_required
def actualizar_asistencia(request, asignacion_id):
    hoy = timezone.now().date()
    asignacion = get_object_or_404(AsignacionCiclo, id=asignacion_id)
    asistencia, created = Asistencia.objects.get_or_create(fecha=hoy, asignacion_ciclo=asignacion)

    asistencia.presente = not asistencia.presente
    asistencia.save()

    return redirect('lista_asistencia')

@login_required
def ver_asistencias(request):
    fechas_asistencias = Asistencia.objects.values('fecha').distinct().order_by('-fecha')
    context = {
        'fechas_asistencias': fechas_asistencias,
    }
    return render(request, 'ver_asistencias.html', context)

@login_required
def detalle_asistencia(request, fecha):
    asistencias = Asistencia.objects.filter(fecha=fecha, asignacion_ciclo__user=request.user)
    context = {
        'asistencias': asistencias,
        'fecha': fecha,
    }
    return render(request, 'detalle_asistencia.html', context)
