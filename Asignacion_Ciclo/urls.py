from django.urls import path
from .views import (
     AsignacionCicloCreateView, AsignacionCicloUpdateView, AsignacionCicloDeleteView
)
from .views import AsignacionCicloListView

urlpatterns = [
    path('', AsignacionCicloListView, name='asignacionciclo-list'),
    #path('nueva/', AsignacionCicloCreateView.as_view(), name='asignacionciclo-create'),
    path('<int:pk>/editar/', AsignacionCicloUpdateView.as_view(), name='asignacionciclo-update'),
    path('<int:pk>/eliminar/', AsignacionCicloDeleteView.as_view(), name='asignacionciclo-delete'),
    
    path('asignar/<int:pk>/', AsignacionCicloCreateView.as_view(), name='asignacionciclo-create'),
]
