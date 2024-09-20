from django.urls import path
from .views import activar_alumna_view, alumna_edit_view, alumna_inactive_list_view, alumna_list_view, contacto_delete_view, contacto_edit_view, desactivar_alumna_view, persona_create_view, alumna_create_view, contacto_create_view

urlpatterns = [
    path('', alumna_list_view, name='alumna-list'),
    path('alumna/create/', alumna_create_view, name='alumna-create'),
    path('<int:alumna_id>/editar/', alumna_edit_view, name='alumna-edit'),
    path('persona/create/', persona_create_view, name='persona-create'),
    path('contacto/create/<int:alumna_id>/', contacto_create_view, name='contacto-create'),
    path('contacto/edit/<int:contacto_id>/', contacto_edit_view, name='contacto-edit'),
    path('contacto/delete/<int:contacto_id>/', contacto_delete_view, name='contacto-delete'),
    
    
    
    path('alumnas/inactivas/', alumna_inactive_list_view, name='alumna-inactive-list'),
    path('alumna/desactivar/<int:alumna_id>/', desactivar_alumna_view, name='alumna-desactivar'),
    path('alumna/activar/<int:alumna_id>/', activar_alumna_view, name='alumna-activar'),
    ]
