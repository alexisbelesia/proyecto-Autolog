from django.db import models
from talleres.models.taller import Taller
from .usuario import Usuario

class AdministradorTecnico(Usuario):  # Hereda de Usuario (que ya hereda de AbstractUser)
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE, related_name='tecnicos')
    
    class Meta:
        verbose_name = "Administrador Técnico"
        verbose_name_plural = "Administradores Técnicos"

    def __str__(self):
        return f"{self.username} (Técnico en {self.taller.nombre})"
    
    #creás solo un objeto Cliente con todos los campos requeridos (incluidos los de Usuario).
    def crear_cliente(self, username, email, password, first_name, last_name=None, dni=None, telefono=None, direccion=None):
        from .cliente import Cliente
        cliente = Cliente.objects.create_user( #El password queda hasheado correctamente y podés usar el sistema de autenticación de Django.
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name or '',
            dni=dni,
            telefono=telefono or '',
            direccion=direccion or '',
        )
        return cliente

    def crear_vehiculo(self, cliente, modelo, año, dominio):
        from vehiculos.models.vehiculo import Vehiculo
        return Vehiculo.objects.create(
        cliente=cliente,
        modelo=modelo,
        año=año,
        dominio=dominio,
        creado_por=self
    )

    def crear_orden_trabajo(self, cliente, vehiculo, observaciones_tecnicas, fecha_siguiente_servicio, fecha_entrega, kilometraje,kilometraje_siguiente_servicio, mantenimiento='preventivo'):
        from ordenes.models.ordenDeTrabajo import OrdenDeTrabajo

        #NO ESTOY SEGURA DE QUE SEA NECESARIO
        if mantenimiento not in dict(OrdenDeTrabajo.TIPOS_TRABAJO).keys():
            raise ValueError(f"Tipo de mantenimiento inválido: {mantenimiento}. Debe ser 'preventivo' o 'correctivo'.")

        orden = OrdenDeTrabajo.objects.create(
            vehiculo=vehiculo,
            tecnico=self,
            taller=self.taller,
            observaciones_tecnicas=observaciones_tecnicas,
            fecha_siguiente_servicio=fecha_siguiente_servicio,
            fecha_entrega=fecha_entrega,
            kilometraje=kilometraje,
            kilometraje_siguiente_servicio=kilometraje_siguiente_servicio,
            mantenimiento=mantenimiento,
            #PRESUPUESTO?
            #PRACTICA?
            #FECHA TURNO? 
        )

        orden.calcular_fecha_siguiente_servicio()
        orden.save()
        return orden

    