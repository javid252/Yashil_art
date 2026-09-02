import uuid

from django.conf import settings
from django.db import models


class CertificateTemplate(models.Model):
    """قالب گواهینامه"""
    name = models.CharField("نام قالب", max_length=100)
    course = models.ForeignKey(
        "courses.Course", verbose_name="دوره مرتبط", related_name="certificate_templates",
        on_delete=models.CASCADE, null=True, blank=True,
        help_text="اگر خالی باشد، قالب عمومی است",
    )
    background_image = models.ImageField("تصویر پس‌زمینه", upload_to="certificates/templates/")
    logo = models.ImageField("لوگو", upload_to="certificates/logos/", null=True, blank=True)
    title_template = models.CharField(
        "عنوان قالب", max_length=200, default="گواهینامه پایان دوره",
        help_text="از {student_name} و {course_name} می‌توانید استفاده کنید",
    )
    description_template = models.TextField(
        "متن قالب", blank=True,
        default="این گواهینامه به شرح زیر صادر می‌گردد:",
    )
    signature_left = models.ImageField("امضای چپ", upload_to="certificates/signatures/", null=True, blank=True)
    signature_right = models.ImageField("امضای راست", upload_to="certificates/signatures/", null=True, blank=True)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        verbose_name = "قالب گواهینامه"
        verbose_name_plural = "قالب‌های گواهینامه"

    def __str__(self):
        return self.name


class Certificate(models.Model):
    """گواهینامه صادر شده"""

    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار تایید"
        ISSUED = "issued", "صادر شده"
        REVOKED = "revoked", "لغو شده"

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="دانشجو", related_name="certificates",
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        "courses.Course", verbose_name="دوره", related_name="certificates",
        on_delete=models.CASCADE,
    )
    enrollment = models.OneToOneField(
        "enrollments.Enrollment", verbose_name="ثبت‌نام", related_name="certificate",
        on_delete=models.CASCADE, null=True, blank=True,
    )
    template = models.ForeignKey(
        CertificateTemplate, verbose_name="قالب", related_name="certificates",
        on_delete=models.SET_NULL, null=True, blank=True,
    )

    certificate_number = models.CharField("شماره گواهینامه", max_length=50, unique=True, blank=True)
    unique_code = models.UUIDField("کد یکتا", default=uuid.uuid4, unique=True)

    student_name = models.CharField("نام دانشجو", max_length=200)
    course_name = models.CharField("نام دوره", max_length=200)
    instructor_name = models.CharField("نام استاد", max_length=200, blank=True)

    issued_date = models.DateField("تاریخ صدور")
    completion_date = models.DateField("تاریخ اتمام دوره", null=True, blank=True)

    final_score = models.DecimalField("نمره نهایی", max_digits=6, decimal_places=2, null=True, blank=True)
    grade = models.CharField("نمره حروفی", max_length=5, blank=True)
    hours_completed = models.PositiveIntegerField("ساعات تکمیل شده", default=0)

    status = models.CharField("وضعیت", max_length=20, choices=Status.choices, default=Status.PENDING)

    pdf_file = models.FileField("فایل PDF", upload_to="certificates/pdfs/", null=True, blank=True)

    notes = models.TextField("یادداشت", blank=True)
    issued_at = models.DateTimeField("تاریخ صدور", auto_now_add=True)
    revoked_at = models.DateTimeField("تاریخ لغو", null=True, blank=True)
    revoke_reason = models.TextField("دلیل لغو", blank=True)

    class Meta:
        verbose_name = "گواهینامه"
        verbose_name_plural = "گواهینامه‌ها"
        ordering = ["-issued_at"]

    def __str__(self):
        return f"{self.student_name} - {self.course_name} ({self.certificate_number})"

    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.certificate_number = f"YA-{self.issued_date.year if self.issued_date else '0000'}-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
