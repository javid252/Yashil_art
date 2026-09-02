from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AttendanceViewSet, ClassSessionViewSet

router = DefaultRouter()
router.register("sessions", ClassSessionViewSet, basename="class-session")
router.register("", AttendanceViewSet, basename="attendance")

urlpatterns = [
    path("", include(router.urls)),
]
