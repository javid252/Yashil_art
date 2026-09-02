from django.conf import settings
from django.db import models


class Enrollment(models.Model):
    """ثبت‌نام دانشجو در دوره"""

    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار پرداخت"
        ACTIVE = "active", "فعال"
        COMPLETED = "completed", "تکمیل شده"
        CANCELLED = "cancelled", "لغو شده"
        SUSPENDED = "suspended", "معلق"

    class PaymentType(models.TextChoices):
        SINGLE = "single", "تک دوره"
        SUBSCRIPTION = "subscription", "اشتراک ماهانه"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="دانشجو", related_name="enrollments",
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        "courses.Course", verbose_name="دوره", related_name="enrollments",
        on_delete=models.CASCADE,
    )
    status = models.CharField("وضعیت", max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_type = models.CharField("نوع پرداخت", max_length=20, choices=PaymentType.choices, default=PaymentType.SINGLE)

    enrolled_at = models.DateTimeField("تاریخ ثبت‌نام", auto_now_add=True)
    starts_at = models.DateTimeField("تاریخ شروع", null=True, blank=True)
    ends_at = models.DateTimeField("تاریخ پایان", null=True, blank=True)
    completed_at = models.DateTimeField("تاریخ تکمیل", null=True, blank=True)

    subscription_expires = models.DateTimeField("تاریخ انقضای اشتراک", null=True, blank=True)

    notes = models.TextField("یادداشت", blank=True)

    class Meta:
        verbose_name = "ثبت‌نام"
        verbose_name_plural = "ثبت‌نام‌ها"
        ordering = ["-enrolled_at"]
        unique_together = [("user", "course")]

    def __str__(self):
        return f"{self.user} - {self.course.title}"

    @property
    def is_subscription_active(self):
        if self.payment_type != self.PaymentType.SUBSCRIPTION:
            return True
        if not self.subscription_expires:
            return False
        from django.utils import timezone
        return timezone.now() <= self.subscription_expires


class SubscriptionPlan(models.Model):
    """طرح اشتراک ماهانه"""
    name = models.CharField("نام طرح", max_length=100)
    price = models.DecimalField("قیمت ماهانه (تومان)", max_digits=12, decimal_places=0)
    description = models.TextField("توضیحات", blank=True)
    features = models.JSONField("ویژگی‌ها", default=list, blank=True)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        verbose_name = "طرح اشتراک"
        verbose_name_plural = "طرح‌های اشتراک"

    def __str__(self):
        return f"{self.name} - {self.price} تومان"
