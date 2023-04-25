from django import forms

class ContactForm(forms.Form):
    nombre=forms.CharField(label='Nombre', max_length=100)
    apellido=forms.CharField(label='Apellido', max_length=100)
    email=forms.CharField(label='Email', max_length=75)
    comentario=forms.CharField(label='Comentario/Consulta', widget=forms.Textarea)

