from django import forms
from django.forms import ValidationError
import re


def solo_caracteres(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('El nombre no puede contener números. %(valor)s',
                            code='Invalid',
                            params={'valor':value})

def validate_email(value):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValidationError('Correo electrónico inválido')
    return value

class ContactForm(forms.Form):
    nombre=forms.CharField(label='Nombre', 
                           max_length=100,
                           widget=forms.TextInput(
                               attrs={'class':'form-control', 
                                      'placeholder':'Nombre'}
                            )
                           )
    apellido=forms.CharField(label='Apellido', 
                           max_length=100,
                           widget=forms.TextInput(
                               attrs={'class':'form-control', 
                                      'placeholder':'Apellido'}
                            )
                           )
    email=forms.EmailField(label='Email', 
                           max_length=100,
                           required=False,
                           validators=(validate_email,),
                           error_messages={'required':'El email es requerido para continuar.'},
                           widget=forms.TextInput(
                               attrs={'class':'form-control', 
                                      'placeholder':'Email',
                                      'type':'email'}
                            ),
                           )
    comentario=forms.CharField(label='Comentario', 
                           max_length=270,
                           widget=forms.Textarea(
                               attrs={'rows':3, 'cols':100, 'class':'form-control', 'placeholder':'Ingrese un comentario o consulta'}
                            )
                           )
class ReservaForm(forms.Form):

    name = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control m-1','placeholder':'Tu nombre' }))
    
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control m-1','placeholder': 'Tu email',}))
    
    check_in_date = forms.DateField(label='Check-in Fecha',widget=forms.DateInput(attrs={'class': 'form-control m-1', 'placeholder':'Ingresá la fecha de llegada',}))
    
    check_out_date = forms.DateField(label='Check-out Fecha',widget=forms.DateInput(attrs={'class': 'form-control m-1', 'placeholder':'Ingresá la fecha de partida',}))
    
    num_guest = forms.IntegerField(label='Número de Huéspedes',widget=forms.NumberInput(attrs={'class': 'form-control m-1','placeholder': 'Ingresá cuántas personas realizan la reserva',}))
    
    campsite_id = forms.IntegerField(label='Camping',required=False, widget=forms.HiddenInput())

    campsite = forms.ChoiceField(choices=())

    def __init__(self, *args, **kwargs):
        campsites_list = kwargs.pop('campsites_list', None)
        super(ReservaForm, self).__init__(*args, **kwargs)
        if campsites_list:
            self.fields['campsite'].choices = [(campsite['id'], campsite['name']) for campsite in campsites_list]


    