from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MyWorkshopRegistrationViewSet, WorkshopCategoryViewSet, WorkshopViewSet

router = DefaultRouter()
router.register("categories", WorkshopCategoryViewSet, basename="workshop-category")
router.register("my", MyWorkshopRegistrationViewSet, basename="my-workshop-registration")
router.register("", WorkshopViewSet, basename="workshop")

urlpatterns = [
    path("", include(router.urls)),
]
