from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.vendors.views import PublicSettingsView

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("api/settings/", PublicSettingsView.as_view(), name="public-settings"),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/", include("apps.products.urls")),
    path("api/cart/", include("apps.cart.urls")),
    path("api/orders/", include("apps.orders.urls")),
    path("api/admin/", include("apps.dashboard.urls")),
    path("api/admin/inventory/", include("apps.inventory.urls")),
    path("api/admin/accounting/", include("apps.accounting.urls")),
    path("api/vendors/", include("apps.vendors.urls")),
    path("api/payments/", include("apps.payments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)