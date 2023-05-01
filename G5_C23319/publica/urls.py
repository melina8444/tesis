from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Inicio"),
    path('login/', views.login, name="login"),
    path('contacto/', views.contacto, name="contacto"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('campsite/category/<str:category>/', views.campsites_by_category, name='campsites_by_category'),
]