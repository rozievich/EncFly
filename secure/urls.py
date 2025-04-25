from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomUserModelViewSet

router = DefaultRouter()
router.register("customer", CustomUserModelViewSet, basename="customers")

urlpatterns = [
    path("", include(router.urls))
]
