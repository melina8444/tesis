from django.shortcuts import render
from django.http import HttpResponse

from django.http import HttpResponseRedirect
from publica.forms import ContactForm, ReservaForm
from django.contrib import messages
from administracion.models import NaturalPark

import publica


def index(request):
    
    naturalparks = NaturalPark.objects.all()
    return render(request, 'publica/index.html', {'naturalparks': naturalparks})

def campsites_by_naturalpark(request, naturalpark_id):
    naturalpark = NaturalPark.objects.get(pk=naturalpark_id)
    campsites = naturalpark.campsites.all()
    return render(request, 'publica/campsites_by_naturalpark.html', {'naturalpark': naturalpark, 'campsites': campsites})

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
    
""" def reserva(request):

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
    return render(request, 'publica/reserva_camp_id.html', {'reservaform':reservaForm, 'campsite_id':campsite_id}) """