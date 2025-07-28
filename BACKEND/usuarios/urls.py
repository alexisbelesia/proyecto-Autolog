#usuarios/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet

# Creamos un router y registramos nuestro viewset
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'tecnicos', AdministradorTecnicoViewSet)

# Las URLs de la API son determinadas automáticamente por el router
urlpatterns = [
    path('', include(router.urls)),
]