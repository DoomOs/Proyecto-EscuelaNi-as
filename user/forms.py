from django import forms
from user.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
       
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'telefono', 'id_rol', 'is_active')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'telefono', 'id_rol', 'is_active')
