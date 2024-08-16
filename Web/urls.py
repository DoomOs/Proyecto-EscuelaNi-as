from Web import views
from django.urls import path
from django.conf import settings  # para agregar la ruta de la imagen
from django.conf.urls.static import static  # para agregar la ruta de la imagen

urlpatterns = [
    path('', views.inicio, name='InicioWeb'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
