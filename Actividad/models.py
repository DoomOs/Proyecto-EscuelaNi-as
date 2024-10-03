from django.db import models

from Asignacion_Ciclo.models import AsignacionCiclo
from Curso.models import Curso

# Create your models here.
class Actividad(models.Model):
    
    """
Modelo que representa una actividad asignada en un curso.

Atributos:
    - ACTIVIDAD_ESTADOS (tuple): Opciones de estado de la actividad (activa o inactiva).
    - actividad (str): Nombre de la actividad, con un máximo de 100 caracteres.
    - punteo (int): Valor máximo de punteo asignado a la actividad.
    - curso (ForeignKey): Relación con el modelo `Curso`. La actividad pertenece a un curso específico.
    - fecha (date): Fecha en la que se creó la actividad, asignada automáticamente.
    - estado (int): Estado de la actividad (1 para activa, 0 para inactiva). Por defecto, el valor es 1 (activa).

Métodos:
    - __str__: Devuelve una representación en cadena de la actividad, que corresponde a su nombre.
"""

    
    
    ACTIVIDAD_ESTADOS = (
        (1, 'Activa'),
        (0, 'Inactiva')
    )
    actividad = models.CharField(max_length=100)
    punteo = models.IntegerField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    estado = models.IntegerField(choices=ACTIVIDAD_ESTADOS, default=1)  # Estado por defecto: activa
    
    def __str__(self):
        return self.actividad

    
class CalificacionActividad(models.Model):
    
    """
Modelo que representa la calificación de una actividad para una alumna específica.

Atributos:
   - descripcion (str): Descripción de la calificación, con un máximo de 100 caracteres. Puede ser nula.
   - punteo (int): Punteo otorgado a la alumna para la actividad.
   - actividad (ForeignKey): Relación con el modelo `Actividad`. La calificación pertenece a una actividad específica.
   - asignacion_ciclo (ForeignKey): Relación con el modelo `AsignacionCiclo`. Identifica a la alumna a la que pertenece la calificación.

Meta:
   - unique_together: Garantiza que cada alumna tenga una única calificación por actividad.

Métodos:
   - __str__: Devuelve una representación en cadena de la calificación, mostrando el nombre de la alumna y la descripción de la calificación.
"""

    
    descripcion = models.CharField(max_length=100, null=True)
    punteo = models.IntegerField()
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    asignacion_ciclo = models.ForeignKey(AsignacionCiclo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('actividad', 'asignacion_ciclo')
    
    def __str__(self):
        return f"{self.asignacion_ciclo.alumna} - {self.descripcion}"