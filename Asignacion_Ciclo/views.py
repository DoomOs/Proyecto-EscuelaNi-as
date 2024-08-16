from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from Curso.models import Grado
from Persona.models import Alumna
from .models import AsignacionCiclo
from .forms import AsignacionCicloForm

class AsignacionCicloListView(ListView):
    model = AsignacionCiclo
    template_name = 'asignacion_ciclo_list.html'

class AsignacionCicloCreateView(LoginRequiredMixin, CreateView):
    model = AsignacionCiclo
    form_class = AsignacionCicloForm
    template_name = 'asignacion_ciclo_form.html'
    success_url = reverse_lazy('alumna-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alumna'] = get_object_or_404(Alumna, id=self.kwargs['pk'])
        context['grados'] = Grado.objects.all()
        return context

    def form_valid(self, form):
        alumna = get_object_or_404(Alumna, id=self.kwargs['pk'])
        form.instance.alumna = alumna
        form.instance.user = self.request.user
        
        # Verificar si el alumno ya está asignado en el mismo año
        if AsignacionCiclo.objects.filter(alumna=alumna, year=form.instance.year).exists():
            form.add_error('year', 'Esta alumna ya está asignada en este año.')
            return self.form_invalid(form)

        return super().form_valid(form)

class AsignacionCicloUpdateView(LoginRequiredMixin, UpdateView):
    model = AsignacionCiclo
    form_class = AsignacionCicloForm
    template_name = 'asignacion_ciclo_form.html'
    success_url = reverse_lazy('asignacionciclo-list')

class AsignacionCicloDeleteView(LoginRequiredMixin, DeleteView):
    model = AsignacionCiclo
    template_name = 'asignacion_ciclo_confirm_delete.html'
    success_url = reverse_lazy('asignacionciclo-list')