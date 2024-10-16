from datetime import datetime
from django import forms

from Actividad.models import Actividad, CalificacionActividad
from Curso.models import Curso

class ActividadForm(forms.ModelForm):
    
    """
Formulario para crear o actualizar instancias del modelo `Actividad`.

Atributos:
    - model (Actividad): El modelo asociado al formulario, que es `Actividad`.
    - fields (list): Lista de campos que serán incluidos en el formulario (`actividad`, `punteo`, `curso`).

Métodos:
   - __init__: Inicializa el formulario. Sobrescribe el queryset del campo `curso` para mostrar solo los cursos activos.

    Args:
       - *args: Argumentos posicionales.
       - **kwargs: Argumentos clave.

    Notas:
        - Este método filtra los cursos activos, es decir, aquellos cuyo estado es `1`.
"""

    
    class Meta:
        model = Actividad
        fields = ['actividad', 'punteo', 'curso']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar los cursos activos en el campo 'curso'
        self.fields['curso'].queryset = Curso.objects.filter(estado=1)

    def clean(self):
        cleaned_data = super().clean()
        punteo = cleaned_data.get('punteo')
        curso = cleaned_data.get('curso')
        
        if punteo is not None and punteo < 0:
            raise forms.ValidationError("El puntaje no puede ser negativo.")
        
        if not curso:
            return cleaned_data

        actividades = Actividad.objects.filter(curso=curso, fecha__year=datetime.now().year, estado=1)  # Solo actividades activas
        total_punteo = sum(actividad.punteo for actividad in actividades)

        if self.instance.pk:
            total_punteo -= self.instance.punteo

        if punteo + total_punteo > 100:
            raise forms.ValidationError(f"El total de punteo no puede exceder 100. Punteo acumulado actual: {total_punteo}. Punteo restante: {100 - total_punteo}.")

        return cleaned_data

        
class CalificacionActividadForm(forms.ModelForm):
    
    """
Formulario para crear o actualizar instancias del modelo `CalificacionActividad`.

Atributos:
    - model (CalificacionActividad): El modelo asociado al formulario, que es `CalificacionActividad`.
    - fields (str): Especifica que todos los campos del modelo serán incluidos en el formulario.
"""

    
    class Meta:
        model = CalificacionActividad
        fields = '__all__'