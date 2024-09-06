from django import forms

from Actividad.models import Actividad, CalificacionActividad
from Curso.models import Curso

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['actividad', 'punteo', 'curso']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar los cursos activos en el campo 'curso'
        self.fields['curso'].queryset = Curso.objects.filter(estado=1)
        
class CalificacionActividadForm(forms.ModelForm):
    class Meta:
        model = CalificacionActividad
        fields = '__all__'