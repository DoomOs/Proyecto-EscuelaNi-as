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
from django.db.models import Max, Q
from django.contrib.auth.decorators import login_required

def persona_create_view(request):
    """
        Maneja la creación de una nueva persona y redirige a la vista de creación de alumna.

    Parámetros:
       - request (HttpRequest): La solicitud HTTP que contiene los datos del formulario de persona.

    Retorna:
       - HttpResponse: Redirige a la vista de creación de alumna con el ID de la persona creada, o renderiza el formulario de persona si hay errores.

    Proceso:
        - Si el método de la solicitud es POST, se valida el formulario de Persona.
        - Si el formulario es válido, se guarda la persona y se redirige a la vista de creación de alumna.
        - Si el formulario no es válido, se renderiza de nuevo el formulario de Persona.

    """
    
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            persona = form.save()
            return redirect(reverse('alumna-create') + f'?persona_id={persona.id}')
    else:
        form = PersonaForm()

    return render(request, 'persona_form.html', {'form': form})

def alumna_create_view(request):
    
    """
        Maneja la creación de una nueva alumna asociada a una persona existente.

    Parámetros:
       - request (HttpRequest): La solicitud HTTP que contiene los datos del formulario de alumna.

    Retorna:
       - HttpResponse: Redirige a la vista de creación de contacto con el ID de la alumna creada, o renderiza el formulario de alumna si hay errores.

    Proceso:
        - Obtiene el ID de la persona desde la URL.
        - Si el método de la solicitud es POST, se valida el formulario de Alumna.
        - Si el formulario es válido, se guarda la alumna y se redirige a la vista de creación de contacto.
        - Si el formulario no es válido, se renderiza de nuevo el formulario de Alumna con el ID de la persona como valor inicial.

    """
    
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
    """
        Maneja la creación de un nuevo contacto asociado a una alumna específica.

    Parámetros:
       - request (HttpRequest): La solicitud HTTP que contiene los datos del formulario de contacto.
       - alumna_id (int): El ID de la alumna a la que se asociará el nuevo contacto.

    Retorna:
       - HttpResponse: Renderiza el formulario de contacto con la lista de contactos existentes de la alumna.

    Proceso:
        - Obtiene la alumna usando el ID proporcionado.
        - Si el método de la solicitud es POST, se valida el formulario de Contacto.
        - Si el formulario es válido, se guarda el contacto asociado a la alumna.
        - Renderiza el formulario de contacto con todos los contactos de la alumna.

    """
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
    """
        Maneja la edición de un contacto existente.

    Parámetros:
       - request (HttpRequest): La solicitud HTTP que contiene los datos del formulario de contacto.
       - contacto_id (int): El ID del contacto a editar.

    Retorna:
       - HttpResponse: Renderiza el formulario de contacto editado y la lista de contactos de la alumna.

    Proceso:
        - Obtiene el contacto usando el ID proporcionado.
        - Si el método de la solicitud es POST, se valida el formulario de Contacto.
        - Si el formulario es válido, se guarda el contacto editado.
        - Renderiza el formulario de contacto con la lista de contactos de la alumna.

    """
    
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
    """
        Maneja la eliminación de un contacto existente.

    Parámetros:
       - request (HttpRequest): La solicitud HTTP que contiene la acción de eliminación.
       - contacto_id (int): El ID del contacto a eliminar.

    Retorna:
       - HttpResponse: Redirige a la vista de creación de contacto de la alumna correspondiente.

    Proceso:
        - Obtiene el contacto usando el ID proporcionado.
        - Si el método de la solicitud es POST, se elimina el contacto.
        - Redirige a la vista de creación de contacto de la alumna después de la eliminación.

    """
    contacto = get_object_or_404(Contacto, id=contacto_id)
    if request.method == 'POST':
        alumno_id = contacto.alumna.id
        contacto.delete()
        messages.success(request, 'Contacto eliminado correctamente.')
        return redirect('contacto-create', alumna_id=alumno_id)
    
    # Si no es POST, no debe llegar a esta vista por el enlace
    return redirect('contacto-create', alumna_id=contacto.alumna.id)


