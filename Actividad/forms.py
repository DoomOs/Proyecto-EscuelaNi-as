from django import forms

from Actividad.models import Actividad, CalificacionActividad

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = '__all__'

class CalificacionActividadForm(forms.ModelForm):
    class Meta:
        model = CalificacionActividad
        fields = '__all__'