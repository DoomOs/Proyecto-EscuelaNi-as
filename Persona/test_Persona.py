import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from Curso.models import Grado
from .models import Persona, Alumna

User = get_user_model()  # Obtiene el modelo de usuario personalizado

@pytest.mark.django_db
class TestAlumnaViews:

    @pytest.fixture
    def user(self):
        """Crea un usuario de prueba."""
        return User.objects.create_user(username='testuser', password='testpass')

    @pytest.fixture
    def grado(self):
        """Crea un grado de prueba."""
        return Grado.objects.create(nombre_grado='Matemáticas')

    @pytest.fixture
    def persona(self):
        """Crea una persona de prueba."""
        return Persona.objects.create(
            nombre='Test',
            apellido='Alumna',
            fecha_nacimiento='2000-01-01',
            genero='F',
            direccion='Dirección de prueba',
        )

    @pytest.fixture
    def alumna(self, persona):
        """Crea una alumna de prueba."""
        return Alumna.objects.create(
            persona=persona,
            codigo='12345',
            estado=True,
        )

    def test_registrar_alumna(self, client, user, grado):
        """
        Caso de prueba: TC-017 - Registrar alumna
        Precondiciones: 1. Que la alumna no exista
                        2. Que existan grados registrados
        Datos de entrada:
            1. Nombre: 'Nuevo'
            2. Apellido: 'Alumno'
            3. Fecha de nacimiento: '2000-01-01'
            4. Genero: 'M'
            5. Dirección: 'Dirección nueva'
            6. Código: '54321'
            7. Grado: 'Matemáticas'
            8. Año: 2024
        Pasos:
            1. Navegar hacia el módulo de alumnas.
            2. Clic en registrar.
            3. Llenar los campos requeridos.
            4. Clic en guardar.
        Resultado esperado:
            Que el sistema registre correctamente a la alumna.
        """
        client.login(username='testuser', password='testpass')
        response = client.post(reverse('alumna-create'), {
            'nombre': 'Nuevo',
            'apellido': 'Alumno',
            'fecha_nacimiento': '2000-01-01',
            'genero': 'M',
            'direccion': 'Dirección nueva',
            'codigo': '54321',
            'grado': grado.id,  # Asegúrate de que el grado existe
        })
        

    def test_registrar_alumna_fallido(self, client, user):
        """
        Caso de prueba: TC-018 - Registrar alumna fallido
        Precondiciones: Ninguno
        Datos de entrada: Ninguno
        Pasos para la ejecución:
            1. Navegar hacia el módulo de alumnas.
            2. Clic en registrar.
            3. No llenar los campos requeridos.
            4. Clic en guardar.
        Resultado esperado:
            Que el sistema no registre datos en blanco y que notifique de los campos requeridos.
        """
        client.login(username='testuser', password='testpass')
        response = client.post(reverse('alumna-create'), {})  # Enviar un formulario vacío
        assert response.status_code == 200  # Debería volver a la misma página
        assert 'Este campo es obligatorio' in response.content.decode()

    def test_editar_alumna(self, client, user, alumna, grado):
        """
        Caso de prueba: TC-019 - Editar alumna
        Precondiciones: 1. Que la alumna se encuentre registrada
                        2. Que existan grados registrados
        Datos de entrada:
            1. Nombre: 'Test Editado'
            2. Apellido: 'Alumna'
            3. Fecha de nacimiento: '2000-01-01'
            4. Genero: 'F'
            5. Dirección: 'Dirección editada'
            6. Código: '12345'
            7. Grado: 'Matemáticas'
            8. Año: 2024
        Pasos para la ejecución:
            1. Navegar hacia el módulo de alumnas.
            2. Listar alumnas y/o filtrar por nombre.
            3. Clic en editar.
            4. Llenar los campos requeridos.
            5. Clic en actualizar.
        Resultado esperado:
            Que el sistema actualice correctamente a la alumna.
        """
        client.login(username='testuser', password='testpass')
        # Actualiza el grado si es necesario, dependiendo de tu lógica de negocio
        response = client.post(reverse('alumna-edit', args=[alumna.id]), {
            'nombre': 'Test Editado',
            'apellido': 'Alumna',
            'fecha_nacimiento': '2000-01-01',
            'genero': 'F',
            'direccion': 'Dirección editada',
            'codigo': '12345',
            'grado': grado.id,  # Usa el grado creado en la fixture
        })
        assert response.status_code == 302  # Redirecciona tras editar
        alumna.refresh_from_db()
        assert alumna.persona.nombre == 'Test Editado'


    def test_listar_alumnas(self, client, user):
        """
        Caso de prueba: TC-020 - Listar alumnas
        Precondiciones: Que existan alumnas registradas
        Datos de entrada: Filtros
            1. Nombre
            2. Grado
        Pasos para la ejecución:
            1. Navegar al módulo de alumnas.
            2. Filtrar datos si se desea; si no se filtran, se entiende que obtienen todos los datos.
        Resultado esperado:
            Visualizar correctamente el listado de alumnas.
        """
        client.login(username='testuser', password='testpass')
        response = client.get(reverse('alumna-list'))
        assert response.status_code == 200
        assert b'Listado de Alumnas' in response.content  # Asegúrate de que el texto esté presente
