from django.urls import path
from .views import (
    UserListView, UserCreateView, UserUpdateView, UserDeleteView,
)
    #RolListView, RolCreateView, RolUpdateView, RolDeleteView

urlpatterns = [
    path('usuarios/', UserListView.as_view(), name='user-list'),
    path('usuarios/nuevo/', UserCreateView.as_view(), name='user-create'),
    path('usuarios/<int:pk>/editar/', UserUpdateView.as_view(), name='user-update'),
    path('usuarios/<int:pk>/eliminar/', UserDeleteView.as_view(), name='user-delete'),

    #path('roles/', RolListView.as_view(), name='rol-list'),
    #path('roles/nuevo/', RolCreateView.as_view(), name='rol-create'),
    #path('roles/<int:pk>/editar/', RolUpdateView.as_view(), name='rol-update'),
    #path('roles/<int:pk>/eliminar/', RolDeleteView.as_view(), name='rol-delete'),
]
