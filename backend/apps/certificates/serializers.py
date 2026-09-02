from rest_framework import serializers

from .models import Certificate, CertificateTemplate


class CertificateTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateTemplate
        fields = ["id", "name", "course", "background_image", "logo", "title_template",
                  "description_template", "is_active"]


class CertificateListSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(read_only=True)
    course_name = serializers.CharField(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id", "certificate_number", "unique_code", "student_name",
            "course_name", "instructor_name", "issued_date", "status",
            "status_display", "final_score", "grade",
        ]


class CertificateDetailSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    verify_url = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = "__all__"

    def get_verify_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/certificates/verify/{obj.unique_code}/")
        return f"/api/certificates/verify/{obj.unique_code}/"
