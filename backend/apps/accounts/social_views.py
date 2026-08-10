from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.access.permissions import IsSuperUser

from .models import SocialAuthSettings, SocialIdentity
from .serializers import UserSerializer
from .social_serializers import (
    AdminSocialAuthSettingsSerializer,
    GoogleAuthSerializer,
    PublicSocialAuthSettingsSerializer,
    SMSRequestSerializer,
    SMSVerifySerializer,
    TelegramAuthSerializer,
)
from .social_services import (
    SMSProviderError,
    SocialAuthError,
    generate_and_send_otp,
    get_or_create_social_user,
    verify_google_credential,
    verify_otp,
    verify_telegram_auth,
)


def _issue_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": UserSerializer(user).data,
    }


class PublicSocialAuthSettingsView(APIView):
    """فرانت‌اند با این endpoint می‌فهمد کدام روش‌های ورود جایگزین فعال‌اند."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(PublicSocialAuthSettingsSerializer(SocialAuthSettings.load()).data)


class AdminSocialAuthSettingsView(APIView):
    """پیکربندی کامل (شامل توکن ربات و کلید API پیامک) - فقط ادمین اصلی."""

    permission_classes = [IsSuperUser]

    def get(self, request):
        return Response(AdminSocialAuthSettingsSerializer(SocialAuthSettings.load()).data)

    def patch(self, request):
        obj = SocialAuthSettings.load()
        serializer = AdminSocialAuthSettingsSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GoogleAuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        settings_obj = SocialAuthSettings.load()
        if not settings_obj.google_enabled:
            return Response({"detail": "ورود با گوگل در حال حاضر غیرفعال است."}, status=403)
        if not settings_obj.google_client_id:
            return Response({"detail": "ورود با گوگل هنوز توسط ادمین پیکربندی نشده است."}, status=503)

        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            payload = verify_google_credential(serializer.validated_data["credential"], settings_obj.google_client_id)
        except SocialAuthError as exc:
            return Response({"detail": str(exc)}, status=400)

        user = get_or_create_social_user(
            provider=SocialIdentity.Provider.GOOGLE,
            provider_user_id=payload["sub"],
            email=payload.get("email"),
            first_name=payload.get("given_name", ""),
            last_name=payload.get("family_name", ""),
            extra_data={"picture": payload.get("picture")},
        )
        return Response(_issue_tokens(user))


class TelegramAuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        settings_obj = SocialAuthSettings.load()
        if not settings_obj.telegram_enabled:
            return Response({"detail": "ورود با تلگرام در حال حاضر غیرفعال است."}, status=403)

        serializer = TelegramAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            verify_telegram_auth(data, settings_obj.telegram_bot_token)
        except SocialAuthError as exc:
            return Response({"detail": str(exc)}, status=400)

        user = get_or_create_social_user(
            provider=SocialIdentity.Provider.TELEGRAM,
            provider_user_id=data["id"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            extra_data={"username": data.get("username"), "photo_url": data.get("photo_url")},
        )
        return Response(_issue_tokens(user))


class SMSRequestOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        settings_obj = SocialAuthSettings.load()
        if not settings_obj.sms_otp_enabled:
            return Response({"detail": "ورود با کد پیامکی در حال حاضر غیرفعال است."}, status=403)

        serializer = SMSRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]

        from django.utils import timezone

        from .models import PhoneOTP

        recent = PhoneOTP.objects.filter(phone_number=phone_number).order_by("-created_at").first()
        if recent and (timezone.now() - recent.created_at).total_seconds() < 60:
            return Response({"detail": "لطفاً کمی صبر کنید و دوباره درخواست دهید."}, status=429)

        try:
            generate_and_send_otp(phone_number)
        except SMSProviderError as exc:
            return Response({"detail": str(exc)}, status=502)

        return Response({"detail": "کد تایید ارسال شد."})


class SMSVerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        settings_obj = SocialAuthSettings.load()
        if not settings_obj.sms_otp_enabled:
            return Response({"detail": "ورود با کد پیامکی در حال حاضر غیرفعال است."}, status=403)

        serializer = SMSVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        code = serializer.validated_data["code"]

        try:
            verify_otp(phone_number, code)
        except SocialAuthError as exc:
            return Response({"detail": str(exc)}, status=400)

        user = get_or_create_social_user(
            provider=SocialIdentity.Provider.PHONE,
            provider_user_id=phone_number,
            phone_number=phone_number,
        )
        return Response(_issue_tokens(user))