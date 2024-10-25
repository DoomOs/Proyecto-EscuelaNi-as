import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Grado, Curso
from django.contrib import messages


@pytest.mark.django_db
def test_registrar_curso(client, django_user_model):
    """
    Caso de prueba: TC-013 - Registrar curso
    Descripción: Registrar nuevo curso
    Precondiciones:
        1. Que exista grados registrados.
        2. Que el curso no exista.
    Datos de entrada:
        1. Nombre del curso.
        2. Grado asignado.
        3. Estado.
    Pasos para la ejecución:
        1. Navegar hacia el módulo de cursos.
        2. Clic en nuevo curso.
        3. Llenar los campos requeridos.
        4. Clic en guardar.
    Resultado esperado:
        Que el sistema notifique que el curso fue registrado y que dirija hacia listado general de cursos.
    """

    user = django_user_model.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')

    # Crear grado
    grado = Grado.objects.create(nombre_grado='10')

    url = reverse('curso-create')
    response = client.post(url, {
        'nombre_curso': 'Curso de Matemáticas',
        'grado': grado.id,
        'estado': True
    })

    assert response.status_code == 302  # Debe redirigir después de guardar


@pytest.mark.django_db
def test_registrar_curso_fallido(client, django_user_model):
    """
    Caso de prueba: TC-014 - Registrar curso fallido
    Descripción: Intentar registrar un curso sin datos
    Precondiciones:
        1. Que exista grados registrados.
    Datos de entrada: Ninguno.
    Pasos para la ejecución:
        1. Navegar hacia el módulo de cursos.
        2. Clic en nuevo curso.
        3. No llenar los campos requeridos.
        4. Clic en guardar.
    Resultado esperado:
        Que el sistema notifique que los datos son requeridos y que no registre datos en blanco.
    """

    user = django_user_model.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')

    # Crear grado
    grado = Grado.objects.create(nombre_grado='10')

    url = reverse('curso-create')
    response = client.post(url, {
        'nombre_curso': '',
        'grado': '',
        'estado': True
    })

    assert response.status_code == 200  # Debe mostrar el formulario de nuevo curso


@pytest.mark.django_db
def test_editar_curso(client, django_user_model):
    """
    Caso de prueba: TC-015 - Editar curso
    Descripción: Actualizar un curso existente
    Precondiciones: Que el curso exista.
    Datos de entrada:
        1. Nombre del curso.
        2. Grado asignado.
        3. Estado.
    Pasos para la ejecución:
        1. Navegar al módulo de cursos.
        2. Listar todos los cursos y/o filtrar por nombre del curso.
        3. Clic en editar.
        4. Llenar o actualizar los campos requeridos.
        5. Clic en actualizar.
    Resultado esperado:
        Que el registro haya sido actualizado y que dirija al listado de cursos.
    """

    user = django_user_model.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')

    # Crear grado y curso
    grado = Grado.objects.create(nombre_grado='10')
    curso = Curso.objects.create(nombre_curso='Curso de Matemáticas', grado=grado, estado=True)

    url = reverse('curso-update', kwargs={'pk': curso.id})
    response = client.post(url, {
        'nombre_curso': 'Curso de Ciencias',
        'grado': grado.id,
        'estado': True
    })

    assert response.status_code == 302  # Debe redirigir después de actualizar
    curso.refresh_from_db()
    assert curso.nombre_curso == 'Curso de Ciencias'  # Debe haber cambiado el nombre del curso


@pytest.mark.django_db
def test_eliminar_curso(client, django_user_model):
    """
    Caso de prueba: TC-016 - Eliminar curso
    Descripción: Eliminar un curso
    Precondiciones: Que el curso exista.
    Datos de entrada: Ninguno.
    Pasos para la ejecución:
        1. Navegar al módulo de cursos.
        2. Listar todos los cursos y/o filtrar por nombre del curso.
        3. Clic en eliminar.
    Resultado esperado:
        Que el registro haya sido eliminado y que dirija al listado de cursos.
    """

    user = django_user_model.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')

    # Crear grado y curso
    grado = Grado.objects.create(nombre_grado='10')
    curso = Curso.objects.create(nombre_curso='Curso de Matemáticas', grado=grado, estado=True)

    url = reverse('curso-delete', kwargs={'pk': curso.id})
    response = client.post(url)




@pytest.mark.django_db
class TestGradoViews:

    @pytest.fixture
    def grado(self):
        """Fixture para crear un grado para las pruebas."""
        return Grado.objects.create(nombre_grado='Matemáticas', estado=True)

    @pytest.fixture
    def user(self, django_user_model):
        """Fixture para crear un usuario para las pruebas."""
        return django_user_model.objects.create_user(username='testuser', password='testpass')

    def test_registrar_grado(self, client, user):
        """
        Caso de prueba: TC-021 - Registro de grado
        Precondiciones: Ninguno
        Datos de entrada:
            1. Nombre: 'Ciencias'
            2. Estado: True
        Pasos para la ejecución:
            1. Navegar hacia el módulo de grados.
            2. Clic en registrar.
            3. Llenar los campos requeridos.
            4. Clic en guardar.
        Resultado esperado:
            Que el sistema registre debidamente el grado.
        """
        client.login(username='testuser', password='testpass')
        response = client.post(reverse('grado-create'), {
            'nombre_grado': 'Ciencias',
            'estado': True,
        })
        assert response.status_code == 302  # Redirección tras guardar
        assert Grado.objects.filter(nombre_grado='Ciencias').exists()

    def test_registrar_grado_fallido(self, client, user):
        """
        Caso de prueba: TC-022 - Registro de grado fallido
        Precondiciones: Ninguno
        Datos de entrada: Ninguno
        Pasos para la ejecución:
            1. Navegar hacia el módulo de grados.
            2. Clic en registrar.
            3. No llenar los campos requeridos.
            4. Clic en guardar.
        Resultado esperado:
            Que el sistema no guarde registros en blanco y que notifique de los campos faltantes.
        """
        client.login(username='testuser', password='testpass')
        response = client.post(reverse('grado-create'), {})
        assert response.status_code == 200  # Debe permanecer en la misma página
        assert 'Este campo es obligatorio.' in str(response.content)  # Mensaje de error esperado

    def test_editar_grado(self, client, user, grado):
        """
        Caso de prueba: TC-023 - Editar grado
        Precondiciones: Ninguno
        Datos de entrada:
            1. Nombre: 'Matemáticas Avanzadas'
            2. Estado: True
        Pasos para la ejecución:
            1. Navegar hacia el módulo de grados.
            2. Listar los grados.
            3. Clic en editar grado.
            4. Llenar los campos requeridos.
            5. Clic en actualizar.
        Resultado esperado:
            Que el sistema actualice debidamente el grado.
        """
        client.login(username='testuser', password='testpass')
        response = client.post(reverse('grado-update', args=[grado.id]), {
            'nombre_grado': 'Matemáticas Avanzadas',
            'estado': True,
        })
        assert response.status_code == 302  # Redirección tras actualizar
        grado.refresh_from_db()
        assert grado.nombre_grado == 'Matemáticas Avanzadas'

