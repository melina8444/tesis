from django.shortcuts import render
from django.http import HttpResponse

from django.http import HttpResponseRedirect
from publica.forms import ContactForm
from django.contrib import messages


import publica

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
         'category':'Camping Premium',
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
         'image':'Caranday.jpeg',
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


def index(request):
    
    context = {                
                'campsites': campsites_list
            }
    return render(request,'publica/index.html',context)

def campsites_by_category(request, category):
    campsites = [campsite for campsite in campsites_list if campsite['category'] == category]
    context = {'campsites': campsites}
    return render(request, 'publica/campsites_by_category.html', context)

def login(request):
    
    return render(request,'publica/login.html')

def contacto(request):
    if request.method == 'POST':
        contactForm = ContactForm(request.POST)
        # contactForm.save(); #Para guardar en la base de datos
        if contactForm.is_valid():
            messages.success(request,'Hemos recibido tus datos')
            return HttpResponseRedirect('/contacto/')
        else:
            messages.warning(request,'Por favor revisa los errores en el formulario')
    else:
        contactForm = ContactForm()
    return render(request, 'publica/contacto.html', {'contactform':contactForm})
        
def aboutus(request):
    developers_list = [
        {'name': 'Melina',
         'role': 'Desarrolladora',
         'image': 'melina.jpg',
         'socialnetinst':'#',
         'socialnetwa':'#',
         },
          {'name': 'Santiago',
         'role': 'Desarrollador',
         'image': 'santi.jpg',
         'socialnetinst':'#',
         'socialnetwa':'#',
         },
          {'name': 'Nicolás',
         'role': 'Desarrollador',
         'image': 'nico.jpg',
         'socialnetinst':'#',
         'socialnetwa':'#',
         },
          {'name': 'Cecilia',
         'role': 'Desarrolladora',
         'image': 'ceci.jpeg',
         'socialnetinst':'#',
         'socialnetwa':'#',
         
         },
         ]
    
    context = {                
                'developers': developers_list
            }
    return render(request,'publica/aboutus.html', context)
    