@login_required
def alumna_list_view(request):
    """
        Maneja la visualización de la lista de alumnas activas.

    Parámetros:
       - request (HttpRequest): La solicitud HTTP que contiene la información del usuario.

    Retorna:
       - HttpResponse: Renderiza la lista de alumnas activas, organizadas por asignación.

    Proceso:
        - Obtiene el usuario logueado y su grado asignado.
        - Filtra las alumnas activas y obtiene su mejor asignación.
        - Calcula la edad de cada alumna y organiza la lista según su grado.
        - Renderiza la lista de alumnas en el contexto de la plantilla.

    """
    user = request.user  # Obtener el usuario logueado
    grado_usuario_id = user.id_ciclo  # Obtener el grado asignado al usuario

    # Obtener todas las alumnas activas
    alumnas = Alumna.objects.filter(estado=True)

    # Crear un diccionario para almacenar la mejor asignación por alumna
    mejor_asignacion = {}

    for alumna in alumnas:
        # Obtener todas las asignaciones de la alumna, ordenadas por grado (mayor ID primero)
        asignaciones = AsignacionCiclo.objects.filter(alumna=alumna).order_by('-grado_id')

        if asignaciones.exists():
            mejor_asignacion[alumna.id] = asignaciones.first()  # Tomar la mejor asignación
        else:
            mejor_asignacion[alumna.id] = None  # Sin asignación

    # Listas para alumnas en el mismo grado y las demás
    alumnas_en_mismo_grado = []
    alumnas_otros_grados = []

    for alumna in alumnas:
        asignacion = mejor_asignacion[alumna.id]
        if asignacion:
            alumna.asignacion = asignacion.grado.nombre_grado
        else:
            alumna.asignacion = 'No asignada'

        # Calcular la edad
        alumna.edad = now().year - alumna.persona.fecha_nacimiento.year

        # Agregar a la lista correspondiente
        if asignacion and asignacion.grado.id == grado_usuario_id:
            alumnas_en_mismo_grado.append(alumna)
        else:
            alumnas_otros_grados.append(alumna)

    # Combinar las listas, priorizando las alumnas en el mismo grado
    alumnas_finales = alumnas_en_mismo_grado + alumnas_otros_grados

    return render(request, 'alumna_list.html', {
        'alumnas': alumnas_finales
    })


    
def alumna_inactive_list_view(request):
    """
        Maneja la visualización de la lista de alumnas inactivas.

    Parámetros:
       - request (HttpRequest): La solicitud HTTP.

    Retorna:
       - HttpResponse: Renderiza la lista de alumnas inactivas.

    Proceso:
        - Filtra las alumnas inactivas y calcula su edad y asignación.
        - Renderiza la lista de alumnas inactivas en el contexto de la plantilla.

    """
    alumnas = Alumna.objects.filter(estado=False)  # Solo alumnas inactivas
    for alumna in alumnas:
        alumna.edad = now().year - alumna.persona.fecha_nacimiento.year
        asignacion = AsignacionCiclo.objects.filter(alumna=alumna).last()
        alumna.asignacion = asignacion.grado.nombre_grado if asignacion else 'No asignada'

    return render(request, 'alumna_inactive_list.html', {'alumnas': alumnas})

    

def desactivar_alumna_view(request, alumna_id):
    """
        Maneja la desactivación de una alumna específica.

    Parámetros:
       - request (HttpRequest): La solicitud HTTP.
       - alumna_id (int): El ID de la alumna a desactivar.

    Retorna:
       - HttpResponse: Redirige a la lista de alumnas activas.

    Proceso:
        - Obtiene la alumna usando el ID proporcionado.
        - Cambia el estado de la alumna a inactiva y guarda los cambios.
        - Redirige a la lista de alumnas activas.

    """
    alumna = get_object_or_404(Alumna, id=alumna_id)
    alumna.estado = False
    alumna.save()
    return redirect('alumna-list')  # Redirige al listado de alumnas activas

def activar_alumna_view(request, alumna_id):
    """
        Maneja la activación de una alumna específica.

    Parámetros:
       - request (HttpRequest): La solicitud HTTP.
       - alumna_id (int): El ID de la alumna a activar.

    Retorna:
       - HttpResponse: Redirige a la lista de alumnas inactivas.

    Proceso:
        - Obtiene la alumna usando el ID proporcionado.
        - Cambia el estado de la alumna a activa y guarda los cambios.
        - Redirige a la lista de alumnas inactivas.

    """
    alumna = get_object_or_404(Alumna, id=alumna_id)
    alumna.estado = True
    alumna.save()
    return redirect('alumna-inactive-list')  # Redirige al listado de alumnas inactivas
    
    

def alumna_edit_view(request, alumna_id):
    """
        Maneja la edición de los datos de una alumna existente.

    Parámetros:
       - request (HttpRequest): La solicitud HTTP que contiene los datos del formulario de alumna.
       - alumna_id (int): El ID de la alumna a editar.

    Retorna:
       - HttpResponse: Renderiza el formulario de edición de alumna, persona y asignación.

    Proceso:
        - Obtiene la alumna y su persona asociada usando el ID proporcionado.
        - Si el método de la solicitud es POST, se validan los formularios de Alumna y Persona.
        - Si ambos formularios son válidos, se guardan los datos y se maneja la asignación de ciclo.
        - Renderiza el formulario de edición con los datos existentes si no es una solicitud POST.

    """
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