from datetime import date
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied

from .models import Usuario,Cliente,AdministradorTecnico
from .serializers import UsuarioSerializer,ClienteSerializer,AdministradorTecnicoSerializer,PermisoSerializer

from vehiculos.serializers import VehiculoSerializer
from ordenes.serializers import OrdenDeTrabajoSerializer

# ViewSets define el comportamiento de la vista
class UsuarioViewSet(viewsets.ModelViewSet):

    queryset = Usuario.objects.all().order_by('-date_joined')
    serializer_class = UsuarioSerializer

#----cliente
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

            historial = vehiculo.historial
            serializer = OrdenDeTrabajoSerializer(historial,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
          
            


#----admintec
class AdministradorTecnicoViewSet(viewsets.ModelViewSet):
    queryset = AdministradorTecnico.objects.all()
    serializer_class = AdministradorTecnicoSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        # El técnico solo puede acceder a su propio perfil (objeto AdministradorTecnico)
        return AdministradorTecnico.objects.filter(usuario=self.request.user)
    #crud OT desde tecnico (faltaria que puedar leer OT de otros talleres)
    @action(detail=True, methods=["get"])
    def ordenes(self, request, pk=None):
        tecnico = self.get_object()
        ordenes = OrdenDeTrabajo.objects.filter(taller=tecnico.taller)
        serializer = OrdenDeTrabajoSerializer(ordenes, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=["post"])
    def crear_orden(self, request, pk=None):
        tecnico = self.get_object()
        serializer = OrdenDeTrabajoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tecnico=tecnico, taller=tecnico.taller)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=["patch", "delete"], url_path="ordenes/(?P<orden_id>[^/.]+)")
    def modificar_orden(self, request, pk=None, orden_id=None):
        tecnico = self.get_object()
        try:
            orden = OrdenDeTrabajo.objects.get(id=orden_id, taller=tecnico.taller)
        except OrdenDeTrabajo.DoesNotExist:
            return Response({"error": "Orden no encontrada."}, status=404)
        if request.method == "PATCH":
            serializer = OrdenDeTrabajoSerializer(orden, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        if request.method == "DELETE":
            orden.delete()
            return Response(status=204)
    def perform_update(self, serializer):
        serializer.save()
    def perform_destroy(self, instance):
        if instance.usuario == self.request.user:
            instance.delete()
    #crear vehiculo
    @action(detail=True, methods=['post'])
    def crear_vehiculo(self, request, pk=None):
        tecnico = self.get_object()
        serializer = VehiculoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creado_por=tecnico)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
     #crear cliente
    @action(detail=True, methods=['post'])
    def crear_cliente(self, request, pk=None):
        tecnico = self.get_object()
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            cliente = serializer.save()
            # si querés podés hacer algo con el cliente creado y el técnico, ej: asignar taller etc.
            return Response(ClienteSerializer(cliente).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  







#----------------------------
    # @action(detail=True, methods=['post'])
    # def crear_cliente(self, request, pk=None):
    #     tecnico = self.get_object()
    #     serializer = ClienteSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     data = serializer.validated_data
    #     cliente = tecnico.crear_cliente(
    #         username=data['username'],
    #         email=data['email'],
    #         password=data['password'],
    #         first_name=data.get('first_name', ''),
    #         last_name=data.get('last_name', ''),
    #         dni=data.get('dni'),
    #         telefono=data.get('telefono', ''),
    #         direccion=data.get('direccion', ''),
    #     )
    #     return Response(ClienteSerializer(cliente).data, status=status.HTTP_201_CREATED)
    # @action(detail=True, methods=['post'])
    # def crear_vehiculo(self, request, pk=None):
    #     tecnico = self.get_object()
    #     serializer = VehiculoSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     vehiculo = tecnico.crear_vehiculo(
    #         cliente=serializer.validated_data['cliente'],
    #         modelo=serializer.validated_data['modelo'],
    #         año=serializer.validated_data['año'],
    #         dominio=serializer.validated_data['dominio'],
    #     )
    #     return Response(VehiculoSerializer(vehiculo).data, status=status.HTTP_201_CREATED)

    #Crud OT desde tecnico
    # @action(detail=True, methods=['post'])
    # def crear_orden(self, request, pk=None):
    #     tecnico = self.get_object()
    #     serializer = OrdenDeTrabajoSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     orden = tecnico.crear_orden_trabajo(
    #         cliente=serializer.validated_data.get('cliente'),
    #         vehiculo=serializer.validated_data['vehiculo'],
    #         observaciones_tecnicas=serializer.validated_data.get('observaciones_tecnicas', ''),
    #         fecha_siguiente_servicio=serializer.validated_data.get('fecha_siguiente_servicio'),
    #         fecha_entrega=serializer.validated_data['fecha_entrega'],
    #         kilometraje=serializer.validated_data['kilometraje'],
    #         kilometraje_siguiente_servicio=serializer.validated_data.get('kilometraje_siguiente_servicio'),
    #         mantenimiento=serializer.validated_data.get('mantenimiento', 'preventivo'),
    #     )
    #     return Response(OrdenDeTrabajoSerializer(orden).data, status=status.HTTP_201_CREATED)
