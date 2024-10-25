import pytest
from django.urls import reverse

from Curso.models import Grado
from user.models import User

@pytest.mark.django_db
class TestAsignarDocentesViews:

    @pytest.fixture
    def grado(self):
        """Fixture para crear un grado para las pruebas."""
        return Grado.objects.create(nombre_grado='Matemáticas', estado=True)

    @pytest.fixture
    def user(self, django_user_model):
        """Fixture para crear un usuario administrativo para las pruebas."""
        return django_user_model.objects.create_user(username='adminuser', password='adminpass')

    def test_asignar_docente(self, client, user, grado):
        """
        Caso de prueba: TC-024 - Asignar docentes
        Precondiciones: Que existan grados registrados
        Datos de entrada:
            1. Nombre del docente: 'Juan'
            2. Apellido del docente: 'Pérez'
            3. Grado para asignar: 'Matemáticas'
        Pasos para la ejecución:
            1. Navegar al módulo de administración.
            2. Clic en docentes.
            3. Clic en nuevo docente.
            4. Llenar los campos requeridos.
            5. Clic en registrar.
        Resultado esperado:
            Que el sistema registre correctamente al docente.
        """
        client.login(username='adminuser', password='adminpass')
      
        

    def test_asignar_docente_fallido(self, client, user):
        """
        Caso de prueba: TC-025 - Asignar docentes fallido
        Precondiciones: Que existan grados registrados
        Datos de entrada: Ninguno
        Pasos para la ejecución:
            1. Navegar al módulo de administración.
            2. Clic en docentes.
            3. Clic en nuevo docente.
            4. No llenar los campos requeridos.
            5. Clic en registrar.
        Resultado esperado:
            Que el sistema no registre campos en blanco y que notifique.
        """
        client.login(username='adminuser', password='adminpass')
        response = client.post(reverse('Inicio'), {})
        assert response.status_code == 200  # Debe permanecer en la misma página
        assert 'Este campo es obligatorio.' in str(response.content)  # Mensaje de error esperado