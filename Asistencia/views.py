from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Asistencia
from .forms import AsistenciaForm

class AsistenciaListView(ListView):
    model = Asistencia
    template_name = 'asistencia/asistencia_list.html'

class AsistenciaCreateView(CreateView):
    model = Asistencia
    form_class = AsistenciaForm
    template_name = 'asistencia/asistencia_form.html'
    success_url = reverse_lazy('asistencia-list')

class AsistenciaUpdateView(UpdateView):
    model = Asistencia
    form_class = AsistenciaForm
    template_name = 'asistencia/asistencia_form.html'
    success_url = reverse_lazy('asistencia-list')

class AsistenciaDeleteView(DeleteView):
    model = Asistencia
    template_name = 'asistencia/asistencia_confirm_delete.html'
    success_url = reverse_lazy('asistencia-list')
