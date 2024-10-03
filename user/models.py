from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid



class Rol(models.Model):
    """
        Modelo que representa un rol de usuario en el sistema.

    Hereda:
       - models.Model: Clase base para todos los modelos de Django.

    Atributos:
       - rol (CharField): Nombre del rol del usuario, con un máximo de 20 caracteres.

    Métodos:
       - __str__(self): Devuelve una representación en cadena del rol, que es el nombre del rol.

    """
    rol = models.CharField(max_length=20)

    def __str__(self):
        return self.rol

class User(AbstractUser):
    """
        Modelo que extiende el modelo de usuario de Django para incluir campos adicionales.

    Hereda:
       - AbstractUser: Clase base que proporciona la funcionalidad del modelo de usuario de Django.

    Atributos heredados de AbstractUser:
       - username (CharField): Nombre de usuario único para la autenticación.
       - first_name (CharField): Nombre de pila del usuario.
       - last_name (CharField): Apellido del usuario.
       - email (EmailField): Correo electrónico del usuario, único por defecto.
       - password (CharField): Contraseña encriptada del usuario.
       - is_staff (BooleanField): Indica si el usuario puede acceder al área de administración.
       - is_active (BooleanField): Indica si el usuario está activo.
       - is_superuser (BooleanField): Indica si el usuario tiene todos los permisos sin necesidad de asignación.
       - last_login (DateTimeField): Fecha y hora del último inicio de sesión del usuario.
       - date_joined (DateTimeField): Fecha y hora en que el usuario se registró.
    
    Atributos adicionales:
       - telefono (CharField): Número de teléfono del usuario, opcional, con un máximo de 10 caracteres.
       - id_ciclo (IntegerField): Identificador del ciclo al que está asignado el usuario, opcional.
       - id_rol (ForeignKey): Relación con el modelo Rol, que indica el rol del usuario en el sistema.
           - on_delete (CASCADE): Elimina el usuario si el rol asociado es eliminado.
           - blank (bool): Permite que el campo sea vacío.
           - null (bool): Permite que el campo sea nulo.

    Métodos:
       - __str__(self): Devuelve una representación en cadena del usuario, que es el nombre de usuario.

    """
    telefono = models.CharField(max_length=10, blank=True)
    id_ciclo = models.IntegerField(blank=True, null=True)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.username
    
