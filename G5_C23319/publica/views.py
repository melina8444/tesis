from django.shortcuts import render
from django.http import HttpResponse


import publica

def index(request):
    campsites_list = [
        {'name': 'Abracal',
         'location': 'San Javier - Córdoba',
         'category':'Camping',
         'services':'Conservación, educación ambiental, observación de fauna silvestre, turismo',
         'image': 'publica/pimg/abracal.jpeg',
         },
          {'name': '',
         'location': '',
         'category':'',
         'service':'',
         'cimg':'',
         },
          {'name': '',
         'location': '',
         'category':'',
         'service':'',
         'cimg':'',
         },


    ]





    context = {                
                'campsites': campsites_list,
                'title': "Reservas Naturales Privadas",
            }
    return render(request,'publica/index.html',context)

