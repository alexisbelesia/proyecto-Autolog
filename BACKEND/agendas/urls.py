from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgendaViewSet

# El router genera automáticamente las URLs para el ViewSet.
router = DefaultRouter()
router.register(r'agendas', AgendaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]