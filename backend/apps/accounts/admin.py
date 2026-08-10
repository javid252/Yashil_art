from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import PhoneOTP, SocialAuthSettings, SocialIdentity, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "first_name", "last_name", "is_staff", "is_active"]
    fieldsets = UserAdmin.fieldsets + (
        ("اطلاعات تکمیلی", {"fields": ("phone_number",)}),
    )


@admin.register(SocialAuthSettings)
class SocialAuthSettingsAdmin(admin.ModelAdmin):
    list_display = ["google_enabled", "telegram_enabled", "sms_otp_enabled"]


@admin.register(SocialIdentity)
class SocialIdentityAdmin(admin.ModelAdmin):
    list_display = ["user", "provider", "provider_user_id", "created_at"]
    list_filter = ["provider"]


@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ["phone_number", "is_used", "attempts", "expires_at", "created_at"]
    readonly_fields = ["code"]