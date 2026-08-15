from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("hero-slides", views.HeroSlideViewSet, basename="hero-slide")

urlpatterns = router.urls