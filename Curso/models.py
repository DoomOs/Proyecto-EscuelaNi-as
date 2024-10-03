from django.db import models

class Grado(models.Model):
    """
        Modelo que representa un grado académico.

    Atributos:
        nombre_grado (str): Nombre del grado, con un máximo de 50 caracteres.
        estado (bool): Estado del grado, que indica si está activo (True) o inactivo (False).

    Métodos:
        __str__(): Devuelve una representación en forma de cadena del grado, que es su nombre.

    """
    nombre_grado = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)  # Estado: activo/inactivo

    def __str__(self):
        return self.nombre_grado


class Curso(models.Model):
    """
        Modelo que representa un curso académico.

    Atributos:
        nombre_curso (str): Nombre del curso, con un máximo de 100 caracteres.
        grado (ForeignKey): Relación con el modelo Grado, que indica a qué grado pertenece el curso.
        estado (bool): Estado del curso, que indica si está activo (True) o inactivo (False).

    Métodos:
        __str__(): Devuelve una representación en forma de cadena del curso, que es su nombre.

    """
    nombre_curso = models.CharField(max_length=100)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)  # Estado: activo/inactivo

    def __str__(self):
        return self.nombre_curso
