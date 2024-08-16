from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from user.models import User
from django.http import HttpResponse
from decimal import *


@login_required
def inicio(request):
    if not request.user.is_authenticated and not request.user.is_active:
        return redirect('/')
    else:  

        return render(request, 'Inicio/inicio.html')






