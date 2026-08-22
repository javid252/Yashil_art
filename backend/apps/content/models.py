from django.db import models
from apps.common.file_uploads import hero_slide_image_upload_to


class HeroSlide(models.Model):
    """یک اسلاید از اسلایدر هیرو در صفحه اصلی - هرکدام از فیلدها جدا از پنل ادمین قابل ویرایش است."""

    image = models.ImageField("تصویر", upload_to=hero_slide_image_upload_to,)
    label = models.CharField("لیبل بالای عنوان", max_length=100, blank=True)
    title = models.CharField("متن بزرگ (تیتر)", max_length=200)
    description = models.TextField("متن کوچک (توضیح)", blank=True)

    primary_button_text = models.CharField("متن دکمه اول", max_length=50, blank=True)
    primary_button_link = models.CharField(
        "لینک دکمه اول", max_length=255, blank=True,
        help_text="مسیر داخلی مثل /products یا آدرس کامل خارجی مثل https://...",
    )
    secondary_button_text = models.CharField("متن دکمه دوم", max_length=50, blank=True)
    secondary_button_link = models.CharField("لینک دکمه دوم", max_length=255, blank=True)

    order = models.PositiveIntegerField("ترتیب نمایش", default=0)
    is_active = models.BooleanField("فعال / نمایش در سایت", default=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "اسلاید هیرو"
        verbose_name_plural = "اسلایدهای هیرو"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title