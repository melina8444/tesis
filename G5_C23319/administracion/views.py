
import calendar
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from datetime import date, datetime, timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import NaturalPark, Category, Campsite, Availability, Profile, Reservation, Guest, Season
from .forms import CampsiteFilterForm, NaturalParkForm, NaturalParkFilterForm, NaturalParkFilterForm, CategoryForm, CampsiteForm, AvailabilityForm, AvailabilityCampsiteFilterForm, ProfileFilterForm, ProfileForm, ReservationCampsiteFilterForm, ReservationForm, GuestForm, GuestFilterForm, SeasonForm
from django.db.models import Min, Sum, Q, OuterRef, Subquery
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal
import uuid
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from openpyxl import Workbook
from django.http import HttpResponse
from collections import defaultdict
from django.db.models import Count, Case, When, IntegerField
from django.db.models import Min, Max
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from django.db.models.functions import ExtractMonth, ExtractYear
import json
from django.db.models.functions import TruncMonth
from django.db.models import Sum,F, FloatField, DecimalField, ExpressionWrapper
from django.http import JsonResponse


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


        if not campsites_occupancy:
            campsites_occupancy = None

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

class SeasonListView(ListView):
    model = Season
    template_name = 'administracion/temporadas/season_list.html'
    context_object_name = 'seasons'

class SeasonCreateView(CreateView):
    model = Season
    form_class = SeasonForm
    template_name = 'administracion/temporadas/season_create.html'
    
    success_url = reverse_lazy('season_list')

class SeasonUpdateView(UpdateView):
    model = Season
    form_class = SeasonForm
    template_name = 'administracion/temporadas/season_update.html'
    success_url = reverse_lazy('season_list')
    
class SeasonDeleteView(DeleteView):
    model = Season
    template_name = 'administracion/temporadas/season_delete.html'
    success_url = reverse_lazy('season_list')

class ReservationListView(ListView):
    model = Reservation
    template_name = 'administracion/reservas/reservation_list.html'
    context_object_name = 'reservations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ReservationCampsiteFilterForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        campsite_name = self.request.GET.get('campsite_name')
        if campsite_name:
            queryset = queryset.filter(campsite__name__icontains=campsite_name)
        return Reservation.objects.filter(baja=False)
 
""" class ReservationCreateView(SuccessMessageMixin, CreateView):
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

class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'administracion/reservas/reservation_delete.html'
    success_url = reverse_lazy('reservation_list')
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = get_object_or_404(Reservation, pk=pk)
        return obj
    
    #se puede sobreescribir el metodo delete por defecto de la VBC, para que no se realice una baja fisica
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()  # Llamada al método soft_delete() del modelo
        return HttpResponseRedirect(self.get_success_url())

 """

# RESERVAS NUEVO
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
    
    def calculate_season_multiplier(self, check_in, check_out):
        season_now = Season.objects.filter(fecha_inicio_lte=check_in, fecha_fin_gte=check_out).first()
        
        if season_now:
            return Decimal(season_now.porcentaje)  # Utiliza el campo 'porcentaje' de la temporada
        
        return Decimal('1.0')

    def form_valid(self, form):
        campsite = form.cleaned_data.get('campsite')
        number_guests = form.cleaned_data.get('number_guests')
        check_in = form.cleaned_data.get('check_in')
        check_out = form.cleaned_data.get('check_out')

        if campsite and number_guests:
            capacity = campsite.categories.aggregate(min_capacity=Min('capacity'))['min_capacity']
            if capacity:
                multiplier = self.calculate_season_multiplier(check_in, check_out)  # Obtiene el multiplicador de temporada
                total_cost = (number_guests / capacity) * campsite.categories.aggregate(sum_price=Sum('price'))['sum_price'] * (check_out - check_in).days * multiplier
                form.instance.total_cost = total_cost

        availability = Availability.objects.get(campsite=form.cleaned_data['campsite'])
        form.instance.availability = availability

        return super().form_valid(form)
    
    # pdf reservas
    def create_pdf(self, reservation):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reservation_{reservation.code}.pdf"'

        # Crear el objeto PDF
        p = canvas.Canvas(response, pagesize=letter)

        # Agregar contenido al PDF
        p.drawString(100, 750, 'Reserva de Camping')
        p.drawString(100, 730, '----------------------------------')

        # Aquí puedes agregar más detalles de la reserva como la fecha, campsite, etc.
        p.drawString(100, 710, f'Código de Reserva: {reservation.code}')
        p.drawString(100, 690, f'Fecha de Check-In: {reservation.check_in}')
        p.drawString(100, 670, f'Fecha de Check-Out: {reservation.check_out}')
        p.drawString(100, 650, f'Número de Invitados: {reservation.number_guests}')

        # Agregar información del usuario
        p.drawString(100, 630, 'Información del Usuario:')
        p.drawString(100, 610, f'Nombre de Usuario: {reservation.user.username}')
        p.drawString(100, 590, f'Nombre: {reservation.user.first_name} {reservation.user.last_name}')
        p.drawString(100, 570, f'DNI: {reservation.user.profile.dni}')
        p.drawString(100, 550, f'Teléfono: {reservation.user.profile.phone}')
        p.drawString(100, 530, f'Dirección: {reservation.user.profile.address}')

        # Cerrar el objeto PDF y devolver la respuesta
        p.showPage()
        p.save()
        return response

    def form_valid(self, form):
        # ... (código existente)

        # Llamar a la función para crear el PDF y adjuntarlo a la respuesta
        pdf_response = self.create_pdf(form.instance)

        # Renderizar la plantilla HTML con los datos de la reserva y la URL del PDF
        context = {
            'reservation': form.instance,
            'pdf_url': pdf_response.url,
        }
        return render(self.request, 'administracion/reservas/reservation_details.html', context)

