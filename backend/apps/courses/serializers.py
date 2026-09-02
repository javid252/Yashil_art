from rest_framework import serializers

from .models import Course, CourseCategory, CourseGallery, CourseSchedule


class CourseCategorySerializer(serializers.ModelSerializer):
    course_count = serializers.SerializerMethodField()

    class Meta:
        model = CourseCategory
        fields = ["id", "name", "slug", "description", "icon", "image", "is_active", "order", "course_count"]

    def get_course_count(self, obj):
        return obj.courses.filter(is_active=True).count()


class CourseScheduleSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(source="get_day_of_week_display", read_only=True)

    class Meta:
        model = CourseSchedule
        fields = ["id", "day_of_week", "day_display", "start_time", "end_time", "room", "is_active"]


class CourseGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseGallery
        fields = ["id", "image", "caption", "order"]


class CourseListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True, default="")
    instructor_name = serializers.CharField(source="instructor.display_name", read_only=True, default="")
    level_display = serializers.CharField(source="get_level_display", read_only=True)
    final_price = serializers.DecimalField(max_digits=12, decimal_places=0, read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)
    available_spots = serializers.IntegerField(read_only=True)
    total_sessions = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", "title", "slug", "short_description", "level", "level_display",
            "status", "pricing_type", "price", "discount_price", "final_price",
            "discount_percent", "duration_weeks", "sessions_per_week",
            "session_duration_minutes", "max_students", "enrolled_count",
            "available_spots", "total_sessions", "thumbnail", "cover_image",
            "is_featured", "is_active", "created_at",
            "category", "category_name", "instructor", "instructor_name",
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CourseCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=CourseCategory.objects.all(), source="category", write_only=True, required=False,
    )
    schedules = CourseScheduleSerializer(many=True, read_only=True)
    gallery_images = CourseGallerySerializer(many=True, read_only=True)
    instructor_name = serializers.CharField(source="instructor.display_name", read_only=True, default="")
    instructor_slug = serializers.CharField(source="instructor.slug", read_only=True, default="")
    level_display = serializers.CharField(source="get_level_display", read_only=True)
    final_price = serializers.DecimalField(max_digits=12, decimal_places=0, read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)
    available_spots = serializers.IntegerField(read_only=True)
    total_sessions = serializers.IntegerField(read_only=True)
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_enrolled(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.enrollments.filter(user=request.user, status__in=["active", "completed"]).exists()
        return False
