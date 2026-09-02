from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Assessment(models.Model):
    """ارزیابی / تکلیف"""

    class Type(models.TextChoices):
        ASSIGNMENT = "assignment", "تکلیف"
        QUIZ = "quiz", "آزمون کوتاه"
        EXAM = "exam", "امتحان"
        PROJECT = "project", "پروژه"
        PARTICIPATION = "participation", "مشارکت"

    course = models.ForeignKey("courses.Course", related_name="assessments", on_delete=models.CASCADE)
    title = models.CharField("عنوان", max_length=200)
    description = models.TextField("توضیحات", blank=True)
    assessment_type = models.CharField("نوع", max_length=20, choices=Type.choices)
    max_score = models.PositiveIntegerField("حداکثر نمره", default=100)
    weight = models.PositiveIntegerField(
        "وزن (درصد)", default=10,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    due_date = models.DateTimeField("تاریخ تحویل", null=True, blank=True)
    is_published = models.BooleanField("منتشر شده", default=False)

    class Meta:
        verbose_name = "ارزیابی"
        verbose_name_plural = "ارزیابی‌ها"
        ordering = ["due_date"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Grade(models.Model):
    """نمره دانشجو"""
    assessment = models.ForeignKey(Assessment, related_name="grades", on_delete=models.CASCADE)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="دانشجو", related_name="grades",
        on_delete=models.CASCADE,
    )
    score = models.DecimalField(
        "نمره", max_digits=6, decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    feedback = models.TextField("بازخورد", blank=True)
    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="ثبت شده توسط", related_name="graded_assessments",
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    graded_at = models.DateTimeField("تاریخ ثبت نمره", auto_now_add=True)
    updated_at = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "نمره"
        verbose_name_plural = "نمرات"
        unique_together = [("assessment", "student")]

    def __str__(self):
        return f"{self.student} - {self.assessment.title}: {self.score}"

    @property
    def percentage(self):
        if self.assessment.max_score:
            return round((self.score / self.assessment.max_score) * 100, 1)
        return 0


class FinalGrade(models.Model):
    """نمره نهایی دوره"""

    class LetterGrade(models.TextChoices):
        A_PLUS = "A+", "عالی+"
        A = "A", "عالی"
        B_PLUS = "B+", "خوب+"
        B = "B", "خوب"
        C_PLUS = "C+", "متوسط+"
        C = "C", "متوسط"
        D = "D", "قابل قبول"
        F = "F", "مردود"

    course = models.ForeignKey("courses.Course", related_name="final_grades", on_delete=models.CASCADE)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="دانشجو", related_name="final_grades",
        on_delete=models.CASCADE,
    )
    enrollment = models.OneToOneField(
        "enrollments.Enrollment", verbose_name="ثبت‌نام", related_name="final_grade",
        on_delete=models.CASCADE, null=True, blank=True,
    )
    total_score = models.DecimalField("نمره نهایی", max_digits=6, decimal_places=2, default=0)
    letter_grade = models.CharField("نمره حروفی", max_length=5, choices=LetterGrade.choices, blank=True)
    passed = models.BooleanField("قبول شده", default=False)
    notes = models.TextField("یادداشت", blank=True)
    calculated_at = models.DateTimeField("تاریخ محاسبه", auto_now_add=True)

    class Meta:
        verbose_name = "نمره نهایی"
        verbose_name_plural = "نمرات نهایی"
        unique_together = [("course", "student")]

    def __str__(self):
        return f"{self.student} - {self.course.title}: {self.total_score}"
