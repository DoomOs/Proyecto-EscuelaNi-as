from datetime import datetime
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.db.models import Avg, F
from django.db.models import Min, Count

from Actividad.models import Actividad, CalificacionActividad
from Actividad.reportes import generar_reporte_excel
from Asignacion_Ciclo.models import AsignacionCiclo, Promocion
from Persona.models import Alumna
from .models import Curso, Grado
from .forms import CursoForm, GradoForm, SeleccionarGradosForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction


class CursoListView(LoginRequiredMixin,ListView):
    """
        Vista basada en clase para listar los cursos activos.

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - ListView: Vista genérica para mostrar una lista de objetos.

    Métodos:
       - get_queryset(): Devuelve un queryset que filtra solo los cursos con estado activo.

    """
    model = Curso
    template_name = 'curso_list.html'

    def get_queryset(self):
        return Curso.objects.filter(estado=True)  # Mostrar solo cursos activos

class CursoCreateView(LoginRequiredMixin,CreateView):
    """
        Vista basada en clase para crear un nuevo curso.

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - CreateView: Vista genérica para crear un nuevo objeto.

    Atributos:
       - model (Model): El modelo asociado a la vista (Curso).
       - form_class (Form): El formulario para crear un nuevo curso (CursoForm).
       - template_name (str): Nombre de la plantilla utilizada para el formulario.
       - success_url (str): URL a la que se redirigirá tras la creación exitosa.

    """
    model = Curso
    form_class = CursoForm
    template_name = 'curso_form.html'
    success_url = reverse_lazy('curso-list')

class CursoUpdateView(LoginRequiredMixin,UpdateView):
    """
        Vista basada en clase para actualizar un curso existente.

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - UpdateView: Vista genérica para actualizar un objeto existente.

    Atributos:
       - model (Model): El modelo asociado a la vista (Curso).
       - form_class (Form): El formulario para actualizar el curso (CursoForm).
       - template_name (str): Nombre de la plantilla utilizada para el formulario.
       - success_url (str): URL a la que se redirigirá tras la actualización exitosa.

    """
    model = Curso
    form_class = CursoForm
    template_name = 'curso_form.html'
    success_url = reverse_lazy('curso-list')

class CursoDeleteView(LoginRequiredMixin,View):
    """
        Vista basada en clase para desactivar un curso existente.

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - View: Vista base para definir métodos HTTP.

    Atributos:
       - success_url (str): URL a la que se redirigirá tras desactivar el curso.

    Métodos:
       - get(request, *args, **kwargs): Maneja la solicitud GET para desactivar un curso
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
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - View: Vista base para definir métodos HTTP.

    Atributos:
       - success_url (str): URL a la que se redirigirá tras activar el curso.

    Métodos:
       - get(request, *args, **kwargs): Maneja la solicitud GET para activar un curso 
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
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - ListView: Vista genérica para mostrar una lista de objetos.

    Métodos:
       - get_queryset(): Devuelve un queryset que filtra solo los grados con estado activo.

    """
    model = Grado
    template_name = 'grado_list.html'

    def get_queryset(self):
        return Grado.objects.filter(estado=True)  # Mostrar solo grados activos

class GradoCreateView(LoginRequiredMixin,CreateView):
    """
        Vista basada en clase para crear un nuevo grado.

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - CreateView: Vista genérica para crear un nuevo objeto.

    Atributos:
       - model (Model): El modelo asociado a la vista (Grado).
       - form_class (Form): El formulario para crear un nuevo grado (GradoForm).
       - template_name (str): Nombre de la plantilla utilizada para el formulario.
       - success_url (str): URL a la que se redirigirá tras la creación exitosa.

    """
    model = Grado
    form_class = GradoForm
    template_name = 'grado_form.html'
    success_url = reverse_lazy('grado-list')

