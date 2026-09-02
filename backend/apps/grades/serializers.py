from rest_framework import serializers

from .models import Assessment, Grade, FinalGrade


class AssessmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)
    type_display = serializers.CharField(source="get_assessment_type_display", read_only=True)

    class Meta:
        model = Assessment
        fields = [
            "id", "course", "course_title", "title", "description",
            "assessment_type", "type_display", "max_score", "weight",
            "due_date", "is_published",
        ]


class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    assessment_title = serializers.CharField(source="assessment.title", read_only=True)
    percentage = serializers.DecimalField(max_digits=5, decimal_places=1, read_only=True)

    class Meta:
        model = Grade
        fields = [
            "id", "assessment", "assessment_title", "student", "student_name",
            "score", "percentage", "feedback", "graded_at",
        ]


class FinalGradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = FinalGrade
        fields = [
            "id", "course", "course_title", "student", "student_name",
            "total_score", "letter_grade", "passed", "notes", "calculated_at",
        ]
