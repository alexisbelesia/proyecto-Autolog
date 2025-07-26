from django.db import models

# Create your models here.
class Taller(models.Model):
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
