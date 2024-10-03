from django.http import JsonResponse, HttpResponse
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

class ActividadListView(LoginRequiredMixin, ListView):
    """
    ActividadListView muestra una lista de actividades activas ordenadas por fecha descendente.

    Hereda:
        LoginRequiredMixin: Requiere que el usuario esté autenticado.
        ListView: Vista genérica para mostrar una lista de objetos.

    Atributos:
        model (Actividad): El modelo utilizado para generar la lista de actividades.
        template_name (str): La plantilla utilizada para renderizar la vista de lista.
        context_object_name (str): Nombre del contexto para acceder a las actividades en la plantilla.

    Métodos:
        get_queryset():
            Filtra las actividades por curso y fecha, y solo muestra las actividades activas.

            Retorna:
                QuerySet: Un conjunto de actividades filtradas y ordenadas por fecha.

        get_context_data(**kwargs):
            Añade los cursos activos al contexto.

            Retorna:
                dict: El contexto extendido con los cursos activos.

    Ejemplo:
        .. code-block:: python

            class ActividadListView(LoginRequiredMixin, ListView):
                model = Actividad
                template_name = 'actividad_list.html'
                context_object_name = 'actividades'
    """

    
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
    
    """
ActividadInactivaListView muestra una lista de actividades inactivas, ordenadas por fecha descendente.

Hereda:
    LoginRequiredMixin: Requiere que el usuario esté autenticado.
    ListView: Vista genérica para mostrar una lista de objetos.

Atributos:
    model (Actividad): El modelo utilizado para generar la lista de actividades.
    template_name (str): La plantilla utilizada para renderizar la vista de lista.
    context_object_name (str): Nombre del contexto para acceder a las actividades en la plantilla.

Métodos:
    get_queryset():
        Filtra las actividades por curso y solo muestra actividades inactivas.

        Retorna:
            QuerySet: Un conjunto de actividades inactivas filtradas y ordenadas por fecha.

    get_context_data(**kwargs):
        Añade todos los cursos al contexto.

        Retorna:
            dict: El contexto extendido con todos los cursos.

Ejemplo:
    .. code-block:: python

        class ActividadInactivaListView(LoginRequiredMixin, ListView):
            model = Actividad
            template_name = 'actividad_inactiva_list.html'
            context_object_name = 'actividades'
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
ActividadInactivarView inactiva una actividad específica.

Hereda:
    View: Vista genérica de Django.

Atributos:
    success_url (str): URL a la que se redirige después de inactivar la actividad.

Métodos:
    get(request, *args, **kwargs):
        Inactiva la actividad estableciendo su estado a 0 y redirige a la URL de éxito.

        Parámetros:
            request (HttpRequest): La solicitud HTTP.
            *args: Argumentos posicionales adicionales.
            **kwargs: Argumentos con nombre adicionales.

        Retorna:
            HttpResponseRedirect: Redirección a la URL de éxito.

Ejemplo:
    .. code-block:: python

        class ActividadInactivarView(View):
            success_url = reverse_lazy('actividad-list')
            def get(self, request, *args, **kwargs):
                actividad = get_object_or_404(Actividad, pk=self.kwargs['pk'])
                actividad.estado = 0
                actividad.save()
                return redirect(self.success_url)
"""

    
    success_url = reverse_lazy('actividad-list')

    def get(self, request, *args, **kwargs):
        actividad = get_object_or_404(Actividad, pk=self.kwargs['pk'])
        actividad.estado = 0  # Inactivar la actividad
        actividad.save()
        return redirect(self.success_url)

class ActividadReactivarView(View):
    
    """
ActividadReactivarView reactiva una actividad inactiva.

Hereda:
    View: Vista genérica de Django.

Atributos:
    success_url (str): URL a la que se redirige después de reactivar la actividad.

Métodos:
    get(request, *args, **kwargs):
        Reactiva la actividad estableciendo su estado a 1 y redirige a la URL de éxito.

        Parámetros:
            request (HttpRequest): La solicitud HTTP.
            *args: Argumentos posicionales adicionales.
            **kwargs: Argumentos con nombre adicionales.

        Retorna:
            HttpResponseRedirect: Redirección a la URL de éxito.

Ejemplo:
    .. code-block:: python

        class ActividadReactivarView(View):
            success_url = reverse_lazy('actividad-inactiva-list')
            def get(self, request, *args, **kwargs):
                actividad = get_object_or_404(Actividad, pk=self.kwargs['actividad_id'])
                actividad.estado = 1
                actividad.save()
                return redirect(self.success_url)
"""

    
    success_url = reverse_lazy('actividad-inactiva-list')

    def get(self, request, *args, **kwargs):
        actividad = get_object_or_404(Actividad, pk=self.kwargs['actividad_id'])
        actividad.estado = 1  # Reactivar la actividad
        actividad.save()
        return redirect(self.success_url)


