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
        
        
        
class SeleccionarGradosForm(forms.Form):
    grados = forms.ModelMultipleChoiceField(
        queryset=Grado.objects.filter(estado=True), 
        widget=forms.CheckboxSelectMultiple,
        label="Seleccionar 4 Grados",
        help_text="Debes seleccionar exactamente 4 grados."
    )

    def clean_grados(self):
        grados = self.cleaned_data.get('grados')
        if len(grados) != 4:
            raise forms.ValidationError("Debes seleccionar exactamente 4 grados.")
        return grados