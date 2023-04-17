from django.shortcuts import render
from django.http import HttpResponse



def index_admin(request):
    return render(request, 'administracion/index_master.html')


def listar_clientes(request):
    clientes = [
        {'nombre': 'Melina',
         'apellido': 'Yangüez',
         'email':'mel@gmail.com',
         'telefono': '114564568',
         'f_nac':'27/02/1980',
         'dni': '26776232',
         },

         {'nombre': 'Cecilia',
         'apellido': 'Santillan',
         'email':'ceci@gmail.com',
         'telefono': '11245689',
         'f_nac':'02/08/1988',
         'dni':'',
         },
    ]
    context = {                
                'clientes': clientes,
                'title': "Admnistracion Reservas Naturales Privadas",
            }
    return render(request, 'clientes/listar.html', context)


