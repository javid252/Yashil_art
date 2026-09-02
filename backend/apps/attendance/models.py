from django.conf import settings
from django.db import models


class ClassSession(models.Model):
    """جلسه کلاس"""
    course = models.ForeignKey("courses.Course", related_name="sessions", on_delete=models.CASCADE)
    title = models.CharField("عنوان جلسه", max_length=200)
    description = models.TextField("توضیحات", blank=True)
    session_number = models.PositiveIntegerField("شماره جلسه")
    date = models.DateField("تاریخ برگزاری")
    start_time = models.TimeField("ساعت شروع")
    end_time = models.TimeField("ساعت پایان")
    room = models.CharField("اتاق", max_length=100, blank=True)
    materials = models.TextField("مواد آموزشی / تکالیف", blank=True)
    is_completed = models.BooleanField("برگزار شده", default=False)

    class Meta:
        verbose_name = "جلسه کلاس"
        verbose_name_plural = "جلسات کلاس"
        ordering = ["date", "start_time"]
        unique_together = [("course", "session_number")]

    def __str__(self):
        return f"{self.course.title} - جلسه {self.session_number}"


class Attendance(models.Model):
    """حضور و غیاب"""

    class Status(models.TextChoices):
        PRESENT = "present", "حاضر"
        ABSENT = "absent", "غایب"
        LATE = "late", "تاخیر"
        EXCUSED = "excused", "مرخصی"

    session = models.ForeignKey(ClassSession, related_name="attendances", on_delete=models.CASCADE)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="دانشجو", related_name="attendances",
        on_delete=models.CASCADE,
    )
    status = models.CharField("وضعیت", max_length=10, choices=Status.choices, default=Status.PRESENT)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="ثبت شده توسط", related_name="marked_attendances",
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    note = models.CharField("یادداشت", max_length=200, blank=True)
    marked_at = models.DateTimeField("زمان ثبت", auto_now_add=True)

    class Meta:
        verbose_name = "حضور و غیاب"
        verbose_name_plural = "حضور و غیاب‌ها"
        ordering = ["-session__date"]
        unique_together = [("session", "student")]

    def __str__(self):
        return f"{self.student} - {self.session} ({self.get_status_display()})"
