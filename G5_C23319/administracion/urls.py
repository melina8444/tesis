from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.index_admin, name='inicio_admin'),
    path('clientes/listar/', views.listar_clientes, name='listar_clientes'),
    #path('natural_parks/create', views.create_natural_park, name='create_natural_parks'),
    #path('natural_parks/list', views.list_natural_park, name='list_natural_parks')
]