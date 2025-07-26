from .models import Taller
from rest_framework import viewsets
from .serializers import TallerSerializer

class TallerViewSet(viewsets.ModelViewSet):
    queryset = Taller.objects.all()
    permission_classes = [permissions.Allowany]
    serializer_class = TallerSerializer
