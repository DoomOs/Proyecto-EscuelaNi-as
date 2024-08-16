from django.db import models

from Asignacion_Ciclo.models import AsignacionCiclo

# Create your models here.
class Asistencia(models.Model):
    fecha = models.DateField()
    presente = models.BooleanField(default=False)
    asignacion_ciclo = models.ForeignKey(AsignacionCiclo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fecha)