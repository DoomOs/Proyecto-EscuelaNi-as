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
    
    
@login_required
def asignar_alumnas(request, grado_id):
    


    
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