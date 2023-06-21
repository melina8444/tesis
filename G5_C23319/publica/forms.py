from django import forms
from django.forms import ValidationError
import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from administracion.models import Usuario, Profile


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

class UsuarioCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=255,label='Teléfono', widget=forms.TextInput(attrs={'class': 'form-control'}) )
    address = forms.CharField(max_length=255,label='Dirección', widget=forms.TextInput(attrs={'class': 'form-control'}))
    dni = forms.CharField(max_length=255, label='DNI', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email',
            'password1': 'Contraseña',
            'password2': 'Confirmación de contraseña',
        }

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if dni:
            if not dni.isnumeric():
                raise forms.ValidationError("El DNI debe ser un valor numérico.")
            if len(dni) < 7 or len(dni) > 8:
                raise forms.ValidationError("El DNI debe tener entre 7 y 8 dígitos.")
        return dni
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = Profile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address'],
                dni=self.cleaned_data['dni'],
                is_client=False
            )
        return user
    
 
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Contraseña", strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
