from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from publica.forms import ContactForm, UsuarioCreationForm, LoginForm
from django.contrib import messages
from administracion.models import Availability, Campsite, NaturalPark, Reservation, Category
from administracion.forms import ReservationForm
from django.views.generic import CreateView, TemplateView
from django.db.models import Min, Sum

import publica


def index(request):
    
    naturalparks = NaturalPark.objects.all()
    return render(request, 'publica/index.html', {'naturalparks': naturalparks})

def campsites_by_naturalpark(request, naturalpark_id):
    naturalpark = NaturalPark.objects.get(pk=naturalpark_id)
    campsites = naturalpark.campsites.all()
    return render(request, 'publica/campsites_by_naturalpark.html', {'naturalpark': naturalpark, 'campsites': campsites})

""" def login(request):
    
    return render(request,'publica/login.html') """

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
    
class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    template_name = 'publica/reserva.html'
    form_class = ReservationForm
    success_url = reverse_lazy('success')

    def get_initial(self):
        initial = super().get_initial()
        campsite_id = self.kwargs.get('campsite_id')
        campsite = get_object_or_404(Campsite, id=campsite_id)
        initial['campsite'] = campsite
        return initial
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.is_authenticated:
            form.fields['user'].initial = self.request.user
        return form
    
    def form_valid(self, form):

        campsite = form.cleaned_data.get('campsite')
        number_guests = form.cleaned_data.get('number_guests')
        check_in = form.cleaned_data.get('check_in')
        check_out = form.cleaned_data.get('check_out')

        if campsite and number_guests:
            capacity = campsite.categories.aggregate(min_capacity=Min('capacity'))['min_capacity']
            if capacity:
                total_cost = (number_guests / capacity) * campsite.categories.aggregate(sum_price=Sum('price'))['sum_price'] * (check_out - check_in).days
                form.instance.total_cost = total_cost

        availability = Availability.objects.get(campsite=form.cleaned_data['campsite'])
        form.instance.availability = availability


        return super().form_valid(form)
        
    
class SuccessView(TemplateView):
    template_name = 'publica/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén la reserva guardada
        reservation = Reservation.objects.latest('id')
        context['reservation'] = reservation
        return context


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'publica/login.html'
    success_url = reverse_lazy('Inicio') 

    def form_valid(self, form):
        user = form.get_user()

        if user.is_authenticated:
            if user.is_staff:
                return redirect('inicio_admin')
            else:
                return super().form_valid(form)
            
        return super().form_valid(form)

class RegistroUsuarioView(CreateView):
    form_class = UsuarioCreationForm
    template_name = 'publica/register.html'
    success_url = reverse_lazy('loginrn')  
    
class CustomLogoutView(LogoutView):
    next_page = 'Inicio'  # URL a la que redirigir después de cerrar sesión

class VerificacionRegView(TemplateView):
    template_name = 'publica/register_verification.html'

    def get(self, request, *args, **kwargs):
        next_url = request.GET.get('next')
        campsite_id = request.GET.get('campsite_id')

        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            # Si está autenticado, redirigir directamente a la página de reserva
            if next_url:
                return redirect(next_url)
            elif campsite_id:
                return redirect('reservation_campsite', campsite_id=campsite_id)

        return super().get(request, *args, **kwargs)


def categories(request):
    
    categories = Category.objects.all()
    return render(request, 'publica/categories.html', {'categories': categories})


        