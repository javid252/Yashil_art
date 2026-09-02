from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Instructor
from .serializers import InstructorDetailSerializer, InstructorListSerializer


class InstructorViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filterset_fields = ["is_featured", "is_active"]
    search_fields = ["display_name", "bio"]
    ordering_fields = ["rating", "years_experience", "created_at"]

    def get_queryset(self):
        return Instructor.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return InstructorDetailSerializer
        return InstructorListSerializer
