from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Enrollment, SubscriptionPlan
from .serializers import (
    EnrollmentCreateSerializer,
    EnrollmentDetailSerializer,
    EnrollmentListSerializer,
    SubscriptionPlanSerializer,
)


class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated]


class MyEnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EnrollmentListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return EnrollmentDetailSerializer
        return EnrollmentListSerializer

    @action(detail=False, methods=["post"])
    def enroll(self, request):
        serializer = EnrollmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from apps.courses.models import Course
        try:
            course = Course.objects.get(id=serializer.validated_data["course_id"], is_active=True)
        except Course.DoesNotExist:
            return Response({"error": "دوره یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        if course.is_full:
            return Response({"error": "ظرفیت دوره تکمیل است."}, status=status.HTTP_400_BAD_REQUEST)

        if Enrollment.objects.filter(user=request.user, course=course, status__in=["active", "pending"]).exists():
            return Response({"error": "شما قبلاً در این دوره ثبت‌نام کرده‌اید."}, status=status.HTTP_400_BAD_REQUEST)

        enrollment = Enrollment.objects.create(
            user=request.user,
            course=course,
            payment_type=serializer.validated_data["payment_type"],
        )
        course.enrolled_count += 1
        course.save(update_fields=["enrolled_count"])

        return Response(EnrollmentDetailSerializer(enrollment).data, status=status.HTTP_201_CREATED)