""" 
def reservation_chart(request):
    reservations_by_month = Reservation.objects.filter(status='Abonada').annotate(
        month=ExtractMonth('reservation_date')
    ).values('month').annotate(
        total_cost=Sum('total_cost')
    ).order_by('month')
    
    return render(request, 'administracion/reservas/graficos3.html', {'reservations_by_month': reservations_by_month})
     """
"""     
def tu_vista(request):
    # Calcular la suma total de los importes de las reservas por mes
    monthly_data = Reservation.objects.annotate(
        month=TruncMonth('reservation_date')
    ).values('month').annotate(
        total_cost=Sum('total_cost')
    ).order_by('month')

    labels = [str(entry['month'].strftime('%B %Y')) for entry in monthly_data]
    data = [entry['total_cost'] for entry in monthly_data]

    context = {
        'labels': labels,
        'data': data,
    }

    return render(request, 'administracion/reservas/graficos3.html', context)
 """
""" def reservations_by_month(request):
    # Calcular el importe total de las reservas por mes
    data = (
        Reservation.objects
        .annotate(month=ExtractMonth('check_in'))
        .values('month')
        .annotate(total_cost=Sum('total_cost'))
        .order_by('month')
    )

    # Separar los datos en etiquetas (nombres de los meses) y valores (importe total)
    labels = [calendar.month_name[month['month']] for month in data]
    values = [month['total_cost'] for month in data]

    context = {
        'labels': labels,
        'data': values,
    }

    return render(request, 'administracion/reservas/graficos3.html', context)
 """
def reservations_by_month(request):
    # Calcular el importe total de las reservas por mes y año
    data = (
        Reservation.objects
        .filter(baja=False)  # Filtrar solo las reservas con baja=False
        .annotate(month=ExtractMonth('check_in'))
        .annotate(year=ExtractYear('check_in'))
        .values('year', 'month')
        .annotate(total_cost=Sum(F('total_cost'), output_field=FloatField()))
        .order_by('year', 'month')
    )

    # Crear etiquetas en el formato "Mes Año"
    labels = [f"{calendar.month_name[month['month']]} {month['year']}" for month in data]
    values = [month['total_cost'] for month in data]

    context = {
        'labels': labels,
        'data': values,
    }

    return render(request, 'administracion/reservas/graficos3.html', context)

