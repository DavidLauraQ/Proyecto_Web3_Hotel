from django.db import models
from django.core.validators import MinValueValidator, EmailValidator
from django.core.exceptions import ValidationError
from datetime import date

class Cliente(models.Model):
    """Modelo que representa a un cliente del hotel"""
    id_cliente = models.AutoField(primary_key=True)  # Clave primaria autoincremental
    nombre = models.CharField(max_length=50)  # Nombre del cliente
    apellido = models.CharField(max_length=50)  # Apellido del cliente
    email = models.EmailField(unique=True, validators=[EmailValidator()])  # Email único con validación
    telefono = models.CharField(max_length=20)  # Teléfono de contacto
    
    def __str__(self):
        """Representación en string del cliente (nombre + apellido)"""
        return f"{self.nombre} {self.apellido}"

class TipoHabitacion(models.Model):
    """Modelo para los tipos de habitación (Individual, Doble, Suite, etc.)"""
    id_tipo_habitacion = models.AutoField(primary_key=True)  # Clave primaria
    nombre_tipo = models.CharField(max_length=50, unique=True)  # Nombre único del tipo
    descripcion = models.TextField()  # Descripción detallada
    precio_noche = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]  # Precio no puede ser negativo
    )
    
    def __str__(self):
        """Representación en string del tipo de habitación"""
        return self.nombre_tipo

class Habitacion(models.Model):
    """Modelo que representa una habitación física del hotel"""
    # Opciones para el estado de la habitación
    ESTADOS_HABITACION = (
        ('D', 'Disponible'),  # Disponible para reserva
        ('O', 'Ocupada'),    # Actualmente ocupada
        ('M', 'Mantenimiento'),  # En reparación/no disponible
    )
    
    id_habitacion = models.AutoField(primary_key=True)  # Clave primaria
    numero_habitacion = models.CharField(max_length=10, unique=True)  # Número único de habitación
    id_tipo_habitacion = models.ForeignKey(
        TipoHabitacion, 
        on_delete=models.PROTECT,  # Evita borrar tipo si hay habitaciones
        db_column='id_tipo_habitacion'  # Nombre de columna en BD
    )
    capacidad = models.PositiveIntegerField(default=1)  # Número máximo de huéspedes
    estado = models.CharField(
        max_length=1, 
        choices=ESTADOS_HABITACION, 
        default='D'  # Por defecto disponible
    )
    
    def __str__(self):
        """Representación en string (Número + Estado)"""
        return f"Habitación {self.numero_habitacion} ({self.get_estado_display()})"
    
    class Meta:
        verbose_name = 'Habitación'  # Nombre singular en admin
        verbose_name_plural = 'Habitaciones'  # Nombre plural en admin

class Reserva(models.Model):
    """Modelo para las reservas de los clientes"""
    # Estados posibles de una reserva
    ESTADOS_RESERVA = (
        ('P', 'Pendiente'),   # Creada pero no confirmada
        ('C', 'Confirmada'),  # Reserva activa
        ('X', 'Cancelada'),   # Reserva cancelada
        ('F', 'Finalizada'),  # Estancia completada
    )
    
    id_reserva = models.AutoField(primary_key=True)  # Clave primaria
    id_cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.PROTECT,  # Protege al cliente si tiene reservas
        db_column='id_cliente'
    )
    id_habitacion = models.ForeignKey(
        Habitacion, 
        on_delete=models.PROTECT,  # Protege habitación si tiene reservas
        db_column='id_habitacion'
    )
    fecha_inicio = models.DateField()  # Fecha de check-in
    fecha_fin = models.DateField()     # Fecha de check-out
    estado_reserva = models.CharField(
        max_length=1, 
        choices=ESTADOS_RESERVA, 
        default='P'  # Por defecto pendiente
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha creación automática
    
    def __str__(self):
        """Representación en string (ID + Cliente)"""
        return f"Reserva #{self.id_reserva} - {self.id_cliente}"
    
    def clean(self):
        """
        Validaciones adicionales antes de guardar:
        1. Fechas coherentes
        2. No reservas pasadas
        3. Habitación disponible
        4. No superposición con otras reservas
        """
        # Validar que fecha_fin sea mayor que fecha_inicio
        if self.fecha_fin <= self.fecha_inicio:
            raise ValidationError("La fecha de fin debe ser posterior a la de inicio")
        
        # Validar que no se reserve para fechas pasadas
        if self.fecha_inicio < date.today():
            raise ValidationError("No se pueden hacer reservas para fechas pasadas")
        
        # Validar disponibilidad de la habitación
        if self.estado_reserva == 'C' and self.id_habitacion.estado != 'D':
            raise ValidationError("La habitación no está disponible para reserva")
        
        # Verificar superposición de reservas para la misma habitación
        reservas_existentes = Reserva.objects.filter(
            id_habitacion=self.id_habitacion,
            estado_reserva='C',  # Solo considerar reservas confirmadas
            fecha_inicio__lt=self.fecha_fin,  # Inicio antes que mi fin
            fecha_fin__gt=self.fecha_inicio   # Fin después de mi inicio
        ).exclude(pk=self.pk)  # Excluir la propia reserva en actualizaciones
        
        if reservas_existentes.exists():
            raise ValidationError("La habitación ya está reservada para esas fechas")
    
    def save(self, *args, **kwargs):
        """Método save personalizado para validar y actualizar estados"""
        self.full_clean()  # Ejecuta las validaciones de clean()
        super().save(*args, **kwargs)
        
        # Actualizar estado de la habitación si la reserva está confirmada
        if self.estado_reserva == 'C':
            self.id_habitacion.estado = 'O'
            self.id_habitacion.save()
    
    class Meta:
        ordering = ['-fecha_creacion']  # Ordenar por fecha descendente
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'