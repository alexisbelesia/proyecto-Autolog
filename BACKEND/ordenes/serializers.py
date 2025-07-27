from rest_framework import serializers
from .models import OrdenDeTrabajo



class OrdenDeTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenDeTrabajo
        fields = '__all__'