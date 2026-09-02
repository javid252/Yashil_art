from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify


class GalleryCategory(models.Model):
    """دسته‌بندی آثار هنری"""
    name = models.CharField("نام دسته", max_length=100)
    slug = models.SlugField("اسلاگ", max_length=120, unique=True, blank=True)
    description = models.TextField("توضیحات", blank=True)
    icon = models.CharField("آیکون", max_length=50, blank=True)
    is_active = models.BooleanField("فعال", default=True)
    order = models.PositiveIntegerField("ترتیب", default=0)

    class Meta:
        verbose_name = "دسته‌بندی گالری"
        verbose_name_plural = "دسته‌بندی‌های گالری"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class GalleryExhibition(models.Model):
    """نمایشگاه"""
    title = models.CharField("عنوان نمایشگاه", max_length=200)
    slug = models.SlugField("اسلاگ", max_length=220, unique=True, blank=True)
    description = models.TextField("توضیحات")
    cover_image = models.ImageField("تصویر کاور", upload_to="gallery/exhibitions/")
    start_date = models.DateField("تاریخ شروع")
    end_date = models.DateField("تاریخ پایان", null=True, blank=True)
    location = models.CharField("محل نمایشگاه", max_length=200, blank=True)
    is_active = models.BooleanField("فعال", default=True)
    is_virtual = models.BooleanField("مجازی", default=False)

    class Meta:
        verbose_name = "نمایشگاه"
        verbose_name_plural = "نمایشگاه‌ها"
        ordering = ["-start_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class GalleryArtwork(models.Model):
    """اثر هنری"""

    class Medium(models.TextChoices):
        PAINTING = "painting", "نقاشی"
        SCULPTURE = "sculpture", "مجسمه‌سازی"
        CALLIGRAPHY = "calligraphy", "خوشنویسی"
        DIGITAL = "digital", "دیجیتال آرت"
        PHOTOGRAPHY = "photography", "عکاسی"
        POTTERY = "pottery", "سفالگری"
        TEXTILE = "textile", "نساجی و بافندگی"
        MIXED = "mixed", "تکنیک ترکیبی"
        OTHER = "other", "سایر"

    artist = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="هنرمند", related_name="gallery_artworks",
        on_delete=models.CASCADE,
    )
    instructor = models.ForeignKey(
        "instructors.Instructor", verbose_name="استاد راهنما", related_name="artworks",
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    category = models.ForeignKey(
        GalleryCategory, verbose_name="دسته‌بندی", related_name="artworks",
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    exhibition = models.ForeignKey(
        GalleryExhibition, verbose_name="نمایشگاه", related_name="artworks",
        on_delete=models.SET_NULL, null=True, blank=True,
    )

    title = models.CharField("عنوان اثر", max_length=200)
    slug = models.SlugField("اسلاگ", max_length=220, unique=True, blank=True)
    description = models.TextField("توضیحات اثر", blank=True)
    medium = models.CharField("تکنیک / مدیوم", max_length=20, choices=Medium.choices)
    dimensions = models.CharField("ابعاد", max_length=100, blank=True, help_text="مثلاً 50x70 سانتی‌متر")
    year_created = models.PositiveIntegerField("سال خلق", null=True, blank=True)

    image = models.ImageField("تصویر اثر", upload_to="gallery/artworks/")
    thumbnail = models.ImageField("تصویر بندانگشتی", upload_to="gallery/thumbnails/", null=True, blank=True)

    likes_count = models.PositiveIntegerField("تعداد لایک", default=0)
    views_count = models.PositiveIntegerField("تعداد بازدید", default=0)

    is_featured = models.BooleanField("اثر ویژه", default=False)
    is_published = models.BooleanField("منتشر شده", default=True)

    # قابلیت فروش در آینده
    is_for_sale = models.BooleanField("قابل فروش", default=False)
    sale_price = models.DecimalField(
        "قیمت فروش (تومان)", max_digits=12, decimal_places=0, null=True, blank=True,
    )
    is_sold = models.BooleanField("فروخته شده", default=False)

    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "اثر هنری"
        verbose_name_plural = "آثار هنری"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.artist}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            while GalleryArtwork.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)


class GalleryComment(models.Model):
    """نظر درباره اثر هنری"""
    artwork = models.ForeignKey(GalleryArtwork, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="کاربر", related_name="gallery_comments",
        on_delete=models.CASCADE,
    )
    text = models.TextField("متن نظر")
    is_approved = models.BooleanField("تایید شده", default=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "نظر گالری"
        verbose_name_plural = "نظرات گالری"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.artwork.title}"


class GalleryLike(models.Model):
    """لایک اثر هنری"""
    artwork = models.ForeignKey(GalleryArtwork, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="کاربر", related_name="gallery_likes",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک‌ها"
        unique_together = [("artwork", "user")]

    def __str__(self):
        return f"{self.user} likes {self.artwork.title}"
