from datetime import datetime
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from Asignacion_Ciclo.models import AsignacionCiclo
from Curso.models import Curso, Grado
from Persona.models import Alumna
from .models import Actividad, CalificacionActividad
from .forms import ActividadForm, CalificacionActividadForm

from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render
from django.utils.timezone import now
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



class ActividadListView(LoginRequiredMixin, ListView):
    """
    Clase que gestiona la vista de lista de actividades activas.

    Hereda:
        - LoginRequiredMixin: Requiere que el usuario esté autenticado.
        - ListView: Vista genérica para listar objetos de un modelo.

    Atributos:
        - model (Actividad): Modelo utilizado para representar las actividades.
        - template_name (str): Nombre del template a utilizar para renderizar la vista.
        - context_object_name (str): Nombre del contexto que se utilizará en la plantilla.

    Métodos:
        get_queryset():
            Obtiene el conjunto de consultas filtrado y ordenado por fecha.

            Retorna:
                - QuerySet: Un conjunto de actividades activas filtradas por curso y fecha, ordenadas por fecha descendente.

        get_context_data(kwargs):
            Añade cursos activos al contexto de la vista.

            Parámetros:
                - kwargs: Argumentos adicionales que se pueden pasar al contexto.

            Retorna:
                - dict: El contexto actualizado que incluye los cursos activos.
    """
    
    model = Actividad
    template_name = 'actividad_list.html'
    context_object_name = 'actividades'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-fecha')
        curso_id = self.request.GET.get('curso')
        fecha = self.request.GET.get('fecha')
        calificado = self.request.GET.get('calificado')

        if curso_id:
            queryset = queryset.filter(curso_id=curso_id)
        if fecha:
            queryset = queryset.filter(fecha=fecha)
        
        if calificado == "1":  # Calificado
            queryset = queryset.filter(calificacion_estado=1)
        elif calificado == "0":  # No Calificado
            queryset = queryset.filter(calificacion_estado=0)

        return queryset.filter(estado=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cursos'] = Curso.objects.filter(estado=True)
        return context

class ActividadInactivaListView(LoginRequiredMixin, ListView):
    
    """
        Clase que gestiona la vista de lista de actividades inactivas. 

    Hereda:
        - LoginRequiredMixin: Requiere que el usuario esté autenticado.
        - ListView: Vista genérica para listar objetos de un modelo.

    Atributos:
        - model (Actividad): Modelo utilizado para representar las actividades. 
        - template_name (str): Nombre del template a utilizar para renderizar la vista. 
        - context_object_name (str): Nombre del contexto que se utilizará en la plantilla. 

    Métodos:
        get_queryset(): 
            Obtiene el conjunto de consultas filtrado y ordenado por fecha.
            
            Retorna:
               - QuerySet: Un conjunto de actividades inactivas filtradas por curso, ordenadas por fecha descendente.

        get_context_data(kwargs):
            Añade todos los cursos al contexto de la vista.
            Parámetros:
               - kwargs: Argumentos adicionales que se pueden pasar al contexto.
                
            Retorna:
               - dict: El contexto actualizado que incluye todos los cursos.

    
    """

    
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
    
    """
        Clase que gestiona la inactivación de una actividad específica. 

    Hereda:
        View: Clase base para todas las vistas.

    Atributos:
        success_url (str): URL a la que se redirige después de inactivar la actividad.

    Métodos:
        get(request, args, kwargs):
            Inactiva una actividad y redirige a la URL de éxito.
            
            Parámetros:
               - request (HttpRequest): Objeto de solicitud HTTP.
               - args: Argumentos adicionales para el método.
               - kwargs: Argumentos adicionales que se pueden pasar al método.
            
            Retorna:
               - HttpResponseRedirect: Redirección a la URL especificada en success_url.

    """

    
    success_url = reverse_lazy('actividad-list')

    def get(self, request, *args, **kwargs):
        actividad = get_object_or_404(Actividad, pk=self.kwargs['pk'])
        actividad.estado = 0  # Inactivar la actividad
        actividad.save()
        return redirect(self.success_url)

class ActividadReactivarView(View):
    
    """
        Clase que gestiona la reactivación de una actividad específica. 

    Hereda:
        View: Clase base para todas las vistas.

    Atributos:
        success_url (str): URL a la que se redirige después de reactivar la actividad.

    Métodos:
        get(request, *args, **kwargs):
            Reactiva una actividad y redirige a la URL de éxito.
            
            Parámetros:
               - request (HttpRequest): Objeto de solicitud HTTP.
               - *args: Argumentos adicionales para el método.
               - **kwargs: Argumentos adicionales que se pueden pasar al método.
            
            Retorna:
               - HttpResponseRedirect: Redirección a la URL especificada en success_url.

    """
    
    success_url = reverse_lazy('actividad-inactiva-list')

    def get(self, request, *args, **kwargs):
        actividad = get_object_or_404(Actividad, pk=self.kwargs['actividad_id'])
        actividad.estado = 1  # Reactivar la actividad
        actividad.save()
        return redirect(self.success_url)


class ActividadCreateView(LoginRequiredMixin,CreateView):
    
    """
        Clase que gestiona la creación de una nueva actividad. 

    Hereda:
        - LoginRequiredMixin: Requiere que el usuario esté autenticado.
        - CreateView: Vista genérica para crear un objeto.

    Atributos:
       - model (Actividad): Modelo utilizado para representar las actividades.
       - form_class (ActividadForm): Formulario utilizado para crear la actividad.
       - template_name (str): Nombre del template a utilizar para renderizar la vista.
       - success_url (str): URL a la que se redirige después de crear la actividad.

    """

    
    model = Actividad
    form_class = ActividadForm
    template_name = 'actividad_form.html'
    success_url = reverse_lazy('actividad-list')

    def form_valid(self, form):
        form.instance.fecha = timezone.now()
        
        # Obtén el total de puntaje actual del curso
        total_punteo = self.get_total_punteo(form.cleaned_data['curso'])
        nuevo_punteo = form.cleaned_data['punteo']

        # Verifica si el puntaje total excede 100
        if total_punteo + nuevo_punteo > 100:
            messages.error(self.request, 'El puntaje de la actividad supera el total permitido de 100 puntos.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, Verifica que todos los datos sean correctos.')
        return super().form_invalid(form)

    def get_total_punteo(self, curso):
        current_year = timezone.now().year
        actividades = Actividad.objects.filter(curso=curso, fecha__year=current_year, estado=1)
        total_punteo = sum(actividad.punteo for actividad in actividades)
        return total_punteo

class ActividadUpdateView(LoginRequiredMixin, UpdateView):
    """
        Clase que gestiona la actualización de una actividad existente. 

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - UpdateView: Vista genérica para actualizar un objeto.

    Atributos:
       - model (Actividad): Modelo utilizado para representar las actividades.
       - form_class (ActividadForm): Formulario utilizado para actualizar la actividad.
       - template_name (str): Nombre del template a utilizar para renderizar la vista.
       - success_url (str): URL a la que se redirige después de actualizar la actividad.

    """
   
    model = Actividad
    form_class = ActividadForm
    template_name = 'actividad_form.html'
    success_url = reverse_lazy('actividad-list')

    def form_valid(self, form):
        form.instance.fecha = self.object.fecha
        
        # Obtén el total de puntaje actual del curso
        total_punteo = self.get_total_punteo(form.cleaned_data['curso'])
        nuevo_punteo = form.cleaned_data['punteo']

        # Calcula el total de punteo después de la actualización
        if self.object.punteo:  # Asegúrate de que la actividad existe y tiene un puntaje
            total_punteo -= self.object.punteo  # Resta el puntaje anterior

        # Verifica si el nuevo puntaje total excede 100
        if total_punteo + nuevo_punteo > 100:
            messages.error(self.request, 'El puntaje de la actividad supera el total permitido de 100 puntos.')
            return self.form_invalid(form)

        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, Verifica que todos los datos sean correctos.')
        return super().form_invalid(form)
    
    def get_total_punteo(self, curso):
        current_year = timezone.now().year
        actividades = Actividad.objects.filter(curso=curso, fecha__year=current_year, estado=1)
        total_punteo = sum(actividad.punteo for actividad in actividades)
        return total_punteo
 
    



def get_total_punteo(request, curso_id):
    # Obtener el año actual
    current_year = now().year
    # Filtrar actividades activas del curso y del año actual
    actividades = Actividad.objects.filter(curso_id=curso_id, fecha__year=current_year, estado=1)
    total_punteo = sum(actividad.punteo for actividad in actividades)
    return JsonResponse({'total_punteo': total_punteo})


class ActividadDeleteView(LoginRequiredMixin, DeleteView):
    
    """
        Clase que gestiona la eliminación de una actividad existente. 

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - DeleteView: Vista genérica para eliminar un objeto.

    Atributos:
       - model (Actividad): Modelo utilizado para representar las actividades.
       - template_name (str): Nombre del template a utilizar para confirmar la eliminación.
       - success_url (str): URL a la que se redirige después de eliminar la actividad.

    """
    
    model = Actividad
    template_name = 'actividad_confirm_delete.html'
    success_url = reverse_lazy('actividad-list')

class CalificacionActividadListView(LoginRequiredMixin, ListView):
    
    """
        Clase que gestiona la vista de lista de calificaciones de actividades. 

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - ListView: Vista genérica para listar objetos de un modelo.

    Atributos:
       - model (CalificacionActividad): Modelo utilizado para representar las calificaciones de actividades.
       - template_name (str): Nombre del template a utilizar para renderizar la vista.

    """
    
    model = CalificacionActividad
    template_name = 'calificacionactividad_list.html'


class CalificarAlumnoView(LoginRequiredMixin, TemplateView):

    """
        Clase que gestiona la vista para calificar a los alumnos en una actividad específica. 

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - TemplateView: Vista que utiliza un template para renderizar.

    Atributos:
       - template_name (str): Nombre del template a utilizar para renderizar la vista.

    Métodos:
    
        get_context_data(**kwargs):
            Prepara el contexto para la calificación de alumnos, incluyendo la actividad y listas de alumnos calificados y no calificados.
            
            Parámetros:
               - **kwargs: Argumentos adicionales que se pueden pasar al contexto.
            
            Retorna:
                -dict: El contexto actualizado con la actividad y las listas de alumnos.

        post(request, *args, **kwargs):
            Maneja la solicitud POST para guardar las calificaciones de los alumnos.
            
            Parámetros:
               - request (HttpRequest): Objeto de solicitud HTTP.
               - *args: Argumentos adicionales para el método.
               - **kwargs: Argumentos adicionales que se pueden pasar al método.
            
            Retorna:
               - HttpResponseRedirect: Redirección a la misma vista para reflejar los cambios guardados.

    """
    template_name = 'calificar_alumno_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actividad_id = self.kwargs['actividad_id']
        actividad = get_object_or_404(Actividad, id=actividad_id)
        
        # Solo alumnas activas
        asignaciones = AsignacionCiclo.objects.filter(grado=actividad.curso.grado, alumna__estado=True)

        # Filtrando alumnos calificados y no calificados
        alumnos_calificados = CalificacionActividad.objects.filter(actividad=actividad)
        alumnos_no_calificados = asignaciones.exclude(id__in=alumnos_calificados.values_list('asignacion_ciclo', flat=True))

        context['actividad'] = actividad
        context['alumnos_no_calificados'] = alumnos_no_calificados
        context['alumnos_calificados'] = alumnos_calificados
        return context

    
    def post(self, request, *args, **kwargs):
        actividad = get_object_or_404(Actividad, id=self.kwargs['actividad_id'])
        
        # Solo alumnas activas
        asignaciones = AsignacionCiclo.objects.filter(grado=actividad.curso.grado, alumna__estado=True)

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
        total_asignaciones = asignaciones.count()
        total_calificados = CalificacionActividad.objects.filter(actividad=actividad).count()
        
        if total_asignaciones == total_calificados:
            actividad.calificacion_estado = 1
            actividad.save()
        # Redirigir a la misma vista para reflejar los cambios guardados
        return redirect('calificar-alumno', actividad_id=actividad.id)

def eliminar_calificacion(request):
    calificacion_id = request.GET.get('id')
    actividad_id = request.GET.get('actividad_id')
    
    calificacion = get_object_or_404(CalificacionActividad, id=calificacion_id)
    
    # Eliminar la calificación
    calificacion.delete()
    messages.success(request, 'Calificación quitada correctamente.')
    
    return redirect('calificar-alumno', actividad_id=actividad_id)

class CalificacionActividadUpdateView(LoginRequiredMixin, UpdateView):
    
    """
        Clase que gestiona la actualización de una calificación de actividad existente. 

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - UpdateView: Vista genérica para actualizar un objeto.

    Atributos:
       - model (CalificacionActividad): Modelo utilizado para representar las calificaciones de actividades.
       - form_class (CalificacionActividadForm): Formulario utilizado para actualizar la calificación.
       - template_name (str): Nombre del template a utilizar para renderizar la vista.
       - success_url (str): URL a la que se redirige después de actualizar la calificación.

    """
    
    model = CalificacionActividad
    form_class = CalificacionActividadForm
    template_name = 'calificacionactividad_form.html'
    success_url = reverse_lazy('calificacionactividad-list')

class CalificacionActividadDeleteView(LoginRequiredMixin, DeleteView):

    """
        Clase que gestiona la eliminación de una calificación de actividad existente. 

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - DeleteView: Vista genérica para eliminar un objeto.

    Atributos:
       - model (CalificacionActividad): Modelo utilizado para representar las calificaciones de actividades.
       - template_name (str): Nombre del template a utilizar para confirmar la eliminación.
       - success_url (str): URL a la que se redirige después de eliminar la calificación.

    """
    model = CalificacionActividad
    template_name = 'calificacionactividad_confirm_delete.html'
    success_url = reverse_lazy('calificacionactividad-list')




def calificaciones_alumna_view(request, alumna_id):
    """
        Vista que gestiona la visualización de calificaciones de una alumna específica.

    Parámetros:
       - request (HttpRequest): Objeto de solicitud HTTP.
       - alumna_id (int): ID de la alumna cuyas calificaciones se van a visualizar.

    Retorna:
       - HttpResponse: Renderiza la plantilla 'calificaciones_alumna.html' con el contexto de la alumna y sus calificaciones.

    """
    alumna = get_object_or_404(Alumna, id=alumna_id)
    grado_id = request.GET.get('grado')
    year = request.GET.get('year')
    curso_id = request.GET.get('curso')

    calificaciones = CalificacionActividad.objects.filter(asignacion_ciclo__alumna=alumna).order_by('-actividad__fecha')

    if grado_id:
        calificaciones = calificaciones.filter(asignacion_ciclo__grado_id=grado_id)
    if year:
        calificaciones = calificaciones.filter(asignacion_ciclo__year=year)
    if curso_id:
        calificaciones = calificaciones.filter(actividad__curso_id=curso_id)

    grados = Grado.objects.all()

    return render(request, 'calificaciones_alumna.html', {
        'alumna': alumna,
        'calificaciones': calificaciones,
        'grados': grados
    })

def get_anos_cursos(request):
    """
        Vista que obtiene los años asociados a un grado específico y devuelve la lista de años en formato JSON.

    Parámetros:
       - request (HttpRequest): Objeto de solicitud HTTP.

    Retorna:
       - JsonResponse: Respuesta JSON con la lista de años disponibles para el grado especificado.

    """
    grado_id = request.GET.get('grado_id')
    asignaciones = AsignacionCiclo.objects.filter(grado_id=grado_id).distinct()
    anos_list = list(asignaciones.values_list('year', flat=True).distinct())
    return JsonResponse({'years': anos_list})

def get_cursos(request):

    """
        Vista que obtiene los cursos asociados a un grado específico y año, y devuelve la lista de cursos en formato JSON.

    Parámetros:
       - request (HttpRequest): Objeto de solicitud HTTP.

    Retorna:
       - JsonResponse: Respuesta JSON con la lista de cursos disponibles para el grado y año especificados.

    """
    grado_id = request.GET.get('grado_id')
    year = request.GET.get('year')
    cursos = Curso.objects.filter(grado_id=grado_id, estado=True)
    cursos_list = [{'id': curso.id, 'nombre': curso.nombre_curso} for curso in cursos]
    return JsonResponse({'cursos': cursos_list})
