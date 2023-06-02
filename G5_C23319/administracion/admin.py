from django.contrib import admin
from .models import NaturalPark, Category, Campsite, Availability, Reservation, Profile, Usuario
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin


# Registro de modelos por defecto al admin de Django
""" admin.site.register(NaturalPark)
admin.site.register(Category)
admin.site.register(Campsite)
admin.site.register(Availability)
admin.site.register(Reservation)
admin.site.register(Profile)
admin.site.register(Usuario) """

#Admin Personalizado

class RNAdminSite(admin.AdminSite):
    site_header = 'Administración de Rerservas Naturales - G5 - CaC'
    site_title = 'Administración para el superuser'
    index_title= 'Administracion del sitio - Gestión interna de datos'
    empty_value_display = 'Sin datos para mostrar'

class NaturalParkAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'location', 'province', 'image', 'website')
    search_fields = ('name', 'province')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'capacity', 'price')
    search_fields = ('name', 'capacity')

class CampsiteAdmin(admin.ModelAdmin):
    list_display = ('natural_park', 'name', 'description', 'images')
    search_fields = ('name', 'categories')
    filter_horizontal = ('categories',)

class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('campsite', 'start_date', 'end_date', 'max_capacity')
    search_fields = ('start_date', 'end_date')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('code', 'campsite', 'availability', 'user', 'check_in', 'check_out', 'number_guests')
    search_fields = ('code', 'user', 'user.last_name')

class ProfileAdminInline(admin.TabularInline):
    model = Profile

class UsuarioAdmin(UserAdmin):
    inlines = [
        ProfileAdminInline,
    ]

rn_admin = RNAdminSite(name='rnadmin')
rn_admin.register(NaturalPark, NaturalParkAdmin)
rn_admin.register(Category, CategoryAdmin)
rn_admin.register(Campsite, CampsiteAdmin)
rn_admin.register(Availability, AvailabilityAdmin)
rn_admin.register(Reservation, ReservationAdmin)
rn_admin.register(Usuario, UsuarioAdmin)
rn_admin.register(Group, GroupAdmin)





