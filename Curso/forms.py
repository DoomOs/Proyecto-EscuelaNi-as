from django import forms

from Curso.models import Curso, Grado

class CursoForm(forms.ModelForm):
    """
        Formulario para crear o actualizar un curso.

    Hereda:
       - forms.ModelForm: Clase base para formularios basados en modelos.

    Atributos:
       - Meta (class): Configuración de la clase, incluyendo el modelo y los campos a incluir en el formulario.

    """
    class Meta:
        model = Curso
        fields = '__all__'
    
    
class GradoForm(forms.ModelForm):
    """
        Formulario para crear o actualizar un grado.

    Hereda:
        - forms.ModelForm: Clase base para formularios basados en modelos.

    Atributos:
       - Meta (class): Configuración de la clase, incluyendo el modelo y los campos a incluir en el formulario.

    """
    class Meta:
        model = Grado
        fields = '__all__'