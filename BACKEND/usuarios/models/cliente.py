from datetime import date
from django.db import models

from usuarios.models.pemisoAcceso import PermisoDeAcceso
from usuarios.models.usuario import Usuario

from django.contrib.auth.models import UserManager

class Cliente (models.Model):
    
    usuario = models.OneToOneField('Usuario', on_delete=models.PROTECT )
    #DE PERMISOS QUE ORTORGA UN CLIENTEA SACO A QUIENES LE DIO PERMISO(TALLERES, CLIENTES Y VEHICULOS) SEGURAMENTE SE USE MAS ADELANTE
    @property
    def vehiculos_autorizados (self):
        return [permiso.vehiculo_autorizado for permiso in self.permiso_que_otorgo.all()]
    
    @property
    def talleres_autorizados(self):
        return [permiso.taller_autorizado for permiso in self.permiso_que_otorgo.all()]
    
    @property
    def clientes_autorizados(self):
        return [permiso.cliente_autorizado for permiso in self.permiso_que_otorgo.all()]
    
    # FIN PERMISOS QUE OTORGA
    
    @property
    def mis_vehiculos(self):
        return self.vehiculos.all()
    
    @property
    def permisos_de_acceso(self):
        return self.permiso.all()
    
    # metodos
    def crear_permiso(self, vehiculo_autorizado, usuario_autorizado=None, taller_autorizado=None):
        
        if vehiculo_autorizado.propietario_id != self.id:
            print(f"{self} vs {vehiculo_autorizado.propietario}")
            raise ValueError("No se puede otorgar permiso para un vehículo que no te pertenece.")
        
        if not usuario_autorizado and not taller_autorizado:
            raise ValueError("Debe autorizar a un taller o a un usuario.")
        
        if PermisoDeAcceso.objects.filter(vehiculo_autorizado = vehiculo_autorizado, usuario_autorizado=usuario_autorizado,   taller_autorizado=taller_autorizado).exists():
            raise ValueError("Ya existe un permiso igual.")

        permiso = PermisoDeAcceso.objects.create(
            vehiculo_autorizado = vehiculo_autorizado,
            autoriza=self,
            usuario_autorizado=usuario_autorizado,
            taller_autorizado=taller_autorizado,
            fecha_autorizacion=date.today()
        )
        return permiso
    
    def __str__(self):
        return f"id:{self.pk} - username:{self.usuario.username}"
    