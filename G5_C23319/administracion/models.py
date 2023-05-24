from django.db import models

# Create your models here.
class CategoriaCamping(models.Model):
    class Meta:
        db_table = 'categoria_camping'
        
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=150)
    capacidad = models.IntegerField(blank=True , null= True)
    precio = models.FloatField(max_length=7, blank=True , null= True)

    def __str__(self):
        return f'nombre = {self.nombre}' 

class DisponibilidadCamping(models.Model):
    class Meta:
        db_table = 'disponibilidad_camping'

    categoria = models.ForeignKey(CategoriaCamping,  on_delete=models.CASCADE)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'fecha inicio = {self.fecha_inicio} + fecha fin = {self.fecha_fin}'