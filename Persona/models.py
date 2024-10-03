from django.db import models

from Curso.models import Grado
from user.models import User

# Create your models here.
class Persona(models.Model):
    """
        Representa a una persona con información básica.

    Hereda:
       - models.Model: Clase base para todos los modelos de Django.

    Atributos:
       - nombre (CharField): El nombre de la persona, con una longitud máxima de 100 caracteres.
       - apellido (CharField): El apellido de la persona, con una longitud máxima de 100 caracteres.
       - fecha_nacimiento (DateField): La fecha de nacimiento de la persona.
       - genero (CharField): El género de la persona, representado por un solo carácter (por ejemplo, 'M' para masculino, 'F' para femenino).
       - direccion (CharField): La dirección de la persona, con una longitud máxima de 150 caracteres.

    Métodos:
       - __str__(): Devuelve una representación en cadena del objeto, que consiste en el nombre y apellido de la persona.

    """
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1)
    direccion = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Alumna(models.Model):
    """
        Representa a una alumna con información específica relacionada con la educación.

    Hereda:
       - models.Model: Clase base para todos los modelos de Django.

    Atributos:
       - persona (OneToOneField): Relación uno a uno con el modelo Persona, representando la información personal de la alumna.
       - codigo (CharField): Un código único para identificar a la alumna, con una longitud máxima de 30 caracteres.
       - estado (BooleanField): El estado de la alumna, activo (True) o inactivo (False), con un valor predeterminado de True.

    Métodos:
       - __str__(): Devuelve una representación en cadena del objeto, que consiste en el código de la alumna.

    """
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=30)
    estado = models.BooleanField(default=True) 

    def __str__(self):
        return self.codigo

class Contacto(models.Model):
    """
        Representa a un contacto asociado a una alumna.

    Hereda:
       - models.Model: Clase base para todos los modelos de Django.

    Atributos:
       - alumna (ForeignKey): Relación con el modelo Alumna, permitiendo la asociación de múltiples contactos con una sola alumna.
       - nombre (CharField): El nombre del contacto, con una longitud máxima de 100 caracteres.
       - apellido (CharField): El apellido del contacto, con una longitud máxima de 100 caracteres.
       - parentesco (CharField): El parentesco del contacto con la alumna, con una longitud máxima de 100 caracteres.
       - telefono (CharField): El número de teléfono del contacto, con una longitud máxima de 15 caracteres.
       - email (EmailField): La dirección de correo electrónico del contacto.

    Métodos:
       - __str__(): Devuelve una representación en cadena del objeto, que consiste en el nombre y apellido del contacto.

    """
    alumna = models.ForeignKey(Alumna, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    parentesco = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"