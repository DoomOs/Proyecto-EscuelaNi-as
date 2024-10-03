from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User


def login_in(request):
    """
        Maneja el proceso de inicio de sesión de un usuario.

    Parámetros:
        request (HttpRequest): La solicitud HTTP que contiene datos del formulario de inicio de sesión.

    Retorna:
        HttpResponse: Redirige a la página de inicio si las credenciales son válidas, o de lo contrario, renderiza el formulario de inicio de sesión con un mensaje de error.

    Excepciones:
        AttributeError: Si hay un problema al acceder a los datos del formulario, muestra un mensaje de error de credenciales inválidas.

    Proceso:
        - Si el método de la solicitud es POST, se valida el formulario con las credenciales proporcionadas.
        - Si las credenciales son válidas y el usuario está activo, se inicia sesión y se redirige a la página de inicio.
        - Si las credenciales son inválidas, se redirige a la página principal con un mensaje de error.

    """
    
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
    """
        Maneja el proceso de cierre de sesión de un usuario.

    Parámetros:
        request (HttpRequest): La solicitud HTTP que contiene la información de la sesión del usuario.

    Retorna:
        HttpResponse: Redirige a la página de inicio de sesión después de cerrar la sesión.

    Excepciones:
        AttributeError: Si hay un problema al acceder a la sesión, redirige a la página principal.

    Proceso:
        - Se eliminan los datos de la sesión del usuario.
        - Se cierra la sesión del usuario y se muestra un mensaje de éxito.

    """
    try: 
        del request.session['member_id']
        logout(request)
        messages.success(request,'Sesion Finalizada con Exito')
        return redirect('Login')
    except AttributeError:
        return redirect('/')

