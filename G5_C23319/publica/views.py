from django.shortcuts import render
from django.http import HttpResponse


import publica

def index(request):
    campsites_list = [
        {'name': 'Abracal',
         'location': 'San Javier - Córdoba',
         'category':'Camping',
         'services':'Conservación, educación ambiental, observación de fauna silvestre, turismo',
         'image': 'abracal.jpeg',
         },
          {'name': 'Achalay',
         'location': 'Primera sección de islas del Delta, Tigre, Provincia de Buenos Aires',
         'category':'Camping',
         'service':'Conservación, educación ambiental, turismo, investigación, observación de fauna silvestre',
         'image': 'achalay.jpeg',
         },
          {'name': 'Curindy',
         'location': 'Localidad de Garuhapé, provincia de Misiones',
         'category':'Camping',
         'service':'Conservación, explotación forestal, ganadería, investigación y turismo',
         'image':'curindy.jpeg',
         },
 
    ]

    context = {                
                'campsites': campsites_list,
                'title': "Reservas Naturales Privadas",
            }
    return render(request,'publica/index.html',context)

