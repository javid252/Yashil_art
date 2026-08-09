from django.conf import settings
from django.db import models


class PaymentSettings(models.Model):
    """
    تنظیمات روش‌های پرداخت - الگوی singleton (فقط یک رکورد، مثل PlatformSettings).
    هرکدام از دو روش مستقل فعال/غیرفعال می‌شود.
    """

    # کارت‌به‌کارت
    card_transfer_enabled = models.BooleanField("کارت‌به‌کارت فعال باشد", default=True)
    card_number = models.CharField("شماره کارت", max_length=20, blank=True, help_text="مثلاً 6037-9977-XXXX-XXXX")
    card_holder_name = models.CharField("نام صاحب حساب", max_length=100, blank=True)
    bank_name = models.CharField("نام بانک", max_length=100, blank=True)
    card_transfer_instructions = models.TextField(
        "توضیحات اضافه برای مشتری", blank=True,
        help_text="مثلاً: لطفاً حتماً شماره سفارش را در توضیحات واریز بنویسید.",
    )

    # درگاه آنلاین (زرین‌پال)
    online_gateway_enabled = models.BooleanField("درگاه آنلاین فعال باشد", default=False)
    zarinpal_merchant_id = models.CharField(
        "Merchant ID زرین‌پال", max_length=64, blank=True,
        help_text="از پنل زرین‌پال شما (merchant.zarinpal.com) گرفته می‌شود.",
    )
    zarinpal_sandbox = models.BooleanField(
        "حالت آزمایشی (Sandbox)", default=True,
        help_text="تا زمانی که Merchant ID واقعی و تاییدشده ندارید، این را روشن نگه دارید.",
    )

    class Meta:
        verbose_name = "تنظیمات پرداخت"
        verbose_name_plural = "تنظیمات پرداخت"

    def __str__(self):
        return "تنظیمات پرداخت"

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Payment(models.Model):
    class Method(models.TextChoices):
        CARD_TRANSFER = "card_transfer", "کارت‌به‌کارت"
        ZARINPAL = "zarinpal", "درگاه آنلاین (زرین‌پال)"

    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار پرداخت"
        SUBMITTED = "submitted", "در انتظار بررسی رسید"
        VERIFIED = "verified", "تاییدشده"
        REJECTED = "rejected", "رد شده"
        FAILED = "failed", "ناموفق"

    order = models.ForeignKey(
        "orders.Order", verbose_name="سفارش", related_name="payments", on_delete=models.CASCADE,
    )
    method = models.CharField("روش پرداخت", max_length=20, choices=Method.choices)
    status = models.CharField("وضعیت", max_length=20, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField("مبلغ (تومان)", max_digits=14, decimal_places=0)

    # کارت‌به‌کارت
    receipt_image = models.ImageField("تصویر رسید", upload_to="payment-receipts/", null=True, blank=True)

    # زرین‌پال
    gateway_authority = models.CharField("کد Authority زرین‌پال", max_length=64, blank=True)
    gateway_ref_id = models.CharField("کد پیگیری (RefID)", max_length=64, blank=True)

    admin_note = models.CharField("یادداشت ادمین", max_length=255, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="بررسی‌شده توسط",
        related_name="reviewed_payments", on_delete=models.SET_NULL, null=True, blank=True,
    )
    reviewed_at = models.DateTimeField("تاریخ بررسی", null=True, blank=True)
    created_at = models.DateTimeField("تاریخ ثبت", auto_now_add=True)

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_method_display()} - سفارش #{self.order_id} - {self.get_status_display()}"