from django.db import models
from .modelo import Modelo



# Create your models here.
class Vehiculo(models.Model):
    año = models.PositiveIntegerField()
    dominio = models.CharField(max_length=7, unique=True)

    #Relaciones

    #marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='vehiculo')
    modelo = models.ForeignKey(Modelo,on_delete=models.PROTECT, related_name='vehiculos')
    

    @property
    def marca(self):
        return self.modelo.marca
    
    def obtenerOrdenes(self):
        ordenes = self.ordenes.all()
        return ordenes
    
    def obtenerUltimaOrdenPreventiva(self):
        return self.obtenerOrdenes.filter(mantenimiento = 'PREVENTIVO').order_by('fecha_siguiente_servicio').first()
        #ACA PUEDE HABER LIO SI TOMA LA ULTIMA ORDEN A LA QUE ESTOY CREANDO, PROBAR BIEN

    def calcularFechaProxService(self):
        ultima_orden_preventiva = self.obtenerUltimaOrdenPreventiva()
        if ultima_orden_preventiva and ultima_orden_preventiva.fecha_turno:
            return ultima_orden_preventiva.fecha_siguiente_servicio
        return None 

    def __str__(self):
        return f"{self.modelo.marca.nombre} {self.modelo.nombre} {self.año} {self.dominio}"

