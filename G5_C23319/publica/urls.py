from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="Inicio"),
    path('accounts/profile/', auth_views.LoginView.as_view(
            template_name='publica/login.html',
            extra_context={'variable':'TEST'},
        )),
    path('contact/',views.contact, name="contact"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('campsite/category/<str:category>/', views.campsites_by_category, name='campsites_by_category'),
    path ('reserva/<int:campsite_id>/', views.reserva_camp_id, name='reserva_camp_id'),
    path ('reserva/', views.reserva, name='reserva'),
]