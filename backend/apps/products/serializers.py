from django.db.models import Avg, Count
from rest_framework import serializers

from .models import Category, Product, ProductImage, ProductVariant, Review


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "icon", "image", "is_active", "order", "product_count"]

    def get_product_count(self, obj):
        return Product.objects.filter(category=obj, is_active=True).count()


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image", "is_main", "order"]


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ["id", "product", "attribute_name", "value", "price_modifier", "stock"]


class ProductListSerializer(serializers.ModelSerializer):
    """سریالایزر سبک برای لیست/گرید محصولات."""

    category_name = serializers.CharField(source="category.name", read_only=True, default="")
    vendor_name = serializers.CharField(source="vendor.store_name", read_only=True, default=None)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "price", "discount_price", "final_price",
            "discount_percent", "in_stock", "is_featured", "category_name",
            "vendor_name", "main_image",
        ]

    def get_main_image(self, obj):
        request = self.context.get("request")
        main = obj.images.filter(is_main=True).first() or obj.images.first()
        if main and request:
            return request.build_absolute_uri(main.image.url)
        return None


class ReviewSerializer(serializers.ModelSerializer):
    user_display_name = serializers.CharField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id", "product", "user", "user_display_name", "rating",
            "title", "comment", "is_approved", "created_at", "updated_at",
        ]
        read_only_fields = ["user", "is_approved"]


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    vendor_name = serializers.CharField(source="vendor.store_name", read_only=True, default=None)
    vendor_slug = serializers.CharField(source="vendor.store_slug", read_only=True, default=None)
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    rating_distribution = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "price", "discount_price",
            "final_price", "discount_percent", "stock", "in_stock", "is_featured",
            "category", "vendor_name", "vendor_slug", "images", "variants",
            "average_rating", "reviews_count", "rating_distribution", "created_at",
        ]

    def get_average_rating(self, obj):
        result = obj.reviews.filter(is_approved=True).aggregate(avg=Avg("rating"))
        return round(result["avg"], 1) if result["avg"] else None

    def get_reviews_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()

    def get_rating_distribution(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        dist = {i: 0 for i in range(1, 6)}
        for r in reviews:
            dist[r.rating] = dist.get(r.rating, 0) + 1
        total = reviews.count()
        return {k: {"count": v, "percent": round(v / total * 100) if total else 0} for k, v in dist.items()}


class ProductWriteSerializer(serializers.ModelSerializer):
    """
    برای ایجاد/ویرایش محصول.
    فیلد vendor عمداً قابل نوشتن است: در حالت چندفروشندگی، ویو مربوطه
    (ProductViewSet) این مقدار را خودش بر اساس فروشنده لاگین‌کرده تنظیم
    می‌کند تا یک فروشنده نتواند محصول را به نام فروشنده دیگری ثبت کند؛
    فقط ادمین اجازه دارد این فیلد را آزادانه از درخواست تغییر دهد.
    """

    class Meta:
        model = Product
        fields = [
            "id", "name", "category", "vendor", "description", "price",
            "discount_price", "stock", "is_active", "is_featured",
        ]