from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import social_views, views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", views.MeView.as_view(), name="me"),
    path("change-password/", views.ChangePasswordView.as_view(), name="change_password"),
    path("password-reset/", views.PasswordResetRequestView.as_view(), name="password_reset"),
    path("password-reset/confirm/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("social/settings/", social_views.PublicSocialAuthSettingsView.as_view(), name="social-settings"),
    path("social/google/", social_views.GoogleAuthView.as_view(), name="social-google"),
    path("social/telegram/", social_views.TelegramAuthView.as_view(), name="social-telegram"),
    path("social/sms/request/", social_views.SMSRequestOTPView.as_view(), name="social-sms-request"),
    path("social/sms/verify/", social_views.SMSVerifyOTPView.as_view(), name="social-sms-verify"),
]