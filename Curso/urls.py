from django.urls import path
from .views import (
    CursoListView, CursoCreateView, CursoUpdateView, CursoDeleteView,
    GradoListView, GradoCreateView, GradoUpdateView, GradoDeleteView
)

urlpatterns = [
    path('cursos/', CursoListView.as_view(), name='curso-list'),
    path('cursos/nuevo/', CursoCreateView.as_view(), name='curso-create'),
    path('cursos/<int:pk>/editar/', CursoUpdateView.as_view(), name='curso-update'),
    path('cursos/<int:pk>/eliminar/', CursoDeleteView.as_view(), name='curso-delete'),

    path('grados/', GradoListView.as_view(), name='grado-list'),
    path('grados/nuevo/', GradoCreateView.as_view(), name='grado-create'),
    path('grados/<int:pk>/editar/', GradoUpdateView.as_view(), name='grado-update'),
    path('grados/<int:pk>/eliminar/', GradoDeleteView.as_view(), name='grado-delete'),
]
