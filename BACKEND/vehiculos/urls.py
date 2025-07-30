from rest_framework.routers import DefaultRouter
from .views import VehiculoViewSet, MarcaViewSet, ModeloViewset


router = DefaultRouter()
router.register('vehiculo', VehiculoViewSet)
router.register('marca', MarcaViewSet)
router.register('modelo', ModeloViewset)

urlpatterns = router.urls