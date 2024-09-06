from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from Asignacion_Ciclo.models import AsignacionCiclo
from Curso.models import Curso
from .models import Actividad, CalificacionActividad
from .forms import ActividadForm, CalificacionActividadForm

from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render

class ActividadListView(LoginRequiredMixin, ListView):
    model = Actividad
    template_name = 'actividad_list.html'
    context_object_name = 'actividades'
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-fecha')  # Ordenar por fecha descendente
        
        # Obtener parámetros de filtrado
        curso_id = self.request.GET.get('curso')
        fecha = self.request.GET.get('fecha')
        
        if curso_id:
            queryset = queryset.filter(curso_id=curso_id)
        if fecha:
            queryset = queryset.filter(fecha=fecha)
        
        # Solo mostrar actividades activas
        return queryset.filter(estado=1)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir los cursos activos al contexto
        context['cursos'] = Curso.objects.filter(estado=True)
        return context

class ActividadInactivaListView(LoginRequiredMixin, ListView):
    model = Actividad
    template_name = 'actividad_inactiva_list.html'
    context_object_name = 'actividades'
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-fecha')  # Ordenar por fecha descendente
        
        # Obtener parámetro de filtrado
        curso_id = self.request.GET.get('curso')
        
        if curso_id:
            queryset = queryset.filter(curso_id=curso_id)
        
        # Solo mostrar actividades inactivas
        return queryset.filter(estado=0)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir todos los cursos al contexto
        context['cursos'] = Curso.objects.all()
        return context

    
class ActividadInactivarView(View):
    success_url = reverse_lazy('actividad-list')

    def get(self, request, *args, **kwargs):
        actividad = get_object_or_404(Actividad, pk=self.kwargs['pk'])
        actividad.estado = 0  # Inactivar la actividad
        actividad.save()
        return redirect(self.success_url)

class ActividadReactivarView(View):
    success_url = reverse_lazy('actividad-inactiva-list')

    def get(self, request, *args, **kwargs):
        actividad = get_object_or_404(Actividad, pk=self.kwargs['actividad_id'])
        actividad.estado = 1  # Reactivar la actividad
        actividad.save()
        return redirect(self.success_url)


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

        errores = []
        for asignacion in asignaciones:
            punteo = request.POST.get(f'punteo_{asignacion.id}')
            descripcion = request.POST.get(f'descripcion_{asignacion.id}')

            # Validaciones
            if punteo:
                try:
                    punteo = int(punteo)
                    if punteo < 0:
                        errores.append(f"El punteo para {asignacion.alumna.persona.nombre} no puede ser negativo.")
                    elif punteo > actividad.punteo:
                        errores.append(f"El punteo para {asignacion.alumna.persona.nombre} no puede exceder el máximo de {actividad.punteo}.")
                except ValueError:
                    errores.append(f"El punteo para {asignacion.alumna.persona.nombre} no es válido.")

        # Mostrar los errores con SweetAlert para los alumnos con problemas
        if errores:
            for error in errores:
                messages.error(request, error)

        # Guardar calificaciones solo para los alumnos que no tuvieron errores
        for asignacion in asignaciones:
            punteo = request.POST.get(f'punteo_{asignacion.id}')
            descripcion = request.POST.get(f'descripcion_{asignacion.id}')
            
            # Solo guardar si no hay errores en el punteo de este alumno
            if punteo and int(punteo) <= actividad.punteo and int(punteo) >= 0:
                CalificacionActividad.objects.update_or_create(
                    actividad=actividad,
                    asignacion_ciclo=asignacion,
                    defaults={'punteo': punteo, 'descripcion': descripcion}
                )

        # Redirigir a la misma vista para reflejar los cambios guardados
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
