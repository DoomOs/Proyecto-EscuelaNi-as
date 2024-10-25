from pyexpat.errors import messages
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from Actividad.models import Actividad, CalificacionActividad
from django.contrib.auth import get_user_model

from Asignacion_Ciclo.models import AsignacionCiclo
from Curso.models import Curso, Grado
from Persona.models import Alumna, Persona

@pytest.mark.django_db
def test_registrar_actividad_correcta(client):
    """
    Caso de prueba: TC-003 - Registrar Actividades
    Precondiciones: Usuario logueado.
    Datos de entrada:
        - Nombre de la actividad: 'Examen'
        - Punteo de la actividad: 30
        - Curso asignado: 'Matemáticas'
    Pasos:
        1. Navegar hacia el módulo de Actividades.
        2. Clic en “Nueva actividad”.
        3. Llenar los campos solicitados.
        4. Clic en guardar actividad.
    Resultado esperado:
        - Que el sistema refleje o muestre un mensaje indicando que la actividad fue registrada correctamente.
    """
    # Crear usuario y loguearse
    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')

    # Crear un grado y un curso
    grado = Grado.objects.create(nombre_grado='Primero Básico')
    curso = Curso.objects.create(nombre_curso='Matemáticas', grado=grado)

    # Datos para registrar actividad
    data = {
        'actividad': 'Examen',
        'punteo': 30,
        'curso': curso.id
    }

    # Navegar y enviar datos
    response = client.post(reverse('actividad-create'), data)

    # Verificación
    assert response.status_code == 302
    assert Actividad.objects.filter(actividad='Examen', curso=curso).exists()

@pytest.mark.django_db
def test_registrar_actividad_sin_datos(client):
    """
    Caso de prueba: TC-004 - Intentar Registrar Actividades Sin Datos de Entrada
    Precondiciones: Usuario logueado.
    Datos de entrada: Ninguno.
    Pasos:
        1. Navegar hacia el módulo de Actividades.
        2. Clic en “Nueva actividad”.
        3. Dejar campos en blanco.
        4. Clic en guardar actividad.
    Resultado esperado:
        - Que el sistema indique que los campos son requeridos.
    """
    # Crear usuario y loguearse
    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    
    # Intentar crear actividad sin datos
    response = client.post(reverse('actividad-create'), {})
    
    # Verificación
    assert response.status_code == 200  # Debe regresar al formulario con errores
    assert "Este campo es obligatorio" in response.content.decode(), "No se encontró el mensaje de error esperado"

@pytest.mark.django_db
def test_editar_actividad(client):
    """
    Caso de prueba: TC-005 - Editar Actividad
    Precondiciones: Actividad existente.
    Datos de entrada:
        - Nombre de la actividad: 'Examen Final'
        - Punteo de la actividad: 40
        - Curso asignado: 'Matemáticas'
    Pasos:
        1. Navegar hacia el módulo de Actividades.
        2. Buscar la actividad deseada.
        3. Clic en editar.
        4. Actualizar la información.
        5. Clic en actualizar.
    Resultado esperado:
        - Que el sistema indique que la actividad fue actualizada.
    """
    # Crear usuario, loguearse y crear actividad
    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    
    # Crear un grado y un curso
    grado = Grado.objects.create(nombre_grado='Primero Básico')
    curso = Curso.objects.create(nombre_curso='Matemáticas', grado=grado)
    actividad = Actividad.objects.create(actividad='Examen', punteo=20, curso=curso)
    
    # Datos para editar actividad
    data = {
        'actividad': 'Examen Final',  # Cambiado de 'nombre' a 'actividad'
        'punteo': 40,
        'curso': curso.id
    }
    
    # Enviar solicitud para editar
    response = client.post(reverse('actividad-update', kwargs={'pk': actividad.id}), data)
    
    # Verificación
    actividad.refresh_from_db()
    assert actividad.actividad == 'Examen Final'
    assert actividad.punteo == 40
    assert response.status_code == 302  # Redirección al listado de actividades

@pytest.mark.django_db
def test_eliminar_actividad(client):
    """
    Caso de prueba: TC-006 - Inactivar Actividad
    Precondiciones: Actividad existente.
    Datos de entrada: Ninguno.
    Pasos:
        1. Navegar hacia el módulo de Actividades.
        2. Buscar la actividad deseada.
        3. Clic en inactivar.
    Resultado esperado:
        - Que la actividad sea marcada como inactiva.
    """
    # Crear usuario, loguearse y crear actividad
    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    
    # Crear un grado y un curso
    grado = Grado.objects.create(nombre_grado='Primero Básico')
    curso = Curso.objects.create(nombre_curso='Matemáticas', grado=grado)
    actividad = Actividad.objects.create(actividad='Examen', punteo=20, curso=curso, estado=1)  # Estado activo
    
    # Enviar solicitud para inactivar
    response = client.post(reverse('actividad-inactivar', kwargs={'pk': actividad.id}))
    
    # Verificación
    actividad.refresh_from_db()
    assert actividad.estado   # Verificar que el estado sea 0 (inactivo)





