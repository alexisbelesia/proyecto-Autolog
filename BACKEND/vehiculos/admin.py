from django.contrib import admin
from .models.vehiculo import Vehiculo
from .models.marca import Marca
from .models.modelo import Modelo

admin.site.register(Vehiculo)
admin.site.register(Marca)
admin.site.register(Modelo)

# Register your models here.