class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    template_name = 'publica/reserva.html'
    form_class = ReservationForm
    success_url = reverse_lazy('success')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.is_authenticated:
            form.fields['user'].initial = self.request.user
        return form
    
    def calculate_season_multiplier(self, check_in, check_out):
        season_now = Season.objects.filter(fecha_inicio_lte=check_in, fecha_fin_gte=check_out).first()
        
        if season_now:
            return Decimal(season_now.porcentaje)  # Utiliza el campo 'porcentaje' de la temporada
        
        return Decimal('1.0')

    def form_valid(self, form):
        campsite = form.cleaned_data.get('campsite')
        number_guests = form.cleaned_data.get('number_guests')
        check_in = form.cleaned_data.get('check_in')
        check_out = form.cleaned_data.get('check_out')

        if campsite and number_guests:
            capacity = campsite.categories.aggregate(min_capacity=Min('capacity'))['min_capacity']
            if capacity:
                multiplier = self.calculate_season_multiplier(check_in, check_out)  # Obtiene el multiplicador de temporada
                total_cost = (number_guests / capacity) * campsite.categories.aggregate(sum_price=Sum('price'))['sum_price'] * (check_out - check_in).days * multiplier
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
                total_cost = (number_guests / capacity) * campsite.categories.aggregate(sum_price=Sum('price'))['sum_price'] * (check_out - check_in).days
                reservation.total_cost = total_cost
        
        if reservation.code == 0:
            reservation.code = uuid.uuid4().hex[:8].upper()  # Generar un código aleatorio
      
        return super().form_valid(form)

class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'administracion/reservas/reservation_delete.html'
    success_url = reverse_lazy('reservation_list')
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = get_object_or_404(Reservation, pk=pk)
        return obj
    
    #se puede sobreescribir el metodo delete por defecto de la VBC, para que no se realice una baja fisica
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()  # Llamada al método soft_delete() del modelo
        return HttpResponseRedirect(self.get_success_url())









class GuestListView(ListView):
    model = Guest
    template_name = 'administracion/huespedes/guest_list.html'
    context_object_name = 'guests'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = GuestFilterForm(self.request.GET)
        
        reservation_code = self.request.GET.get('reservation_code')
        if reservation_code:
            queryset = self.get_queryset()
            if not queryset:
                messages.info(self.request, "No hay reservas con ese código.")
                
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        reservation_code = self.request.GET.get('reservation_code')
        if reservation_code:
            queryset = queryset.filter(reservation__code=reservation_code)
        return queryset

""" class GuestCreateView(CreateView):
    model = Guest
    form_class = GuestForm
    template_name = 'administracion/huespedes/guest_create.html'
    success_url = reverse_lazy('guest_list') """

class GuestUpdateView(UpdateView):
    model = Guest
    form_class = GuestForm
    template_name = 'administracion/huespedes/guest_update.html'
    success_url = reverse_lazy('guest_list')

class GuestDeleteView(DeleteView):
    model = Guest
    template_name = 'administracion/huespedes/guest_delete.html'
    success_url = reverse_lazy('guest_list')

def download_excel(request):
    reservations = Reservation.objects.all()  # Obtener todas las reservas

    # Crear un nuevo libro de Excel y una hoja de cálculo
    workbook = Workbook()
    worksheet = workbook.active

    # Agregar encabezados a la hoja de cálculo
    headers = [
        'Código Reserva',
        'Fecha de Reserva',
        'Nombre y Apellido',
        'Camping',
        'Check-in',
        'Check-out',
        'Número de Huéspedes',
        'Costo Total',
    ]
    worksheet.append(headers)

    # Agregar los datos de las reservas a la hoja de cálculo
    for reservation in reservations:
       
        # Convertir fechas para que las acepte Excel
        reservation_date = datetime.combine(reservation.reservation_date, datetime.min.time())
        check_in = datetime.combine(reservation.check_in, datetime.min.time())
        check_out = datetime.combine(reservation.check_out, datetime.min.time())

        row = [
            reservation.code,
            reservation_date.astimezone(timezone.utc).replace(tzinfo=None),
            reservation.user.username,
            reservation.campsite.name,
            check_in.astimezone(timezone.utc).replace(tzinfo=None),
            check_out.astimezone(timezone.utc).replace(tzinfo=None),
            reservation.number_guests,
            reservation.total_cost,
        ]
        worksheet.append(row)

    # Configurar la respuesta HTTP para descargar el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=reservas.xlsx'

    # Guardar el libro de Excel en la respuesta
    workbook.save(response)

    return response

