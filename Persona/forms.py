from django import forms
from .models import Persona, Alumna, Contacto

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'genero', 'direccion']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'genero': forms.Select(choices=[('M', 'Masculino'), ('F', 'Femenino')])
        }

class AlumnaForm(forms.ModelForm):
    persona = forms.ModelChoiceField(queryset=Persona.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Alumna
        fields = ['codigo']

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['parentesco', 'telefono', 'email']
        widgets = {
            'parentesco': forms.Select(choices=[
                ('Mamá', 'Mamá'),
                ('Papá', 'Papá'),
                ('Hermano', 'Hermano'),
                ('Hermana', 'Hermana'),
                ('Abuelo', 'Abuelo'),
                ('Abuela', 'Abuela'),
                ('Tutor legal', 'Tutor legal')
            ])
        }
