from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.products.models import Category, Product, ProductVariant

User = get_user_model()


class Command(BaseCommand):
    help = "دیتای نمونه برای دسته‌بندی، محصولات و کاربر ادمین می‌سازد."

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin", email="admin@kaavan-shop.local", password="Admin@12345",
            )
            self.stdout.write(self.style.SUCCESS("کاربر ادمین ساخته شد: admin / Admin@12345"))

        categories_data = [
            ("پوشاک", "👕"), ("کیف و کفش", "👜"), ("لوازم دیجیتال", "🎧"),
            ("خانه و آشپزخانه", "🍳"), ("زیبایی و سلامت", "💆"),
        ]
        categories = {}
        for name, icon in categories_data:
            cat, _ = Category.objects.get_or_create(name=name, defaults={"icon": icon})
            categories[name] = cat

        sample_products = [
            ("پیراهن کتان مردانه", "پوشاک", 890000, 690000, True),
            ("کفش اسپرت سفید", "کیف و کفش", 1250000, None, True),
            ("هدفون بی‌سیم یاشیل آرت", "لوازم دیجیتال", 2450000, 1990000, True),
            ("قابلمه استیل ۵ لیتری", "خانه و آشپزخانه", 1580000, None, False),
            ("ست مراقبت پوست", "زیبایی و سلامت", 720000, 590000, True),
            ("کیف دستی چرم زنانه", "کیف و کفش", 1340000, None, False),
            ("تیشرت نخی ساده", "پوشاک", 350000, 280000, False),
            ("اسپیکر بلوتوثی قابل حمل", "لوازم دیجیتال", 1890000, None, True),
        ]
        for name, cat_name, price, discount, featured in sample_products:
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": categories[cat_name],
                    "description": f"{name} با کیفیت بالا و ارسال سریع از فروشگاه یاشیل آرت.",
                    "price": price,
                    "discount_price": discount,
                    "stock": 25,
                    "is_featured": featured,
                },
            )
            if created and cat_name == "پوشاک":
                for size in ["S", "M", "L", "XL"]:
                    ProductVariant.objects.create(
                        product=product, attribute_name="سایز", value=size, stock=10,
                    )

        self.stdout.write(self.style.SUCCESS("دیتای نمونه با موفقیت ساخته شد."))
