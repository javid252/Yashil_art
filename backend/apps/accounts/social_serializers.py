from rest_framework import serializers

from .models import SocialAuthSettings


class PublicSocialAuthSettingsSerializer(serializers.ModelSerializer):
    """نسخه عمومی - توکن ربات و کلید API پیامک هرگز اینجا نمی‌آید."""

    class Meta:
        model = SocialAuthSettings
        fields = ["google_enabled", "google_client_id", "telegram_enabled", "telegram_bot_username", "sms_otp_enabled"]


class AdminSocialAuthSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAuthSettings
        fields = [
            "google_enabled", "google_client_id",
            "telegram_enabled", "telegram_bot_username", "telegram_bot_token",
            "sms_otp_enabled", "sms_provider", "sms_api_key", "sms_sender_line",
        ]


class GoogleAuthSerializer(serializers.Serializer):
    credential = serializers.CharField()


class TelegramAuthSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)
    photo_url = serializers.CharField(required=False, allow_blank=True)
    auth_date = serializers.IntegerField()
    hash = serializers.CharField()


class SMSRequestSerializer(serializers.Serializer):
    phone_number = serializers.RegexField(r"^09\d{9}$", error_messages={"invalid": "شماره موبایل معتبر نیست (مثال: 09123456789)."})


class SMSVerifySerializer(serializers.Serializer):
    phone_number = serializers.RegexField(r"^09\d{9}$")
    code = serializers.RegexField(r"^\d{6}$", error_messages={"invalid": "کد باید ۶ رقم باشد."})