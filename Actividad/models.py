from django.db import models

from Asignacion_Ciclo.models import AsignacionCiclo
from Curso.models import Curso

# Create your models here.
class Actividad(models.Model):
    actividad = models.CharField(max_length=100)
    punteo = models.IntegerField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.actividad
    
class CalificacionActividad(models.Model):
    descripcion = models.CharField(max_length=100, null=True)
    punteo = models.IntegerField()
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    asignacion_ciclo = models.ForeignKey(AsignacionCiclo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('actividad', 'asignacion_ciclo')
    
    def __str__(self):
        return f"{self.asignacion_ciclo.alumna} - {self.descripcion}"