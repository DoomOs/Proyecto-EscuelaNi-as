import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_login_correcto(client):
    """
    Caso de prueba: TC-001 - Login correcto
    Precondiciones: Usuario registrado.
    Datos de entrada:
        - Usuario: 'testuser'
        - Contraseña: 'testpassword123'
    Pasos:
        1. Ir a la página de inicio de sesión.
        2. Ingresar credenciales correctas.
    Resultado esperado:
        - El sistema redirige a la página principal.
    """
    # Configuración: Crear usuario
    User = get_user_model()
    User.objects.create_user(username='testuser', password='testpassword123')
    
    # Ejecución
    response = client.post(reverse('Login'), {'username': 'testuser', 'password': 'testpassword123'})
    
    # Verificación
    assert response.status_code == 302  # Verificar redirección
    assert response.url == reverse('Inicio')

@pytest.mark.django_db
def test_login_incorrecto(client):
    """
    Caso de prueba: TC-002 - Login incorrecto
    Precondiciones: Usuario registrado.
    Datos de entrada:
        - Usuario: 'testuser'
        - Contraseña: 'wrongpassword'
    Pasos:
        1. Ir a la página de inicio de sesión.
        2. Ingresar credenciales incorrectas.
    Resultado esperado:
        - El sistema no permite el acceso y muestra mensaje de error.
    """
    # Configuración: Crear usuario
    User = get_user_model()
    User.objects.create_user(username='testuser', password='testpassword123')
    
    # Ejecución
    response = client.post(reverse('Login'), {'username': 'testuser', 'password': 'wrongpassword'})
    
    # Verificación
    assert response.status_code == 200  # Verificar que se mantiene en la misma página
    assert "Credenciales inválidas, intenta nuevamente." in response.content.decode(), "El mensaje de error no apareció en la página."