class ActividadCreateView(LoginRequiredMixin,CreateView):
    
    """
ActividadCreateView crea una nueva actividad.

Hereda:
    LoginRequiredMixin: Requiere que el usuario esté autenticado.
    CreateView: Vista genérica para crear un objeto.

Atributos:
    model (Actividad): El modelo para la creación de una nueva actividad.
    form_class (ActividadForm): El formulario asociado a la creación de la actividad.
    template_name (str): La plantilla utilizada para renderizar la vista de creación.
    success_url (str): La URL a la que se redirige tras la creación exitosa.

Ejemplo:
    .. code-block:: python

        class ActividadCreateView(LoginRequiredMixin, CreateView):
            model = Actividad
            form_class = ActividadForm
            template_name = 'actividad_form.html'
            success_url = reverse_lazy('actividad-list')
"""

    
    model = Actividad
    form_class = ActividadForm
    template_name = 'actividad_form.html'
    success_url = reverse_lazy('actividad-list')

class ActividadUpdateView(LoginRequiredMixin, UpdateView):
    
    """
ActividadUpdateView actualiza una actividad existente.

Hereda:
    LoginRequiredMixin: Requiere que el usuario esté autenticado.
    UpdateView: Vista genérica para actualizar un objeto.

Atributos:
    model (Actividad): El modelo para la actualización de la actividad.
    form_class (ActividadForm): El formulario asociado a la actualización de la actividad.
    template_name (str): La plantilla utilizada para renderizar la vista de actualización.
    success_url (str): La URL a la que se redirige tras la actualización exitosa.

Ejemplo:
    .. code-block:: python

        class ActividadUpdateView(LoginRequiredMixin, UpdateView):
            model = Actividad
            form_class = ActividadForm
            template_name = 'actividad_form.html'
            success_url = reverse_lazy('actividad-list')
"""

    
    model = Actividad
    form_class = ActividadForm
    template_name = 'actividad_form.html'
    success_url = reverse_lazy('actividad-list')

class ActividadDeleteView(LoginRequiredMixin, DeleteView):
    
    """
ActividadDeleteView elimina una actividad.

Hereda:
    LoginRequiredMixin: Requiere que el usuario esté autenticado.
    DeleteView: Vista genérica para eliminar un objeto.

Atributos:
    model (Actividad): El modelo para eliminar la actividad.
    template_name (str): La plantilla utilizada para renderizar la confirmación de eliminación.
    success_url (str): La URL a la que se redirige tras la eliminación exitosa.

Ejemplo:
    .. code-block:: python

        class ActividadDeleteView(LoginRequiredMixin, DeleteView):
            model = Actividad
            template_name = 'actividad_confirm_delete.html'
            success_url = reverse_lazy('actividad-list')
"""

    
    model = Actividad
    template_name = 'actividad_confirm_delete.html'
    success_url = reverse_lazy('actividad-list')

class CalificacionActividadListView(LoginRequiredMixin, ListView):
    model = CalificacionActividad
    template_name = 'calificacionactividad_list.html'


