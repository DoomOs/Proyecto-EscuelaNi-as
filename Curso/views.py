from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Curso, Grado
from .forms import CursoForm, GradoForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class CursoListView(LoginRequiredMixin,ListView):
    model = Curso
    template_name = 'curso_list.html'

    def get_queryset(self):
        return Curso.objects.filter(estado=True)  # Mostrar solo cursos activos

class CursoCreateView(LoginRequiredMixin,CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'curso_form.html'
    success_url = reverse_lazy('curso-list')

class CursoUpdateView(LoginRequiredMixin,UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'curso_form.html'
    success_url = reverse_lazy('curso-list')

class CursoDeleteView(LoginRequiredMixin,View):
    success_url = reverse_lazy('curso-list')

    def get(self, request, *args, **kwargs):
        #curso que deseas desactivar
        curso = get_object_or_404(Curso, pk=kwargs['pk'])
        curso.estado = False  # Cambia el estado a inactivo
        curso.save()
        return redirect(self.success_url)
    
class CursoActivateView(LoginRequiredMixin,View):
    success_url = reverse_lazy('curso-list')

    def get(self, request, *args, **kwargs):
        curso = get_object_or_404(Curso, pk=self.kwargs['pk'])  
        curso.estado = True  # Cambia el estado a activo
        curso.save()
        return redirect(self.success_url)

class GradoListView(LoginRequiredMixin,ListView):
    model = Grado
    template_name = 'grado_list.html'

    def get_queryset(self):
        return Grado.objects.filter(estado=True)  # Mostrar solo grados activos

class GradoCreateView(LoginRequiredMixin,CreateView):
    model = Grado
    form_class = GradoForm
    template_name = 'grado_form.html'
    success_url = reverse_lazy('grado-list')

class GradoUpdateView(LoginRequiredMixin,UpdateView):
    model = Grado
    form_class = GradoForm
    template_name = 'grado_form.html'
    success_url = reverse_lazy('grado-list')

class GradoDeleteView(LoginRequiredMixin,View):
    success_url = reverse_lazy('grado-list')

    def get(self, request, *args, **kwargs):
        # Obtén el grado que deseas desactivar
        grado = get_object_or_404(Grado, pk=kwargs['pk'])
        grado.estado = False  # Cambia el estado a inactivo
        grado.save()
        return redirect(self.success_url)
    
class CursoInactivoListView(LoginRequiredMixin,ListView):
    model = Curso
    template_name = 'curso_inactivo_list.html'

    def get_queryset(self):
        return Curso.objects.filter(estado=False)  

class GradoInactivoListView(LoginRequiredMixin,ListView):
    model = Grado
    template_name = 'grado_inactivo_list.html'

    def get_queryset(self):
        return Grado.objects.filter(estado=False)  # Mostrar solo grados inactivos


class GradoActivateView(LoginRequiredMixin,View):
    success_url = reverse_lazy('grado-list')

    def get(self, request, *args, **kwargs):
        grado = get_object_or_404(Grado, pk=self.kwargs['pk']) 
        grado.estado = True  # Reactivar el grado
        grado.save()
        return redirect(self.success_url)
