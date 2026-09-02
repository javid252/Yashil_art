from django.conf import settings
from django.db import models
from django.utils.text import slugify


class WorkshopCategory(models.Model):
    """دسته‌بندی کارگاه‌ها"""
    name = models.CharField("نام دسته", max_length=100)
    slug = models.SlugField("اسلاگ", max_length=120, unique=True, blank=True)
    icon = models.CharField("آیکون", max_length=50, blank=True)
    is_active = models.BooleanField("فعال", default=True)
    order = models.PositiveIntegerField("ترتیب", default=0)

    class Meta:
        verbose_name = "دسته‌بندی کارگاه"
        verbose_name_plural = "دسته‌بندی‌های کارگاه"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Workshop(models.Model):
    """کارگاه آموزشی"""

    class DurationType(models.TextChoices):
        SHORT = "short", "کوتاه‌مدت"
        LONG = "long", "بلندمدت"
        ONE_SESSION = "one", "تک جلسه‌ای"
        INTENSIVE = "intensive", "فشرده"

    class Status(models.TextChoices):
        UPCOMING = "upcoming", "پیش رو"
        ONGOING = "ongoing", "در حال برگزاری"
        COMPLETED = "completed", "تکمیل شده"
        CANCELLED = "cancelled", "لغو شده"

    category = models.ForeignKey(
        WorkshopCategory, verbose_name="دسته‌بندی", related_name="workshops",
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    instructor = models.ForeignKey(
        "instructors.Instructor", verbose_name="مدرس", related_name="workshops",
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    title = models.CharField("عنوان کارگاه", max_length=200)
    slug = models.SlugField("اسلاگ", max_length=220, unique=True, blank=True)
    description = models.TextField("توضیحات")
    short_description = models.CharField("توضیحات کوتاه", max_length=300, blank=True)

    duration_type = models.CharField("نوع مدت", max_length=15, choices=DurationType.choices)
    status = models.CharField("وضعیت", max_length=15, choices=Status.choices, default=Status.UPCOMING)

    start_date = models.DateField("تاریخ شروع")
    end_date = models.DateField("تاریخ پایان", null=True, blank=True)
    start_time = models.TimeField("ساعت شروع")
    end_time = models.TimeField("ساعت پایان")
    sessions_count = models.PositiveIntegerField("تعداد جلسات", default=1)

    price = models.DecimalField("قیمت (تومان)", max_digits=12, decimal_places=0, default=0)
    max_participants = models.PositiveIntegerField("حداکثر شرکت‌کننده", default=20)
    enrolled_count = models.PositiveIntegerField("تعداد ثبت‌نام", default=0)

    thumbnail = models.ImageField("تصویر بندانگشتی", upload_to="workshops/thumbnails/", null=True, blank=True)
    cover_image = models.ImageField("تصویر کاور", upload_to="workshops/covers/", null=True, blank=True)

    prerequisites = models.TextField("پیش‌نیازها", blank=True)
    materials = models.TextField("وسایل مورد نیاز", blank=True)
    location = models.CharField("محل برگزاری", max_length=200, blank=True)
    is_online = models.BooleanField("آنلاین", default=False)

    is_featured = models.BooleanField("ویژه", default=False)
    is_active = models.BooleanField("فعال", default=True)

    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "کارگاه"
        verbose_name_plural = "کارگاه‌ها"
        ordering = ["start_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Workshop.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def is_full(self):
        return self.enrolled_count >= self.max_participants

    @property
    def available_spots(self):
        return max(0, self.max_participants - self.enrolled_count)

    @property
    def duration_display(self):
        if self.end_date:
            delta = self.end_date - self.start_date
            return f"{delta.days + 1} روز"
        return f"{self.sessions_count} جلسه"


class WorkshopRegistration(models.Model):
    """ثبت‌نام در کارگاه"""

    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار پرداخت"
        CONFIRMED = "confirmed", "تایید شده"
        CANCELLED = "cancelled", "لغو شده"

    workshop = models.ForeignKey(Workshop, related_name="registrations", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="شرکت‌کننده", related_name="workshop_registrations",
        on_delete=models.CASCADE,
    )
    status = models.CharField("وضعیت", max_length=15, choices=Status.choices, default=Status.PENDING)
    registered_at = models.DateTimeField("تاریخ ثبت‌نام", auto_now_add=True)

    class Meta:
        verbose_name = "ثبت‌نام کارگاه"
        verbose_name_plural = "ثبت‌نام‌های کارگاه"
        unique_together = [("workshop", "user")]

    def __str__(self):
        return f"{self.user} - {self.workshop.title}"
