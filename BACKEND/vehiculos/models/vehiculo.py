from django.db import models
from .modelo import Modelo
from usuarios.models import Cliente

# Create your models here.
class Vehiculo(models.Model):
    año = models.PositiveIntegerField()
    dominio = models.CharField(max_length=7, unique=True)

    #Relaciones

    #marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='vehiculo')
    modelo = models.ForeignKey(Modelo,on_delete=models.PROTECT, related_name='vehiculos')
    titular = models.ForeignKey('usuarios.cliente')

    @property
    def marca(self):
        return self.modelo.marca

    def __str__(self):
        return f"{self.modelo.marca.nombre} {self.modelo.nombre} {self.año} {self.dominio}"

