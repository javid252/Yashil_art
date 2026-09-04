from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Instructor, InstructorPortfolio

User = get_user_model()


class InstructorPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorPortfolio
        fields = ["id", "title", "description", "image", "year", "order"]


class InstructorListSerializer(serializers.ModelSerializer):
    courses_count = serializers.SerializerMethodField()

    class Meta:
        model = Instructor
        fields = [
            "id", "display_name", "slug", "bio", "specializations", "photo",
            "years_experience", "students_count", "rating",
            "is_active", "is_featured", "courses_count",
        ]

    def get_courses_count(self, obj):
        return obj.courses.filter(is_active=True).count()


class InstructorWriteSerializer(serializers.ModelSerializer):
    """سریالایزر ساخت/ویرایش استاد از پنل مدیریت آموزشگاه."""

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True,
    )
    specializations = serializers.JSONField(required=False)

    class Meta:
        model = Instructor
        fields = [
            "id", "user", "display_name", "bio", "specializations",
            "photo", "resume", "website", "instagram", "telegram",
            "years_experience", "students_count", "rating",
            "is_active", "is_featured",
        ]


class InstructorDetailSerializer(serializers.ModelSerializer):
    portfolio = InstructorPortfolioSerializer(many=True, read_only=True)
    courses = serializers.SerializerMethodField()
    courses_count = serializers.SerializerMethodField()

    class Meta:
        model = Instructor
        fields = "__all__"

    def get_courses(self, obj):
        from apps.courses.serializers import CourseListSerializer
        courses = obj.courses.filter(is_active=True)
        return CourseListSerializer(courses, many=True, context=self.context).data

    def get_courses_count(self, obj):
        return obj.courses.filter(is_active=True).count()
