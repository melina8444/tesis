from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import NaturalPark
from .forms import NaturalParkForm, NaturalParkFilterForm, NaturalParkFilterForm


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
