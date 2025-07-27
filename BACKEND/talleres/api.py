from .models import Taller
from rest_framework import viewsets
from .serializers import TallerSerializer
from rest_framework import permissions

class TallerViewSet(viewsets.ModelViewSet):
    queryset = Taller.objects.all()
    permission_classes = [permissions.Allowany] #Si querés restringir el acceso, podés usar otros permisos como IsAuthenticated.
    serializer_class = TallerSerializer
