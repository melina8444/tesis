from django import forms
from .models import NaturalPark, Category, Campsite, Availability, Reservation, Profile, User

class NaturalParkForm(forms.ModelForm):
    class Meta:
        model = NaturalPark
        fields = ['name', 'description', 'location', 'province', 'image', 'website']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'province': forms.Select(attrs={'class': 'form-control'}),
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

class CampsiteForm(forms.ModelForm):
    class Meta:
        model = Campsite
        fields = ['natural_park', 'name', 'description', 'image', 'categories']
        widgets = {
            'natural_park': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'categories': forms.ModelMultipleChoiceField(
                queryset=Category.objects.all(),
                widget=forms.SelectMultiple(attrs={'class': 'form-control'})
            ),
        }
        labels = {
            'natural_park': 'Natural Park',
            'name': 'Name',
            'description': 'Description',
            'image': 'Image',
            'categories': 'Categories',
        }

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['campsite', 'start_date', 'end_date']
        widgets = {
            'campsite': forms.ModelMultipleChoiceField(
                queryset=User.objects.all(),
                widget=forms.SelectMultiple(attrs={'class': 'form-control'})
            ),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'campsite': 'Campamento',
            'start_date': 'Fecha de inicio',
            'end_date': 'Fecha de fin',
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['user', 'campsite', 'availability', 'check_in', 'check_out', 'number_guests']
        widgets = {
            'user': forms.ModelMultipleChoiceField(
                queryset=User.objects.filter(is_client=True),
                widget=forms.Select(attrs={'class': 'form-control'})
            ),
            'campsite': forms.ModelMultipleChoiceField(
                queryset=Campsite.objects.all(),
                widget=forms.SelectMultiple(attrs={'class': 'form-control'})
            ),
            'availability': forms.ModelMultipleChoiceField(
                queryset=Availability.objects.none(),
                widget=forms.Select(attrs={'class': 'form-control'})
            ),
            'check_in': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'number_guests': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'user': 'Usuario',
            'campsite': 'Camping',
            'availability': 'Disponibilidad',
            'check_in': 'Fecha de entrada',
            'check_out': 'Fecha de salida',
            'number_guests': 'Número de huéspedes',
        }
        help_texts = {
            'availability': 'Seleccione las disponibilidades para la reserva',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'campsite' in self.data:
            try:
                campsite_id = int(self.data.get('campsite'))
                self.fields['availability'].queryset = Availability.objects.filter(campsite_id=campsite_id)
            except (ValueError, TypeError):
                self.add_error(Availability, "Ocurrió un error al obtener las disponibilidades.")
        elif self.instance.pk:
            self.fields['availability'].queryset = self.instance.campsite.availabilities.all()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'phone', 'address', 'dni', 'is_client']
        widgets = {
            'user': forms.ModelMultipleChoiceField(
                queryset=User.objects.all(),
                widget=forms.SelectMultiple(attrs={'class': 'form-control'})
            ),
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
            'is_client': 'Es cliente',
        }

  
