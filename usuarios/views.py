from django.shortcuts import render

# Create your views here.

# users/views.py
from rest_framework import viewsets
from .models import Usuario
from .serializers import UsuarioSerializer

# ViewSets define el comportamiento de la vista
class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Usuario.objects.all().order_by('-date_joined')
    serializer_class = UsuarioSerializer