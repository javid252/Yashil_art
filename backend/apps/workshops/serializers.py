from rest_framework import serializers

from apps.instructors.models import Instructor

from .models import Workshop, WorkshopCategory, WorkshopRegistration


class WorkshopCategorySerializer(serializers.ModelSerializer):
    workshops_count = serializers.SerializerMethodField()

    class Meta:
        model = WorkshopCategory
        fields = ["id", "name", "slug", "icon", "is_active", "order", "workshops_count"]

    def get_workshops_count(self, obj):
        return obj.workshops.filter(is_active=True).count()


class WorkshopListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True, default="")
    instructor_name = serializers.CharField(source="instructor.display_name", read_only=True, default="")
    duration_type_display = serializers.CharField(source="get_duration_type_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    available_spots = serializers.IntegerField(read_only=True)
    duration_display = serializers.CharField(read_only=True)

    class Meta:
        model = Workshop
        fields = [
            "id", "title", "slug", "short_description", "category", "category_name",
            "instructor", "instructor_name", "duration_type", "duration_type_display",
            "status", "status_display", "start_date", "end_date", "start_time", "end_time",
            "sessions_count", "price", "max_participants", "enrolled_count",
            "available_spots", "duration_display", "thumbnail", "cover_image",
            "is_featured", "is_active", "is_online", "location",
        ]


class WorkshopDetailSerializer(serializers.ModelSerializer):
    category = WorkshopCategorySerializer(read_only=True)
    instructor_name = serializers.CharField(source="instructor.display_name", read_only=True, default="")
    duration_type_display = serializers.CharField(source="get_duration_type_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    available_spots = serializers.IntegerField(read_only=True)
    duration_display = serializers.CharField(read_only=True)
    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Workshop
        fields = "__all__"

    def get_is_registered(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.registrations.filter(user=request.user, status="confirmed").exists()
        return False


class WorkshopWriteSerializer(serializers.ModelSerializer):
    """سریالایزر ساخت/ویرایش کارگاه از پنل مدیریت آموزشگاه."""

    category = serializers.PrimaryKeyRelatedField(
        queryset=WorkshopCategory.objects.all(), required=False, allow_null=True,
    )
    instructor = serializers.PrimaryKeyRelatedField(
        queryset=Instructor.objects.all(), required=False, allow_null=True,
    )

    class Meta:
        model = Workshop
        fields = [
            "id", "category", "instructor", "title", "slug", "description",
            "short_description", "duration_type", "status",
            "start_date", "end_date", "start_time", "end_time", "sessions_count",
            "price", "max_participants",
            "thumbnail", "cover_image",
            "prerequisites", "materials", "location", "is_online",
            "is_featured", "is_active",
        ]


class WorkshopRegistrationSerializer(serializers.ModelSerializer):
    workshop_title = serializers.CharField(source="workshop.title", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = WorkshopRegistration
        fields = ["id", "workshop", "workshop_title", "status", "status_display", "registered_at"]
        read_only_fields = ["user", "status"]
