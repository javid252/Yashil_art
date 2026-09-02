from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Assessment, FinalGrade, Grade
from .serializers import AssessmentSerializer, FinalGradeSerializer, GradeSerializer


class AssessmentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filterset_fields = ["course", "assessment_type", "is_published"]
    serializer_class = AssessmentSerializer

    def get_queryset(self):
        return Assessment.objects.filter(is_published=True)


class GradeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["assessment", "student"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Grade.objects.all()
        return Grade.objects.filter(student=user)


class FinalGradeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FinalGradeSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["course", "student"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return FinalGrade.objects.all()
        return FinalGrade.objects.filter(student=user)
