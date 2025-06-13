from django.db import models

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
    id = models.AutoField(primary_key=True)  # Opcional, Django lo crea automáticamente
    numero_habitacion = models.CharField(max_length=10)
    tipo_habitacion = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE)
    capacidad = models.IntegerField()
    estado = models.CharField(
        max_length=1, 
        choices=[('D','Disponible'), ('O','Ocupada'), ('M','Mantenimiento')], 
        default='D'
    )

    def __str__(self):
        return f"Habitación {self.numero_habitacion}"


class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Quitar db_column para evitar problemas
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)  # Igual aquí
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
        return f"Reserva {self.id_reserva} - {self.cliente} en {self.habitacion}"
