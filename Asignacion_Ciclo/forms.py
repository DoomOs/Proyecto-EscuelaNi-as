from django import forms

from Asignacion_Ciclo.models import AsignacionCiclo

class AsignacionCicloForm(forms.ModelForm):
    class Meta:
        model = AsignacionCiclo
        fields = ['grado', 'year']
