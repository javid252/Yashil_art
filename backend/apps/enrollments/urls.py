from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MyEnrollmentViewSet, SubscriptionPlanViewSet

router = DefaultRouter()
router.register("plans", SubscriptionPlanViewSet, basename="subscription-plan")
router.register("my", MyEnrollmentViewSet, basename="my-enrollment")

urlpatterns = [
    path("", include(router.urls)),
]