class GradoUpdateView(LoginRequiredMixin,UpdateView):
    """
        Vista basada en clase para actualizar un grado existente.

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - UpdateView: Vista genérica para actualizar un objeto existente.

    Atributos:
       - model (Model): El modelo asociado a la vista (Grado).
       - form_class (Form): El formulario para actualizar el grado (GradoForm).
       - template_name (str): Nombre de la plantilla utilizada para el formulario.
       - success_url (str): URL a la que se redirigirá tras la actualización exitosa.

    """
    model = Grado
    form_class = GradoForm
    template_name = 'grado_form.html'
    success_url = reverse_lazy('grado-list')

class GradoDeleteView(LoginRequiredMixin,View):
    """
        Vista basada en clase para desactivar un grado existente.

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - View: Vista base para definir métodos HTTP.

    Atributos:
       - success_url (str): URL a la que se redirigirá tras desactivar el grado.

    Métodos:
       - get(request, *args, **kwargs): Maneja la solicitud GET para desactivar un grado 
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
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - ListView: Vista genérica para mostrar una lista de objetos.

    Métodos:
       - get_queryset(): Devuelve un queryset que filtra solo los cursos con estado inactivo.

    """
    model = Curso
    template_name = 'curso_inactivo_list.html'

    def get_queryset(self):
        return Curso.objects.filter(estado=False)  

class GradoInactivoListView(LoginRequiredMixin,ListView):
    """
        Vista basada en clase para listar los grados inactivos.

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - ListView: Vista genérica para mostrar una lista de objetos.

    Métodos:
       - get_queryset(): Devuelve un queryset que filtra solo los grados con estado inactivo.

    """
    model = Grado
    template_name = 'grado_inactivo_list.html'

    def get_queryset(self):
        return Grado.objects.filter(estado=False)  # Mostrar solo grados inactivos


class GradoActivateView(LoginRequiredMixin,View):
    """
        Vista basada en clase para activar un grado existente.

    Hereda:
       - LoginRequiredMixin: Requiere que el usuario esté autenticado.
       - View: Vista base para definir métodos HTTP.

    Atributos:
       - success_url (str): URL a la que se redirigirá tras activar el grado.

    Métodos:
       - get(request, *args, **kwargs): Maneja la solicitud GET para activar un grado 
        y redirigir a la lista de grados.

    """
    success_url = reverse_lazy('grado-list')

    def get(self, request, *args, **kwargs):
        grado = get_object_or_404(Grado, pk=self.kwargs['pk']) 
        grado.estado = True  # Reactivar el grado
        grado.save()
        return redirect(self.success_url)



