# users/serializers.py
from rest_framework import serializers
from .models import Usuario
from .models import AdministradorTecnico

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # Definimos los campos que queremos que se vean en la API
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'telefono', 'direccion', 'role', 'password']
        
        # Configuramos campos extra para seguridad
        extra_kwargs = {
            'password': {'write_only': True} # La contraseña no debe ser visible al pedir datos
        }

    def create(self, validated_data):
        # Este método se asegura de que la contraseña se guarde de forma segura (hasheada)
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class AdministradorTecnicoSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # <-- acá indicás que sea solo escriturapassword = serializers.CharField(write_only=True)  # <-- acá indicás que sea solo escritura
    class Meta:
        model = AdministradorTecnico
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        tecnico = AdministradorTecnico(**validated_data)
        tecnico.set_password(password)
        tecnico.save()
        return tecnico

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance