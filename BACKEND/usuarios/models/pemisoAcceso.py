from django.db import models

class PermisoDeAcceso(models.Model):

    fecha_autorizacion = models.DateField()

    vehiculo_autorizado = models.OneToOneField('vehiculos.Vehiculo', on_delete=models.PROTECT, null=True, blank=True)

    autoriza = models.ForeignKey('usuarios.Cliente', on_delete=models.PROTECT, related_name='permiso_que_otorgo')
    
    usuario_autorizado = models.ForeignKey('usuarios.Usuario', on_delete=models.PROTECT, blank=True, null=True, related_name='permiso_que_recibi')

    taller_autorizado = models.ForeignKey('talleres.Taller', on_delete=models.PROTECT, blank=True, null=True, related_name='permiso_de_acceso')


