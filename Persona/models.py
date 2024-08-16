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

    def __str__(self):
        return self.codigo

class Contacto(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    alumna = models.ForeignKey(Alumna, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    parentesco = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.parentesco