"""
URL configuration for escuela project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('web',include('Web.urls')),
    path('usuarios/',include('user.urls')),
    path('',include('Login.urls')),
    path('inicio/',include('Inicio.urls')), 
    
    path('Actividad/',include('Actividad.urls')), 
    path('Asignacion_Ciclo/',include('Asignacion_Ciclo.urls')), 
    path('Persona/',include('Persona.urls')), 
    path('Curso/',include('Curso.urls')), 
    path('Asistencia/',include('Asistencia.urls')), 
    
]
