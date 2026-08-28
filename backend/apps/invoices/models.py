from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Invoice(models.Model):
    """
    فاکتور فروش - پس از تأیید سفارش به‌صورت خودکار صادر می‌شود.
    هر فاکتور منحصربفرد یک شماره فاکتور دارد و قابل بایگانی، چاپ PDF
    و ارسال ایمیل به خریدار است.
    """

    class Status(models.TextChoices):
        DRAFT = "draft", "پیش‌نویس"
        ISSUED = "issued", "صادر شده"
        PAID = "paid", "پرداخت شده"
        CANCELLED = "cancelled", "لغو شده"
        ARCHIVED = "archived", "بایگانی شده"

    # ---- اطلاعات فاکتور ----
    invoice_number = models.CharField(
        "شماره فاکتور", max_length=30, unique=True, editable=False,
        help_text="شماره خودکار منحصربفرد فاکتور",
    )
    status = models.CharField(
        "وضعیت", max_length=20, choices=Status.choices, default=Status.DRAFT,
    )

    # ---- روابط ----
    order = models.OneToOneField(
        "orders.Order", verbose_name="سفارش مرتبط",
        related_name="invoice", on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="خریدار",
        related_name="invoices", on_delete=models.PROTECT,
    )

    # ---- اطلاعات صورتحساب خریدار ----
    buyer_full_name = models.CharField("نام خریدار", max_length=150)
    buyer_phone = models.CharField("تلفن خریدار", max_length=15, blank=True)
    buyer_email = models.EmailField("ایمیل خریدار", blank=True)
    buyer_address = models.TextField("آدرس صورتحساب", blank=True)
    buyer_postal_code = models.CharField("کد پستی", max_length=10, blank=True)

    # ---- مبالغ ----
    subtotal = models.DecimalField(
        "جمع آیتم‌ها (تومان)", max_digits=14, decimal_places=0, default=0,
    )
    discount_total = models.DecimalField(
        "مجموع تخفیف (تومان)", max_digits=14, decimal_places=0, default=0,
    )
    tax_total = models.DecimalField(
        "مجموع مالیات (تومان)", max_digits=14, decimal_places=0, default=0,
    )
    grand_total = models.DecimalField(
        "مبلغ نهایی (تومان)", max_digits=14, decimal_places=0, default=0,
    )

    # ---- یادداشت و بایگانی ----
    notes = models.TextField("یادداشت‌های فاکتور", blank=True)
    is_archived = models.BooleanField("بایگانی شده", default=False)
    archived_at = models.DateTimeField("تاریخ بایگانی", null=True, blank=True)

    # ---- ارسال ایمیل ----
    email_sent = models.BooleanField("ایمیل ارسال شده", default=False)
    email_sent_at = models.DateTimeField("تاریخ ارسال ایمیل", null=True, blank=True)

    # ---- تاریخ‌ها ----
    issued_at = models.DateTimeField("تاریخ صدور", null=True, blank=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "فاکتور"
        verbose_name_plural = "فاکتورها"
        ordering = ["-created_at"]
        permissions = [
            ("view_all_invoices", "مشاهده همه فاکتورها"),
            ("archive_invoice", "بایگانی فاکتور"),
            ("send_invoice_email", "ارسال ایمیل فاکتور"),
        ]

    def __str__(self):
        return f"فاکتور {self.invoice_number} - سفارش #{self.order_id}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self._generate_number()
        super().save(*args, **kwargs)

    def _generate_number(self):
        """تولید شماره فاکتور منحصربفرد: INV-YYYY-XXXXX"""
        year = timezone.now().year
        prefix = f"INV-{year}-"
        last = (
            Invoice.objects.filter(invoice_number__startswith=prefix)
            .order_by("-invoice_number")
            .values_list("invoice_number", flat=True)
            .first()
        )
        if last:
            try:
                num = int(last.split("-")[-1]) + 1
            except (ValueError, IndexError):
                num = 1
        else:
            num = 1
        return f"{prefix}{num:05d}"

    # ---- متدهای وضعیت ----
    def mark_issued(self):
        """تغییر وضعیت به صادر شده"""
        self.status = self.Status.ISSUED
        self.issued_at = timezone.now()
        self.save(update_fields=["status", "issued_at", "updated_at"])

    def mark_paid(self):
        """تغییر وضعیت به پرداخت شده"""
        self.status = self.Status.PAID
        self.save(update_fields=["status", "updated_at"])

    def mark_cancelled(self):
        """لغو فاکتور"""
        self.status = self.Status.CANCELLED
        self.save(update_fields=["status", "updated_at"])

    def archive(self):
        """بایگانی فاکتور"""
        self.is_archived = True
        self.status = self.Status.ARCHIVED
        self.archived_at = timezone.now()
        self.save(update_fields=["is_archived", "status", "archived_at", "updated_at"])

    def unarchive(self):
        """خارج کردن از بایگانی"""
        self.is_archived = False
        self.status = self.Status.ISSUED
        self.archived_at = None
        self.save(update_fields=["is_archived", "status", "archived_at", "updated_at"])

    def recalculate_totals(self):
        """محاسبه مجدد جمع کل از آیتم‌ها"""
        items = self.items.all()
        self.subtotal = sum(item.line_total for item in items)
        self.grand_total = self.subtotal - self.discount_total + self.tax_total
        self.save(update_fields=["subtotal", "grand_total", "updated_at"])

    @property
    def status_display_fa(self):
        return self.get_status_display()

    @property
    def formatted_grand_total(self):
        """فرمت فارسی مبلغ نهایی"""
        return f"{int(self.grand_total):,}".replace(",", "،")


class InvoiceItem(models.Model):
    """آیتم فاکتور - هر ردیف از جدول فاکتور"""

    invoice = models.ForeignKey(
        Invoice, verbose_name="فاکتور", related_name="items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        "products.Product", verbose_name="محصول",
        related_name="invoice_items", on_delete=models.SET_NULL, null=True,
    )
    product_name = models.CharField("نام محصول", max_length=200)
    variant_label = models.CharField("مشخصات تنوع", max_length=100, blank=True)
    unit_price = models.DecimalField(
        "قیمت واحد (تومان)", max_digits=12, decimal_places=0,
    )
    quantity = models.PositiveIntegerField("تعداد", default=1)
    discount_amount = models.DecimalField(
        "تخفیف ردیف (تومان)", max_digits=12, decimal_places=0, default=0,
    )
    tax_amount = models.DecimalField(
        "مالیات ردیف (تومان)", max_digits=12, decimal_places=0, default=0,
    )

    class Meta:
        verbose_name = "آیتم فاکتور"
        verbose_name_plural = "آیتم‌های فاکتور"

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"

    @property
    def line_total(self):
        """جمع ردیف (بدون تخفیف و مالیات)"""
        return self.unit_price * self.quantity

    @property
    def line_total_after_discount(self):
        """جمع ردیف بعد از تخفیف"""
        return self.line_total - self.discount_amount

    @property
    def formatted_unit_price(self):
        return f"{int(self.unit_price):,}".replace(",", "،")

    @property
    def formatted_line_total(self):
        return f"{int(self.line_total):,}".replace(",", "،")

    @property
    def formatted_line_total_after_discount(self):
        return f"{int(self.line_total_after_discount):,}".replace(",", "،")