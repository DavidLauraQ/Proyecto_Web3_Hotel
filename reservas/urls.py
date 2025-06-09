from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('clientes/', views.lista_clientes, name='clientes'),
    path('habitaciones/', views.lista_habitaciones, name='habitaciones'),
    path('reservas/', views.lista_reservas, name='reservas'),
    path('reservar/', views.crear_reserva, name='reservar'),
]