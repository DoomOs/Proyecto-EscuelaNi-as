from django.urls import path
from . import views

urlpatterns = [
    path('asistencia/', views.lista_asistencia, name='lista_asistencia'),
    path('asistencia/ver/', views.ver_asistencias, name='ver_asistencias'),
    path('asistencia/actualizar/<int:asignacion_id>/<int:presente>/', views.actualizar_asistencia, name='actualizar_asistencia'),
    path('asistencia/<str:fecha>/', views.detalle_asistencia, name='detalle_asistencia'),
    
    
     path('asistencia/pdf/<str:fecha>/', views.generar_pdf, name='generar_pdf'),
    path('asistencia/excel/<str:fecha>/', views.generar_excel, name='generar_excel'),
]
