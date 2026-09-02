from django.contrib import admin

from .models import Assessment, FinalGrade, Grade


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "assessment_type", "max_score", "weight", "due_date", "is_published"]
    list_filter = ["assessment_type", "is_published"]
    search_fields = ["title", "course__title"]
    raw_id_fields = ["course"]


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ["student", "assessment", "score", "percentage", "graded_at"]
    search_fields = ["student__username", "assessment__title"]
    raw_id_fields = ["student", "assessment", "graded_by"]


@admin.register(FinalGrade)
class FinalGradeAdmin(admin.ModelAdmin):
    list_display = ["student", "course", "total_score", "letter_grade", "passed"]
    list_filter = ["passed", "letter_grade"]
    search_fields = ["student__username", "course__title"]
    raw_id_fields = ["student", "course"]
