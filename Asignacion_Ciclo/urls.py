from django.urls import path
from .views import (
    AsignacionCicloListView, AsignacionCicloCreateView, AsignacionCicloUpdateView, AsignacionCicloDeleteView
)

urlpatterns = [
    path('', AsignacionCicloListView.as_view(), name='asignacionciclo-list'),
    #path('nueva/', AsignacionCicloCreateView.as_view(), name='asignacionciclo-create'),
    path('<int:pk>/editar/', AsignacionCicloUpdateView.as_view(), name='asignacionciclo-update'),
    path('<int:pk>/eliminar/', AsignacionCicloDeleteView.as_view(), name='asignacionciclo-delete'),
    
    path('asignar/<int:pk>/', AsignacionCicloCreateView.as_view(), name='asignacionciclo-create'),
]
