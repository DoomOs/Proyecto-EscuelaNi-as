import pytest
from django.urls import reverse
from django.utils import timezone

from Asignacion_Ciclo.models import AsignacionCiclo
from Asistencia.models import Asistencia
from Curso.models import Grado
from Persona.models import Alumna, Persona

@pytest.mark.django_db
class TestAsistenciaViews:

    @pytest.fixture
    def user(self, django_user_model):
        # Crear un usuario normal
        return django_user_model.objects.create_user(username='testuser', password='testpass')

    @pytest.fixture
    def persona(self):
        # Crear una instancia de Persona
        return Persona.objects.create(
            nombre='Test',
            apellido='User',
            fecha_nacimiento='2000-01-01',
            genero='M',
            direccion='123 Test St'
        )

    @pytest.fixture
    def alumna(self, persona):
        # Crear una instancia de Alumna asociada a Persona
        return Alumna.objects.create(persona=persona, codigo='A001', estado=True)

    @pytest.fixture
    def grado(self):
        # Crear un grado para la prueba
        return Grado.objects.create(nombre_grado='Primer Grado', estado=True)

    @pytest.fixture
    def asignacion(self, alumna, grado, user):
        # Crear una asignación de ciclo para la prueba, asegurándose de asignar un usuario
        return AsignacionCiclo.objects.create(alumna=alumna, grado=grado, user=user, year=timezone.now().year)

    def test_toma_asistencia(self, client, user, alumna):
        """
        Caso de prueba: TC-026 - Toma de asistencia
        Precondiciones: Que existan alumnos registrados
        Datos de entrada: Ninguno, se utiliza un checklist de Si/No
        Pasos para la ejecución:
            1. Navegar al grado deseado.
            2. Listar los alumnos del grado.
            3. Seleccionar la opción deseada por alumno, si asistió o no lo hizo.
        Resultado esperado:
            Que al hacer clic sobre SI o NO, que el sistema se actualice mostrando la asistencia del alumno chequeado.
        """
        # Loguear al usuario
        client.login(username='testuser', password='testpass')

        # Crear una asignación de ciclo para la alumna
        grado = Grado.objects.create(nombre_grado='Matemáticas')
        asignacion_ciclo = AsignacionCiclo.objects.create(
            grado=grado,
            alumna=alumna,
            user=user,  # Asegúrate de que este usuario esté bien creado
            year=2024
        )

        # Simular la solicitud para la lista de asistencia
        response = client.get(reverse('lista_asistencia'))


        # Probar la actualización de asistencia
        response = client.post(reverse('actualizar_asistencia', args=[asignacion_ciclo.id, 1]))  # 1 para 'presente'

        # Verificar que la asistencia se ha actualizado
        asistencia = Asistencia.objects.get(asignacion_ciclo=asignacion_ciclo)


    