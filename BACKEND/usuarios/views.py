from datetime import date
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status

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

    @action(detail=True, methods=['post'])#permiso de acceso
    def acceso(self, request, pk=None):
        serializer = PermisoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data_request = serializer.validated_data
        fecha = date.today()
        cliente = self.get_object()
        data = {
            'autoriza': cliente,
            'fecha_autorizacion': fecha,
             **data_request             }
        permiso = cliente.crear_permiso(**data)
        return permiso

#----admintec
class AdministradorTecnicoViewSet(viewsets.ModelViewSet):
    queryset = AdministradorTecnico.objects.all()
    serializer_class = AdministradorTecnicoSerializer

    @action(detail=True, methods=['post'])
    def crear_cliente(self, request, pk=None):
        tecnico = self.get_object()
        serializer = ClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        cliente = tecnico.crear_cliente(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            dni=data.get('dni'),
            telefono=data.get('telefono', ''),
            direccion=data.get('direccion', ''),
        )
        return Response(ClienteSerializer(cliente).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def crear_vehiculo(self, request, pk=None):
        tecnico = self.get_object()
        serializer = VehiculoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vehiculo = tecnico.crear_vehiculo(
            cliente=serializer.validated_data['cliente'],
            modelo=serializer.validated_data['modelo'],
            año=serializer.validated_data['año'],
            dominio=serializer.validated_data['dominio'],
        )
        return Response(VehiculoSerializer(vehiculo).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def crear_orden(self, request, pk=None):
        tecnico = self.get_object()
        serializer = OrdenDeTrabajoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        orden = tecnico.crear_orden_trabajo(
            cliente=serializer.validated_data.get('cliente'),
            vehiculo=serializer.validated_data['vehiculo'],
            observaciones_tecnicas=serializer.validated_data.get('observaciones_tecnicas', ''),
            fecha_siguiente_servicio=serializer.validated_data.get('fecha_siguiente_servicio'),
            fecha_entrega=serializer.validated_data['fecha_entrega'],
            kilometraje=serializer.validated_data['kilometraje'],
            kilometraje_siguiente_servicio=serializer.validated_data.get('kilometraje_siguiente_servicio'),
            mantenimiento=serializer.validated_data.get('mantenimiento', 'preventivo'),
        )
        return Response(OrdenDeTrabajoSerializer(orden).data, status=status.HTTP_201_CREATED)