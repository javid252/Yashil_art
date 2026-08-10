from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.access.views import PermissionCatalogueView, RoleViewSet
from apps.accounts.social_views import AdminSocialAuthSettingsView
from apps.orders.views import AdminOrderViewSet
from apps.payments.views import AdminPaymentSettingsView, AdminPaymentViewSet
from apps.vendors.views import AdminSettingsView, AdminVendorViewSet

from . import views

router = DefaultRouter()
router.register("users", views.AdminUserViewSet, basename="admin-users")
router.register("orders", AdminOrderViewSet, basename="admin-orders")
router.register("vendors", AdminVendorViewSet, basename="admin-vendors")
router.register("roles", RoleViewSet, basename="admin-roles")
router.register("payments", AdminPaymentViewSet, basename="admin-payments")

urlpatterns = [
    path("stats/", views.DashboardStatsView.as_view(), name="admin-stats"),
    path("settings/", AdminSettingsView.as_view(), name="admin-settings"),
    path("payments-settings/", AdminPaymentSettingsView.as_view(), name="admin-payments-settings"),
    path("social-auth-settings/", AdminSocialAuthSettingsView.as_view(), name="admin-social-auth-settings"),
    path("permissions/", PermissionCatalogueView.as_view(), name="admin-permissions"),
    *router.urls,
]