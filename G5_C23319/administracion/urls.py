from django.urls import path
from . import views
from .views import NaturalParkListView, NaturalParkCreateView,NaturalParkUpdateView, NaturalParkDeleteView, CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, CampsiteListView, CampsiteCreateView, CampsiteUpdateView, CampsiteDeleteView, AvailabilityListView, AvailabilityCreateView, AvailabilityUpdateView, AvailabilityDeleteView, ProfileListView, ProfileCreateView, ProfileUpdateView, ProfileDeleteView, ReservationListView, ReservationCreateView, ReservationDeleteView, ReservationUpdateView, GuestListView, GuestDeleteView, GuestUpdateView, SeasonListView, SeasonCreateView, SeasonUpdateView, SeasonDeleteView

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
    path('profiles/', ProfileListView.as_view(), name='profile_list'),
    path('profiles/create/', ProfileCreateView.as_view(), name='profile_create'),
    path('profiles/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profiles/<int:pk>/delete/', ProfileDeleteView.as_view(), name='profile_delete'),
    path('reservations/', ReservationListView.as_view(), name='reservation_list'),
    path('reservations/create/', ReservationCreateView.as_view(), name='reservation_create'),
    path('reservations/update/<int:pk>/', ReservationUpdateView.as_view(), name='reservation_update'),
    path('reservations/delete/<int:pk>/', ReservationDeleteView.as_view(), name='reservation_delete'),
    path('guests/', GuestListView.as_view(), name='guest_list'),
    #path('guests/create/', GuestCreateView.as_view(), name='guest_create'),
    path('guests/update/<int:pk>/', GuestUpdateView.as_view(), name='guest_update'),
    path('guests/delete/<int:pk>/', GuestDeleteView.as_view(), name='guest_delete'),
    path('access_denied/', views.access_denied, name='access_denied'),
    path('reservations/download_excel/', views.download_excel, name='download_excel'),
    path('reservations/grafico/', views.grafico, name='grafico'),
    

    #TEMPORADA
    path('season/', SeasonListView.as_view(), name='season_list'),
    path('season/create/', SeasonCreateView.as_view(), name='season_create'),
    path('season/update/<int:pk>/', SeasonUpdateView.as_view(), name='season_update'),
    path('season/delete/<int:pk>/', SeasonDeleteView.as_view(), name='season_delete'),
    

]
