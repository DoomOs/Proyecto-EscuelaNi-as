from django.db import models

from Curso.models import Grado
from Persona.models import Alumna
from user.models import User

class AsignacionCiclo(models.Model):
    
    """
        Modelo que representa la asignación de una alumna a un grado en un año específico.

    Atributos:
       - grado (ForeignKey): Clave foránea que relaciona la asignación con el modelo Grado. 
            Elimina la asignación si el grado asociado se elimina.
       - alumna (ForeignKey): Clave foránea que relaciona la asignación con el modelo Alumna.
            Elimina la asignación si la alumna asociada se elimina.
       - user (ForeignKey): Clave foránea que relaciona la asignación con el modelo User.
            Elimina la asignación si el usuario asociado se elimina.
       - year (IntegerField): Campo que almacena el año de la asignación.

    Meta:
       - unique_together: Restringe que no se puedan crear asignaciones duplicadas para la misma alumna, grado y año.

    Métodos:
       - __str__():
            Devuelve una representación en forma de cadena de la asignación, que incluye el nombre y apellido de la alumna, 
            el nombre del grado y el año.
            
            Retorna:
                str: Cadena formateada que describe la asignación.

    """
    
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)
    alumna = models.ForeignKey(Alumna, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()

    class Meta:
        unique_together = ('alumna', 'grado', 'year')  # Modificamos la restricción de unicidad

    def __str__(self):
        return f"{self.alumna.persona.nombre} {self.alumna.persona.apellido} - {self.grado.nombre_grado} ({self.year})"



class Promocion(models.Model):
    año = models.IntegerField()
    asignacion_ciclo = models.ForeignKey(AsignacionCiclo, on_delete=models.CASCADE)
    aprobado = models.BooleanField()

    def __str__(self):
        estado = "Aprobado" if self.aprobado else "Reprobado"
        return f"{self.asignacion_ciclo.alumna.persona.nombre} {self.asignacion_ciclo.alumna.persona.apellido} - {estado} ({self.año})"