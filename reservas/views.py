from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Habitacion, Reserva
from .forms import ReservaForm, HabitacionForm, ClienteForm

def inicio(request):
    return render(request, 'inicio.html')

# CLIENTES

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})


def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'crear_cliente.html', {'form': form})

def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'editar_cliente.html', {'form': form, 'cliente': cliente})

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, 'eliminar_cliente.html', {'cliente': cliente})

# HABITACIONES

def lista_habitaciones(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'habitaciones.html', {'habitaciones': habitaciones})

def crear_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('habitaciones')
    else:
        form = HabitacionForm()
    return render(request, 'crear_habitacion.html', {'form': form})

def editar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        form = HabitacionForm(request.POST, instance=habitacion)
        if form.is_valid():
            form.save()
            return redirect('habitaciones')
    else:
        form = HabitacionForm(instance=habitacion)
    return render(request, 'editar_habitacion.html', {'form': form, 'habitacion': habitacion})

def eliminar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        habitacion.delete()
        return redirect('habitaciones')
    return render(request, 'eliminar_habitacion.html', {'habitacion': habitacion})

# RESERVAS

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

def editar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('reservas')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'editar_reserva.html', {'form': form, 'reserva': reserva})

def eliminar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.delete()
        return redirect('reservas')
    return render(request, 'eliminar_reserva.html', {'reserva': reserva})

