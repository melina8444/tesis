from django.urls import path, re_path, include
from . import views
from .views import NaturalParkListView, NaturalParkCreateView,NaturalParkUpdateView, NaturalParkDeleteView, CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, CampsiteListView, CampsiteCreateView, CampsiteUpdateView, CampsiteDeleteView, AvailabilityListView, AvailabilityCreateView, AvailabilityUpdateView, AvailabilityDeleteView


urlpatterns = [
    path('', views.index_admin, name='inicio_admin'),
    #path('clientes/listar/', views.listar_clientes, name='listar_clientes'),
    path('naturalparks/', NaturalParkListView.as_view(), name='naturalpark_list'),
    path('naturalparks/create/', NaturalParkCreateView.as_view(), name='naturalpark_create'),
    path('naturalparks/update/<int:pk>/', NaturalParkUpdateView.as_view(), name='naturalpark_update'),
    path('naturalparks/delete/<int:pk>/', NaturalParkDeleteView.as_view(), name='naturalpark_delete'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('campsites/', CampsiteListView.as_view(), name='campsite_list'),
    path('campsites/create/', CampsiteCreateView.as_view(), name='campsite_create'),
    path('campsites/update/<int:pk>/', CampsiteUpdateView.as_view(), name='campsite_update'),
    path('campsites/delete/<int:pk>/', CampsiteDeleteView.as_view(), name='campsite_delete'),
    path('availabilities/', AvailabilityListView.as_view(), name='availability_list'),
    path('availabilities/create/', AvailabilityCreateView.as_view(), name='availability_create'),
    path('availabilities/update/<int:pk>/', AvailabilityUpdateView.as_view(), name='availability_update'),
    path('availabilities/delete/<int:pk>/', AvailabilityDeleteView.as_view(), name='availability_delete'),
]
