from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('habitaciones/', views.lista_habitaciones, name='habitaciones'),
    path('reservas/', views.lista_reservas, name='reservas'),
    path('reservar/', views.crear_reserva, name='reservar'),
    path('reservas/eliminar/<int:pk>/', views.eliminar_reserva, name='eliminar_reserva'),
    path('reservas/editar/<int:pk>/', views.editar_reserva, name='editar_reserva'),
    path('habitaciones/nueva/', views.crear_habitacion, name='crear_habitacion'),
    path('habitaciones/editar/<int:pk>/', views.editar_habitacion, name='editar_habitacion'),
    path('habitaciones/eliminar/<int:pk>/', views.eliminar_habitacion, name='eliminar_habitacion'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
]