from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Certificate
from .serializers import CertificateDetailSerializer, CertificateListSerializer


class MyCertificateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CertificateListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Certificate.objects.filter(student=self.request.user, status="issued")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CertificateDetailSerializer
        return CertificateListSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def verify_certificate(request, unique_code):
    """اعتبارسنجی گواهینامه با کد یکتا"""
    try:
        cert = Certificate.objects.get(unique_code=unique_code, status="issued")
        return Response({
            "valid": True,
            "certificate_number": cert.certificate_number,
            "student_name": cert.student_name,
            "course_name": cert.course_name,
            "instructor_name": cert.instructor_name,
            "issued_date": cert.issued_date,
            "grade": cert.grade,
            "final_score": str(cert.final_score) if cert.final_score else None,
        })
    except Certificate.DoesNotExist:
        return Response(
            {"valid": False, "error": "گواهینامه یافت نشد یا نامعتبر است."},
            status=status.HTTP_404_NOT_FOUND,
        )
