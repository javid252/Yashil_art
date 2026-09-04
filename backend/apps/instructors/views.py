from rest_framework import viewsets

from apps.access.permissions import IsEducationAdmin

from .models import Instructor
from .serializers import InstructorDetailSerializer, InstructorListSerializer, InstructorWriteSerializer


class InstructorViewSet(viewsets.ModelViewSet):
    """اساتید: خواندن عمومی، نوشتن فقط مدیر آموزشگاه/مدیرکل."""

    permission_classes = [IsEducationAdmin]
    filterset_fields = ["is_featured", "is_active"]
    search_fields = ["display_name", "bio"]
    ordering_fields = ["rating", "years_experience", "created_at"]

    def get_queryset(self):
        qs = Instructor.objects.all()
        user = self.request.user
        if user and user.is_authenticated and user.is_staff:
            return qs
        return qs.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "list":
            return InstructorListSerializer
        if self.action == "retrieve":
            return InstructorDetailSerializer
        return InstructorWriteSerializer