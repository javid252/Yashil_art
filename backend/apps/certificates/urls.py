from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MyCertificateViewSet, verify_certificate

router = DefaultRouter()
router.register("my", MyCertificateViewSet, basename="my-certificate")

urlpatterns = [
    path("verify/<uuid:unique_code>/", verify_certificate, name="verify-certificate"),
    path("", include(router.urls)),
]
