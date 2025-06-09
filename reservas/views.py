from django.shortcuts import render, redirect
from .models import Cliente, Habitacion, Reserva
from .forms import ReservaForm


# REGISTRAR
from .forms import RegistroUsuarioForm
from .models import Cliente

def registrar(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear cliente asociado
            Cliente.objects.create(
                nombre=form.cleaned_data['nombre'],
                apellido=form.cleaned_data['apellido'],
                email=form.cleaned_data['email'],
                telefono=form.cleaned_data['telefono']
            )
            login(request, user)
            return redirect('home')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registration/registrar.html', {'form': form})



# LOGIN

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm

           
def salir(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html')

# MODELOS

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