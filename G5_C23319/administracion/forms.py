import random
import string
import uuid
from django import forms
from .models import NaturalPark, Category, Campsite, Availability, Reservation, Profile, Usuario, Guest
from django.db.models import Sum
from django.core.exceptions import ValidationError

Province = NaturalPark.Province

class NaturalParkFilterForm(forms.Form):
    name = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre'}))

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            if not NaturalPark.objects.filter(name=name).exists():
                raise forms.ValidationError("No se encontraron parques naturales con ese nombre")
        return name
class NaturalParkForm(forms.ModelForm):
    province = forms.ChoiceField(choices=Province.choices, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = NaturalPark
        fields = ['name', 'description', 'location', 'province', 'image', 'website']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'location': 'Ubicación',
            'province': 'Provincia',
            'image': 'Imagen',
            'website': 'Sitio web',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['province'].choices = [(choice.value, choice.name) for choice in Province]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'capacity', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'capacity': 'Capacidad',
            'price': 'Precio',
        }

class CampsiteFilterForm(forms.Form):
    name = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre'}))

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            if not Campsite.objects.filter(name=name).exists():
                raise forms.ValidationError("No se encontraron campings con ese nombre.")
        return name
class CampsiteForm(forms.ModelForm):

    class Meta:
        model = Campsite
        fields = ['natural_park', 'name', 'description', 'images', 'categories']
        widgets = {
            'natural_park': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'images': forms.FileInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'})
            
        }
        labels = {
            'natural_park': 'Natural Park',
            'name': 'Name',
            'description': 'Description',
            'image': 'Image',
            'categories': 'Categories',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.all()
        self.fields['natural_park'].queryset = NaturalPark.objects.all()

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['campsite', 'start_date', 'end_date', 'max_capacity']
        widgets = {
            'campsite': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'max_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'campsite': 'Camping',
            'start_date': 'Fecha de inicio',
            'end_date': 'Fecha de fin',
            'max_capacity': 'Capacidad máxima'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['campsite'].queryset = Campsite.objects.all()

class AvailabilityCampsiteFilterForm(forms.Form):
    campsite_name = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre'}))

    def clean_campsite_name(self):
        campsite_name = self.cleaned_data.get('campsite_name')
        if campsite_name:
            if not Availability.objects.filter(campsite__name=campsite_name).exists():
                raise forms.ValidationError("No se encontraron disponibilidades para ese camping o el nombre es incorrecto.")
        return campsite_name


class ReservationForm(forms.ModelForm):

    code = forms.CharField(label='Código de Reserva', widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
    check_in = forms.DateField(label='Check_in - Fecha de Llegada', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    check_out = forms.DateField(label='Check_out - Fecha de Salida',widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    user = forms.ModelChoiceField(label='Usuario',queryset=Usuario.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Reservation
        fields = ['code', 'campsite', 'user', 'check_in', 'check_out', 'number_guests']
        widgets = {
            'campsite': forms.Select(attrs={'class': 'form-control'}),
            'number_guests': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'campsite': 'Camping',
            'number_guests': 'Número de Huéspedes'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Verificar si es una nueva reserva
            self.initial['code'] = self.generate_random_code()

    def generate_random_code(self):
        length = 8
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def clean(self):

        cleaned_data = super().clean()
        campsite = cleaned_data.get('campsite')
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        number_guests = cleaned_data.get('number_guests')

        if campsite and check_in and check_out and number_guests:
            try:
                availability = Availability.objects.get(campsite=campsite)
                if check_in < availability.start_date or check_out > availability.end_date:
                    self.add_error(None, forms.ValidationError(f"Las fechas de check-in y check-out deben estar dentro del rango de disponibilidad: De {availability.start_date} a {availability.end_date}"))
            
                suma_guests = Reservation.objects.filter(campsite=campsite, check_in__lte=check_out, check_out__gte=check_in).aggregate(total_guests=Sum('number_guests'))['total_guests']

                # Verificar si la suma de guests_number supera el max_capacity de availability
                if suma_guests is not None and (suma_guests + number_guests) > availability.max_capacity:
                    self.add_error(None, forms.ValidationError(f"El camping seleccionado para este rango de fechas está ocupado al 100%"))
            
            except Availability.DoesNotExist:
                self.add_error(None, forms.ValidationError(f"No se encontró disponibilidad para el camping seleccionado."))

        """ if check_out <= check_in:
            self.add_error(None, forms.ValidationError(f"La fecha de check-out debe ser posterior a la fecha de check-in.")) """
        
        if check_out is not None and check_in is not None:
            if check_out <= check_in:
                self.add_error(None, forms.ValidationError(f"La fecha de check-out debe ser posterior a la fecha de check-in."))
        
        if number_guests <= 0:
            self.add_error(None, forms.ValidationError(f"Se debe ingresar un número de huéspedes"))

        return cleaned_data

class ReservationCampsiteFilterForm(forms.Form):
    campsite_name = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre'}))

    def clean_campsite_name(self):
        campsite_name = self.cleaned_data.get('campsite_name')
        if campsite_name:
            if not Reservation.objects.filter(campsite__name=campsite_name).exists():
                raise forms.ValidationError("No se encontraron reservas para ese camping o el nombre del camping es incorrecto.")
        return campsite_name
class GuestForm(forms.ModelForm):
    
    class Meta:
        model = Guest
        fields = ['first_name', 'last_name', 'dni', 'age']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'dni': 'DNI',
            'age': 'Edad',
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'phone', 'address', 'dni', 'is_client']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'is_client': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'user': 'Usuario',
            'phone': 'Teléfono',
            'address': 'Dirección',
            'dni': 'DNI',
            'is_client': 'Is Client',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = Usuario.objects.all()

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if dni:
            if not dni.isnumeric():
                raise forms.ValidationError("El DNI debe ser un valor numérico.")
            if len(dni) < 7 or len(dni) > 8:
                raise forms.ValidationError("El DNI debe tener entre 7 y 8 dígitos.")
        return dni
    
class ProfileFilterForm(forms.Form):
    user = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el usuario'}))
    is_client = forms.BooleanField(label='Es cliente', widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),required=False)

    def clean_name(self):
        user = self.cleaned_data.get('user')
        if user:
            if not Profile.objects.filter(user__username=user).exists():
                raise forms.ValidationError("No se encontraron perfiles con ese nombre.")
        return user

class GuestFilterForm(forms.Form):
    reservation_code = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la reserva'}))

    def clean_reservation_code(self):
        reservation_code = self.cleaned_data.get('reservation_code')
        if reservation_code:
            if not Guest.objects.filter(reservation__code=reservation_code).exists():
                raise forms.ValidationError("No se encontraron huéspedes para esa reserva.")
        return reservation_code