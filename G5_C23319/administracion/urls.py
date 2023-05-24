from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.index_admin, name='inicio_admin'),
    path('clientes/listar/', views.listar_clientes, name='listar_clientes'),
    path('clientes/crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('clientes/modificar_cliente/<id>/', views.modificar_cliente, name='modificar_cliente'),

]