from django.urls import path
from .views import (
    ActividadListView, ActividadCreateView, ActividadUpdateView, ActividadDeleteView,
    CalificacionActividadListView, CalificacionActividadCreateView, CalificacionActividadUpdateView, CalificacionActividadDeleteView, CalificarAlumnoView
)

urlpatterns = [
    path('actividades/', ActividadListView.as_view(), name='actividad-list'),
    path('actividades/nueva/', ActividadCreateView.as_view(), name='actividad-create'),
    path('actividades/<int:pk>/editar/', ActividadUpdateView.as_view(), name='actividad-update'),
    path('actividades/<int:pk>/eliminar/', ActividadDeleteView.as_view(), name='actividad-delete'),

    path('calificaciones/', CalificacionActividadListView.as_view(), name='calificacionactividad-list'),
    path('calificaciones/nueva/', CalificacionActividadCreateView.as_view(), name='calificacionactividad-create'),
    path('calificaciones/<int:pk>/editar/', CalificacionActividadUpdateView.as_view(), name='calificacionactividad-update'),
    path('calificaciones/<int:pk>/eliminar/', CalificacionActividadDeleteView.as_view(), name='calificacionactividad-delete'),
    path('calificar/<int:actividad_id>/', CalificarAlumnoView.as_view(), name='calificar-alumno'),

]
