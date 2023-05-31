
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import NaturalPark, Category, Campsite, Availability, Profile, Reservation
from .forms import CampsiteFilterForm, NaturalParkForm, NaturalParkFilterForm, NaturalParkFilterForm, CategoryForm, CampsiteForm, AvailabilityForm, AvailabilityCampsiteFilterForm, ProfileFilterForm, ProfileForm, ReservationForm
from django.db.models import Min, Avg
from datetime import timedelta
import uuid

def index_admin(request):
    return render(request, 'administracion/index_master.html')


""" def listar_clientes(request):
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
    return render(request, 'administracion/clientes/listar_clientes.html', context)
 """

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
        
class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'administracion/reservas/reservation_create.html'
    success_url = reverse_lazy('reservation_list')

    def form_valid(self, form):
        campsite = form.cleaned_data.get('campsite')
        number_guests = form.cleaned_data.get('number_guests')
        check_in = form.cleaned_data.get('check_in')
        check_out = form.cleaned_data.get('check_out')

        if campsite and number_guests:
            capacity = campsite.categories.aggregate(min_capacity=Min('capacity'))['min_capacity']
            if capacity:
                total_cost = (number_guests / capacity) * campsite.categories.aggregate(avg_price=Avg('price'))['avg_price'] * (check_out - check_in).days
                form.instance.total_cost = total_cost

        availability = Availability.objects.get(campsite=form.cleaned_data['campsite'])
        form.instance.availability = availability

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
                total_cost = (number_guests / capacity) * campsite.categories.aggregate(avg_price=Avg('price'))['avg_price'] * (check_out - check_in).days
                reservation.total_cost = total_cost
        
        if reservation.code == 0:
            reservation.code = uuid.uuid4().hex[:8].upper()  # Generar un código aleatorio
            
        
        return super().form_valid(form)


class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'administracion/reservas/reservation_delete.html'
    success_url = reverse_lazy('reservation_list')

