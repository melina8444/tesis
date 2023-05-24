from django.db import models
from django.contrib.auth.models import User


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

class Image(models.Model):
    campsite = models.ForeignKey(Campsite, related_name='campsiteimages', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='imagenes/')

class Availability(models.Model):
    class Meta:
        db_table='Disponibilidades'

    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE, related_name='availabilities')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Fecha inicio: {self.start_date}  Fecha fin: {self.start_date}'
class Reservation(models.Model):
    class Meta:
        db_table='Reservas'
    
    code = models.FloatField(unique=True, auto_created=True, default=0.0)
    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE)
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    number_guests = models.IntegerField()
    total_cost = models.FloatField(max_length=10)

    def __str__(self):
        return f'Código Reserva: {self.code} + Nombre y Apellido: {self.user.first_name}+ " " +{self.user.last_name}'

class Profile(models.Model):
    class Meta:
        db_table="Perfiles"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    dni = models.CharField(max_length=255)
    is_client = models.BooleanField(default=True)

