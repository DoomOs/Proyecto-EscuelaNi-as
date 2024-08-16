from django import forms

from Curso.models import Curso, Grado

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
    
    
class GradoForm(forms.ModelForm):
    class Meta:
        model = Grado
        fields = '__all__'