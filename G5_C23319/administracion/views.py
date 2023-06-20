
import calendar
from django.shortcuts import render, redirect
from datetime import date, datetime
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import NaturalPark, Category, Campsite, Availability, Profile, Reservation, Guest
from .forms import CampsiteFilterForm, NaturalParkForm, NaturalParkFilterForm, NaturalParkFilterForm, CategoryForm, CampsiteForm, AvailabilityForm, AvailabilityCampsiteFilterForm, ProfileFilterForm, ProfileForm, ReservationForm, GuestForm, GuestFilterForm
from django.db.models import Min, Sum, Q, OuterRef, Subquery
import uuid
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required(login_url='access_denied')  # Requiere que el usuario sea miembro del staff
@login_required(login_url='loginrn')  # Requiere que el usuario esté autenticado
def index_admin(request):
    if not request.user.is_staff:
        # Si el usuario no es miembro del staff, redirigir a una página de acceso denegado o mostrar un mensaje de error.
        return redirect('access_denied')
   
    today = date.today()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    num_naturalparks = NaturalPark.objects.count()
    num_clients = Profile.objects.filter(is_client=True).count()
    num_reservations = Reservation.objects.count()
    reservations_today = Reservation.objects.filter(reservation_date__range=(start_of_day, end_of_day))
    total_cost_today = reservations_today.aggregate(total_cost_today=Sum('total_cost'))['total_cost_today']

    #reservations_today = Reservation.objects.filter(reservation_date__range=(start_of_day, end_of_day))
    mes = request.GET.get('mes')

    if mes:
        mes = int(mes)
        year = datetime.now().year
        start_date = date(year, mes, 1)
        end_date = date(year, mes, calendar.monthrange(year, mes)[1])

        # Obtener el total de huéspedes de las reservas para el mes seleccionado
        total_guests_month = Reservation.objects.filter(
            Q(check_in__month=mes, check_in__year=year) | Q(check_out__month=mes, check_out__year=year)
        ).aggregate(total_guests_month=Sum('number_guests'))['total_guests_month']

        # Obtener la suma de number_guests por campsite y mes
        reservations_capacity = Reservation.objects.filter(
            Q(check_in__month=mes, check_in__year=year) | Q(check_out__month=mes, check_out__year=year)
        ).values('campsite').annotate(total_guests=Sum('number_guests')).values('campsite', 'total_guests')

        # Obtener la capacidad máxima por campsite y mes
        availabilities_capacity = Availability.objects.filter(
            start_date__gte=start_date, end_date__lte=end_date
        ).values('campsite').annotate(total_capacity=Sum('max_capacity')).values('campsite', 'total_capacity')

        campsites_occupancy = Campsite.objects.annotate(
            total_guests=Subquery(
                reservations_capacity.filter(campsite=OuterRef('pk')).values('total_guests')[:1]
            ),
            total_capacity=Subquery(
                availabilities_capacity.filter(campsite=OuterRef('pk')).values('total_capacity')[:1]
            ),
        ).values('name', 'total_guests', 'total_capacity')

        # Calcular la capacidad total para ese mes
        total_capacity = sum(campsite['total_capacity'] or 0 for campsite in campsites_occupancy)

        # Calcular el porcentaje de ocupación
        for campsite in campsites_occupancy:
            total_guests = campsite['total_guests']
            total_capacity = campsite['total_capacity']

            if total_capacity:
                occupancy_percentage = (total_guests / total_capacity) * 100
            else:
                occupancy_percentage = 0

            campsite['occupancy_percentage'] = occupancy_percentage

        context = {
            'num_naturalparks': num_naturalparks,
            'num_clients': num_clients,
            'num_reservations': num_reservations,
            'reservations_today': reservations_today,
            'total_capacity': total_capacity,
            'mes': mes,
            'campsites_occupancy': campsites_occupancy,
            'total_guests_month': total_guests_month,
            'total_cost_today': total_cost_today,
        }
    else:
        context = {
            'num_naturalparks': num_naturalparks,
            'num_clients': num_clients,
            'num_reservations': num_reservations,
            'reservations_today': reservations_today,
            'total_cost_today': total_cost_today,
        }

    return render(request, 'administracion/index_master.html', context)
