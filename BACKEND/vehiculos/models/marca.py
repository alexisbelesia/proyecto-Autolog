from django.db import models
from .modelo import Modelo

# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True, blank=False)
    #Relaciones

    def __str__(self):
        return self.nombre
    