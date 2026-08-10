from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    کاربر سفارشی سامانه. ایمیل به عنوان فیلد یکتا استفاده می‌شود
    تا هم برای ورود و هم بازیابی رمز عبور قابل استفاده باشد.
    """

    email = models.EmailField("ایمیل", unique=True)
    phone_number = models.CharField("شماره موبایل", max_length=15, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username


class SocialAuthSettings(models.Model):
    """
    تنظیمات روش‌های ورود جایگزین - الگوی singleton (مثل PlatformSettings و
    PaymentSettings). هرکدام مستقل از پنل ادمین فعال/غیرفعال می‌شود.
    """

    google_enabled = models.BooleanField("ورود با گوگل فعال باشد", default=False)
    google_client_id = models.CharField(
        "Google Client ID", max_length=255, blank=True,
        help_text="از Google Cloud Console (APIs & Services → Credentials) گرفته می‌شود. این مقدار عمومی است.",
    )

    telegram_enabled = models.BooleanField("ورود با تلگرام فعال باشد", default=False)
    telegram_bot_username = models.CharField(
        "یوزرنیم ربات تلگرام", max_length=64, blank=True,
        help_text="بدون @ ، مثلاً YashilArtBot - این مقدار عمومی است.",
    )
    telegram_bot_token = models.CharField(
        "توکن ربات تلگرام", max_length=100, blank=True,
        help_text="از @BotFather گرفته می‌شود - این مقدار محرمانه است و هرگز به فرانت‌اند ارسال نمی‌شود.",
    )

    sms_otp_enabled = models.BooleanField("ورود با کد پیامکی فعال باشد", default=False)
    sms_provider = models.CharField(
        "سرویس‌دهنده پیامک", max_length=30, default="kavenegar",
        help_text="فعلاً فقط kavenegar پیاده‌سازی شده.",
    )
    sms_api_key = models.CharField("کلید API سرویس پیامک", max_length=100, blank=True)
    sms_sender_line = models.CharField("شماره خط ارسال (اختیاری)", max_length=20, blank=True)

    class Meta:
        verbose_name = "تنظیمات ورود اجتماعی"
        verbose_name_plural = "تنظیمات ورود اجتماعی"

    def __str__(self):
        return "تنظیمات ورود اجتماعی"

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SocialIdentity(models.Model):
    """پیوند بین یک کاربر سامانه و هویت او در یک سرویس بیرونی (گوگل/تلگرام)."""

    class Provider(models.TextChoices):
        GOOGLE = "google", "گوگل"
        TELEGRAM = "telegram", "تلگرام"
        PHONE = "phone", "شماره موبایل"

    user = models.ForeignKey(User, verbose_name="کاربر", related_name="social_identities", on_delete=models.CASCADE)
    provider = models.CharField("سرویس", max_length=20, choices=Provider.choices)
    provider_user_id = models.CharField("شناسه کاربر در سرویس", max_length=191)
    extra_data = models.JSONField("اطلاعات تکمیلی", default=dict, blank=True)
    created_at = models.DateTimeField("تاریخ اتصال", auto_now_add=True)

    class Meta:
        verbose_name = "هویت اجتماعی"
        verbose_name_plural = "هویت‌های اجتماعی"
        unique_together = [("provider", "provider_user_id")]

    def __str__(self):
        return f"{self.get_provider_display()} - {self.user}"


class PhoneOTP(models.Model):
    """کد یک‌بارمصرف پیامکی برای ورود/ثبت‌نام با شماره موبایل."""

    phone_number = models.CharField("شماره موبایل", max_length=15, db_index=True)
    code = models.CharField("کد", max_length=6)
    is_used = models.BooleanField("استفاده‌شده", default=False)
    attempts = models.PositiveSmallIntegerField("تعداد تلاش‌های ناموفق", default=0)
    expires_at = models.DateTimeField("انقضا")
    created_at = models.DateTimeField("تاریخ ارسال", auto_now_add=True)

    class Meta:
        verbose_name = "کد یک‌بارمصرف پیامکی"
        verbose_name_plural = "کدهای یک‌بارمصرف پیامکی"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.phone_number} - {self.code}"