from django.urls import path
from . import views

urlpatterns = [
    path('asistencia/', views.lista_asistencia, name='lista_asistencia'),
    path('asistencia/ver/', views.ver_asistencias, name='ver_asistencias'),
    path('asistencia/actualizar/<int:asignacion_id>/', views.actualizar_asistencia, name='actualizar_asistencia'),
    path('asistencia/<str:fecha>/', views.detalle_asistencia, name='detalle_asistencia'),
]
