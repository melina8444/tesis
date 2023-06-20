from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from publica.forms import ContactForm, UsuarioCreationForm, LoginForm
from django.contrib import messages
from administracion.models import Availability, Campsite, NaturalPark, Reservation, Category, Guest
from administracion.forms import ReservationForm, GuestForm
from django.views.generic import CreateView, TemplateView, DetailView
from django.db.models import Min, Sum
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def index(request):
    naturalparks = NaturalPark.objects.all()
    is_staff = request.user.is_staff
    return render(request, 'publica/index.html', {'naturalparks': naturalparks, 'is_staff': is_staff})

def campsites_by_naturalpark(request, naturalpark_id):
    naturalpark = NaturalPark.objects.get(pk=naturalpark_id)
    campsites = naturalpark.campsites.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        campsites = campsites.filter(
            availabilities__start_date__lte=start_date,
            availabilities__end_date__gte=end_date
        )

    return render(request, 'publica/campsites_by_naturalpark.html', {'naturalpark': naturalpark, 'campsites': campsites})

def contact(request):
    if request.method == 'POST':
        contactForm = ContactForm(request.POST)
        if contactForm.is_valid():
            messages.success(request, 'Hemos recibido tus datos')

            # Obtener los datos del formulario
            nombre = contactForm.cleaned_data['nombre']
            email = contactForm.cleaned_data['email']
            comentario = contactForm.cleaned_data['comentario']

            # enviar el correo electrónico utilizando send_mail()
            subject = 'Nuevo mensaje de contacto'
            message = f'Nombre: {nombre}\nEmail: {email}\nMensaje: {comentario}'
            from_email = settings.EMAIL_HOST_USER
            recipient_email = 'chikhakituti@gmail.com'

            send_mail(subject, message, from_email, [recipient_email])
           
            return render(request, 'publica/contact.html', {'contactform': contactForm})
        else:
            messages.warning(request, 'Por favor revisa los errores en el formulario')
    else:
        contactForm = ContactForm()
    return render(request, 'publica/contact.html', {'contactform': contactForm})
        
def aboutus(request):
    developers_list = [
        {'name': 'Melina',
         'role': 'Desarrolladora',
         'image': 'melina.jpg',
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
    
def success_view(request):
    try:
        reservation = Reservation.objects.latest('id')
    except Reservation.DoesNotExist:
        # Si no se encuentra la reserva, redirigir a página de error
        return redirect(reverse('error_page'))

    if request.method == 'POST':
        GuestFormSet = formset_factory(GuestForm, extra=reservation.number_guests)
        formset = GuestFormSet(request.POST)

        if formset.is_valid():
            # Eliminar los huéspedes existentes marcados como guardados
            Guest.objects.filter(reservation=reservation, is_saved=True).delete()

            # Crear los nuevos huéspedes y marcarlos como guardados
            for form in formset:
                guest = form.save(commit=False)
                guest.reservation = reservation
                guest.is_saved = True  # Marcar el huésped como guardado
                guest.save()

            # Actualizar el campo is_client en el perfil del usuario
            profile = request.user.profile
            profile.is_client = True
            profile.save()

            # Realizar la redirección
            return redirect(reverse('reserva_info', args=[reservation.id]))
        else:
            messages.error(request, "Ha ocurrido un error. Por favor, revisa los datos ingresados.")
    else:
        # Verificar si existen huéspedes marcados como guardados y eliminarlos
        Guest.objects.filter(reservation=reservation, is_saved=True).delete()

        GuestFormSet = formset_factory(GuestForm, extra=reservation.number_guests)
        formset = GuestFormSet()

    return render(request, 'publica/success.html', {
        'reservation': reservation,
        'formset': formset
    })

class ReservaDetailView(DetailView):
    model = Reservation
    template_name = 'publica/reserva_info.html'
    context_object_name = 'reservation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation = self.get_object()
        guests = reservation.guest_set.all()

        total_cost = reservation.total_cost
        twenty_percent = total_cost * 0.2
        context['twenty_percent'] = twenty_percent

        # Enviar correo electrónico al usuario con los datos de la reserva y los invitados
        try:

            recipient_email = reservation.user.email
            subject = 'Datos de tu Reserva'
            context['reservation'] = reservation
            context['guests'] = guests
            context['twenty_percent'] = twenty_percent
            html_message = render_to_string('publica/reserva_mail.html', context)
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, plain_message, from_email, [recipient_email], html_message=html_message)
           
        except:
            messages.error(self.request, "Error al enviar el correo electrónico. Por favor, inténtalo nuevamente.")
        
        return context

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'publica/login.html'
    success_url = reverse_lazy('Inicio') 

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

def error_page(request):

    return render(request, 'publica/error_page.html')
        