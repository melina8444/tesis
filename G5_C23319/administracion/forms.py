from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime


class CalendarWidget(forms.TextInput):
    class Media:
        CSS = { 'all': ('pretty.css',) }
        js = ('animations.js', 'actions.js')

class ClienteForm(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Solo letras'}),max_length=50, label='Nombre')
    apellido = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control',  'placeholder': 'Solo letras'}),max_length=30, label='Apellido')
    email = forms.EmailField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'type': 'email',  'placeholder': 'ej: xxx@gmail.com'}),max_length=50, label='E-mail', required=False)
    telefono = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control',  'placeholder': 'Solo Números'}),max_length=30, label='Telefono')
    f_nac = forms.DateField(widget=forms.SelectDateWidget(attrs={ 'class': 'form-control'}),label='Fecha de Nacimiento')
    f_registro = forms.DateTimeField(widget=forms.TextInput(attrs={ 'class': 'form-control'}),label="Fecha de registro")

