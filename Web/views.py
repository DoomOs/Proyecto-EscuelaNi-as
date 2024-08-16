from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from Web.models import Carrusel


def inicio(request):
    carrusel = Carrusel.objects.all().order_by('fecha')
    return render(request, 'Web/inicio.html', {'c': carrusel})
