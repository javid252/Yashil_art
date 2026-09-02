from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify


class CourseCategory(models.Model):
    """دسته‌بندی دوره‌ها - مثلاً نقاشی، مجسمه‌سازی، گرافیک"""
    name = models.CharField("نام دسته", max_length=100)
    slug = models.SlugField("اسلاگ", max_length=120, unique=True, blank=True)
    description = models.TextField("توضیحات", blank=True)
    icon = models.CharField("آیکون", max_length=50, blank=True)
    image = models.ImageField("تصویر", upload_to="course_categories/", null=True, blank=True)
    is_active = models.BooleanField("فعال", default=True)
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)

    class Meta:
        verbose_name = "دسته‌بندی دوره"
        verbose_name_plural = "دسته‌بندی‌های دوره"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Course(models.Model):
    """دوره آموزشی"""

    class Level(models.TextChoices):
        BEGINNER = "beginner", "مبتدی"
        INTERMEDIATE = "intermediate", "متوسط"
        ADVANCED = "advanced", "پیشرفته"
        ALL_LEVELS = "all", "همه سطوح"

    class Status(models.TextChoices):
        DRAFT = "draft", "پیش‌نویس"
        PUBLISHED = "published", "منتشر شده"
        ARCHIVED = "archived", "بایگانی شده"

    class PricingType(models.TextChoices):
        SINGLE = "single", "تک دوره"
        SUBSCRIPTION = "subscription", "اشتراک ماهانه"
        BOTH = "both", "هر دو"

    category = models.ForeignKey(
        CourseCategory, verbose_name="دسته‌بندی", related_name="courses",
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    instructor = models.ForeignKey(
        "instructors.Instructor", verbose_name="استاد", related_name="courses",
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    title = models.CharField("عنوان دوره", max_length=200)
    slug = models.SlugField("اسلاگ", max_length=220, unique=True, blank=True)
    description = models.TextField("توضیحات دوره")
    short_description = models.CharField("توضیحات کوتاه", max_length=300, blank=True)

    level = models.CharField("سطح", max_length=20, choices=Level.choices, default=Level.ALL_LEVELS)
    status = models.CharField("وضعیت", max_length=20, choices=Status.choices, default=Status.DRAFT)
    pricing_type = models.CharField("نوع قیمت‌گذاری", max_length=20, choices=PricingType.choices, default=PricingType.SINGLE)

    price = models.DecimalField("قیمت (تومان)", max_digits=12, decimal_places=0, default=0)
    subscription_price = models.DecimalField(
        "قیمت اشتراک ماهانه (تومان)", max_digits=12, decimal_places=0, null=True, blank=True,
    )
    discount_price = models.DecimalField(
        "قیمت با تخفیف (تومان)", max_digits=12, decimal_places=0, null=True, blank=True,
    )

    duration_weeks = models.PositiveIntegerField("مدت دوره (هفته)", default=1)
    sessions_per_week = models.PositiveIntegerField("تعداد جلسات در هفته", default=1)
    session_duration_minutes = models.PositiveIntegerField("مدت هر جلسه (دقیقه)", default=90)
    max_students = models.PositiveIntegerField("حداکثر ظرفیت", default=20)
    enrolled_count = models.PositiveIntegerField("تعداد ثبت‌نام شده", default=0)

    prerequisites = models.TextField("پیش‌نیازها", blank=True)
    what_you_learn = models.JSONField("چه چیزی یاد می‌گیرید", default=list, blank=True)
    materials_needed = models.TextField("وسایل مورد نیاز", blank=True)

    thumbnail = models.ImageField("تصویر بندانگشتی", upload_to="courses/thumbnails/", null=True, blank=True)
    cover_image = models.ImageField("تصویر کاور", upload_to="courses/covers/", null=True, blank=True)
    promo_video_url = models.URLField("لینک ویدیو معرفی", blank=True)

    is_featured = models.BooleanField("دوره ویژه", default=False)
    is_active = models.BooleanField("فعال", default=True)

    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "دوره"
        verbose_name_plural = "دوره‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def discount_percent(self):
        if self.discount_price and self.price:
            return round((1 - (self.discount_price / self.price)) * 100)
        return 0

    @property
    def is_full(self):
        return self.enrolled_count >= self.max_students

    @property
    def available_spots(self):
        return max(0, self.max_students - self.enrolled_count)

    @property
    def total_sessions(self):
        return self.duration_weeks * self.sessions_per_week


class CourseSchedule(models.Model):
    """برنامه زمانی ثابت دوره"""

    class DayOfWeek(models.TextChoices):
        SATURDAY = "saturday", "شنبه"
        SUNDAY = "sunday", "یکشنبه"
        MONDAY = "monday", "دوشنبه"
        TUESDAY = "tuesday", "سه‌شنبه"
        WEDNESDAY = "wednesday", "چهارشنبه"
        THURSDAY = "thursday", "پنجشنبه"
        FRIDAY = "friday", "جمعه"

    course = models.ForeignKey(Course, related_name="schedules", on_delete=models.CASCADE)
    day_of_week = models.CharField("روز هفته", max_length=15, choices=DayOfWeek.choices)
    start_time = models.TimeField("ساعت شروع")
    end_time = models.TimeField("ساعت پایان")
    room = models.CharField("اتاق/محل", max_length=100, blank=True)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        verbose_name = "برنامه زمانی"
        verbose_name_plural = "برنامه‌های زمانی"
        ordering = ["day_of_week", "start_time"]
        unique_together = [("course", "day_of_week", "start_time")]

    def __str__(self):
        return f"{self.course.title} - {self.get_day_of_week_display()} {self.start_time}"


class CourseGallery(models.Model):
    """تصاویر گالری دوره"""
    course = models.ForeignKey(Course, related_name="gallery_images", on_delete=models.CASCADE)
    image = models.ImageField("تصویر", upload_to="courses/gallery/")
    caption = models.CharField("توضیح", max_length=200, blank=True)
    order = models.PositiveIntegerField("ترتیب", default=0)

    class Meta:
        verbose_name = "تصویر گالری دوره"
        verbose_name_plural = "تصاویر گالری دوره"
        ordering = ["order"]
