from rest_framework.routers import DefaultRouter
from .api import TallerViewSet
from django.urls import path, include
from django.contrib import admin


router = DefaultRouter()
router.register(r'talleres', TallerViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]
