from django.contrib import admin
from .models import Cliente,Reserva,Habitacion,TipoHabitacion

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Reserva)
admin.site.register(Habitacion)
admin.site.register(TipoHabitacion)