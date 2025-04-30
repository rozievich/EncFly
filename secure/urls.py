from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomUserModelViewSet, FileModelViewSet

router = DefaultRouter()
router.register("customer", CustomUserModelViewSet, basename="customers")
router.register("file", FileModelViewSet, basename="file")

urlpatterns = [
    path("", include(router.urls))
]
