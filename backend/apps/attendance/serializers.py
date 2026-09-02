from rest_framework import serializers

from .models import ClassSession, Attendance


class ClassSessionSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)
    attendance_count = serializers.SerializerMethodField()

    class Meta:
        model = ClassSession
        fields = [
            "id", "course", "course_title", "title", "description",
            "session_number", "date", "start_time", "end_time",
            "room", "materials", "is_completed", "attendance_count",
        ]

    def get_attendance_count(self, obj):
        return obj.attendances.filter(status="present").count()


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    session_title = serializers.CharField(source="session.title", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Attendance
        fields = [
            "id", "session", "session_title", "student", "student_name",
            "status", "status_display", "note", "marked_at",
        ]


class AttendanceBulkSerializer(serializers.Serializer):
    """ثبت گروهی حضور و غیاب"""
    session_id = serializers.IntegerField()
    records = serializers.ListField(
        child=serializers.DictField(), help_text="لیست [{student_id, status, note}]"
    )
