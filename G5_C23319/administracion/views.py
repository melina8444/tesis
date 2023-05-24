from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ClienteForm
from django.contrib import messages



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



def crear_cliente(request):
    form = ClienteForm()
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Cliente creado con éxito')
            form.save()
            return redirect('/listar/')
        else:
            messages.error(request, 'Por favor revisar datos en el formulario')

    ctx = {
        'form':form
    }

    return render(request, 'clientes/crear_cliente.html', ctx ) 

def modificar_cliente(request, id):
    cliente = ClienteForm.objects.get(id=id)
    form = ClienteForm(instance=cliente)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('/listar/')

    ctx = {
        'form':form
    }

    return render(request, 'clientes/modificar_cliente.html', ctx )