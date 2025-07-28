from django.shortcuts import render
from rest_framework import viewsets
from .models import Vehiculo, Marca, Modelo
from .serializers import VehiculoSerializer, MarcaSerializer, ModeloSerializer


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class MarcaViewSet(viewsets.ModelViewSet):
    queryset= Marca.objects.all()
    serializer_class = MarcaSerializer

class ModeloViewset(viewsets.ModelViewSet):
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer
