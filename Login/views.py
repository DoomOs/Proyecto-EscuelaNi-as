from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User


def login_in(request):
   try:
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            clave = form.cleaned_data.get('password')
            user = authenticate(username=usuario,password=clave)
            if user is not None :
               if user.is_active:
                       login(request,user)
                       request.session['member_id'] = user.id
                       return redirect('Inicio')
            else:
                return redirect('/')


    form = AuthenticationForm()
    return render(request,'Login/login.html',{'form':form})
   except AttributeError:
       messages.error(request, 'Credenciales Invalidas')
       return redirect('/')
       




def logout_out(request):
   try: 
    del request.session['member_id']
    logout(request)
    messages.success(request,'Sesion Finalizada con Exito')
    return redirect('Login')
   except AttributeError:
     return redirect('/')

