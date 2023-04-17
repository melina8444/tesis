from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.index_admin, name='inicio_admin'),
    path('clientes/listar', views.listar_clientes, name='listar_clientes'),
]