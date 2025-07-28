from rest_framework import serializers
from .models import Vehiculo, Marca, Modelo

class VehiculoSerializer(serializers.ModelSerializer):

    marca = serializers.SerializerMethodField(), 
    # Este campo no existe directamente en el modelo como atributo o columna de base de datos.
    # Es un campo de modelo, y modelo si es fk en vehiculo
    # Al usar serializers.SerializerMethodField(), DRF buscará un método llamado get_marca(self, obj)
    # para obtener su valor durante la serialización.
    # El parámetro obj es una instancia del modelo Vehiculo (el que se está serializando).
    # En este caso, el valor se obtiene a través de la propiedad @property marca definida en el modelo Vehiculo,
    # que retorna self.modelo.marca (es decir, accede a un campo relacionado).
    

    class Meta:
        model = Vehiculo
        fields = '__all__'
    
    def get_marca(self, obj):
        return obj.marca

class ModeloSerializer (serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = '__all__'

class MarcaSerializer (serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'