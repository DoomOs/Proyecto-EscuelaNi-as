from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid



class Rol(models.Model):
    rol = models.CharField(max_length=20)

    def __str__(self):
        return self.rol

class User(AbstractUser):
    telefono = models.CharField(max_length=10, blank=True)
    id_ciclo = models.IntegerField(blank=True, null=True)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.username
    
