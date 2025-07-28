from django.db import models

from autolog import settings
from .modelo import Modelo



# Create your models here.
class Vehiculo(models.Model):
    año = models.PositiveIntegerField()
    dominio = models.CharField(max_length=7, unique=True)
    intervalo_servicio = models.IntegerField()
    
    fecha_prox_servicio = models.DateField(null=True, blank=True)
    kilometraje_prox_servicio = models.IntegerField(null=True, blank=True)
    
    #Relaciones

    modelo = models.ForeignKey(Modelo,on_delete=models.PROTECT, related_name='vehiculos')
    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='vehiculos')

    @property
    def marca(self):
        return self.modelo.marca
    
    @property
    def historial(self):
        return self.ordenes.all().order_by('fecha_turno') 

    def __str__(self):
        return f"{self.modelo.marca.nombre} {self.modelo.nombre} {self.año} {self.dominio}"

