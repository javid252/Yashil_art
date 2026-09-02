from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AssessmentViewSet, FinalGradeViewSet, GradeViewSet

router = DefaultRouter()
router.register("assessments", AssessmentViewSet, basename="assessment")
router.register("my", GradeViewSet, basename="my-grade")
router.register("final", FinalGradeViewSet, basename="final-grade")

urlpatterns = [
    path("", include(router.urls)),
]
