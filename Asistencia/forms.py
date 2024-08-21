from django import forms
from .models import Asistencia

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['presente']

        widgets = {
            'presente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
