# users/serializers.py
from rest_framework import serializers
from .models import Usuario,AdministradorTecnico, Cliente, PermisoDeAcceso
from talleres.models.taller import Taller


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username','first_name','last_name','email','password','dni','telefono','direccion']
        # Configuramos campos extra para seguridad
        extra_kwargs = {
            'password': {'write_only': True} # La contraseña no debe ser visible al pedir datos
        }

    def create(self, validated_data):
        # Este método se asegura de que la contraseña se guarde de forma segura (hasheada)
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None: #si permitimos que sea None despues no vamos a poder usar authenticate(), VERR MAS ADELANTE
            instance.set_password(password) #este metodo heredado de abstractuser hace el hash
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance,attr,value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
class ClienteSerializer(UsuarioSerializer): 
    usuarios_autorizados = serializers.SerializerMethodField()
    talleres_autorizados = serializers.SerializerMethodField()
    class Meta(UsuarioSerializer.Meta):
        model = Cliente
        fields =(UsuarioSerializer.Meta.fields)+['usuarios_autorizados','talleres_autorizados']
    
    def get_usuarios_autorizados(self, obj):
        return obj.usuarios_autorizados
    
    def get_talleres_autorizados(self, obj):
        return obj.talleres_autorizados
    



###############Heredar UsuarioSerializer############################3
class AdministradorTecnicoSerializer(UsuarioSerializer):
    taller = serializers.PrimaryKeyRelatedField(queryset=Taller.objects.all())

    class Meta(UsuarioSerializer.Meta):
        model = AdministradorTecnico
        fields = UsuarioSerializer.Meta.fields + ['taller']
    
class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermisoDeAcceso
        fields = ['vehiculo_autorizado','usuario_autorizado', 'taller_autorizado']
        