class CalificarAlumnoView(LoginRequiredMixin, TemplateView):
    
    """
CalificarAlumnoView muestra la vista para calificar alumnas en una actividad.

Hereda:
    LoginRequiredMixin: Requiere que el usuario esté autenticado.
    TemplateView: Vista genérica para renderizar una plantilla con contexto personalizado.

Atributos:
    template_name (str): La plantilla utilizada para mostrar las alumnas y sus calificaciones.

Métodos:
    get_context_data(**kwargs):
        Proporciona el contexto con la actividad, alumnas no calificadas y alumnas calificadas.

        Parámetros:
            **kwargs: Argumentos adicionales.

        Retorna:
            dict: Contexto con la información para la plantilla.

    post(request, *args, **kwargs):
        Procesa las calificaciones de las alumnas y guarda los cambios.

        Parámetros:
            request (HttpRequest): La solicitud HTTP.
            *args: Argumentos posicionales adicionales.
            **kwargs: Argumentos con nombre adicionales.

        Retorna:
            HttpResponseRedirect: Redirección a la misma vista para reflejar los cambios.

Ejemplo:
    .. code-block:: python

        class CalificarAlumnoView(LoginRequiredMixin, TemplateView):
            template_name = 'calificar_alumno_list.html'
            def post(self, request, *args, **kwargs):
                # Lógica de guardado de calificaciones
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

        # Redirigir a la misma vista para reflejar los cambios guardados
        return redirect('calificar-alumno', actividad_id=actividad.id)





class CalificacionActividadUpdateView(LoginRequiredMixin, UpdateView):
    
    """
CalificacionActividadUpdateView actualiza una calificación de actividad existente.

Hereda:
    LoginRequiredMixin: Requiere que el usuario esté autenticado.
    UpdateView: Vista genérica para actualizar un objeto.

Atributos:
    model (CalificacionActividad): El modelo para la actualización de la calificación de actividad.
    form_class (CalificacionActividadForm): El formulario asociado a la actualización de la calificación.
    template_name (str): La plantilla utilizada para renderizar la vista de actualización.
    success_url (str): La URL a la que se redirige tras la actualización exitosa.
"""

    
    model = CalificacionActividad
    form_class = CalificacionActividadForm
    template_name = 'calificacionactividad_form.html'
    success_url = reverse_lazy('calificacionactividad-list')

class CalificacionActividadDeleteView(LoginRequiredMixin, DeleteView):
    
    """
CalificacionActividadDeleteView elimina una calificación de actividad.

Hereda:
    LoginRequiredMixin: Requiere que el usuario esté autenticado.
    DeleteView: Vista genérica para eliminar un objeto.

Atributos:
    model (CalificacionActividad): El modelo para eliminar la calificación de actividad.
    template_name (str): La plantilla utilizada para renderizar la confirmación de eliminación.
    success_url (str): La URL a la que se redirige tras la eliminación exitosa.
"""

    
    model = CalificacionActividad
    template_name = 'calificacionactividad_confirm_delete.html'
    success_url = reverse_lazy('calificacionactividad-list')




def calificaciones_alumna_view(request, alumna_id):
    
    """
Muestra las calificaciones de una alumna específica filtradas por grado, año y curso.

Parámetros:
    request (HttpRequest): La solicitud HTTP.
    alumna_id (int): El identificador de la alumna.

Retorna:
    HttpResponse: La respuesta HTTP que muestra la lista de calificaciones filtradas de la alumna.

Filtra:
    - Grado.
    - Año.
    - Curso.
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
Obtiene los años disponibles para un grado específico.

Parámetros:
    request (HttpRequest): La solicitud HTTP con el grado especificado mediante el parámetro 'grado_id'.

Retorna:
    JsonResponse: Un diccionario JSON con la lista de años disponibles para el grado.
"""

    
    grado_id = request.GET.get('grado_id')
    asignaciones = AsignacionCiclo.objects.filter(grado_id=grado_id).distinct()
    anos_list = list(asignaciones.values_list('year', flat=True).distinct())
    return JsonResponse({'years': anos_list})

def get_cursos(request):
    
    """
Obtiene los cursos activos para un grado específico y un año determinado.

Parámetros:
    request (HttpRequest): La solicitud HTTP con el grado y el año especificados mediante los parámetros 'grado_id' y 'year'.

Retorna:
    JsonResponse: Un diccionario JSON con la lista de cursos activos.
"""

    grado_id = request.GET.get('grado_id')
    year = request.GET.get('year')
    cursos = Curso.objects.filter(grado_id=grado_id, estado=True)
    cursos_list = [{'id': curso.id, 'nombre': curso.nombre_curso} for curso in cursos]
    return JsonResponse({'cursos': cursos_list})
