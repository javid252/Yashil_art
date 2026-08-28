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
    path("api/content/", include("apps.content.urls")),
    path("api/invoices/", include("apps.invoices.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



#  path('', views, HomePage.as_view(), name='homepage'),
#  path('category/<<category>/', view.categoryList.as_view(), name='categories'),
#  path('product/<int:pk>/<str:slug>/', views.productDetail.as_view(), name='product_detail'),
#  re_path(r'^product/(?p<pk>\d+)/(?p<slug>[^/]+)/$,views.productDetail.as_view(),name='product_detail'),    