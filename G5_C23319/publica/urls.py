from django.urls import path
from . import views
from .views import ReservationCreateView, SuccessView

urlpatterns = [
    path('', views.index, name="Inicio"),
    # path('accounts/profile/',auth_views.LoginView.as_view(
    #         template_name='publica/login.html',
    #         extra_context={'variable':'TEST'},
    #     )),
    path('contact/',views.contact, name="contact"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('naturalpark/<int:naturalpark_id>/', views.campsites_by_naturalpark, name='campsites_by_naturalpark'),
    #path ('reserva/<int:campsite_id>/', views.reserva_camp_id, name='reserva_camp_id'),
    #path ('reserva/', views.reserva, name='reserva'),
    #path('register/', RegisterView.as_view(), name='register'),
    #path('login/', LoginView.as_view(), name='login'),
    path('success/', SuccessView.as_view(), name='success'),
    #path('reservation/', ReservationCreateView.as_view(), name='reservation'),
    path('reservation/<int:campsite_id>/', ReservationCreateView.as_view(), name='reservation_campsite'),
]