from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente, Habitacion, Reserva, TipoHabitacion
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroUsuarioForm(UserCreationForm):
    nombre = forms.CharField(max_length=100, required=True)
    apellido = forms.CharField(max_length=100, required=True)
    telefono = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # Aquí no existen nombre, apellido, telefono en User, debes manejarlo aparte
        if commit:
            user.save()
            # Aquí puedes guardar los datos adicionales en un perfil extendido
        return user


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TipoHabitacionForm(forms.ModelForm):
    class Meta:
        model = TipoHabitacion
        fields = ['nombre_tipo', 'descripcion', 'precio_noche']
        widgets = {
            'nombre_tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'precio_noche': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['numero_habitacion', 'tipo_habitacion', 'capacidad', 'estado']
        widgets = {
            'numero_habitacion': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_habitacion': forms.Select(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'habitacion', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'habitacion': forms.Select(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(
                format='%m/%d/%Y',
                attrs={'class': 'form-control', 'placeholder': 'MM/DD/YYYY', 'type': 'text'}
            ),
            'fecha_fin': forms.DateInput(
                format='%m/%d/%Y',
                attrs={'class': 'form-control', 'placeholder': 'MM/DD/YYYY', 'type': 'text'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_inicio'].input_formats = ['%m/%d/%Y']
        self.fields['fecha_fin'].input_formats = ['%m/%d/%Y']

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        habitacion = cleaned_data.get('habitacion')

        if fecha_inicio and fecha_fin:
            if fecha_inicio < date.today():
                raise ValidationError("No se pueden hacer reservas en fechas pasadas.")
            if fecha_fin <= fecha_inicio:
                raise ValidationError("La fecha de salida debe ser posterior a la de entrada.")

        if habitacion and fecha_inicio and fecha_fin:
            reservas_solapadas = Reserva.objects.filter(
                habitacion=habitacion,
                estado_reserva='confirmada',
                fecha_inicio__lt=fecha_fin,
                fecha_fin__gt=fecha_inicio
            )
            if self.instance.pk:
                reservas_solapadas = reservas_solapadas.exclude(pk=self.instance.pk)

            if reservas_solapadas.exists():
                raise ValidationError("La habitación no está disponible para esas fechas.")


class DisponibilidadForm(forms.Form):
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    tipo_habitacion = forms.ModelChoiceField(
        queryset=TipoHabitacion.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            if fecha_fin <= fecha_inicio:
                raise ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")
