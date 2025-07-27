from django.shortcuts import render
from rest_framework import viewsets
from .models import Vehiculo, Marca, Modelo
from .serializers import VehiculoSerializers, MarcaSerializers, ModeloSerializers


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializers

class MarcaViewSet(viewsets.ModelViewSet):
    queryset= Marca.objects.all()
    serializer_class = MarcaSerializers

class ModeloViewset(viewsets.ModelViewSet):
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializers
