from django.shortcuts import render, redirect
from .models import Cliente, Habitacion, Reserva
from .forms import ReservaForm

def inicio(request):
    return render(request, 'inicio.html')

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

def lista_habitaciones(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'habitaciones.html', {'habitaciones': habitaciones})

def lista_reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'reservas.html', {'reservas': reservas})

def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservas')
    else:
        form = ReservaForm()
    
    return render(request, 'reservar.html', {'form': form})