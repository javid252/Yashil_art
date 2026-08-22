from django.db import models
from django.utils.text import slugify

from apps.common.file_uploads import product_image_upload_to
from apps.common.file_uploads import category_image_upload_to


class Category(models.Model):
    name = models.CharField("نام دسته", max_length=100)
    slug = models.SlugField("اسلاگ", max_length=120, unique=True, blank=True)
    parent = models.ForeignKey(
        "self", verbose_name="دسته والد", null=True, blank=True,
        related_name="children", on_delete=models.CASCADE,
    )
    icon = models.CharField(
        "آیکون (نام کلاس یا اموجی)", max_length=50, blank=True,
        help_text="مثلا 📦 یا نام آیکون - اگر تصویر آپلود نشود، همین نمایش داده می‌شود",
    )
    image = models.ImageField(
        "تصویر دسته‌بندی", upload_to= category_image_upload_to, null=True, blank=True,
    )
    is_active = models.BooleanField("فعال / قابل نمایش", default=True)
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(
        Category, verbose_name="دسته‌بندی", related_name="products",
        on_delete=models.SET_NULL, null=True,
    )
    vendor = models.ForeignKey(
        "vendors.Vendor", verbose_name="فروشنده", related_name="products",
        on_delete=models.SET_NULL, null=True, blank=True,
        help_text="در حالت تک‌فروشگاهی خالی می‌ماند.",
    )
    name = models.CharField("نام محصول", max_length=200)
    slug = models.SlugField("اسلاگ", max_length=220, unique=True, blank=True)
    description = models.TextField("توضیحات", blank=True)
    price = models.DecimalField("قیمت (تومان)", max_digits=12, decimal_places=0)
    discount_price = models.DecimalField(
        "قیمت با تخفیف (تومان)", max_digits=12, decimal_places=0, null=True, blank=True,
    )
    stock = models.PositiveIntegerField("موجودی انبار", default=0)
    is_active = models.BooleanField("فعال / قابل نمایش", default=True)
    is_featured = models.BooleanField("محصول ویژه", default=False)
    created_at = models.DateTimeField("تاریخ ثبت", auto_now_add=True)
    updated_at = models.DateTimeField("آخرین ویرایش", auto_now=True)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
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
    def in_stock(self):
        return self.stock > 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField("تصویر", upload_to=product_image_upload_to,)
    is_main = models.BooleanField("تصویر اصلی", default=False)
    order = models.PositiveIntegerField("ترتیب نمایش", default=0)

    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصول"
        ordering = ["order", "id"]

    def __str__(self):
        return f"تصویر {self.product.name}"


class ProductVariant(models.Model):
    """تنوع محصول - مثلا سایز یا رنگ."""

    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    attribute_name = models.CharField("نوع تنوع", max_length=50, help_text="مثلا سایز، رنگ")
    value = models.CharField("مقدار", max_length=50, help_text="مثلا L، قرمز")
    price_modifier = models.DecimalField(
        "تغییر قیمت (تومان)", max_digits=10, decimal_places=0, default=0,
        help_text="مقدار مثبت یا منفی که به قیمت پایه اضافه می‌شود",
    )
    stock = models.PositiveIntegerField("موجودی این تنوع", default=0)

    class Meta:
        verbose_name = "تنوع محصول"
        verbose_name_plural = "تنوع‌های محصول"

    def __str__(self):
        return f"{self.product.name} - {self.attribute_name}: {self.value}"
