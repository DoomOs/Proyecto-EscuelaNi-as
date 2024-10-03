from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Asistencia, AsignacionCiclo
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas
import pandas as pd

@login_required
def lista_asistencia(request):
    """
        Vista que muestra la lista de alumnas y su asistencia del día actual para el grado asignado al usuario logueado.

    Parámetros:
        request (HttpRequest): Objeto de solicitud HTTP que contiene información sobre la solicitud del usuario.

    Retorna:
        HttpResponse: Renderiza la plantilla 'lista_asistencia.html' con el contexto que incluye 
        las asignaciones sin asistencia y las asistencias registradas para el día actual.

    """
    hoy = timezone.localtime(timezone.now()).date()
    user = request.user  # Usuario logueado

    # Obtener el grado asignado al usuario (docente)
    grado_usuario = user.id_ciclo

    if grado_usuario is not None:
        # Filtrar asignaciones de alumnas activas que pertenecen al grado del usuario logueado
        asignaciones = AsignacionCiclo.objects.filter(grado_id=grado_usuario, year=hoy.year, alumna__estado=True)

        # Asistencias registradas hoy
        asistencias_hoy = Asistencia.objects.filter(fecha=hoy, asignacion_ciclo__in=asignaciones)

        # Asignaciones que aún no tienen asistencia registrada hoy
        asignaciones_sin_asistencia = asignaciones.exclude(id__in=asistencias_hoy.values_list('asignacion_ciclo_id', flat=True))

        context = {
            'asignaciones_sin_asistencia': asignaciones_sin_asistencia,
            'asistencias_hoy': asistencias_hoy,
            'hoy': hoy,
        }

        return render(request, 'lista_asistencia.html', context)
    
    else:
        # En caso de que el usuario no tenga un grado asignado, mostrar un mensaje o redirigir
        return render(request, 'lista_asistencia.html', {
            'mensaje_error': 'No tienes un grado asignado.',
        })


@login_required
def actualizar_asistencia(request, asignacion_id, presente):
    """
        Vista que actualiza el estado de asistencia de una alumna para el día actual.

    Parámetros:
        request (HttpRequest): Objeto de solicitud HTTP que contiene información sobre la solicitud del usuario.
        asignacion_id (int): ID de la asignación de ciclo de la alumna.
        presente (bool): Indica si la alumna estuvo presente (1) o ausente (0).

    Retorna:
        HttpResponse: Redirige a la vista de lista de asistencia después de actualizar el estado de asistencia.

    """
    hoy = timezone.localtime(timezone.now()).date()
    asignacion = get_object_or_404(AsignacionCiclo, id=asignacion_id)
    
    asistencia, created = Asistencia.objects.get_or_create(fecha=hoy, asignacion_ciclo=asignacion)

    asistencia.presente = bool(int(presente))
    asistencia.save()

    return redirect('lista_asistencia')


@login_required
def ver_asistencias(request):
    """
        Vista que muestra las fechas en las que se han registrado asistencias.

    Parámetros:
        request (HttpRequest): Objeto de solicitud HTTP que contiene información sobre la solicitud del usuario.

    Retorna:
        HttpResponse: Renderiza la plantilla 'ver_asistencias.html' con el contexto que incluye 
        las fechas de las asistencias registradas.

    """
    
    fechas_asistencias = Asistencia.objects.values('fecha').distinct().order_by('-fecha')
    context = {
        'fechas_asistencias': fechas_asistencias,
    }
    return render(request, 'ver_asistencias.html', context)

@login_required
def detalle_asistencia(request, fecha):
    """
        Vista que muestra el detalle de asistencias registradas en una fecha específica.

    Parámetros:
        request (HttpRequest): Objeto de solicitud HTTP que contiene información sobre la solicitud del usuario.
        fecha (date): Fecha para la cual se desea ver las asistencias.

    Retorna:
        HttpResponse: Renderiza la plantilla 'detalle_asistencia.html' con el contexto que incluye 
        las asistencias registradas en la fecha especificada.

    """
    asistencias = Asistencia.objects.filter(fecha=fecha, asignacion_ciclo__user=request.user)
    context = {
        'asistencias': asistencias,
        'fecha': fecha,
    }
    return render(request, 'detalle_asistencia.html', context)



@login_required
def generar_pdf(request, fecha):
    """
        Vista que genera un archivo PDF con la asistencia registrada en una fecha específica.

    Parámetros:
        request (HttpRequest): Objeto de solicitud HTTP que contiene información sobre la solicitud del usuario.
        fecha (date): Fecha para la cual se generará el PDF de asistencias.

    Retorna:
        HttpResponse: Archivo PDF que contiene la lista de alumnas y su estado de asistencia para la fecha especificada.

    """
    # Filtrar asistencias por fecha
    asistencias = Asistencia.objects.filter(fecha=fecha)

    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="asistencia_{fecha}.pdf"'

    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Títulos de la tabla
    data = [["Alumno", "Presente"]]

    for asistencia in asistencias:
        alumno = asistencia.asignacion_ciclo.alumna
        presente = "Sí" if asistencia.presente else "No"
        data.append([f"{alumno.persona.nombre} {alumno.persona.apellido}", presente])

    # Crear la tabla
    table = Table(data)
    
    # Estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    table.setStyle(style)
    elements.append(table)

    # Construir el PDF
    pdf.build(elements)
    return response

@login_required
def generar_excel(request, fecha):
    """
        Vista que genera un archivo Excel con la asistencia registrada en una fecha específica.

    Parámetros:
        request (HttpRequest): Objeto de solicitud HTTP que contiene información sobre la solicitud del usuario.
        fecha (date): Fecha para la cual se generará el archivo Excel de asistencias.

    Retorna:
        HttpResponse: Archivo Excel que contiene la lista de alumnas y su estado de asistencia para la fecha especificada.

    """
    # Filtrar asistencias por fecha
    asistencias = Asistencia.objects.filter(fecha=fecha)

    # Crear un DataFrame
    data = {
        'Alumno': [],
        'Presente': [],
    }

    for asistencia in asistencias:
        alumno = asistencia.asignacion_ciclo.alumna
        data['Alumno'].append(f"{alumno.persona.nombre} {alumno.persona.apellido}")
        data['Presente'].append("Sí" if asistencia.presente else "No")

    df = pd.DataFrame(data)

    # Crear el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="asistencia_{fecha}.xlsx"'

    # Guardar el DataFrame en un archivo Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Asistencia')

    return response