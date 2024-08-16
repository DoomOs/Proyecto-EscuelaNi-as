from django.urls import path
from .views import (
    AsistenciaListView, AsistenciaCreateView, AsistenciaUpdateView, AsistenciaDeleteView
)

urlpatterns = [
    path('', AsistenciaListView.as_view(), name='asistencia-list'),
    path('nueva/', AsistenciaCreateView.as_view(), name='asistencia-create'),
    path('<int:pk>/editar/', AsistenciaUpdateView.as_view(), name='asistencia-update'),
    path('<int:pk>/eliminar/', AsistenciaDeleteView.as_view(), name='asistencia-delete'),
]
