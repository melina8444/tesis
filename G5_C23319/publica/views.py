from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm
from django.http import HttpResponseRedirect


import publica

def index(request):
    campsites_list = [
        {'name': 'Abracal',
         'location': 'San Javier - Córdoba',
         'category':'Camping Premium',
         'description':'Conservación, educación ambiental, observación de fauna silvestre, turismo',
         'image': 'Abracaral.jpeg',
         'availability': 'Enero-Marzo 2023'
         },
          {'name': 'Achalay',
         'location': 'Primera sección de islas del Delta, Tigre, Provincia de Buenos Aires',
         'category':'Camping Premium',
         'description':'Conservación, educación ambiental, turismo, investigación, observación de fauna silvestre',
         'image': 'Achalay.jpeg',
         'availability': 'Marzo-Diciembre 2023'
         },
          {'name': 'Curindy',
         'location': 'Localidad de Garuhapé, provincia de Misiones',
         'category':'Camping Básico',
         'description':'Conservación, explotación forestal, ganadería, investigación y turismo',
         'image':'Curindy.jpeg',
         'availability': 'Octubre-Diciembre 2023'
         },
          {'name': 'Cachape',
         'location': 'Localidad de General José de San Martín, provincia de Chaco',
         'category':'Camping Básico',
         'description':'Conservación compatible con turismo y producción',
         'image':'Cachape.jpeg',
         'availability': 'Junio-Noviembre 2023'
         },
          {'name': 'Caranday',
         'location': ' Villaguay, Entre Ríos',
         'category':'Camping Aventurero',
         'description':'Conservación compatible con Turismo y Producción',
         'image':'curindy.jpeg',
         'availability': 'Octubre-Diciembre 2023'
         },
          {'name': 'Caspinchango',
         'location': 'Localidad de Famaillá, provincia de Tucumán',
         'category':'Camping Premium',
         'description':'Conservación, educación ambiental, producción e investigación científica',
         'image':'Caspinchango.jpeg',
         'availability': 'Marzo-Diciembre 2023'
         },
          {'name': 'Cerro Champaquí',
         'location': 'Paraje Los Molles, Villa de las Rosas, provincia de Córdoba',
         'category':'Camping Aventurero',
         'description':'Conservación compatible con turismo y producción',
         'image':'Cerro-Champaqui.jpeg',
         'availability': 'Marzo-Diciembre 2023'
         },
          {'name': 'El cantar de la Pachamama',
         'location': 'Localidad de El Soberbio, provincia de Misiones',
         'category':'Camping Premium',
         'description':'',
         'image':'Pachamama.jpeg',
         'availability': 'Marzo-Diciembre 2023'
         },
         
 
    ]

    context = {                
                'campsites': campsites_list
            }
    return render(request,'publica/index.html',context)

def login(request):
    
    return render(request,'publica/login.html')

def contacto(request):
    if request.method == 'POST':
        contactForm = ContactForm(request.POST)
        if contactForm.is_valid():
            return HttpResponseRedirect('/contacto/')
    else:
        contactForm = ContactForm()
    return render(request, 'publica/contacto.html', {'form':contactForm})
        
    
    
