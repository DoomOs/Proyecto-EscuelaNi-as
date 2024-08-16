from django.db import models

# Create your models here.

class Grado(models.Model):
    nombre_grado = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_grado
    


class Curso(models.Model):
    nombre_curso = models.CharField(max_length=100)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_curso