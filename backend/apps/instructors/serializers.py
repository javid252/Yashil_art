from rest_framework import serializers

from .models import Instructor, InstructorPortfolio


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
