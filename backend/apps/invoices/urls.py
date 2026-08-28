from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("my", views.MyInvoiceViewSet, basename="my-invoices")
router.register("admin", views.AdminInvoiceViewSet, basename="admin-invoices")

urlpatterns = [
    *router.urls,
]