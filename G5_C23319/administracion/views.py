from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect


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
         'dni': '36565789',
         },
    ]
    context = {
                'clientes': clientes,
                'title': "Reservas Naturales Privadas",
            }
    return render(request, 'administracion/listar_clientes.html', context)
