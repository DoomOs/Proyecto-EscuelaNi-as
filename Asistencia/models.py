from django.db import models

from Asignacion_Ciclo.models import AsignacionCiclo

# Create your models here.
class Asistencia(models.Model):
    """
        Modelo que representa la asistencia de una alumna en un día específico.

    Atributos:
       - fecha (DateField): Fecha de la asistencia.
       - presente (BooleanField): Indica si la alumna estuvo presente (True) o ausente (False).
       - asignacion_ciclo (ForeignKey): Relación con el modelo AsignacionCiclo, representando la asignación 
        del ciclo escolar de la alumna a la que se refiere esta asistencia.

    Métodos:
       - __str__(): Retorna una representación en cadena de la fecha de asistencia.

    """
    fecha = models.DateField()
    presente = models.BooleanField(default=False)
    asignacion_ciclo = models.ForeignKey(AsignacionCiclo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fecha)