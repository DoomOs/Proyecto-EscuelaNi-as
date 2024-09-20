from django.urls import path
from .views import (
     AsignacionCicloCreateView, AsignacionCicloUpdateView, AsignacionCicloDeleteView, 
)
from .views import AsignacionCicloListView, asignar_alumnas,asignar_grado_usuario

urlpatterns = [
    path('', AsignacionCicloListView, name='asignacionciclo-list'),
    #path('nueva/', AsignacionCicloCreateView.as_view(), name='asignacionciclo-create'),
    path('<int:pk>/editar/', AsignacionCicloUpdateView.as_view(), name='asignacionciclo-update'),
    path('<int:pk>/eliminar/', AsignacionCicloDeleteView.as_view(), name='asignacionciclo-delete'),
    
    path('asignar/<int:pk>/', AsignacionCicloCreateView.as_view(), name='asignacionciclo-create'),
    
    
     # URL para asignar alumnas al ciclo de un grado
    path('grado/<int:grado_id>/asignar-alumnas/', asignar_alumnas, name='asignar-alumnas'),

    # URL para asignar el ciclo al docente (user)
    path('asignar-grado-usuario/', asignar_grado_usuario, name='asignar-grado-usuario'),
]
