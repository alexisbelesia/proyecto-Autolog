from django.db import models

# Create your models here.
class OrdenDeTrabajo(models.Model):
    fecha_entrega = models.DateField()
    kilometraje = models.PositiveIntegerField()
    fecha_siguiente_servicio = models.DateField(null=True, blank=True)
    observaciones_tecnicas = models.TextField(blank=True)

    # Relaciones
    vehiculo = models.ForeignKey(
        'vehiculos.Vehiculo', on_delete=models.CASCADE, related_name='ordenes'
    )
    tecnico = models.ForeignKey(
        'usuarios.AdministradorTecnico', on_delete=models.SET_NULL, null=True, related_name='ordenes'
    )
    practica = models.ForeignKey(
        'ordenes.PracticaMantenimiento', on_delete=models.SET_NULL, null=True
    )
    presupuesto = models.ForeignKey(
        'presupuestos.Presupuesto', on_delete=models.SET_NULL, null=True
    )
    turno = models.ForeignKey(
        'agenda.Turno', on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"Orden #{self.id} - {self.vehiculo} - {self.fecha_entrega}"