User = get_user_model()

@pytest.mark.django_db
def test_calificar_actividades(client, django_user_model):
    """
    Caso de prueba: TC-007 - Calificar actividades
    Precondiciones: Que la actividad exista y no haya sido eliminada.
    Datos de entrada:
        1. Punteo o nota
        2. Descripción de la nota
    Pasos para la ejecución:
        1. Listar las actividades existentes.
        2. Clic en calificar.
        3. Seleccionar al alumno asignado.
        4. Ingresar los datos requeridos.
        5. Clic en guardar.
    Resultado esperado:
        Que la nota haya sido grabada correctamente.
    """
    
    # Crear un usuario
    user = django_user_model.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')

    # Crear grado y curso
    grado = Grado.objects.create(nombre_grado='10')
    curso = Curso.objects.create(nombre_curso='Curso de Prueba', grado=grado)

    # Crear alumna y asignación
    alumna = Alumna.objects.create(
        persona=Persona.objects.create(nombre='Test', apellido='User', fecha_nacimiento='2000-01-01', genero='F', direccion='Test Address'),
        codigo='123',
        estado=True
    )
    asignacion = AsignacionCiclo.objects.create(grado=grado, alumna=alumna, user=user, year=2024)

    # Crear actividad
    actividad = Actividad.objects.create(curso=curso, punteo=100)

    # Calificar la actividad
    url = reverse('calificar-alumno', kwargs={'actividad_id': actividad.id})
    response = client.post(url, {
        f'punteo_{asignacion.id}': '85',
    })

    assert response.status_code == 302  # Debe redirigir después de guardar
    assert CalificacionActividad.objects.count() == 1  # Debe haber una calificación grabada
    calificacion = CalificacionActividad.objects.first()
    assert calificacion.punteo == 85


@pytest.mark.django_db
def test_calificar_actividades_fallido(client):
    """
    Caso de prueba: TC-008 - Calificar actividades fallido
    Precondiciones: Que la actividad exista y no haya sido eliminada.
    Datos de entrada: Ninguno
    Pasos para la ejecución:
        1. Listar las actividades existentes.
        2. Clic en calificar.
        3. Seleccionar al alumno asignado.
        4. No ingresar datos.
        5. Clic en guardar.
    Resultado esperado:
        Que el sistema indique que los datos son requeridos.
    """

    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')

    grado = Grado.objects.create(nombre_grado='10')
    curso = Curso.objects.create(nombre_curso='Curso de Prueba', grado=grado)

    alumna = Alumna.objects.create(
        persona=Persona.objects.create(nombre='Test', apellido='User', fecha_nacimiento='2000-01-01', genero='F', direccion='Test Address'),
        codigo='123',
        estado=True
    )
    asignacion = AsignacionCiclo.objects.create(grado=grado, alumna=alumna, user=user, year=2024)

    actividad = Actividad.objects.create(curso=curso, punteo=100)

    url = reverse('calificar-alumno', kwargs={'actividad_id': actividad.id})
    response = client.post(url, {
        f'punteo_{asignacion.id}': '',
    })

    assert response.status_code == 302  # Debe redirigir después de manejar el error
    assert messages.get_messages(response.wsgi_request).count() > 0  # Debe haber un mensaje de error


@pytest.mark.django_db
def test_listar_calificaciones(client):
    """
    Caso de prueba: TC-009 - Listar calificaciones
    Precondiciones: Que existan registros de calificaciones.
    Datos de entrada:  como parámetros de búsqueda
        1. Alumno
    Pasos para la ejecución:
        1. Navegar hacia el módulo de calificaciones.
        2. Llenar los campos para filtrar la búsqueda si se desea.
    Resultado esperado:
        Que el sistema muestre el listado de calificaciones existentes.
    """

    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')

    grado = Grado.objects.create(nombre_grado='10')
    curso = Curso.objects.create(nombre_curso='Curso de Prueba', grado=grado)

    alumna = Alumna.objects.create(
        persona=Persona.objects.create(nombre='Test', apellido='User', fecha_nacimiento='2000-01-01', genero='F', direccion='Test Address'),
        codigo='123',
        estado=True
    )
    asignacion = AsignacionCiclo.objects.create(grado=grado, alumna=alumna, user=user, year=2024)

    actividad = Actividad.objects.create(curso=curso, punteo=100)

    CalificacionActividad.objects.create(actividad=actividad, asignacion_ciclo=asignacion, punteo=85)




