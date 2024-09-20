from django.db import models

from Curso.models import Grado
from user.models import User

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1)
    direccion = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Alumna(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=30)
    estado = models.BooleanField(default=True) 

    def __str__(self):
        return self.codigo

class Contacto(models.Model):
    alumna = models.ForeignKey(Alumna, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    parentesco = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"