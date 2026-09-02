from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import InstructorViewSet

router = DefaultRouter()
router.register("", InstructorViewSet, basename="instructor")

urlpatterns = [
    path("", include(router.urls)),
]