""" # PARA EL GRAFICO DE OCUPACION DE CAMPING
def principal(request):
    reservas = Reservation.objects.all()
    campings = Campsite.objects.all()
    
    # Crear un diccionario para almacenar la ocupación de cada camping
    ocupacion_campings = {camping.name: 0 for camping in campings}
    
    # Calcular la ocupación de cada camping
    for reserva in reservas:
        if not reserva.baja:
            ocupacion_campings[reserva.campsite.name] += reserva.number_guests
    
    # Convertir los datos a listas para el gráfico
    campings_labels = list(ocupacion_campings.keys())
    ocupacion_data = list(ocupacion_campings.values())
    
    return render(request, 'administracion/reservas/graficos.html', {
        'campings_labels': campings_labels,
        'ocupacion_data': ocupacion_data,
    })

 """

#RESERVAS POR MES Y AÑO(grafico)
def principal(request):
    reservas = Reservation.objects.filter(baja=False)
    
    # Agrupar las reservas por mes y año
    reservas_por_mes_y_anio = reservas.annotate(
        year=ExtractYear('check_in'),
        month=ExtractMonth('check_in')
    ).values('year', 'month').annotate(count=Count('id')).order_by('year', 'month')
    
    # Crear listas para las etiquetas del gráfico y los datos
    labels = []
    data = []
    
    for reserva in reservas_por_mes_y_anio:
        mes = reserva['month']
        año = reserva['year']
        cantidad_reservas = reserva['count']
        labels.append(f'{mes}/{año}')
        data.append(cantidad_reservas)
    
    return render(request, 'administracion/reservas/graficos.html', {
        'labels': labels,
        'data': data,
    })

 
""" 
def principal(request):
    reservas = Reservation.objects.filter(baja=False)
    
    # Agrupar las reservas por mes
    reservas_por_mes = reservas.annotate(
        month=ExtractMonth('check_in')
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    # Crear listas para las etiquetas del gráfico y los datos
    labels = []
    data = []
    
    for reserva in reservas_por_mes:
        mes = reserva['month']
        cantidad_reservas = reserva['count']
        labels.append(f'Mes {mes}')
        data.append(cantidad_reservas)
    
    return render(request, 'administracion/reservas/graficos.html', {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    })
 """
""" 
#PARA EL GRAFICO DE OCUPACION DE CAMPINGS POR MES
def principal2(request):
    reservas = Reservation.objects.all()
    campings = Campsite.objects.all()
    
    # Crear un diccionario para almacenar la ocupación de cada camping por mes
    ocupacion_campings_mes = defaultdict(lambda: defaultdict(int))
    
    # Calcular la ocupación de cada camping por mes
    for reserva in reservas:
        if not reserva.baja:
            check_in_month = reserva.check_in.month
            check_out_month = reserva.check_out.month
            campsite_name = reserva.campsite.name
            for month in range(check_in_month, check_out_month + 1):
                ocupacion_campings_mes[campsite_name][month] += reserva.number_guests
    
    # Crear listas para las etiquetas de camping y datos de ocupación por mes
    campings_labels = list(campings.values_list('name', flat=True))
    months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    ocupacion_data = [[] for _ in range(12)]
    
    for camping_name in campings_labels:
        for month in range(1, 13):
            ocupacion_data[month - 1].append(ocupacion_campings_mes[camping_name][month])
    
    return render(request, 'administracion/reservas/graficos2.html', {
        'campings_labels': campings_labels,
        'ocupacion_data': ocupacion_data,
        'months': months,
    })
 """

# PARA EL GRAFICO DE RESERVAS POR AÑO(grafico 3)

def principal3(request):
    reservas = Reservation.objects.all()
    importes_por_mes_anio = defaultdict(float)

    for reserva in reservas:
        if not reserva.baja:
            year = reserva.check_in.year
            month = reserva.check_in.month
            importes_por_mes_anio[(year, month)] += reserva.total_cost

    # Convertir el diccionario en listas para usar en JavaScript
    years_months = list(importes_por_mes_anio.keys())
    importes = list(importes_por_mes_anio.values())

    return render(request, 'administracion/reservas/graficos3.html', {'years_months': years_months, 'importes': importes})


""" def principal3(request):
    reservas = Reservation.objects.all()
    ocupacion_por_anio = defaultdict(int)

    for reserva in reservas:
        if not reserva.baja:
            year = reserva.check_in.year
            ocupacion_por_anio[year] += 1

    # Convertir el diccionario en listas para usar en JavaScript
    years = list(ocupacion_por_anio.keys())
    ocupacion = list(ocupacion_por_anio.values())

    return render(request, 'administracion/reservas/graficos3.html', {'years': years, 'ocupacion': ocupacion})

 """

