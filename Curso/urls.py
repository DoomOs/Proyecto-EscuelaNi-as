from django.urls import path
from .views import (
    CursoActivateView, CursoListView, CursoCreateView, CursoUpdateView, CursoDeleteView,
    CursoInactivoListView, GradoActivateView, GradoListView, GradoCreateView, GradoUpdateView, GradoDeleteView, GradoInactivoListView
)

urlpatterns = [
    path('cursos/', CursoListView.as_view(), name='curso-list'),
    path('cursos/nuevo/', CursoCreateView.as_view(), name='curso-create'),
    path('cursos/<int:pk>/editar/', CursoUpdateView.as_view(), name='curso-update'),
    path('cursos/<int:pk>/eliminar/', CursoDeleteView.as_view(), name='curso-delete'),
    path('cursos/inactivos/', CursoInactivoListView.as_view(), name='curso-inactivo-list'),  # Cursos inactivos
    path('cursos/<int:pk>/activar/', CursoActivateView.as_view(), name='curso-activar'),


    path('grados/', GradoListView.as_view(), name='grado-list'),
    path('grados/nuevo/', GradoCreateView.as_view(), name='grado-create'),
    path('grados/<int:pk>/editar/', GradoUpdateView.as_view(), name='grado-update'),
    path('grados/<int:pk>/eliminar/', GradoDeleteView.as_view(), name='grado-delete'),
    path('grados/inactivos/', GradoInactivoListView.as_view(), name='grado-inactivo-list'),  # Grados inactivos
    path('grados/<int:pk>/activar/', GradoActivateView.as_view(), name='grado-activar'),

]