"""     # Obtener la fecha actual
    today = date.today()

    # Definir el rango de fechas desde el inicio hasta el final del día
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())


    num_naturalparks = NaturalPark.objects.count()
    num_clients = Profile.objects.filter(is_client=True).count()
    num_reservations = Reservation.objects.count()

    # Obtener las reservas del día
    reservations_today = Reservation.objects.filter(reservation_date__range=(start_of_day, end_of_day))

    context = {
        'num_naturalparks': num_naturalparks,
        'num_clients': num_clients,
        'num_reservations': num_reservations,
        'reservations_today': reservations_today,
    }

    return render(request, 'administracion/index_master.html', context) """

def access_denied(request):

    return render(request, 'administracion/access_denied.html')

class NaturalParkListView(ListView):
    model = NaturalPark
    template_name = 'administracion/parques_naturales/naturalpark_list.html'
    context_object_name = 'naturalparks'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = NaturalParkFilterForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

class NaturalParkCreateView(CreateView):
    model = NaturalPark
    form_class = NaturalParkForm
    template_name = 'administracion/parques_naturales/naturalpark_create.html'
    success_url = reverse_lazy('naturalpark_list')

class NaturalParkUpdateView(UpdateView):
    model = NaturalPark
    form_class = NaturalParkForm
    template_name = 'administracion/parques_naturales/naturalpark_update.html'
    success_url = reverse_lazy('naturalpark_list')

class NaturalParkDeleteView(DeleteView):
    model = NaturalPark
    template_name = 'administracion/parques_naturales/naturalpark_delete.html'
    success_url = reverse_lazy('naturalpark_list')

class CategoryListView(ListView):
    model = Category
    template_name = 'administracion/categorias/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'administracion/categorias/category_create.html'
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'administracion/categorias/category_update.html'
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'administracion/categorias/category_delete.html'
    success_url = reverse_lazy('category_list')

class CampsiteListView(ListView):
    model = Campsite
    template_name = 'administracion/campings/campsite_list.html'
    context_object_name = 'campsites'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = CampsiteFilterForm(self.request.GET)
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

class CampsiteCreateView(CreateView):
    model = Campsite
    form_class = CampsiteForm
    template_name = 'administracion/campings/campsite_create.html'
    success_url = reverse_lazy('campsite_list')

class CampsiteUpdateView(UpdateView):
    model = Campsite
    form_class = CampsiteForm
    template_name = 'administracion/campings/campsite_update.html'
    success_url = reverse_lazy('campsite_list')

class CampsiteDeleteView(DeleteView):
    model = Campsite
    template_name = 'administracion/campings/campsite_delete.html'
    success_url = reverse_lazy('campsite_list')

class AvailabilityListView(ListView):
    model = Availability
    template_name = 'administracion/disponibilidades/availability_list.html'
    context_object_name = 'availabilities'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = AvailabilityCampsiteFilterForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        campsite_name = self.request.GET.get('campsite_name')
        if campsite_name:
            queryset = queryset.filter(campsite__name__icontains=campsite_name)
        return queryset

class AvailabilityCreateView(CreateView):
    model = Availability
    form_class = AvailabilityForm
    template_name = 'administracion/disponibilidades/availability_create.html'
    success_url = reverse_lazy('availability_list')

class AvailabilityUpdateView(UpdateView):
    model = Availability
    form_class = AvailabilityForm
    template_name = 'administracion/disponibilidades/availability_update.html'
    success_url = reverse_lazy('availability_list')

class AvailabilityDeleteView(DeleteView):
    model = Availability
    template_name = 'administracion/disponibilidades/availability_delete.html'
    success_url = reverse_lazy('availability_list')

