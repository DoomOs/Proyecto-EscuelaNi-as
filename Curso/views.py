from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Curso, Grado
from .forms import CursoForm, GradoForm

class CursoListView(ListView):
    model = Curso
    template_name = 'curso_list.html'

class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'curso_form.html'
    success_url = reverse_lazy('curso-list')

class CursoUpdateView(UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'curso_form.html'
    success_url = reverse_lazy('curso-list')

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'curso_confirm_delete.html'
    success_url = reverse_lazy('curso-list')

class GradoListView(ListView):
    model = Grado
    template_name = 'grado_list.html'

class GradoCreateView(CreateView):
    model = Grado
    form_class = GradoForm
    template_name = 'grado_form.html'
    success_url = reverse_lazy('grado-list')

class GradoUpdateView(UpdateView):
    model = Grado
    form_class = GradoForm
    template_name = 'grado_form.html'
    success_url = reverse_lazy('grado-list')

class GradoDeleteView(DeleteView):
    model = Grado
    template_name = 'grado_confirm_delete.html'
    success_url = reverse_lazy('grado-list')
