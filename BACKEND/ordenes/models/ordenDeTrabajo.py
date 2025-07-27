from django.db import models
from dateutil.relativedelta import relativedelta
from talleres.models.taller import Taller


# Create your models here.
class OrdenDeTrabajo(models.Model):
    fecha_entrega = models.DateField()
    kilometraje = models.PositiveIntegerField(default = 0)
    fecha_siguiente_servicio = models.DateField(null=True, blank=True)
    kilometraje_siguiente_servicio = models.PositiveIntegerField(null=True, blank=True) 
    observaciones_tecnicas = models.TextField(blank=True)

    #ESTO NO VA, SOLO PARA PRBAR
    fecha_turno = models.DateField()
    cliente = models.CharField(max_length=50, null=True)

    PREVENTIVO = 'preventivo'
    CORRECTIVO = 'correctivo'
    TIPOS_TRABAJO = [(PREVENTIVO,'Preventivo'), (CORRECTIVO,'Correctivo')]

    mantenimiento = models.CharField(max_length = 15, choices = TIPOS_TRABAJO, default=PREVENTIVO)
   
    # Relaciones
    vehiculo = models.ForeignKey(
        'vehiculos.Vehiculo', on_delete=models.PROTECT, related_name='ordenes'
    )
    taller = models.ForeignKey(Taller, on_delete=models.PROTECT, related_name='orden_de_trabajo')
    '''
    tecnico = models.ForeignKey(
        'usuarios.AdministradorTecnico', on_delete=models.PROTECT, null=True, related_name='ordenes'
    )
    
    practica = models.ForeignKey(
        'ordenes.PracticaMantenimiento', on_delete=models.PROTECT, null=True
    )
    
    presupuesto = models.OneToOneField(
        'presupuesto.Presupuesto', on_delete=models.PROTECT, null=True
    )
    fecha_turno = models.ForeignKey(
        'agenda.Turno', on_delete=models.SET_NULL, null=True
    )'''

    def calcular_fecha_siguiente_servicio(self):
        if self.mantenimiento == 'PREVENTIVO' and self.fecha_turno:
            self.fecha_siguiente_servicio = self.fecha_turno + relativedelta(years=1)

    def __str__(self):
        return f"Orden #{self.id} - {self.vehiculo} - {self.fecha_entrega}"