from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("categories", views.CategoryViewSet, basename="category")
router.register("products", views.ProductViewSet, basename="product")
router.register("product-images", views.ProductImageViewSet, basename="product-image")
router.register("product-variants", views.ProductVariantViewSet, basename="product-variant")
router.register("reviews", views.ReviewViewSet, basename="review")

urlpatterns = router.urls + [
    path(
        "products/<int:pk>/similar/",
        views.SimilarProductsView.as_view(),
        name="similar-products",
    ),
]