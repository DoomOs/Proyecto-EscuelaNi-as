from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from Asignacion_Ciclo.forms import AsignacionCicloForm
from Asignacion_Ciclo.models import AsignacionCiclo
from .models import Persona, Alumna, Contacto
from .forms import PersonaForm, AlumnaForm, ContactoForm
from django.contrib import messages
from django.urls import reverse
from django.utils.timezone import now

def persona_create_view(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            persona = form.save()
            return redirect(reverse('alumna-create') + f'?persona_id={persona.id}')
    else:
        form = PersonaForm()

    return render(request, 'persona_form.html', {'form': form})

def alumna_create_view(request):
    persona_id = request.GET.get('persona_id')

    if request.method == 'POST':
        form = AlumnaForm(request.POST)
        if form.is_valid():
            alumna = form.save(commit=False)
            alumna.persona_id = persona_id
            alumna.save()
            return redirect(reverse('contacto-create', args=[alumna.id]))
    else:
        form = AlumnaForm(initial={'persona': persona_id})

    return render(request, 'alumna_form.html', {'form': form})


def contacto_create_view(request, alumna_id):
    alumno = get_object_or_404(Alumna, id=alumna_id)

    if request.method == 'POST':
        contacto_form = ContactoForm(request.POST)
        if contacto_form.is_valid():
            contacto = contacto_form.save(commit=False)
            contacto.alumna = alumno
            contacto.save()
            return redirect('contacto-create', alumna_id=alumna_id)
        else:
            messages.error(request, 'Hay errores en el formulario.')
    else:
        contacto_form = ContactoForm()

    contactos = Contacto.objects.filter(alumna_id=alumna_id)

    return render(request, 'contacto_form.html', {
        'form_title': 'Crear Contacto',
        'contacto_form': contacto_form,
        'contactos': contactos
    })

def contacto_edit_view(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id)
    
    if request.method == 'POST':
        contacto_form = ContactoForm(request.POST, instance=contacto)
        if contacto_form.is_valid():
            contacto_form.save()
            messages.success(request, 'Contacto actualizado correctamente.')
            return redirect('contacto-create', alumna_id=contacto.alumna.id)
    else:
        contacto_form = ContactoForm(instance=contacto)

    return render(request, 'contacto_form.html', {
        'form_title': 'Editar Contacto',
        'contacto_form': contacto_form,
        'contactos': Contacto.objects.filter(alumna_id=contacto.alumna.id),
    })

def contacto_delete_view(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id)
    if request.method == 'POST':
        alumno_id = contacto.alumna.id
        contacto.delete()
        messages.success(request, 'Contacto eliminado correctamente.')
        return redirect('contacto-create', alumna_id=alumno_id)
    
    # Si no es POST, no debe llegar a esta vista por el enlace
    return redirect('contacto-create', alumna_id=contacto.alumna.id)


def alumna_list_view(request):
    alumnas = Alumna.objects.all()
    for alumna in alumnas:
        alumna.edad = now().year - alumna.persona.fecha_nacimiento.year
        asignacion = AsignacionCiclo.objects.filter(alumna=alumna).first()
        alumna.asignacion = asignacion.grado.nombre_grado if asignacion else 'No asignada'
    
    return render(request, 'alumna_list.html', {
        'alumnas': alumnas
    })
    
    
    

def alumna_edit_view(request, alumna_id):
    alumna = get_object_or_404(Alumna, id=alumna_id)
    persona = alumna.persona
    
    if request.method == 'POST':
        # Incluye el valor del campo oculto 'persona' en los datos del formulario
        post_data = request.POST.copy()
        post_data['persona'] = persona.id
        
        # Recibe datos del formulario para Alumna y Persona
        alumna_form = AlumnaForm(post_data, instance=alumna)
        persona_form = PersonaForm(request.POST, instance=persona)
        asignacion_form = AsignacionCicloForm(request.POST)
        
        if alumna_form.is_valid() and persona_form.is_valid():
            # Guarda los datos de Alumna y Persona
            alumna_form.save()
            persona_form.save()
            
            # Manejo de la asignación de ciclo
            if asignacion_form.is_valid():
                asignacion = AsignacionCiclo.objects.filter(alumna=alumna).first()
                if asignacion:
                    asignacion_form = AsignacionCicloForm(request.POST, instance=asignacion)
                else:
                    asignacion = asignacion_form.save(commit=False)
                    asignacion.alumna = alumna
                    asignacion.user = request.user
                    asignacion.save()
                    
            messages.success(request, 'Datos actualizados correctamente.')
            return redirect('alumna-list')
    else:
        # Carga los formularios con los datos existentes
        alumna_form = AlumnaForm(instance=alumna)
        persona_form = PersonaForm(instance=persona)
        asignacion = AsignacionCiclo.objects.filter(alumna=alumna).first()
        asignacion_form = AsignacionCicloForm(instance=asignacion)
    
    return render(request, 'alumna_edit.html', {
        'alumna_form': alumna_form,
        'persona_form': persona_form,
        'asignacion_form': asignacion_form
    })