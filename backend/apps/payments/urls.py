from django.urls import path

from . import views

urlpatterns = [
    path("settings/", views.PublicPaymentSettingsView.as_view(), name="payments-public-settings"),
    path("card-transfer/", views.CardTransferSubmitView.as_view(), name="payments-card-transfer"),
    path("online/initiate/", views.OnlinePaymentInitiateView.as_view(), name="payments-online-initiate"),
    path("online/callback/", views.OnlinePaymentCallbackView.as_view(), name="payments-online-callback"),
]