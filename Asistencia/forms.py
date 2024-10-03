from django import forms
from .models import Asistencia

class AsistenciaForm(forms.ModelForm):
    """
        Formulario para registrar la asistencia de una alumna en un día específico.

    Atributos:
        Meta (class): Clase interna que define la configuración del formulario.
            model (Model): El modelo asociado al formulario (Asistencia).
            fields (list): Lista de campos que se incluirán en el formulario, en este caso solo 'presente'.
            widgets (dict): Diccionario que define la representación de los campos del formulario; 
            el campo 'presente' se representará como un checkbox con clase 'form-check-input'.

    """
    class Meta:
        model = Asistencia
        fields = ['presente']

        widgets = {
            'presente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
