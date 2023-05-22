from django.urls import path, re_path, include
from . import views
from .views import NaturalParkListView, NaturalParkCreateView, NaturalParkUpdateView, NaturalParkDeleteView

urlpatterns = [
    path('', views.index_admin, name='inicio_admin'),
    #path('clientes/listar/', views.listar_clientes, name='listar_clientes'),
    path('naturalparks/', NaturalParkListView.as_view(), name='naturalpark_list'),
    path('naturalparks/create/', NaturalParkCreateView.as_view(), name='naturalpark_create'),
    path('naturalparks/update/<int:pk>/', NaturalParkUpdateView.as_view(), name='naturalpark_update'),
    path('naturalparks/delete/<int:pk>/', NaturalParkDeleteView.as_view(), name='naturalpark_delete'),

]