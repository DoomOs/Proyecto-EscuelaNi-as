from django.urls import path

from Actividad.reportes import exportar_calificaciones_excel, exportar_punteo_acumulado_excel
from .views import (
    ActividadInactivaListView, ActividadInactivarView, ActividadListView, ActividadCreateView, ActividadReactivarView, ActividadUpdateView, ActividadDeleteView,
    CalificacionActividadListView, CalificacionActividadUpdateView, CalificacionActividadDeleteView, CalificarAlumnoView, get_anos_cursos, get_cursos
)
from .views import  calificaciones_alumna_view,get_total_punteo
from . import views

urlpatterns = [
    path('actividades/', ActividadListView.as_view(), name='actividad-list'),
    path('actividades/nueva/', ActividadCreateView.as_view(), name='actividad-create'),
    path('actividades/<int:pk>/editar/', ActividadUpdateView.as_view(), name='actividad-update'),
    path('actividad/inactivar/<int:pk>/', ActividadInactivarView.as_view(), name='actividad-inactivar'),
    path('reactivar/<int:actividad_id>/', ActividadReactivarView.as_view(), name='actividad-reactivar'),
    path('actividades-inactivas/', ActividadInactivaListView.as_view(), name='actividad-inactiva-list'),

    path('calificaciones/', CalificacionActividadListView.as_view(), name='calificacionactividad-list'),
    path('calificaciones/<int:pk>/editar/', CalificacionActividadUpdateView.as_view(), name='calificacionactividad-update'),
    path('calificaciones/<int:pk>/eliminar/', CalificacionActividadDeleteView.as_view(), name='calificacionactividad-delete'),
    path('calificar/<int:actividad_id>/', CalificarAlumnoView.as_view(), name='calificar-alumno'),
    
    
    path('calificaciones/<int:alumna_id>/', calificaciones_alumna_view, name='calificaciones-alumna'),
    path('get_anos_cursos/', get_anos_cursos, name='get_anos_cursos'),
    path('get_cursos/', get_cursos, name='get_cursos'),
    
    path('exportar_calificaciones/<int:alumna_id>/', exportar_calificaciones_excel, name='exportar_calificaciones'),
    path('exportar_punteo_acumulado/<int:alumna_id>/', exportar_punteo_acumulado_excel, name='exportar_punteo_acumulado'),

    path('get-total-punteo/<int:curso_id>/', get_total_punteo, name='get-total-punteo'),
    path('calificacionactividad/delete/<int:pk>/', CalificacionActividadDeleteView.as_view(), name='calificacionactividad-delete'),

    path('eliminar-calificacion/', views.eliminar_calificacion, name='eliminar_calificacion'),

]
