from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Attendance, ClassSession
from .serializers import AttendanceSerializer, ClassSessionSerializer


class ClassSessionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filterset_fields = ["course", "is_completed", "date"]
    ordering_fields = ["date", "start_time"]

    def get_queryset(self):
        return ClassSession.objects.all()

    serializer_class = ClassSessionSerializer


class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["session", "student", "status"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Attendance.objects.all()
        return Attendance.objects.filter(student=user)
