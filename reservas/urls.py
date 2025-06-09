from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.inicio, name='home'),
    path('clientes/', views.lista_clientes, name='clientes'),
    path('habitaciones/', views.lista_habitaciones, name='habitaciones'),
    path('reservas/', views.lista_reservas, name='reservas'),
    path('reservar/', views.crear_reserva, name='reservar'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.salir, name='logout'),
    path('accounts/registro/', views.registrar, name='registrar'),

]