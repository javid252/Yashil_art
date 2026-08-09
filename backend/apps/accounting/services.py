from django.utils import timezone


def ensure_income_transaction(order, user=None):
    """
    اگر برای این سفارش قبلاً تراکنش درآمدی ثبت نشده، یکی خودکار می‌سازد.
    این تابع هم از پنل ادمین (تغییر دستی وضعیت سفارش) و هم از فلوی تایید
    پرداخت (کارت‌به‌کارت تاییدشده یا زرین‌پال موفق) صدا زده می‌شود تا منطق
    یک‌جا باشد و تراکنش تکراری ساخته نشود.
    """
    from .models import Transaction

    if Transaction.objects.filter(related_order=order).exists():
        return None
    return Transaction.objects.create(
        type=Transaction.Type.INCOME,
        amount=order.total_price,
        description=f"درآمد سفارش #{order.id}",
        related_order=order,
        is_automatic=True,
        created_by=user,
        occurred_at=timezone.now().date(),
    )