from django.urls import path
from . import views

urlpatterns = [
    path('', views.Bienvenidos_RN, name="Bienvenidos"),
]