@login_required
def verificar_contrasena(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        # Re-autenticar al usuario con su contraseña actual
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            # Si la autenticación es exitosa, redirigir a seleccionar grados
            return redirect(reverse('seleccionar_grados'))
        else:
            messages.error(request, "Contraseña incorrecta. Inténtalo de nuevo.")
    return render(request, 'verificar_contraseña.html')

@login_required
def seleccionar_grados(request):
    if request.method == 'POST':
        form = SeleccionarGradosForm(request.POST)
        if form.is_valid():
            grados = form.cleaned_data['grados']
            current_year = datetime.now().year
            return calcular_promociones(grados, current_year)
    else:
        form = SeleccionarGradosForm()

    return render(request, 'seleccionar_grados.html', {'form': form})



def calcular_promociones(grados_ids, year):
    """
    Calcula las promociones de las alumnas basado en sus calificaciones en los ciclos seleccionados
    y crea un único registro de promoción por alumna.
    
    Args:
        grados_ids (list): Lista de IDs de los grados a considerar
        year (int): Año para el cual se calculan las promociones
    """
    
    # Obtener todas las asignaciones de ciclo para los grados y año especificados
    asignaciones = AsignacionCiclo.objects.filter(
        grado_id__in=grados_ids,
        year=year
    ).select_related('alumna', 'grado')
    
    # Agrupar asignaciones por alumna
    asignaciones_por_alumna = {}
    for asignacion in asignaciones:
        if asignacion.alumna_id not in asignaciones_por_alumna:
            asignaciones_por_alumna[asignacion.alumna_id] = []
        asignaciones_por_alumna[asignacion.alumna_id].append(asignacion)
    
    # Procesar cada alumna
    with transaction.atomic():
        for alumna_id, asignaciones_alumna in asignaciones_por_alumna.items():
            # Verificar que la alumna tenga asignaciones en todos los grados requeridos
            if len(asignaciones_alumna) != len(grados_ids):
                continue
                
            aprobo_todo = True
            
            # Procesar cada asignación de la alumna
            for asignacion in asignaciones_alumna:
                # Obtener todos los cursos del grado
                cursos = Curso.objects.filter(grado=asignacion.grado, estado=True)
                
                # Revisar cada curso
                for curso in cursos:
                    # Obtener todas las actividades del curso
                    actividades = Actividad.objects.filter(curso=curso)
                    
                    # Calcular promedio de las calificaciones para este curso
                    calificaciones = CalificacionActividad.objects.filter(
                        asignacion_ciclo=asignacion,
                        actividad__in=actividades
                    )
                    
                    if calificaciones.exists():
                        promedio_curso = calificaciones.aggregate(
                            promedio=Avg('punteo')
                        )['promedio'] or 0
                        
                        # Si el promedio es menor a 60, la alumna no aprueba
                        if promedio_curso < 60:
                            aprobo_todo = False
                            break
                
                if not aprobo_todo:
                    break
            
            # Actualizar el estado de la alumna
            alumna = Alumna.objects.get(id=alumna_id)
            alumna.estado = 1 if not aprobo_todo else 0  # 1 para las que perdieron, 0 para las que aprobaron
            alumna.save()
            
            # Crear un único registro de promoción usando la primera asignación
            # (ya que todas son del mismo año y alumna)
            primera_asignacion = asignaciones_alumna[0]
            Promocion.objects.update_or_create(
                asignacion_ciclo=primera_asignacion,
                año=year,
                defaults={'aprobado': aprobo_todo}
            )
    
    return redirect('Inicio')

def calcular_promedio_puntos(asignacion):
    calificaciones = CalificacionActividad.objects.filter(asignacion_ciclo=asignacion)
    total_puntos = sum([cal.punteo for cal in calificaciones])
    total_actividades = len(calificaciones)
    
    # Retornar el promedio, asegurándose de no dividir por 0
    return total_puntos / total_actividades if total_actividades > 0 else 0





def listar_promociones(request):
    # Obtener los años únicos de las promociones
    años = Promocion.objects.values_list('año', flat=True).distinct()
    return render(request, 'listar_promociones.html', {'años': años})


@login_required
def detalle_promocion(request, año):
    # Obtener las promociones del año específico
    promociones = Promocion.objects.filter(año=año)
    
    # Crear una lista con la información de cada alumna y su estado de aprobación
    alumnas = [
        {
            'nombre': promo.asignacion_ciclo.alumna.persona.nombre,
            'apellido': promo.asignacion_ciclo.alumna.persona.apellido,
            'aprobo': promo.aprobado,
            'id': promo.asignacion_ciclo.alumna.id,
            'grado_id': promo.asignacion_ciclo.grado.id  # Agregar el ID del grado
        }
        for promo in promociones
    ]
    
    if request.method == 'POST':
        # Obtener todos los grados activos
        grados_ids = Grado.objects.filter(estado=True).values_list('id', flat=True)

        # Llamar a la función que genera el reporte Excel
        return descargar_reporte(request, grados_ids, año)  # Pasar directamente la lista de IDs

    return render(request, 'detalle_promocion.html', {'alumnas': alumnas, 'año': año})


@login_required
def descargar_reporte(request, grados_ids, año):
    try:
        # Generar el archivo Excel
        excel_file = generar_reporte_excel(grados_ids, año)  # Usar el año pasado como parámetro
        
        # Crear respuesta HTTP
        response = HttpResponse(
            excel_file,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=reporte_notas_{año}.xlsx'  # Cambiar a año específico
        
        return response
        
    except Exception as e:
        messages.error(request, f'Error al generar el reporte: {str(e)}')
        return redirect('detalle_promocion', año=año)  # Redirigir al año correcto
