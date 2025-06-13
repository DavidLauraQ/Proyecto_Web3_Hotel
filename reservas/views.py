from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Habitacion, Reserva, TipoHabitacion
from .forms import ReservaForm, HabitacionForm, ClienteForm, TipoHabitacionForm
from .forms import RegistroUsuarioForm
from .models import Cliente
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required, user_passes_test

def es_admin(user):
    return user.is_staff

# REGISTRAR (público)
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

# LOGIN / LOGOUT

def salir(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html')

# MODELOS (público o proteger si lo deseas)
def inicio(request):
    return render(request, 'inicio.html')

# CLIENTES
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

@login_required
@user_passes_test(es_admin)
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'crear_cliente.html', {'form': form})


@login_required
@user_passes_test(es_admin)
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
@login_required
@user_passes_test(es_admin)
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, 'eliminar_cliente.html', {'cliente': cliente})

# TIPO HABITACIONES
@login_required
@user_passes_test(es_admin)
def crear_tipohabitacion(request):
    if request.method == 'POST':
        form = TipoHabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('habitaciones')
    else:
        form = TipoHabitacionForm()
    return render(request, 'crear_tipohabitacion.html', {'form': form})

# HABITACIONES
@login_required
def lista_habitaciones(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'habitaciones.html', {'habitaciones': habitaciones})

@login_required
@user_passes_test(es_admin)
def crear_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('habitaciones')
    else:
        form = HabitacionForm()
    return render(request, 'crear_habitacion.html', {'form': form})

@login_required
@user_passes_test(es_admin)
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
@login_required
@user_passes_test(es_admin)
def eliminar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        habitacion.delete()
        return redirect('habitaciones')
    return render(request, 'eliminar_habitacion.html', {'habitacion': habitacion})

# RESERVAS
@login_required
def lista_reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'reservas.html', {'reservas': reservas})

@login_required
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            habitacion = form.cleaned_data['habitacion']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']

            # Verificar estado de la habitación
            if habitacion.estado != 'D':  # 'D' para Disponible
                messages.error(request, 'La habitación no está disponible para reservar.')
                return render(request, 'reservar.html', {'form': form})

            # Verificar que no haya reservas solapadas
            solapamiento = Reserva.objects.filter(
                habitacion=habitacion,
                fecha_fin__gte=fecha_inicio,
                fecha_inicio__lte=fecha_fin
            ).exists()

            if solapamiento:
                messages.error(request, 'La habitación ya está reservada en esas fechas.')
                return render(request, 'reservar.html', {'form': form})

            # Si pasa todas las validaciones, guardar reserva
            form.save()
            messages.success(request, 'Reserva creada con éxito.')
            return redirect('reservas')
    else:
        form = ReservaForm()
    return render(request, 'reservar.html', {'form': form})
@login_required
@user_passes_test(es_admin)
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

@login_required
@user_passes_test(es_admin)
def eliminar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.delete()
        return redirect('reservas')
    return render(request, 'eliminar_reserva.html', {'reserva': reserva})
