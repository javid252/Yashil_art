from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Workshop, WorkshopCategory, WorkshopRegistration
from .serializers import (
    WorkshopCategorySerializer,
    WorkshopDetailSerializer,
    WorkshopListSerializer,
    WorkshopRegistrationSerializer,
)


class WorkshopCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkshopCategory.objects.filter(is_active=True)
    serializer_class = WorkshopCategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None


class WorkshopViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filterset_fields = ["category", "duration_type", "status", "is_featured", "is_online"]
    search_fields = ["title", "description"]
    ordering_fields = ["start_date", "price", "created_at"]

    def get_queryset(self):
        return Workshop.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return WorkshopDetailSerializer
        return WorkshopListSerializer

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
