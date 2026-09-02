from django.contrib import admin

from .models import Attendance, ClassSession


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ["course", "session_number", "title", "date", "start_time", "end_time", "is_completed"]
    list_filter = ["is_completed", "date"]
    search_fields = ["title", "course__title"]
    raw_id_fields = ["course"]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["student", "session", "status", "marked_by", "marked_at"]
    list_filter = ["status"]
    search_fields = ["student__username", "session__title"]
    raw_id_fields = ["student", "session", "marked_by"]
