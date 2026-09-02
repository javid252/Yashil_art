from rest_framework import serializers

from .models import Enrollment, SubscriptionPlan


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ["id", "name", "price", "description", "features", "is_active"]


class EnrollmentListSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)
    course_thumbnail = serializers.ImageField(source="course.thumbnail", read_only=True)
    course_slug = serializers.CharField(source="course.slug", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    payment_type_display = serializers.CharField(source="get_payment_type_display", read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            "id", "course", "course_title", "course_thumbnail", "course_slug",
            "status", "status_display", "payment_type", "payment_type_display",
            "enrolled_at", "starts_at", "ends_at", "completed_at",
            "subscription_expires", "is_subscription_active",
        ]


class EnrollmentDetailSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)
    course_slug = serializers.CharField(source="course.slug", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Enrollment
        fields = "__all__"


class EnrollmentCreateSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    payment_type = serializers.ChoiceField(choices=Enrollment.PaymentType.choices, default=Enrollment.PaymentType.SINGLE)
