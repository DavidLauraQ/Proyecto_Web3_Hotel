from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', auth_views.LoginView.as_view() , name='home1'),
    path('home/', views.home, name='home'),
    
    # Clientes
    path('clientes/', views.lista_clientes, name='clientes'),
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),

    # Habitaciones
    path('habitaciones/', views.lista_habitaciones, name='habitaciones'),
    path('habitaciones/nueva/', views.crear_habitacion, name='crear_habitacion'),
    path('habitaciones/editar/<int:pk>/', views.editar_habitacion, name='editar_habitacion'),
    path('habitaciones/eliminar/<int:pk>/', views.eliminar_habitacion, name='eliminar_habitacion'),
    #
    path('habitaciones/nuevotipo/', views.crear_tipohabitacion, name='crear_tipohabitacion'),

    # Reservas
    path('reservas/', views.lista_reservas, name='reservas'),
    path('reservar/', views.crear_reserva, name='reservar'),
    path('reservas/eliminar/<int:pk>/', views.eliminar_reserva, name='eliminar_reserva'),
    path('reservas/editar/<int:pk>/', views.editar_reserva, name='editar_reserva'),
    
    #Descargar Reservas en pdf y excel
    path('reporte-reservas/pdf/', views.reporte_reservas_pdf, name='reporte_reservas_pdf'),
    path('reporte-reservas/excel/', views.reporte_reservas_excel, name='reporte_reservas_excel'),
    # Autenticación
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.salir, name='logout'),
    path('accounts/registro/', views.registrar, name='registrar'),
]
