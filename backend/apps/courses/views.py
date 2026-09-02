from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Course, CourseCategory
from .serializers import CourseCategorySerializer, CourseDetailSerializer, CourseListSerializer


class CourseCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CourseCategory.objects.filter(is_active=True)
    serializer_class = CourseCategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filterset_fields = ["level", "pricing_type", "is_featured", "category"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "price", "enrolled_count", "title"]

    def get_queryset(self):
        return Course.objects.filter(is_active=True, status="published")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseListSerializer
