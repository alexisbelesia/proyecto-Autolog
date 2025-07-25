# users/serializers.py
from rest_framework import serializers
from .models import Usuario

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