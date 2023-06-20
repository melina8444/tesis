
from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    pass
class NaturalPark(models.Model):

    class Meta:
        db_table='Parques_Naturales'

    class Province(models.IntegerChoices):
        BUENOS_AIRES = 1, "Buenos Aires"
        CIUDAD_AUTONOMA_DE_BUENOS_AIRES = 2, "Ciudad Autónoma de Buenos Aires"
        CATAMARCA = 3, "Catamarca"
        CHACO = 4, "Chaco"
        CHUBUT = 5, "Chubut"
        CORDOBA = 6, "Córdoba"
        CORRIENTES = 7, "Corrientes"
        ENTRE_RIOS = 8, "Entre Ríos"
        FORMOSA = 9, "Formosa"
        JUJUY = 10, "Jujuy"
        SALTA = 11, "Salta"
        TUCUMAN = 12, "Tucumán"
        LA_PAMPA = 13, "La Pampa"
        LA_RIOJA = 14, "La Rioja"
        SAN_JUAN = 15, "San Juan"
        MENDOZA = 16, "Mendoza"
        MISIONES = 17, "Misiones"
        NEUQUEN = 18, "Neuquén"
        RIO_NEGRO = 19, "Río Negro"
        SAN_LUIS = 20, "San Luis"
        SANTA_CRUZ = 21, "Santa Cruz"
        SANTA_FE = 22, "Santa Fé"
        SANTIAGO_DEL_ESTERO = 23, "Santiago del Estero"
        TIERRA_DEL_FUEGO = 24, "Tierra del Fuego"


    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    province = models.IntegerField(choices=Province.choices)
    image = models.ImageField(upload_to='imagenes/', null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'Nombre: {self.name}'
    
class Category(models.Model):

    class Meta:
        db_table='Categorías'

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    capacity = models.IntegerField()
    price = models.FloatField(max_length=10)
    
    def __str__(self):
        return f'Nombre: {self.name}'
    
class Campsite(models.Model):

    class Meta:
        db_table='Campings'

    natural_park = models.ForeignKey(NaturalPark, on_delete=models.CASCADE, related_name='campsites')
    name = models.CharField(max_length=100)
    description = models.TextField()
    images = models.ImageField(upload_to='imagenes/', null=True)
    categories = models.ManyToManyField(Category, related_name='campsites')

    def __str__(self):
        return f'Nombre: {self.name}'

class Availability(models.Model):
    class Meta:
        db_table='Disponibilidades'

    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE, related_name='availabilities')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    max_capacity=models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'Fecha inicio: {self.start_date}  Fecha fin: {self.end_date} Capacidad Máxima: {self.max_capacity}'
    
class Reservation(models.Model):
    class Meta:
        db_table='Reservas'
    
    code = models.CharField(max_length=8, unique=True)
    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE, related_name='reservations')
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    number_guests = models.IntegerField()
    total_cost = models.FloatField(max_length=10)
    reservation_date = models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Código Reserva: {self.code} / Usuario: {self.user.first_name} {self.user.last_name}'

class Guest(models.Model):
    class Meta:
        db_table = 'Guests'

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dni = models.CharField(max_length=10)
    age = models.IntegerField()
    is_saved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.reservation}'

class Profile(models.Model):
    class Meta:
        db_table="Perfiles"

    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    dni = models.CharField(max_length=255)
    is_client = models.BooleanField(default=True)

