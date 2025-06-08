from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class TipoHabitacion(models.Model):
    id_tipo_habitacion = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    precio_noche = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre_tipo

class Habitacion(models.Model):
    id_habitacion = models.AutoField(primary_key=True)
    numero_habitacion = models.CharField(max_length=10, unique=True)
    tipo_habitacion = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE, db_column='id_tipo_habitacion')
    capacidad = models.IntegerField()
    estado = models.CharField(
        max_length=20,
        choices=[
            ('disponible', 'Disponible'),
            ('ocupada', 'Ocupada'),
            ('mantenimiento', 'En Mantenimiento'),
            ('limpieza', 'En Limpieza'),
        ],
        default='disponible'
    )

    def __str__(self):
        return f"Habitación {self.numero_habitacion} ({self.tipo_habitacion.nombre_tipo})"

class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, db_column='id_habitacion')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado_reserva = models.CharField(
        max_length=20,
        choices=[
            ('confirmada', 'Confirmada'),
            ('pendiente', 'Pendiente'),
            ('cancelada', 'Cancelada'),
            ('completada', 'Completada'),
        ],
        default='pendiente'
    )

    def __str__(self):
        return f"Reserva {self.id_reserva} para {self.cliente.nombre} en Habitación {self.habitacion.numero_habitacion}"