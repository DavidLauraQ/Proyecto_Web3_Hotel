from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Incluye las URLs de tu aplicación de reservas
    path('', include('reservas.urls')),  # Las URLs de la app estarán en la raíz    
    
]

