from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import User, Rol
from .forms import CustomUserCreationForm, CustomUserChangeForm

class UserListView(ListView):
    model = User
    template_name = 'user/user_list.html'

class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('user-list')

class UserUpdateView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('user-list')

class UserDeleteView(DeleteView):
    model = User
    template_name = 'user/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')




#class RolListView(ListView):
   # model = Rol
    #template_name = 'user/rol_list.html'

#class RolCreateView(CreateView):
    #model = Rol
    #form_class = RolForm
    #template_name = 'user/rol_form.html'
    #success_url = reverse_lazy('rol-list')

#class RolUpdateView(UpdateView):
#    model = Rol
#    form_class = RolForm
#    template_name = 'user/rol_form.html'
#    success_url = reverse_lazy('rol-list')

#class RolDeleteView(DeleteView):
#    model = Rol
#    template_name = 'user/rol_confirm_delete.html'
#    success_url = reverse_lazy('rol-list')

