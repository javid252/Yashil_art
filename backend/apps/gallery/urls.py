from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GalleryArtworkViewSet, GalleryCategoryViewSet, GalleryExhibitionViewSet

router = DefaultRouter()
router.register("categories", GalleryCategoryViewSet, basename="gallery-category")
router.register("exhibitions", GalleryExhibitionViewSet, basename="gallery-exhibition")
router.register("artworks", GalleryArtworkViewSet, basename="gallery-artwork")

urlpatterns = [
    path("", include(router.urls)),
]