""" def natural_parks_chart(request):
    natural_parks = NaturalPark.objects.all()
    park_names = [park.name for park in natural_parks]
    campsite_counts = [park.campsites.count() for park in natural_parks]

    return render(request, 'administracion/reservas/graficos5.html', {'park_names': park_names, 'campsite_counts': campsite_counts})
 """

#GRAFICO DE CAMPING POR PARQUE NATURAL(grafico 5)
def natural_parks_chart(request):
    natural_parks = NaturalPark.objects.all()
    park_names = [park.name for park in natural_parks]
    campsite_counts = [park.campsites.count() for park in natural_parks]

    # Agrega impresiones para verificar los datos
    print("Park Names:", park_names)
    print("Campsite Counts:", campsite_counts)

    return render(request, 'administracion/reservas/graficos5.html', {'park_names': park_names, 'campsite_counts': campsite_counts})





# PARA EL GRAFICO DE RESERVAS POR AÑO(grafico 3 duplicado para probar)

def principal9(request):
    reservas = Reservation.objects.all()
    importes_por_mes_anio = defaultdict(float)

    for reserva in reservas:
        if not reserva.baja:
            year = reserva.check_in.year
            month = reserva.check_in.month
            importes_por_mes_anio[(year, month)] += reserva.total_cost

    # Convertir el diccionario en listas para usar en JavaScript
    years_months = list(importes_por_mes_anio.keys())
    importes = list(importes_por_mes_anio.values())

    # Definir una lista de nombres de meses en la vista
    monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    # Crear una lista de etiquetas personalizadas que incluyan el año
    labels = [f"{monthNames[month-1]} {year}" for year, month in years_months]

    return render(request, 'administracion/reservas/graficos9.html', {'years_months': years_months, 'importes': importes, 'labels': labels})


""" def occupancy_by_year(request):
    # Obtén la ocupación por año
    occupancy_data = list(
        Reservation.objects.values_list('check_in__year')
        .annotate(count=Count('id'))
        .order_by('check_in__year')
    )
    
    return render(request, 'administracion/reservas/graficos4.html', {'occupancy_data': occupancy_data})
 """
""" 
def occupancy_by_year(request):
    # Obtén la ocupación por año para reservas con estado True
    occupancy_data_true = list(
        Reservation.objects.filter(baja=False)  # Filtra las reservas con estado True
        .values_list('check_in__year')
        .annotate(count=Count('id'))
        .order_by('check_in__year')
    )

    # Obtén la ocupación por año para reservas con estado False
    occupancy_data_false = list(
        Reservation.objects.filter(baja=True)  # Filtra las reservas con estado False
        .values_list('check_in__year')
        .annotate(count=Count('id'))
        .order_by('check_in__year')
    )

    return render(request, 'administracion/reservas/graficos4.html', {
        'occupancy_data_true': occupancy_data_true,
        'occupancy_data_false': occupancy_data_false,
    })
 """
#GRAFICO DE RESERVAS POR AÑO CON FILTRO(grafico 4)
def occupancy_by_year(request):
    # Obtén el año mínimo y máximo de las reservas
    min_year = Reservation.objects.filter(baja=False).aggregate(Min('check_in__year'))['check_in__year__min']
    max_year = Reservation.objects.filter(baja=False).aggregate(Max('check_in__year'))['check_in__year__max']

    # Crea una lista de años desde el mínimo hasta el máximo
    years = list(range(min_year, max_year + 1))

    # Obtén los valores de los checkboxes seleccionados
    selected_occupancy_true = request.GET.get('occupancy_true')
    selected_occupancy_false = request.GET.get('occupancy_false')
    
    # Obtiene el año seleccionado del formulario
    selected_year = request.GET.get('year')

    # Filtra las reservas según el año seleccionado
    if selected_year:
        occupancy_data_true = list(
            Reservation.objects.filter(baja=False, check_in__year=selected_year)
            .values_list('check_in__year')
            .annotate(count=Count('id'))
            .order_by('check_in__year')
        )
        occupancy_data_false = list(
            Reservation.objects.filter(baja=True, check_in__year=selected_year)
            .values_list('check_in__year')
            .annotate(count=Count('id'))
            .order_by('check_in__year')
        )
    else:
        # Si no se selecciona ningún año, muestra todos los datos
        occupancy_data_true = list(
            Reservation.objects.filter(baja=False)
            .values_list('check_in__year')
            .annotate(count=Count('id'))
            .order_by('check_in__year')
        )
        occupancy_data_false = list(
            Reservation.objects.filter(baja=True)
            .values_list('check_in__year')
            .annotate(count=Count('id'))
            .order_by('check_in__year')
        )

    return render(request, 'administracion/reservas/graficos4.html', {
        'occupancy_data_true': occupancy_data_true,
        'occupancy_data_false': occupancy_data_false,
        'years': years,
        'selected_year': selected_year,
    })



    
