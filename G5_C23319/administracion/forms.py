from django import forms
from .models import NaturalPark, Category, Campsite, Availability, Reservation, Profile, User

Province = NaturalPark.Province

class NaturalParkFilterForm(forms.Form):
    name = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre'}))

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            if not NaturalPark.objects.filter(name=name).exists():
                raise forms.ValidationError("Nombre Inexistente")
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
    name = forms.CharField(max_length=255, required=False)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            if not Campsite.objects.filter(name=name).exists():
                raise forms.ValidationError("No se encontraron campamentos con ese nombre.")
        return name
class CampsiteForm(forms.ModelForm):
    class Meta:
        model = Campsite
        fields = ['natural_park', 'name', 'description', 'image', 'categories']
        widgets = {
            'natural_park': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
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

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['campsite', 'start_date', 'end_date']
        widgets = {
            'campsite': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'campsite': 'Campamento',
            'start_date': 'Fecha de inicio',
            'end_date': 'Fecha de fin',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['campiste'].queryset = Campsite.objects.all()

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['user', 'campsite', 'availability', 'check_in', 'check_out', 'number_guests']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'campsite': forms.Select(attrs={'class': 'form-control'}),
            'availability': forms.Select(attrs={'class': 'form-control'}),
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
        self.fields['campiste'].queryset = Campsite.objects.all()

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
            'user': forms.SelectMultiple(attrs={'class': 'form-control'}),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.all()
