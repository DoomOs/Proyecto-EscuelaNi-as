from django.db import models

from Curso.models import Grado
from Persona.models import Alumna
from user.models import User

class AsignacionCiclo(models.Model):
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)
    alumna = models.ForeignKey(Alumna, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()

    class Meta:
        unique_together = ('alumna', 'grado', 'year')  # Modificamos la restricción de unicidad

    def __str__(self):
        return f"{self.alumna.persona.nombre} {self.alumna.persona.apellido} - {self.grado.nombre_grado} ({self.year})"