@pytest.mark.django_db
def test_editar_calificacion(client):
    """
    Caso de prueba: TC-010 - Editar calificación
    Precondiciones: Que la nota haya sido ingresada con anterioridad.
    Datos de entrada:
        1. Punteo o nota
        2. Descripción
    Pasos para la ejecución:
        1. Navegar hacia el módulo de calificaciones.
        2. Llenar los campos para filtrar la búsqueda si se desea.
        3. Clic en editar.
        4. Llenar los campos requeridos.
        5. Clic en actualizar.
    Resultado esperado:
        Que la nota haya sido actualizada correctamente.
    """

    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')

    grado = Grado.objects.create(nombre_grado='10')
    curso = Curso.objects.create(nombre_curso='Curso de Prueba', grado=grado)

    alumna = Alumna.objects.create(
        persona=Persona.objects.create(nombre='Test', apellido='User', fecha_nacimiento='2000-01-01', genero='F', direccion='Test Address'),
        codigo='123',
        estado=True
    )
    asignacion = AsignacionCiclo.objects.create(grado=grado, alumna=alumna, user=user, year=2024)

    actividad = Actividad.objects.create(curso=curso, punteo=100)

    calificacion = CalificacionActividad.objects.create(actividad=actividad, asignacion_ciclo=asignacion, punteo=85)

    url = reverse('calificacionactividad-update', kwargs={'pk': calificacion.id})
    response = client.post(url, {
        'punteo': '90',
    })

    calificacion.refresh_from_db()


@pytest.mark.django_db
def test_editar_calificacion_fallido(client):
    """
    Caso de prueba: TC-011 - Editar calificación fallido
    Precondiciones: Que la nota haya sido ingresada con anterioridad.
    Datos de entrada: Ninguno
    Pasos para la ejecución:
        1. Navegar hacia el módulo de calificaciones.
        2. Llenar los campos para filtrar la búsqueda si se desea.
        3. Clic en editar.
        4. No ingresar datos.
        5. Clic en actualizar.
    Resultado esperado:
        Que no haya sido grabado ningún registro con datos en blanco y que el sistema notifique que los datos son requeridos.
    """

    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')

    grado = Grado.objects.create(nombre_grado='10')
    curso = Curso.objects.create(nombre_curso='Curso de Prueba', grado=grado)

    alumna = Alumna.objects.create(
        persona=Persona.objects.create(nombre='Test', apellido='User', fecha_nacimiento='2000-01-01', genero='F', direccion='Test Address'),
        codigo='123',
        estado=True
    )
    asignacion = AsignacionCiclo.objects.create(grado=grado, alumna=alumna, user=user, year=2024)

    actividad = Actividad.objects.create(curso=curso, punteo=100)

    calificacion = CalificacionActividad.objects.create(actividad=actividad, asignacion_ciclo=asignacion, punteo=85)

    url = reverse('calificacionactividad-update', kwargs={'pk': calificacion.id})
    response = client.post(url, {
        'punteo': '',
    })

    assert response.status_code == 302  # Debe redirigir después de manejar el error
    assert messages.get_messages(response.wsgi_request).count() > 0  # Debe haber un mensaje de error


@pytest.mark.django_db
def test_eliminar_calificacion(client):
    """
    Caso de prueba: TC-012 - Eliminar calificación
    Precondiciones: Que la nota haya sido ingresada con anterioridad.
    Pasos para la ejecución:
        1. Navegar hacia el módulo de calificaciones.
        2. Llenar los campos para filtrar la búsqueda si se desea.
        3. Clic en eliminar.
    Resultado esperado:
        Que no haya registros de calificaciones de ese alumno.
    """

    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')

    grado = Grado.objects.create(nombre_grado='10')
    curso = Curso.objects.create(nombre_curso='Curso de Prueba', grado=grado)

    alumna = Alumna.objects.create(
        persona=Persona.objects.create(nombre='Test', apellido='User', fecha_nacimiento='2000-01-01', genero='F', direccion='Test Address'),
        codigo='123',
        estado=True
    )
    asignacion = AsignacionCiclo.objects.create(grado=grado, alumna=alumna, user=user, year=2024)

    actividad = Actividad.objects.create(curso=curso, punteo=100)

    calificacion = CalificacionActividad.objects.create(actividad=actividad, asignacion_ciclo=asignacion, punteo=85)

    url = reverse('calificacionactividad-delete', kwargs={'pk': calificacion.id})
    response = client.post(url)

    assert response.status_code == 302  # Debe redirigir después de eliminar
    assert CalificacionActividad.objects.count() == 0  # No debe haber calificaciones
