from django.db import models

class Grado(models.Model):
    nombre_grado = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)  # Estado: activo/inactivo

    def __str__(self):
        return self.nombre_grado


class Curso(models.Model):
    nombre_curso = models.CharField(max_length=100)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)  # Estado: activo/inactivo

    def __str__(self):
        return self.nombre_curso
