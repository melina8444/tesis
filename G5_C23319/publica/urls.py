from django.urls import path
from . import views
from .views import CustomLoginView, RegistroUsuarioView, ReservationCreateView, CustomLogoutView, VerificacionRegView, ReservaDetailView

urlpatterns = [
    path('', views.index, name="Inicio"),
    path('contact/',views.contact, name="contact"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('naturalpark/<int:naturalpark_id>/', views.campsites_by_naturalpark, name='campsites_by_naturalpark'),
    path('success/', views.success_view, name='success'),
    path('reservation/<int:campsite_id>/', ReservationCreateView.as_view(), name='reservation_campsite'),
    path('accounts/register/', RegistroUsuarioView.as_view(), name='register'),
    path('accounts/profile/', views.index, name='Inicio'),
    path('accounts/login/', CustomLoginView.as_view(), name='loginrn'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logoutrn'),
    path('register_verification/', VerificacionRegView.as_view(), name='register_verification'),
    path('categories/', views.categories, name="categories"),
    path('reserva_info/<int:pk>/', ReservaDetailView.as_view(), name='reserva_info'),
     path('error_page/', views.error_page, name='error_page'),
]

