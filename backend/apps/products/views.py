from django.db.models import Count
from django_filters import rest_framework as django_filters
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response

from .models import Category, Product, ProductImage, ProductVariant, Review
from .permissions import CanManageProductRelated, IsAdminOrReadOnly, IsAdminOrVendorOwner
from .serializers import (
    CategorySerializer,
    ProductDetailSerializer,
    ProductImageSerializer,
    ProductListSerializer,
    ProductVariantSerializer,
    ProductWriteSerializer,
    ReviewSerializer,
)


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = django_filters.CharFilter(field_name="category__slug")
    vendor = django_filters.CharFilter(field_name="vendor__store_slug")
    is_active = django_filters.BooleanFilter(field_name="is_active")
    has_discount = django_filters.BooleanFilter(field_name="discount_price", lookup_expr="isnull", exclude=True)

    class Meta:
        model = Product
        fields = ["min_price", "max_price", "category", "vendor", "is_featured", "is_active", "has_discount"]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrVendorOwner]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at", "name", "sales_count"]
 #   lookup_field = "slug"

    def get_queryset(self):
        qs = (
            Product.objects.select_related("category", "vendor")
            .prefetch_related("images", "variants")
            .annotate(sales_count=Count("order_items"))
        )
        user = self.request.user
        is_staff = bool(user and user.is_authenticated and user.is_staff)
        vendor = getattr(user, "vendor_profile", None) if user and user.is_authenticated else None

        if is_staff:
            return qs
        if vendor and self.request.query_params.get("mine") == "1":
            return qs.filter(vendor=vendor)
        return qs.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductWriteSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff:
            serializer.save()
            return
        vendor = getattr(user, "vendor_profile", None)
        serializer.save(vendor=vendor)

    def perform_update(self, serializer):
        user = self.request.user
        if user.is_staff:
            serializer.save()
            return
        vendor = getattr(user, "vendor_profile", None)
        serializer.save(vendor=vendor)


class ProductImageViewSet(viewsets.ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [CanManageProductRelated]

    def get_queryset(self):
        qs = ProductImage.objects.select_related("product__vendor")
        user = self.request.user
        if user.is_staff:
            return qs
        vendor = getattr(user, "vendor_profile", None)
        return qs.filter(product__vendor=vendor) if vendor else qs.none()


class ProductVariantViewSet(viewsets.ModelViewSet):
    serializer_class = ProductVariantSerializer
    permission_classes = [CanManageProductRelated]

    def get_queryset(self):
        qs = ProductVariant.objects.select_related("product__vendor")
        user = self.request.user
        if user.is_staff:
            return qs
        vendor = getattr(user, "vendor_profile", None)
        return qs.filter(product__vendor=vendor) if vendor else qs.none()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Review.objects.select_related("user", "product")
        product_id = self.request.query_params.get("product")
        if product_id:
            qs = qs.filter(product_id=product_id, is_approved=True)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SimilarProductsView(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        product_id = self.kwargs.get("pk")
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Product.objects.none()
        return (
            Product.objects
            .filter(category=product.category, is_active=True)
            .exclude(pk=product.id)
            .select_related("category", "vendor")
            .prefetch_related("images")[:6]
        )