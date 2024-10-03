from django import forms

from Asignacion_Ciclo.models import AsignacionCiclo

class AsignacionCicloForm(forms.ModelForm):
    """
        Formulario que se utiliza para crear o actualizar una asignación de ciclo.

    Hereda:
        forms.ModelForm: Clase base para crear formularios a partir de modelos de Django.

    Meta:
        model (AsignacionCiclo): Modelo que se utilizará para generar el formulario.
        fields (list): Lista de campos que se incluirán en el formulario, en este caso 'grado' y 'year'.

    """
    class Meta:
        model = AsignacionCiclo
        fields = ['grado', 'year']
