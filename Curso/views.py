from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Curso, Grado
from .forms import CursoForm, GradoForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class CursoListView(LoginRequiredMixin,ListView):
    """
        Vista basada en clase para listar los cursos activos.

    Hereda:
        LoginRequiredMixin: Requiere que el usuario esté autenticado.
        ListView: Vista genérica para mostrar una lista de objetos.

    Métodos:
        get_queryset(): Devuelve un queryset que filtra solo los cursos con estado activo.

    """
    model = Curso
    template_name = 'curso_list.html'

    def get_queryset(self):
        return Curso.objects.filter(estado=True)  # Mostrar solo cursos activos

class CursoCreateView(LoginRequiredMixin,CreateView):
    """
        Vista basada en clase para crear un nuevo curso.

    Hereda:
        LoginRequiredMixin: Requiere que el usuario esté autenticado.
        CreateView: Vista genérica para crear un nuevo objeto.

    Atributos:
        model (Model): El modelo asociado a la vista (Curso).
        form_class (Form): El formulario para crear un nuevo curso (CursoForm).
        template_name (str): Nombre de la plantilla utilizada para el formulario.
        success_url (str): URL a la que se redirigirá tras la creación exitosa.

    """
    model = Curso
    form_class = CursoForm
    template_name = 'curso_form.html'
    success_url = reverse_lazy('curso-list')

class CursoUpdateView(LoginRequiredMixin,UpdateView):
    """
        Vista basada en clase para actualizar un curso existente.

    Hereda:
        LoginRequiredMixin: Requiere que el usuario esté autenticado.
        UpdateView: Vista genérica para actualizar un objeto existente.

    Atributos:
        model (Model): El modelo asociado a la vista (Curso).
        form_class (Form): El formulario para actualizar el curso (CursoForm).
        template_name (str): Nombre de la plantilla utilizada para el formulario.
        success_url (str): URL a la que se redirigirá tras la actualización exitosa.

    """
    model = Curso
    form_class = CursoForm
    template_name = 'curso_form.html'
    success_url = reverse_lazy('curso-list')

class CursoDeleteView(LoginRequiredMixin,View):
    """
        Vista basada en clase para desactivar un curso existente.

    Hereda:
        LoginRequiredMixin: Requiere que el usuario esté autenticado.
        View: Vista base para definir métodos HTTP.

    Atributos:
        success_url (str): URL a la que se redirigirá tras desactivar el curso.

    Métodos:
        get(request, *args, **kwargs): Maneja la solicitud GET para desactivar un curso
        y redirigir a la lista de cursos.

    """
    success_url = reverse_lazy('curso-list')

    def get(self, request, *args, **kwargs):
        #curso que deseas desactivar
        curso = get_object_or_404(Curso, pk=kwargs['pk'])
        curso.estado = False  # Cambia el estado a inactivo
        curso.save()
        return redirect(self.success_url)
    
class CursoActivateView(LoginRequiredMixin,View):
    """
        Vista basada en clase para activar un curso existente.

    Hereda:
        LoginRequiredMixin: Requiere que el usuario esté autenticado.
        View: Vista base para definir métodos HTTP.

    Atributos:
        success_url (str): URL a la que se redirigirá tras activar el curso.

    Métodos:
        get(request, *args, **kwargs): Maneja la solicitud GET para activar un curso 
        y redirigir a la lista de cursos.

    """
    
    success_url = reverse_lazy('curso-list')

    def get(self, request, *args, **kwargs):
        curso = get_object_or_404(Curso, pk=self.kwargs['pk'])  
        curso.estado = True  # Cambia el estado a activo
        curso.save()
        return redirect(self.success_url)

class GradoListView(LoginRequiredMixin,ListView):
    """
        Vista basada en clase para listar los grados activos.

    Hereda:
        LoginRequiredMixin: Requiere que el usuario esté autenticado.
        ListView: Vista genérica para mostrar una lista de objetos.

    Métodos:
        get_queryset(): Devuelve un queryset que filtra solo los grados con estado activo.

    """
    model = Grado
    template_name = 'grado_list.html'

    def get_queryset(self):
        return Grado.objects.filter(estado=True)  # Mostrar solo grados activos

