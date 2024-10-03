from django import forms
from .models import Persona, Alumna, Contacto
from django.core.validators import RegexValidator


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'genero', 'direccion']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),  
            'genero': forms.Select(choices=[ ('F', 'Femenino')]) # se dejo fuera Masculino('M', 'Masculino'),
        }

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        # Si la persona ya tiene una fecha de nacimiento, formatearla como YYYY-MM-DD
        if self.instance and self.instance.pk and self.instance.fecha_nacimiento:
            self.fields['fecha_nacimiento'].initial = self.instance.fecha_nacimiento.strftime('%Y-%m-%d')


class AlumnaForm(forms.ModelForm):
    persona = forms.ModelChoiceField(queryset=Persona.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Alumna
        fields = ['codigo']



class ContactoForm(forms.ModelForm):
    telefono = forms.CharField(
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$', 'Ingrese un número de teléfono válido de 8 dígitos.')],
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese solo números',
            'maxlength': '8',  # Limita la entrada a 8 caracteres en el frontend
            'pattern': '[0-9]{8}',  # Solo permite números
            'title': 'El número debe tener 8 dígitos'
        })
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'nombre@ejemplo.com'}))

    class Meta:
        model = Contacto
        fields = ['nombre', 'apellido', 'parentesco', 'telefono', 'email']
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
