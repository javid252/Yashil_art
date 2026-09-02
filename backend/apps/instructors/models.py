from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Instructor(models.Model):
    """پروفایل استاد"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name="کاربر", related_name="instructor_profile",
        on_delete=models.CASCADE, null=True, blank=True,
    )
    display_name = models.CharField("نام نمایشی", max_length=150)
    slug = models.SlugField("اسلاگ", max_length=170, unique=True, blank=True)
    bio = models.TextField("بیوگرافی")
    specializations = models.JSONField("تخصص‌ها", default=list, blank=True)
    photo = models.ImageField("عکس پروفایل", upload_to="instructors/photos/", null=True, blank=True)
    resume = models.FileField("رزومه", upload_to="instructors/resumes/", null=True, blank=True)

    website = models.URLField("وب‌سایت شخصی", blank=True)
    instagram = models.CharField("اینستاگرام", max_length=100, blank=True)
    telegram = models.CharField("تلگرام", max_length=100, blank=True)

    years_experience = models.PositiveIntegerField("سال‌های تجربه", default=0)
    students_count = models.PositiveIntegerField("تعداد دانشجو", default=0)
    rating = models.DecimalField(
        "امتیاز", max_digits=3, decimal_places=1, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    is_active = models.BooleanField("فعال", default=True)
    is_featured = models.BooleanField("استاد ویژه", default=False)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "استاد"
        verbose_name_plural = "اساتید"
        ordering = ["-is_featured", "-rating", "display_name"]

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.display_name, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Instructor.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)


class InstructorPortfolio(models.Model):
    """نمونه کار استاد"""
    instructor = models.ForeignKey(Instructor, related_name="portfolio", on_delete=models.CASCADE)
    title = models.CharField("عنوان", max_length=200)
    description = models.TextField("توضیحات", blank=True)
    image = models.ImageField("تصویر اثر", upload_to="instructors/portfolio/")
    year = models.PositiveIntegerField("سال خلق", null=True, blank=True)
    order = models.PositiveIntegerField("ترتیب", default=0)

    class Meta:
        verbose_name = "نمونه کار"
        verbose_name_plural = "نمونه کارها"
        ordering = ["order"]
