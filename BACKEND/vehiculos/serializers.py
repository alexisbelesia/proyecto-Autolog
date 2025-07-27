from rest_framework import serializers
from .models import Vehiculo, Marca, Modelo

class VehiculoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class ModeloSerializers (serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = '__all__'

class MarcaSerializers (serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'