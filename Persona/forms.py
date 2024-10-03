from django import forms
from .models import Persona, Alumna, Contacto
from django.core.validators import RegexValidator


class PersonaForm(forms.ModelForm):
    """
        Formulario para crear o editar información de una persona.

    Hereda:
        forms.ModelForm: Clase base para crear formularios de modelos de Django.

    Atributos:
        Meta: Clase interna que define el modelo asociado y los campos a incluir en el formulario.
            model (Persona): Modelo al que se relaciona este formulario.
            fields (list): Lista de campos a incluir en el formulario: nombre, apellido, fecha de nacimiento, género y dirección.
            widgets (dict): Diccionario que define los widgets personalizados para ciertos campos:
                fecha_nacimiento (DateInput): Campo de fecha con un formato específico.
                genero (Select): Campo de selección para el género, limitado a 'Femenino'.

    Métodos:
        __init__(self, *args, **kwargs): Inicializa el formulario.
            Si la instancia ya existe y tiene una fecha de nacimiento, formatea la fecha en el formato YYYY-MM-DD.

    """
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
    """
        Formulario para crear o editar información de una alumna.

    Hereda:
        forms.ModelForm: Clase base para crear formularios de modelos de Django.

    Atributos:
        persona (ModelChoiceField): Campo oculto que almacena la relación con el modelo Persona,
            permitiendo seleccionar una persona existente.

    Métodos:
        Meta: Clase interna que define el modelo asociado y los campos a incluir en el formulario.
            model (Alumna): Modelo al que se relaciona este formulario.
            fields (list): Lista de campos a incluir en el formulario: código.

    """
    persona = forms.ModelChoiceField(queryset=Persona.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Alumna
        fields = ['codigo']



class ContactoForm(forms.ModelForm):
    """
        Formulario para crear o editar información de un contacto asociado a una alumna.

    Hereda:
        forms.ModelForm: Clase base para crear formularios de modelos de Django.

    Atributos:
        telefono (CharField): Campo para ingresar el número de teléfono del contacto.
            Incluye un validador que permite solo números de 8 dígitos.
            widget (TextInput): Widget personalizado que limita la entrada a 8 caracteres y permite solo números.

        email (EmailField): Campo para ingresar la dirección de correo electrónico del contacto.
            widget (EmailInput): Widget personalizado que proporciona un marcador de posición para el campo de correo electrónico.

    Métodos:
        Meta: Clase interna que define el modelo asociado y los campos a incluir en el formulario.
            model (Contacto): Modelo al que se relaciona este formulario.
            fields (list): Lista de campos a incluir en el formulario: nombre, apellido, parentesco, teléfono y email.
            widgets (dict): Diccionario que define widgets personalizados para ciertos campos:
                parentesco (Select): Campo de selección para elegir el parentesco, con opciones predefinidas.

    """
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
