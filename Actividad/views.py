from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from Asignacion_Ciclo.models import AsignacionCiclo
from .models import Actividad, CalificacionActividad
from .forms import ActividadForm, CalificacionActividadForm

class ActividadListView(LoginRequiredMixin, ListView):
    model = Actividad
    template_name = 'actividad_list.html'

class ActividadCreateView(LoginRequiredMixin,CreateView):
    model = Actividad
    form_class = ActividadForm
    template_name = 'actividad_form.html'
    success_url = reverse_lazy('actividad-list')

class ActividadUpdateView(LoginRequiredMixin, UpdateView):
    model = Actividad
    form_class = ActividadForm
    template_name = 'actividad_form.html'
    success_url = reverse_lazy('actividad-list')

class ActividadDeleteView(LoginRequiredMixin, DeleteView):
    model = Actividad
    template_name = 'actividad_confirm_delete.html'
    success_url = reverse_lazy('actividad-list')

class CalificacionActividadListView(LoginRequiredMixin, ListView):
    model = CalificacionActividad
    template_name = 'calificacionactividad_list.html'


class CalificarAlumnoView(LoginRequiredMixin, TemplateView):
    template_name = 'calificar_alumno_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actividad_id = self.kwargs['actividad_id']
        actividad = get_object_or_404(Actividad, id=actividad_id)
        asignaciones = AsignacionCiclo.objects.filter(grado=actividad.curso.grado)

        # Filtrando alumnos calificados y no calificados
        alumnos_calificados = CalificacionActividad.objects.filter(actividad=actividad)
        alumnos_no_calificados = asignaciones.exclude(id__in=alumnos_calificados.values_list('asignacion_ciclo', flat=True))

        context['actividad'] = actividad
        context['alumnos_no_calificados'] = alumnos_no_calificados
        context['alumnos_calificados'] = alumnos_calificados
        return context

    def post(self, request, *args, **kwargs):
        actividad = get_object_or_404(Actividad, id=self.kwargs['actividad_id'])
        asignaciones = AsignacionCiclo.objects.filter(grado=actividad.curso.grado)

        for asignacion in asignaciones:
            punteo = request.POST.get(f'punteo_{asignacion.id}')
            descripcion = request.POST.get(f'descripcion_{asignacion.id}')
            if punteo and descripcion:
                # Crear o actualizar la calificación
                calificacion, created = CalificacionActividad.objects.update_or_create(
                    actividad=actividad,
                    asignacion_ciclo=asignacion,
                    defaults={'punteo': punteo, 'descripcion': descripcion}
                )

        return redirect('calificar-alumno', actividad_id=actividad.id)

class CalificacionActividadCreateView(LoginRequiredMixin, CreateView):
    model = CalificacionActividad
    form_class = CalificacionActividadForm
    template_name = 'calificacionactividad_form.html'

    def post(self, request, *args, **kwargs):
        actividad = get_object_or_404(Actividad, id=self.kwargs['actividad_id'])
        for asignacion in AsignacionCiclo.objects.filter(grado=actividad.curso.grado, year=actividad.curso.year):
            punteo = request.POST.get(f'punteo_{asignacion.id}')
            descripcion = request.POST.get(f'descripcion_{asignacion.id}')
            if punteo and descripcion:
                CalificacionActividad.objects.create(
                    actividad=actividad,
                    asignacion_ciclo=asignacion,
                    punteo=punteo,
                    descripcion=descripcion
                )
        return redirect('calificar-alumno', actividad_id=actividad.id)


class CalificacionActividadUpdateView(LoginRequiredMixin, UpdateView):
    model = CalificacionActividad
    form_class = CalificacionActividadForm
    template_name = 'calificacionactividad_form.html'
    success_url = reverse_lazy('calificacionactividad-list')

class CalificacionActividadDeleteView(LoginRequiredMixin, DeleteView):
    model = CalificacionActividad
    template_name = 'calificacionactividad_confirm_delete.html'
    success_url = reverse_lazy('calificacionactividad-list')