class ProfileListView(ListView):
    model = Profile
    template_name = 'administracion/clientes/profile_list.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ProfileFilterForm(self.request.GET)
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.GET.get('user')
        is_client = self.request.GET.get('is_client')

        if user:
            queryset = queryset.filter(user__username__icontains=user)
        if is_client:
            queryset = queryset.filter(is_client=True)

        return queryset
    
class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'administracion/clientes/profile_create.html'
    success_url = reverse_lazy('profile_list')

class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'administracion/clientes/profile_update.html'
    success_url = reverse_lazy('profile_list')

class ProfileDeleteView(DeleteView):
    model = Profile
    template_name = 'administracion/clientes/profile_delete.html'
    success_url = reverse_lazy('profile_list')

class ReservationListView(ListView):
    model = Reservation
    template_name = 'administracion/reservas/reservation_list.html'
    context_object_name = 'reservations'
        
class ReservationCreateView(SuccessMessageMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'administracion/reservas/reservation_create.html'
    success_url = reverse_lazy('reservation_list')
    success_message_popup = "La reserva se registró con éxito"
    
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

        messages.success(self.request, self.success_message_popup)

        return super().form_valid(form)
    
class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'administracion/reservas/reservation_update.html'
    success_url = reverse_lazy('reservation_list')

    def form_valid(self, form):
        reservation = form.save(commit=False)
        
        campsite = reservation.campsite
        number_guests = reservation.number_guests
        check_in = reservation.check_in
        check_out = reservation.check_out
        
        if campsite and number_guests:
            capacity = campsite.categories.aggregate(min_capacity=Min('capacity'))['min_capacity']
            if capacity:
                total_cost = (number_guests / capacity) * campsite.categories.aggregate(sum_price=Sum('price'))['sum_price'] * (check_out - check_in).days
                reservation.total_cost = total_cost
        
        if reservation.code == 0:
            reservation.code = uuid.uuid4().hex[:8].upper()  # Generar un código aleatorio
      
        return super().form_valid(form)

        """ response = super().form_valid(form)

        # Obtener el usuario registrado en la reserva
        user = form.cleaned_data['user']

        # Obtener la URL del sitio actual
        current_site = get_current_site(self.request)

        # Generar el contenido del correo electrónico
        subject = 'Confirmación de reserva modificada'
        message = render_to_string('administracion/reservas/reservation_update_confirmation.html', {
            'user': user,
            'reservation': reservation,
            'site': current_site,
        })
        from_email = 'noreply@example.com'
        to_email = user.email

        # Enviar el correo electrónico
        send_mail(subject, message, from_email, [to_email])

        return response
 """
class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'administracion/reservas/reservation_delete.html'
    success_url = reverse_lazy('reservation_list')
    

class GuestListView(ListView):
    model = Guest
    template_name = 'administracion/huespedes/guest_list.html'
    context_object_name = 'guests'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = GuestFilterForm(self.request.GET)
        
        reservation = self.request.GET.get('reservation')
        if reservation:
            queryset = self.get_queryset()
            if not queryset:
                messages.info(self.request, "No hay reservas con ese código.")
                
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        reservation = self.request.GET.get('reservation')
        if reservation:
            queryset = queryset.filter(reservation__code=reservation)
        return queryset

class GuestCreateView(CreateView):
    model = Guest
    form_class = GuestForm
    template_name = 'administracion/huespedes/guest_create.html'
    success_url = reverse_lazy('guest_list')

class GuestUpdateView(UpdateView):
    model = Guest
    form_class = GuestForm
    template_name = 'administracion/huespedes/guest_update.html'
    success_url = reverse_lazy('guest_list')

class GuestDeleteView(DeleteView):
    model = Guest
    template_name = 'administracion/huespedes/guest_delete.html'
    success_url = reverse_lazy('guest_list')