from django.shortcuts import render
from rest_framework import viewsets
from .models import OrdenDeTrabajo
from .serializers import OrdenDeTrabajoSerializer

class OrdenDeTrabajoViewSet(viewsets.ModelViewSet):
    queryset = OrdenDeTrabajo.objects.all()
    serializer_class = OrdenDeTrabajoSerializer

    def get_queryset(self):
        tecnico = self.request.user.tecnico
        return OrdenDeTrabajo.objects.filter(taller=tecnico.taller)

    def perform_create(self, serializer):
        tecnico = self.request.user.tecnico
        serializer.save(tecnico=tecnico, taller=tecnico.taller)

