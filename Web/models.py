from django.db import models
from user.models import User


class Carrusel(models.Model):
    nombre = models.CharField(max_length=250, blank=False, null=False)
    descripcion = models.CharField(
        max_length=250, blank=True, null=True, default='')
    foto = models.ImageField(upload_to="carrusel", null=True, blank=True)
    fecha = models.DateTimeField(blank=True, null=True)
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
