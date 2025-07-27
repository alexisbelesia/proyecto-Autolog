from django.shortcuts import render
from rest_framework import viewsets
from .models import Taller
from .serializers import TallerSerializer

class TallerViewSet(viewsets.ModelViewSet):
    queryset = Taller.objects.all()
    serializer_class = TallerSerializer
