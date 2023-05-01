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

