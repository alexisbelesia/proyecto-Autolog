from datetime import date
from django.db import models

from usuarios.models.pemisoAcceso import PermisoDeAcceso
from usuarios.models.usuario import Usuario

from django.contrib.auth.models import UserManager

class Cliente (Usuario):
    objects = UserManager()  # Esto es necesario

    @property
    def talleres_autorizados(self):
        return [permiso.taller_autorizado for permiso in self.permiso_de_acceso.all()]
    
    @property
    def usuarios_autorizados(self):
        return [permiso.usuario_autorizado for permiso in self.permiso_de_acceso.all()]
    
    def crear_permiso(self, vehiculo, usuario_autorizado=None, taller_autorizado=None, fecha_autorizacion=None):
        
        if vehiculo.propietario != self:
            raise ValueError("No se puede otorgar permiso para un vehículo que no te pertenece.")
        
        if not usuario_autorizado and not taller_autorizado:
            raise ValueError("Debe autorizar a un taller o a un usuario.")
        
        if PermisoDeAcceso.objects.filter(vehiculo=vehiculo, usuario_autorizado=usuario_autorizado,   taller_autorizado=taller_autorizado).exists():
            raise ValueError("Ya existe un permiso igual.")

        permiso = PermisoDeAcceso.objects.create(
            vehiculo=vehiculo,
            autoriza=self,
            usuario_autorizado=usuario_autorizado,
            taller_autorizado=taller_autorizado,
            fecha_autorizacion=fecha_autorizacion or date.today()
        )
        return permiso