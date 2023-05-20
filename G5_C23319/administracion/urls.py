from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.index_admin, name='inicio_admin'),
    path('clientes/listar/', views.listar_clientes, name='listar_clientes'),
    #path('natural_parks/create', create_natural_park.as_view(), name='crear_parques_naturales'),
    #path('natural_parks/list', list_natural_park.as_view(), name='listar_parques_naturales')
]