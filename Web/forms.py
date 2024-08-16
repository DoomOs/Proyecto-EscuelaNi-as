from django import forms
from .models import Carrusel


class CarruselForm(forms.ModelForm):

    class Meta:
        model = Carrusel
        fields = ['nombre', 'descripcion', 'foto']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'require': True, 'autofocus': True, 'placeholder': 'Nombre de Imagen'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'require': True, 'autofocus': True, 'placeholder': 'Descripcion de Imagen'}),
            'foto': forms.FileInput(attrs={'class': 'form-control', 'require': False, 'id': 'foto'}),
        }


class UpdateCarruselForm(forms.ModelForm):

    class Meta:
        model = Carrusel
        fields = ['nombre', 'descripcion', 'foto']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'require': True, 'autofocus': True, 'placeholder': 'Nombre de Imagen'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'require': True, 'autofocus': True, 'placeholder': 'Descripcion de Imagen'}),
            'foto': forms.FileInput(attrs={'class': 'form-control', 'require': False, 'id': 'foto'}),
        }
