from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.access.permissions import IsEducationAdmin

from .models import Workshop, WorkshopCategory, WorkshopRegistration
from .serializers import (
    WorkshopCategorySerializer,
    WorkshopDetailSerializer,
    WorkshopListSerializer,
    WorkshopRegistrationSerializer,
    WorkshopWriteSerializer,
)


class WorkshopCategoryViewSet(viewsets.ModelViewSet):
    queryset = WorkshopCategory.objects.all()
    serializer_class = WorkshopCategorySerializer
    permission_classes = [IsEducationAdmin]
    pagination_class = None

    def get_queryset(self):
        qs = WorkshopCategory.objects.all()
        user = self.request.user
        if user and user.is_authenticated and user.is_staff:
            return qs
        return qs.filter(is_active=True)


class WorkshopViewSet(viewsets.ModelViewSet):
    """کارگاه‌ها: خواندن عمومی، نوشتن فقط مدیر آموزشگاه/مدیرکل."""

    permission_classes = [IsEducationAdmin]
    filterset_fields = ["category", "duration_type", "status", "is_featured", "is_online"]
    search_fields = ["title", "description"]
    ordering_fields = ["start_date", "price", "created_at"]

    def get_queryset(self):
        qs = Workshop.objects.all()
        user = self.request.user
        if user and user.is_authenticated and user.is_staff:
            return qs
        return qs.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "list":
            return WorkshopListSerializer
        if self.action == "retrieve":
            return WorkshopDetailSerializer
        return WorkshopWriteSerializer

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        workshop = self.get_object()
        if workshop.is_full:
            return Response({"error": "ظرفیت کارگاه تکمیل است."}, status=status.HTTP_400_BAD_REQUEST)

        registration, created = WorkshopRegistration.objects.get_or_create(
            workshop=workshop, user=request.user,
            defaults={"status": "confirmed"},
        )
        if not created:
            return Response({"error": "شما قبلاً ثبت‌نام کرده‌اید."}, status=status.HTTP_400_BAD_REQUEST)

        workshop.enrolled_count += 1
        workshop.save(update_fields=["enrolled_count"])

        return Response(WorkshopRegistrationSerializer(registration).data, status=status.HTTP_201_CREATED)


class MyWorkshopRegistrationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WorkshopRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WorkshopRegistration.objects.filter(user=self.request.user)