""" 
def generate_reservation_pdf(request, reservation_id):

    
    # Obtén la reserva y sus datos relacionados
    reservation = Reservation.objects.get(id=reservation_id)
    user = reservation.user
    guests = Guest.objects.filter(reservation=reservation)

    # Configura el response PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reservation_{reservation_id}.pdf"'

    # Crea el objeto PDF
    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []

    # Define los estilos y verifica si ya existen
    styles = getSampleStyleSheet()
    if 'Title' not in styles:
        styles.add(ParagraphStyle(name='Title', fontSize=16, alignment=TA_CENTER))
    if 'Normal' not in styles:
        styles.add(ParagraphStyle(name='Normal', fontSize=12, alignment=TA_LEFT))

    # Agrega información de la reserva al PDF
    elements.append(Paragraph(f'Reservación Nº {reservation.code}', styles['Title']))
    elements.append(Paragraph(f'Usuario realizo reserva: {user.first_name} {user.last_name}', styles['Normal']))
    elements.append(Paragraph(f'Fecha de Check-In: {reservation.check_in}', styles['Normal']))
    elements.append(Paragraph(f'Fecha de Check-Out: {reservation.check_out}', styles['Normal']))
    elements.append(Paragraph(f'Total a Pagar: ${reservation.total_cost}', styles['Normal']))
    elements.append(Paragraph(f'Huéspedes:', styles['Title']))

    # Agregar información de los huéspedes
    for guest in guests:
        guest_info = f'Nombre: {guest.first_name}, Apellido: {guest.last_name}, DNI: {guest.dni}'
        elements.append(Paragraph(guest_info, styles['Normal']))

    # Resto de la lógica para agregar información adicional

    # Construye el PDF
    doc.build(elements)

    return response


 """
 
def generate_reservation_pdf(request, reservation_id):
    # Obtén la reserva y sus datos relacionados
    reservation = Reservation.objects.get(id=reservation_id)
    user = reservation.user
    guests = Guest.objects.filter(reservation=reservation)

    # Configura el response PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reservation_{reservation_id}.pdf"'

    # Crea el objeto PDF
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Define los estilos y verifica si ya existen
    styles = getSampleStyleSheet()
    if 'Title' not in styles:
        styles.add(ParagraphStyle(name='Title', fontSize=16, alignment=TA_CENTER))
    if 'Normal' not in styles:
        styles.add(ParagraphStyle(name='Normal', fontSize=12, alignment=TA_LEFT))

    # Agrega información de la reserva al PDF
    elements.append(Paragraph(f'Reservación Nº {reservation.code}', styles['Title']))
    elements.append(Paragraph(f'Usuario realizó la reserva: {user.first_name} {user.last_name}', styles['Normal']))
    elements.append(Paragraph(f'Fecha de Check-In: {reservation.check_in}', styles['Normal']))
    elements.append(Paragraph(f'Fecha de Check-Out: {reservation.check_out}', styles['Normal']))
    elements.append(Paragraph(f'Total a Pagar: ${reservation.total_cost}', styles['Normal']))
    elements.append(Paragraph(f'Huéspedes:', styles['Title']))

    # Crear una lista de datos de huéspedes para la tabla
    guest_data = [["Nombre", "Apellido", "DNI"]]
    for guest in guests:
        guest_data.append([guest.first_name, guest.last_name, guest.dni])

    # Crear una tabla y establecer su estilo
    guest_table = Table(guest_data, colWidths=[100, 100, 100])
    guest_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Fila de encabezado
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Filas de datos
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(guest_table)

    # Resto de la lógica para agregar información adicional al PDF

    # Construye el PDF
    doc.build(elements)

    return response

