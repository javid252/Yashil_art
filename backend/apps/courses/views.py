from rest_framework import filters, viewsets

from apps.access.permissions import IsEducationAdmin

from .models import Course, CourseCategory
from .serializers import (
    CourseCategorySerializer,
    CourseDetailSerializer,
    CourseListSerializer,
    CourseWriteSerializer,
)


class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    permission_classes = [IsEducationAdmin]
    pagination_class = None

    def get_queryset(self):
        qs = CourseCategory.objects.all()
        user = self.request.user
        if user and user.is_authenticated and user.is_staff:
            return qs
        return qs.filter(is_active=True)


class CourseViewSet(viewsets.ModelViewSet):
    """دوره‌ها: خواندن عمومی، نوشتن (ساخت/ویرایش/حذف) فقط مدیر آموزشگاه/مدیرکل."""

    permission_classes = [IsEducationAdmin]
    filterset_fields = ["level", "pricing_type", "is_featured", "category"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "price", "enrolled_count", "title"]

    def get_queryset(self):
        qs = Course.objects.all()
        user = self.request.user
        # پنل مدیریت همه دوره‌ها (از جمله پیش‌نویس‌ها) را می‌بیند
        if user and user.is_authenticated and user.is_staff:
            return qs
        return qs.filter(is_active=True, status="published")

    def get_serializer_class(self):
        if self.action == "list":
            return CourseListSerializer
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseWriteSerializer