from rest_framework.routers import DefaultRouter
from .api import TallerViewSet

router = DefaultRouter()
router.register(r'talleres', TallerViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]
