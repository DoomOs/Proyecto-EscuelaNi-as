from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from Curso.models import Grado
from Persona.models import Alumna
from .models import AsignacionCiclo
from .forms import AsignacionCicloForm

def AsignacionCicloListView(request):
    query = Q()
    grados = Grado.objects.all()

    year = request.GET.get('year')
    grado = request.GET.get('grado')
    search_query = request.GET.get('q')

    if year:
        query &= Q(year=year)

    if grado:
        query &= Q(grado__id=grado)

    if search_query:
        query &= Q(alumna__persona__nombre__icontains=search_query) | Q(alumna__persona__apellido__icontains=search_query)

    asignaciones = AsignacionCiclo.objects.filter(query)

    context = {
        'object_list': asignaciones,
        'grados': grados,
    }
    return render(request, 'asignacion_ciclo_list.html', context)

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

class AsignacionCicloUpdateView(UpdateView):
    model = AsignacionCiclo
    form_class = AsignacionCicloForm
    template_name = 'asignacion_ciclo_form.html'
    success_url = reverse_lazy('asignacionciclo-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grados'] = Grado.objects.all()
        context['alumna'] = self.object.alumna
        return context

class AsignacionCicloDeleteView(LoginRequiredMixin, DeleteView):
    model = AsignacionCiclo
    template_name = 'asignacion_ciclo_confirm_delete.html'
    success_url = reverse_lazy('asignacionciclo-list')