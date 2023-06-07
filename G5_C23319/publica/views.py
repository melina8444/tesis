from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.http import HttpResponseRedirect
from publica.forms import ContactForm, ReservaForm
from django.contrib import messages


from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView


import publica

campsites_list = [
        {'id': 1,
         'name': 'Abracal',
         'location': 'Camino del Aire km 7 - San Javier',
         'province': 'Cordoba',
         'category':'Camping Premium',
         'description':'Conservación, educación ambiental, observación de fauna silvestre, turismo',
         'image': 'Abracaral.jpeg',
         'availability': 'Enero-Marzo 2023'
         },
         {'id': 2,
         'name': 'Achalay',
         'location': 'Primera sección de islas del Delta, Tigre',
         'province': 'Buenos Aires',
         'category':'Camping Premium',
         'description':'Conservación, educación ambiental, turismo, investigación, observación de fauna silvestre',
         'image': 'Achalay.jpeg',
         'availability': 'Marzo-Diciembre 2023'
         },
         {'id': 3,
         'name': 'Curindy',
         'location': 'Margen del Rio 1, Localidad de Garuhapé',
         'province': 'Misiones',
         'category':'Camping Premium',
         'description':'Conservación, explotación forestal, ganadería, investigación y turismo',
         'image':'Curindy.jpeg',
         'availability': 'Octubre-Diciembre 2023'
         },
         {'id': 4,
         'name': 'Cachape',
         'location': 'Calle del árbol con espinas km 5, Localidad de General José de San Martín',
         'province': 'Chaco',
         'category':'Camping Básico',
         'description':'Conservación compatible con turismo y producción',
         'image':'Cachape.jpeg',
         'availability': 'Junio-Noviembre 2023'
         },
         {'id': 5,
         'name': 'Caranday',
         'location': 'Palmeras y Aguaribay s/n, Villaguay',
         'province': 'Entre Ríos',
         'category':'Camping Aventurero',
         'description':'Conservación compatible con Turismo y Producción',
         'image':'Caranday.jpeg',
         'availability': 'Octubre-Diciembre 2023'
         },
         {'id': 5,
         'name': 'Caspinchango',
         'location': 'Cerro alto km 3, Localidad de Famaillá',
         'province': 'Tucumán',
         'category':'Camping Premium',
         'description':'Conservación, educación ambiental, producción e investigación científica',
         'image':'Caspinchango.jpeg',
         'availability': 'Marzo-Diciembre 2023'
         },
         {'id': 6,
         'name': 'Cerro Champaquí',
         'location': 'Paraje Los Molles, Villa de las Rosas',
         'province': 'Cordoba',
         'category':'Camping Aventurero',
         'description':'Conservación compatible con turismo y producción',
         'image':'Cerro-Champaqui.jpeg',
         'availability': 'Marzo-Diciembre 2023'
         },
         {'id': 7,
         'name': 'El cantar de la Pachamama',
         'location': 'Cascada 4, Localidad de El Soberbio',
         'province': 'Misiones',
         'category':'Camping Premium',
         'description':'Conservación compatible con turismo y educación',
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

def contact(request):
    if request.method == 'POST':
        contactForm = ContactForm(request.POST)
        # contactForm.save(); #Para guardar en la base de datos
        if contactForm.is_valid():
            messages.success(request,'Hemos recibido tus datos')
            return HttpResponseRedirect('/contact/')
        else:
            messages.warning(request,'Por favor revisa los errores en el formulario')
    else:
        contactForm = ContactForm()
    return render(request, 'publica/contact.html', {'contactform':contactForm})
        
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
    
def reserva(request):

    if request.method == 'POST':
        reservaForm = ReservaForm(request.POST, campsites_list)
        # reservaForm.save(); #Para guardar en la base de datos
        if reservaForm.is_valid():
            messages.success(request,'Hemos recibido tus datos')
            return HttpResponseRedirect('/reserva/')
        else:
          
            messages.warning(request,'Por favor revisa los errores en el formulario')
    else:
        reservaForm = ReservaForm()
    return render(request, 'publica/reserva.html', {'reservaform':reservaForm})

def reserva_camp_id(request, campsite_id):
  
    if request.method == 'POST':
        reservaForm = ReservaForm(request.POST)
        # reservaForm.save(); #Para guardar en la base de datos

        if reservaForm.is_valid():
            messages.success(request,'Hemos recibido tus datos')
            return HttpResponseRedirect('/reserva/<int:campsite_id>/')
        else:
            messages.warning(request,'Por favor revisa los errores en el formulario')
    else:
        reservaForm = ReservaForm()
    return render(request, 'publica/reserva_camp_id.html', {'reservaform':reservaForm, 'campsite_id':campsite_id})


def login_view(request):
    if request.method == 'POST':
        # AuthenticationForm_can_also_be_used__
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            nxt = request.GET.get("next", None)
            if nxt is None:
                return redirect('inicio_admin')
            else:
                return redirect(nxt)
        else:
            messages.error(request, f'Cuenta o password incorrecto, realice el login correctamente')
    form = AuthenticationForm()
    return render(request, 'publica/login.html', {'form': form, 'title': 'Log in'})
