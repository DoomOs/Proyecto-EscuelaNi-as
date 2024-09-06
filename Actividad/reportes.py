import pandas as pd
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, PatternFill, Alignment
from Persona.models import Alumna
from .models import CalificacionActividad
from django.db.models import Sum

def exportar_calificaciones_excel(request, alumna_id):
    alumna = get_object_or_404(Alumna, id=alumna_id)
    
    # Obtener los filtros
    grado_id = request.GET.get('grado')
    year = request.GET.get('year')
    curso_id = request.GET.get('curso')

    # Obtener calificaciones según los filtros
    calificaciones = CalificacionActividad.objects.filter(asignacion_ciclo__alumna=alumna).order_by('-actividad__fecha')

    if grado_id:
        calificaciones = calificaciones.filter(asignacion_ciclo__grado_id=grado_id)
    if year:
        calificaciones = calificaciones.filter(asignacion_ciclo__year=year)
    if curso_id:
        calificaciones = calificaciones.filter(actividad__curso_id=curso_id)
    
    # Crear un DataFrame con la información de la alumna
    datos_alumna = {
        "Código": [alumna.codigo],
        "Nombre": [alumna.persona.nombre],
        "Apellido": [alumna.persona.apellido]
    }
    
    df_alumna = pd.DataFrame(datos_alumna)
    
    # Crear un DataFrame con las calificaciones
    datos_calificaciones = []
    for calificacion in calificaciones:
        datos_calificaciones.append({
            "Actividad": calificacion.actividad.actividad,
            "Curso": calificacion.actividad.curso.nombre_curso,
            "Fecha": calificacion.actividad.fecha,
            "Descripción": calificacion.descripcion,
            "Punteo": calificacion.punteo,
            "Punteo Total": calificacion.actividad.punteo,
            "Ciclo": calificacion.asignacion_ciclo.grado.nombre_grado,
            "Año": calificacion.asignacion_ciclo.year
        })
    
    df_calificaciones = pd.DataFrame(datos_calificaciones)

    # Crear un archivo Excel con la información
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="calificaciones_alumna.xlsx"'

    # Crear un libro y una hoja de trabajo
    wb = Workbook()
    ws = wb.active
    ws.title = 'Calificaciones Alumna'

    # Estilos
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="008000", end_color="008000", fill_type="solid")
    center_aligned_text = Alignment(horizontal="center")
    data_fill = PatternFill(start_color="E0E0E0", end_color="E0E0E0", fill_type="solid")

    # Escribir los encabezados de la alumna
    headers_alumna = ["Código", "Nombre", "Apellido"]
    for col_num, header in enumerate(headers_alumna, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_aligned_text

    # Escribir los datos de la alumna
    for col_num, (header, value) in enumerate(datos_alumna.items(), 1):
        cell = ws.cell(row=2, column=col_num, value=value[0] if isinstance(value, list) else value)
        cell.fill = data_fill
        cell.alignment = center_aligned_text

    # Escribir una fila en blanco para separar los datos de la alumna de la tabla de calificaciones
    start_row_calificaciones = len(df_alumna) + 3

    # Escribir los encabezados de la tabla de calificaciones
    headers_calificaciones = ["Actividad", "Curso", "Fecha", "Descripción", "Punteo", "Punteo Maximo", "Ciclo", "Año"]
    for col_num, header in enumerate(headers_calificaciones, 1):
        cell = ws.cell(row=start_row_calificaciones, column=col_num, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_aligned_text

    # Escribir la tabla de calificaciones
    for r_idx, row in enumerate(dataframe_to_rows(df_calificaciones, index=False, header=False), start_row_calificaciones + 1):
        for c_idx, value in enumerate(row, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=value)

    # Ajustar el ancho de las columnas automáticamente
    for column in ws.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)
        for cell in column:
            try:
                if cell.value is not None:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        adjusted_width = max_length + 2
        ws.column_dimensions[column_letter].width = adjusted_width

    # Guardar el libro en la respuesta
    wb.save(response)

    return response







def exportar_punteo_acumulado_excel(request, alumna_id):
    alumna = get_object_or_404(Alumna, id=alumna_id)

    # Obtener los filtros
    grado_id = request.GET.get('grado')
    year = request.GET.get('year')
    curso_id = request.GET.get('curso')

    # Imprimir valores para depuración
    print(f"Grado ID: {grado_id}")
    print(f"Año: {year}")
    print(f"Curso ID: {curso_id}")

    # Iniciar la consulta base
    calificaciones = CalificacionActividad.objects.filter(asignacion_ciclo__alumna=alumna)

    # Aplicar filtros
    if grado_id:
        calificaciones = calificaciones.filter(asignacion_ciclo__grado_id=grado_id)
    if year:
        calificaciones = calificaciones.filter(asignacion_ciclo__year=year)
    if curso_id:
        calificaciones = calificaciones.filter(actividad__curso_id=curso_id)

    # Imprimir el queryset para depuración
    print(calificaciones.query)

    # Calcular el punteo acumulado por curso, grado y año
    acumulado = calificaciones.values(
        'actividad__curso__nombre_curso',
        'asignacion_ciclo__grado__nombre_grado',
        'asignacion_ciclo__year'
    ).annotate(punteo_total=Sum('punteo')).order_by('actividad__curso__nombre_curso', 'asignacion_ciclo__year')

    # Convertir a DataFrame
    df_acumulado = pd.DataFrame(list(acumulado))

    # Verificar si el DataFrame está vacío
    if df_acumulado.empty:
        df_acumulado = pd.DataFrame(columns=['Curso', 'Punteo Total', 'Grado', 'Año'])
    else:
        # Renombrar columnas para que coincidan con los encabezados deseados
        df_acumulado = df_acumulado.rename(columns={
            'actividad__curso__nombre_curso': 'Curso',
            'asignacion_ciclo__grado__nombre_grado': 'Grado',
            'asignacion_ciclo__year': 'Año',
            'punteo_total': 'Punteo Total'
        })

    # Reordenar columnas
    df_acumulado = df_acumulado[['Curso', 'Punteo Total', 'Grado', 'Año']]

    # Imprimir el DataFrame para depuración
    print(df_acumulado)

    # Crear un archivo Excel con la información
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="punteo_acumulado_alumna.xlsx"'

    # Crear un libro y una hoja de trabajo
    wb = Workbook()
    ws = wb.active
    ws.title = 'Punteo Acumulado Alumna'

    # Estilos
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="008000", end_color="008000", fill_type="solid")
    center_aligned_text = Alignment(horizontal="center")
    data_fill = PatternFill(start_color="E0E0E0", end_color="E0E0E0", fill_type="solid")

    # Escribir los encabezados de la alumna
    headers_alumna = ["Código", "Nombre", "Apellido"]
    for col_num, header in enumerate(headers_alumna, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_aligned_text

    # Escribir los datos de la alumna
    datos_alumna = {
        "Código": alumna.codigo,
        "Nombre": alumna.persona.nombre,
        "Apellido": alumna.persona.apellido
    }
    
    for col_num, header in enumerate(headers_alumna, 1):
        cell = ws.cell(row=2, column=col_num, value=datos_alumna[header])
        cell.fill = data_fill
        cell.alignment = center_aligned_text

    # Escribir una fila en blanco para separar los datos de la alumna de la tabla de punteo acumulado
    start_row_acumulado = 4

    # Escribir los encabezados de la tabla de punteo acumulado
    headers_acumulado = ['Curso', 'Punteo Total', 'Grado', 'Año']
    for col_num, header in enumerate(headers_acumulado, 1):
        cell = ws.cell(row=start_row_acumulado, column=col_num, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_aligned_text
        
    # Escribir la tabla de punteo acumulado
    for r_idx, row in df_acumulado.iterrows():
        for col_num, value in enumerate(row, 1):
            cell = ws.cell(row=start_row_acumulado + r_idx + 1, column=col_num, value=value)
            cell.alignment = center_aligned_text

    # Ajustar el ancho de las columnas automáticamente
    for column in ws.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)
        for cell in column:
            try:
                if cell.value is not None:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        adjusted_width = max_length + 2
        ws.column_dimensions[column_letter].width = adjusted_width

    # Guardar el libro en la respuesta
    wb.save(response)

    return response
