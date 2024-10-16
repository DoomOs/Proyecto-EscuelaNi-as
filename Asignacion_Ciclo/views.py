from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from Curso.models import Grado
from Persona.models import Alumna
from .models import AsignacionCiclo
from .forms import AsignacionCicloForm
from .models import AsignacionCiclo, Alumna, Grado
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.db import IntegrityError


@login_required
def AsignacionCicloListView(request):
    """
        Vista que gestiona la visualización de la lista de asignaciones de ciclos.

    Parámetros:
       - request (HttpRequest): Objeto de solicitud HTTP que contiene los parámetros de búsqueda.

    Retorna:
        - HttpResponse: Renderiza la plantilla 'asignacion_ciclo_list.html' con el contexto que incluye la lista de asignaciones y grados disponibles.
    
    Filtra las asignaciones de ciclos según el año, grado y consulta de búsqueda proporcionados en los parámetros GET.

    """
    
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

    """
        Clase que gestiona la creación de una nueva asignación de ciclo.

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - CreateView: Vista genérica para crear un objeto.

    Atributos:
       - model (AsignacionCiclo): Modelo utilizado para representar las asignaciones de ciclos.
       - form_class (AsignacionCicloForm): Formulario utilizado para crear la asignación.
       - template_name (str): Nombre del template a utilizar para renderizar la vista.
       - success_url (str): URL a la que se redirige después de crear la asignación.

    Métodos:
        get_context_data(**kwargs):
            Añade la alumna y los grados al contexto de la vista.
            
            Parámetros:
               - **kwargs: Argumentos adicionales que se pueden pasar al contexto.
            
            Retorna:
               - dict: El contexto actualizado que incluye la alumna y los grados disponibles.

        form_valid(form):
            Procesa el formulario cuando es válido, asignando la alumna y verificando si ya está asignada en el mismo año.
            
            Parámetros:
               - form (AsignacionCicloForm): Formulario con los datos de la asignación.
            
            Retorna:
               - HttpResponseRedirect: Redirección a la URL de éxito si el formulario es válido, o vuelve a mostrar el formulario con errores.

    """
    
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
    
    
class AsignacionCicloUpdateView(LoginRequiredMixin,UpdateView):
    
    """
        Clase que gestiona la actualización de una asignación de ciclo existente.

    Hereda:
        - LoginRequiredMixin: Requiere que el usuario esté autenticado.
        - UpdateView: Vista genérica para actualizar un objeto.

    Atributos:
       - model (AsignacionCiclo): Modelo utilizado para representar las asignaciones de ciclos.
       - form_class (AsignacionCicloForm): Formulario utilizado para actualizar la asignación.
       - template_name (str): Nombre del template a utilizar para renderizar la vista.
       - success_url (str): URL a la que se redirige después de actualizar la asignación.

    Métodos:
        get_context_data(**kwargs):
           - Añade los grados y la alumna al contexto de la vista.
            
            Parámetros:
               - **kwargs: Argumentos adicionales que se pueden pasar al contexto.
            
            Retorna:
               - dict: El contexto actualizado que incluye los grados disponibles y la alumna.

    """
    
    model = AsignacionCiclo
    form_class = AsignacionCicloForm
    template_name = 'asignacion_ciclo_form.html'
    success_url = reverse_lazy('asignacionciclo-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grados'] = Grado.objects.all()
        context['alumna'] = self.object.alumna
        return context

    def form_valid(self, form):
        try:
            # Intentar guardar la asignación
            response = super().form_valid(form)
            # Mostrar mensaje de éxito con SweetAlert
            messages.success(self.request, 'Asignación actualizada correctamente.')
            return response
        except IntegrityError:
            # Capturar error de duplicación y mostrar mensaje de error
            messages.error(self.request, 'Error: La asignación ya existe para esta alumna, grado y año.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Mostrar mensajes de error con SweetAlert
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{form.fields[field].label}: {error}")
        return super().form_invalid(form)



class AsignacionCicloDeleteView(LoginRequiredMixin, DeleteView):
    
    """
        Clase que gestiona la eliminación de una asignación de ciclo existente.

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - DeleteView: Vista genérica para eliminar un objeto.

    Atributos:
       - model (AsignacionCiclo): Modelo utilizado para representar las asignaciones de ciclos.
       - template_name (str): Nombre del template a utilizar para confirmar la eliminación.
       - success_url (str): URL a la que se redirige después de eliminar la asignación.

    """

    
    model = AsignacionCiclo
    template_name = 'asignacion_ciclo_confirm_delete.html'
    success_url = reverse_lazy('asignacionciclo-list')
    
    
@login_required
def asignar_alumnas(request, grado_id):
    
    """   
    Vista que gestiona la asignación de alumnas a un grado específico.

    Parámetros:
       - request (HttpRequest): Objeto de solicitud HTTP que contiene los datos de la asignación.
       - grado_id (int): ID del grado al que se asignarán las alumnas.

    Retorna:
       - HttpResponse: Renderiza la plantilla 'asignar_alumnas.html' con el contexto que incluye el grado, alumnas asignadas y no asignadas.
    
    Permite agregar o remover alumnas de un grado según la acción especificada en la solicitud POST.
"""

    
    grado = Grado.objects.get(id=grado_id)
    year_actual = timezone.localtime(timezone.now()).year

    # Alumnas asignadas al grado
    alumnas_asignadas = AsignacionCiclo.objects.filter(grado=grado, year=year_actual)

    # Alumnas activas que no están asignadas al grado
    alumnas_no_asignadas = Alumna.objects.filter(estado=True).exclude(id__in=alumnas_asignadas.values_list('alumna_id', flat=True))

    if request.method == 'POST':
        alumna_id = request.POST.get('alumna_id')
        accion = request.POST.get('accion')

        # Asignar alumna al grado
        if accion == 'agregar':
            alumna = Alumna.objects.get(id=alumna_id)
            AsignacionCiclo.objects.create(grado=grado, alumna=alumna, user=request.user, year=year_actual)

        # Quitar alumna del grado
        elif accion == 'remover':
            AsignacionCiclo.objects.filter(grado=grado, alumna__id=alumna_id, year=year_actual).delete()

        return redirect('asignar-alumnas', grado_id=grado.id)

    context = {
        'grado': grado,
        'alumnas_asignadas': alumnas_asignadas,
        'alumnas_no_asignadas': alumnas_no_asignadas,
        'year_actual': year_actual,
    }
    return render(request, 'asignar_alumnas.html', context)


@login_required
   
def asignar_grado_usuario(request):
    
    """
        Vista que gestiona la asignación de un grado a un usuario.

    Parámetros:
       - request (HttpRequest): Objeto de solicitud HTTP que contiene los datos de la asignación.

    Retorna:
       - HttpResponse: Renderiza la plantilla 'asignar_grado_usuario.html' con el contexto que incluye el usuario y los grados activos.
    
    Permite al usuario seleccionar un grado, que se guardará en su perfil. 

    """

    
    user = request.user  # Usuario logueado
    grados_activos = Grado.objects.filter(estado=True)  

    if request.method == 'POST':
        grado_id = request.POST.get('grado')  
        if grado_id:
            user.id_ciclo = grado_id  
            user.save()  
        return redirect('grado-list')  

    context = {
        'user': user,
        'grados_activos': grados_activos,
    }
    return render(request, 'asignar_grado_usuario.html', context)