class GradoCreateView(LoginRequiredMixin,CreateView):
    """
        Vista basada en clase para crear un nuevo grado.

    Hereda:
        LoginRequiredMixin: Requiere que el usuario esté autenticado.
        CreateView: Vista genérica para crear un nuevo objeto.

    Atributos:
        model (Model): El modelo asociado a la vista (Grado).
        form_class (Form): El formulario para crear un nuevo grado (GradoForm).
        template_name (str): Nombre de la plantilla utilizada para el formulario.
        success_url (str): URL a la que se redirigirá tras la creación exitosa.

    """
    model = Grado
    form_class = GradoForm
    template_name = 'grado_form.html'
    success_url = reverse_lazy('grado-list')

class GradoUpdateView(LoginRequiredMixin,UpdateView):
    """
        Vista basada en clase para actualizar un grado existente.

    Hereda:
        LoginRequiredMixin: Requiere que el usuario esté autenticado.
        UpdateView: Vista genérica para actualizar un objeto existente.

    Atributos:
        model (Model): El modelo asociado a la vista (Grado).
        form_class (Form): El formulario para actualizar el grado (GradoForm).
        template_name (str): Nombre de la plantilla utilizada para el formulario.
        success_url (str): URL a la que se redirigirá tras la actualización exitosa.

    """
    model = Grado
    form_class = GradoForm
    template_name = 'grado_form.html'
    success_url = reverse_lazy('grado-list')

class GradoDeleteView(LoginRequiredMixin,View):
    """
        Vista basada en clase para desactivar un grado existente.

    Hereda:
        LoginRequiredMixin: Requiere que el usuario esté autenticado.
        View: Vista base para definir métodos HTTP.

    Atributos:
        success_url (str): URL a la que se redirigirá tras desactivar el grado.

    Métodos:
        get(request, *args, **kwargs): Maneja la solicitud GET para desactivar un grado 
        y redirigir a la lista de grados.

    """
    success_url = reverse_lazy('grado-list')

    def get(self, request, *args, **kwargs):
        # Obtén el grado que deseas desactivar
        grado = get_object_or_404(Grado, pk=kwargs['pk'])
        grado.estado = False  # Cambia el estado a inactivo
        grado.save()
        return redirect(self.success_url)
    
class CursoInactivoListView(LoginRequiredMixin,ListView):
    """
        Vista basada en clase para listar los cursos inactivos.

    Hereda:
        LoginRequiredMixin: Requiere que el usuario esté autenticado.
        ListView: Vista genérica para mostrar una lista de objetos.

    Métodos:
        get_queryset(): Devuelve un queryset que filtra solo los cursos con estado inactivo.

    """
    model = Curso
    template_name = 'curso_inactivo_list.html'

    def get_queryset(self):
        return Curso.objects.filter(estado=False)  

class GradoInactivoListView(LoginRequiredMixin,ListView):
    """
        Vista basada en clase para listar los grados inactivos.

    Hereda:
        LoginRequiredMixin: Requiere que el usuario esté autenticado.
        ListView: Vista genérica para mostrar una lista de objetos.

    Métodos:
        get_queryset(): Devuelve un queryset que filtra solo los grados con estado inactivo.

    """
    model = Grado
    template_name = 'grado_inactivo_list.html'

    def get_queryset(self):
        return Grado.objects.filter(estado=False)  # Mostrar solo grados inactivos


class GradoActivateView(LoginRequiredMixin,View):
    """
        Vista basada en clase para activar un grado existente.

    Hereda:
        LoginRequiredMixin: Requiere que el usuario esté autenticado.
        View: Vista base para definir métodos HTTP.

    Atributos:
        success_url (str): URL a la que se redirigirá tras activar el grado.

    Métodos:
        get(request, *args, **kwargs): Maneja la solicitud GET para activar un grado 
        y redirigir a la lista de grados.

    """
    success_url = reverse_lazy('grado-list')

    def get(self, request, *args, **kwargs):
        grado = get_object_or_404(Grado, pk=self.kwargs['pk']) 
        grado.estado = True  # Reactivar el grado
        grado.save()
        return redirect(self.success_url)
