from django.conf import settings
from django.db import models
from django.utils.text import slugify

from apps.common.file_uploads import vendor_logo_upload_to


class PlatformSettings(models.Model):
    """
    تنظیمات سراسری سایت. فقط یک رکورد از این مدل باید وجود داشته باشد
    (الگوی singleton) — با متد load() همیشه همان یک رکورد گرفته می‌شود.

    وقتی multivendor_enabled خاموش باشد، سایت دقیقاً مثل حالت تک‌فروشگاهی
    فعلی کار می‌کند و هیچ بخش مربوط به فروشندگان در فرانت‌اند دیده نمی‌شود.
    """

    multivendor_enabled = models.BooleanField("حالت چندفروشندگی فعال باشد", default=False)
    default_commission_percent = models.DecimalField(
        "درصد کارمزد پیش‌فرض پلتفرم", max_digits=5, decimal_places=2,
        null=True, blank=True,
        help_text="در صورت خالی بودن، فعلاً کارمزدی محاسبه نمی‌شود.",
    )

    class Meta:
        verbose_name = "تنظیمات پلتفرم"
        verbose_name_plural = "تنظیمات پلتفرم"

    def __str__(self):
        return "تنظیمات پلتفرم"

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Vendor(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار تایید"
        APPROVED = "approved", "تاییدشده"
        REJECTED = "rejected", "رد شده"
        SUSPENDED = "suspended", "معلق‌شده"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name="کاربر مالک فروشگاه",
        related_name="vendor_profile", on_delete=models.CASCADE,
    )
    store_name = models.CharField("نام فروشگاه", max_length=150)
    store_slug = models.SlugField("اسلاگ فروشگاه", max_length=170, unique=True, blank=True)
    description = models.TextField("توضیحات فروشگاه", blank=True)
    logo = models.ImageField("لوگو", upload_to=vendor_logo_upload_to, null=True, blank=True)
    status = models.CharField("وضعیت", max_length=20, choices=Status.choices, default=Status.PENDING)
    commission_percent = models.DecimalField(
        "درصد کارمزد اختصاصی (اختیاری)", max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="اگر خالی باشد، درصد پیش‌فرض پلتفرم استفاده می‌شود.",
    )
    created_at = models.DateTimeField("تاریخ ثبت‌نام", auto_now_add=True)
    approved_at = models.DateTimeField("تاریخ تایید", null=True, blank=True)

    class Meta:
        verbose_name = "فروشنده"
        verbose_name_plural = "فروشندگان"
        ordering = ["-created_at"]

    def __str__(self):
        return self.store_name

    def save(self, *args, **kwargs):
        if not self.store_slug:
            base_slug = slugify(self.store_name, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Vendor.objects.filter(store_slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.store_slug = slug
        super().save(*args, **kwargs)

    @property
    def is_approved(self):
        return self.status == self.Status.APPROVED