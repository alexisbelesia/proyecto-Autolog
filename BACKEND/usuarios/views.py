from datetime import date
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from .models import Usuario,Cliente,AdministradorTecnico
from .serializers import UsuarioSerializer,ClienteSerializer,AdministradorTecnicoSerializer,PermisoSerializer

from vehiculos.serializers import VehiculoSerializer
from vehiculos.models import Vehiculo
from ordenes.serializers import OrdenDeTrabajoSerializer
from ordenes.models.ordenDeTrabajo import OrdenDeTrabajo

# ViewSets define el comportamiento de la vista
class UsuarioViewSet(viewsets.ModelViewSet):

    queryset = Usuario.objects.all().order_by('-date_joined')
    serializer_class = UsuarioSerializer

#----------------------------CLIENTE-------------------------------------------#
class clienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    #crear permiso de acceso
    @action(detail=True, methods=['post'])
    def acceso(self, request, pk=None):
        serializer = PermisoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data_request = serializer.validated_data
        #print(data_request)
        cliente = self.get_object()
        permiso = cliente.crear_permiso(**data_request)
        return Response(PermisoSerializer(permiso).data, status=status.HTTP_201_CREATED)

    #ver historial
    @action(detail=True, methods = ['get'])
    def historial(self, request, pk=None):
        cliente = self.get_object()
        vehiculo_id = request.query_params.get('vehiculo_id')

        if not vehiculo_id:
            return Response({'error': 'vehiculo_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            vehiculo = Vehiculo.objects.get(pk=vehiculo_id)
        except Vehiculo.DoesNotExist:
            return Response({'error': 'vehiculo no encontrado'},status=status.HTTP_404_NOT_FOUND)
        
        if cliente.tiene_permiso(vehiculo):
            try:
                historial = vehiculo.historial
                serializer = OrdenDeTrabajoSerializer(historial,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
             return Response({'mensaje': 'El vehiculo no tiene historial de órdenes.'}, status=404)
        else:    
            return Response({'mensaje':'no tenes permiso para ver este historial de vehiculo'}, status=status.HTTP_404_NOT_FOUND)
    
    #vehiculos del cliente
    @action(detail=True, methods=['get'])
    def vehiculos(self,request, pk=None):
        cliente = self.get_object()
        vehiculos = cliente.mis_vehiculos
        if not vehiculos.exists():
            return Response({'mensaje':'usted no tiene vehiculos asociados'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VehiculoSerializer(vehiculos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #proximo service un vehiculo
    @action(detail=True, methods=['get'])
    def service (self,request,pk=None):
        cliente = self.get_object()
        vehiculo_id = request.query_params.get('vehiculo_id')   
        try:
            vehiculo = Vehiculo.objects.get(pk=vehiculo_id)
        except Vehiculo.DoesNotExist:
            return Response({'mensaje': 'vehiculo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        if not cliente.tiene_permiso(vehiculo):
            return Response({"mensaje": "No tenés permiso para ese vehículo"},status=status.HTTP_403_FORBIDDEN) 
        
        fecha = vehiculo.fecha_prox_servicio
        kilometraje = vehiculo.kilometraje_prox_servicio
        
        if not fecha or not kilometraje:
            return Response({'mensaje':'vehiculo sin proximo servicio estimado'}, status=status.HTTP_404_NOT_FOUND) 
        return Response({
            'fecha_prox_servicio': fecha,
            'kilometraje_prox_servicio': kilometraje
        },status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def crear_vehiculo (self, request, pk=None):
        serializer = VehiculoSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)  

        vehiculo_data = serializer.validated_data
        cliente = self.get_object()
        try: 
            vehiculo = cliente.crear_vehiculo(**vehiculo_data)
        except IntegrityError:
            return Response({'mensaje': 'ya existe un vehiculo con esa patente'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'id':vehiculo.id, 'mensaje':'vehiculo creado'}, status=status.HTTP_201_CREATED)


         


#----admintec
class AdministradorTecnicoViewSet(viewsets.ModelViewSet):
    queryset = AdministradorTecnico.objects.all()
    serializer_class = AdministradorTecnicoSerializer
    permission_classes = [permissions.AllowAny] # 👈 acceso público por ahora para probar
    def get_queryset(self):
         # El técnico solo puede acceder a su propio perfil (objeto AdministradorTecnico)
        if self.request.user.is_authenticated:
            return AdministradorTecnico.objects.filter(usuario=self.request.user)
        return AdministradorTecnico.objects.all()  # acceso abierto temporalmente
    

    


    #Crud Cliente desde tecnico
    @action(detail=True, methods=['post'])
    def crear_cliente(self, request, pk=None):
        tecnico = self.get_object()
        serializer = ClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        usuario_data = data['usuario']

        cliente = tecnico.crear_cliente(
            username=usuario_data['username'],
            email=usuario_data['email'],
            password=usuario_data['password'],
            first_name=usuario_data.get('first_name', ''),
            last_name=usuario_data.get('last_name', ''),
            dni=data.get('dni'),
            telefono=data.get('telefono', ''),
            direccion=data.get('direccion', ''),
        )

        return Response(ClienteSerializer(cliente).data, status=status.HTTP_201_CREATED)


    #crud vehiculo desde tecnico    
    @action(detail=True, methods=['post'])
    def crear_vehiculo(self, request, pk=None):
        tecnico = self.get_object()
        serializer = VehiculoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vehiculo = tecnico.crear_vehiculo(
            cliente=serializer.validated_data['propietario'],
            modelo=serializer.validated_data['modelo'],
            año=serializer.validated_data['año'],
            dominio=serializer.validated_data['dominio'],
        )
        return Response(VehiculoSerializer(vehiculo).data, status=status.HTTP_201_CREATED)
    
    #Crud OT desde tecnico
    #POST
    @action(detail=True, methods=['post'])
    def crear_orden(self, request, pk=None):
        tecnico = self.get_object()
        serializer = OrdenDeTrabajoSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        orden = serializer.validated_data
        try:
            orden = tecnico.crear_orden_trabajo(**orden)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Serializar la orden creada
        serializer = OrdenDeTrabajoSerializer(orden)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    #PATCH
    @action(detail=True, methods=["patch"]) #url_path="ordenes/(?P<orden_id>[^/.]+)/actualizar")
    def actualizar_orden(self, request, pk=None, orden_id=None):
        tecnico = self.get_object()
        orden_id = request.query_params.get('orden_id')
        serializer = OrdenDeTrabajoSerializer(data= request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        nuevos_datos = serializer.validated_data

        try:
            orden = OrdenDeTrabajo.objects.get(pk=orden_id)

            if orden.tecnico_id != tecnico.id:
                return Response({"error": "No tiene permiso para modificar esta orden."}, status=403)

            # Aplicar los cambios a la instancia
            for campo, valor in nuevos_datos.items():
                setattr(orden, campo, valor)

            orden.save()
               
            # Podés usar un serializer 
            return Response({
                "mensaje": "Orden actualizada correctamente",
                "orden_id": orden.id
            })

        except OrdenDeTrabajo.DoesNotExist:
            return Response({"error": f"No existe la orden con ID {orden_id}"}, status=404)


    #DELETE
    @action(detail=True, methods=['delete'], url_path='orden/(?P<orden_id>[^/.]+)/eliminar')
    def eliminar_orden(self, request, pk=None, orden_id=None):
        tecnico = self.get_object()
        try:
            mensaje = tecnico.eliminar_orden_trabajo(orden_id)
            return Response({'mensaje': mensaje}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    #GET
    @action(detail=False, methods=['get'], url_path='ordenes-del-taller')
    def ordenes_del_taller(self, request):
        tecnico = self.get_object()
        ordenes = tecnico.get_ordenes_taller()
        serializer = OrdenDeTrabajoSerializer(ordenes, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=["get"])#, url_path="ordenes-del-taller/(?P<orden_id>[^/.]+)")
    def detalle_orden(self, request, pk=None, orden_id=None):
        tecnico = self.get_object()
        orden = tecnico.obtener_orden(orden_id)
        if not orden:
            return Response({"detail": "Orden no encontrada o no pertenece a este taller."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrdenDeTrabajoSerializer(orden)
        return Response(serializer.data)








    
# @action(detail=True, methods=["get"])
    # def ordenes(self, request, pk=None):
    #     tecnico = self.get_object()
    #     ordenes = OrdenDeTrabajo.objects.filter(taller=tecnico.taller)
    #     serializer = OrdenDeTrabajoSerializer(ordenes, many=True)
    #     return Response(serializer.data)
    # @action(detail=True, methods=["post"])
    # def crear_orden(self, request, pk=None):
    #     tecnico = self.get_object()
    #     serializer = OrdenDeTrabajoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(tecnico=tecnico, taller=tecnico.taller)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # @action(detail=True, methods=["patch", "delete"], url_path="ordenes/(?P<orden_id>[^/.]+)")
    # def modificar_orden(self, request, pk=None, orden_id=None):
    #     tecnico = self.get_object()
    #     try:
    #         orden = OrdenDeTrabajo.objects.get(id=orden_id, taller=tecnico.taller)
    #     except OrdenDeTrabajo.DoesNotExist:
    #         return Response({"error": "Orden no encontrada."}, status=404)
    #     if request.method == "PATCH":
    #         serializer = OrdenDeTrabajoSerializer(orden, data=request.data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=400)
    #     if request.method == "DELETE":
    #         orden.delete()
    #         return Response(status=204)
    # def perform_update(self, serializer):
    #     serializer.save()
    # def perform_destroy(self, instance):
    #     if instance.usuario == self.request.user:
    #         instance.delete()
    # #crear vehiculo
    # @action(detail=True, methods=['post'])
    # def crear_vehiculo(self, request, pk=None):
    #     tecnico = self.get_object()
    #     serializer = VehiculoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(creado_por=tecnico)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #  #crear cliente
    # @action(detail=True, methods=['post'])
    # def crear_cliente(self, request, pk=None):
    #     tecnico = self.get_object()
    #     serializer = ClienteSerializer(data=request.data)
    #     if serializer.is_valid():
    #         cliente = serializer.save()
    #         # si querés podés hacer algo con el cliente creado y el técnico, ej: asignar taller etc.
    #         return Response(ClienteSerializer(cliente).data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)