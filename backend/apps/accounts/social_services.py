"""
منطق اصلی ورود جایگزین: تایید هویت گوگل/تلگرام، ارسال/تایید کد پیامکی،
و پیدا کردن یا ساختن کاربر متناظر.
"""
import hashlib
import hmac
import random
import time

import requests
from django.utils import timezone

from .models import PhoneOTP, SocialIdentity, User


class SocialAuthError(Exception):
    pass


# --------------------------------------------------------------------------
# گوگل
# --------------------------------------------------------------------------
def verify_google_credential(credential, client_id):
    """
    credential همان ID Token ای است که Google Identity Services در فرانت‌اند
    برمی‌گرداند. این تابع واقعاً با سرورهای گوگل (برای گرفتن کلیدهای عمومی)
    ارتباط برقرار می‌کند - در محیط توسعه این پروژه دسترسی شبکه به
    accounts.google.com وجود نداشت، پس این تابع فقط بر اساس مستندات رسمی
    google-auth نوشته شده، نه با فراخوانی واقعی تست شده.
    """
    from google.auth.transport import requests as google_requests
    from google.oauth2 import id_token

    try:
        payload = id_token.verify_oauth2_token(credential, google_requests.Request(), client_id)
    except ValueError as exc:
        raise SocialAuthError(f"توکن گوگل نامعتبر است: {exc}") from exc

    if not payload.get("email_verified", True):
        raise SocialAuthError("ایمیل گوگل شما تاییدشده نیست.")

    return payload


# --------------------------------------------------------------------------
# تلگرام - کاملاً آفلاین و قابل‌تست (بدون فراخوانی شبکه)
# طبق مستندات رسمی: https://core.telegram.org/widgets/login#checking-authorization
# --------------------------------------------------------------------------
def verify_telegram_auth(data, bot_token, max_age_seconds=86400):
    if not bot_token:
        raise SocialAuthError("ربات تلگرام هنوز توسط ادمین پیکربندی نشده است.")

    received_hash = data.get("hash")
    if not received_hash:
        raise SocialAuthError("داده تلگرام ناقص است.")

    check_fields = {k: v for k, v in data.items() if k != "hash" and v is not None}
    data_check_string = "\n".join(f"{k}={check_fields[k]}" for k in sorted(check_fields))
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(computed_hash, str(received_hash)):
        raise SocialAuthError("امضای داده تلگرام معتبر نیست.")

    auth_date = int(data.get("auth_date", 0))
    if time.time() - auth_date > max_age_seconds:
        raise SocialAuthError("این ورود تلگرام منقضی شده است؛ دوباره تلاش کنید.")

    return data


# --------------------------------------------------------------------------
# پیامک - کاوه‌نگار (پیش‌فرض). برای افزودن سرویس‌دهنده دیگر، فقط یک کلاس
# مشابه با متد send(to, message) بسازید و در get_sms_client اضافه کنید.
# --------------------------------------------------------------------------
class SMSProviderError(Exception):
    pass


class KavenegarSMSClient:
    def __init__(self, api_key, sender_line=None):
        self.api_key = api_key
        self.sender_line = sender_line or None
        self.send_url = f"https://api.kavenegar.com/v1/{api_key}/sms/send.json"

    def send(self, to, message):
        payload = {"receptor": to, "message": message}
        if self.sender_line:
            payload["sender"] = self.sender_line
        try:
            response = requests.post(self.send_url, data=payload, timeout=10)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise SMSProviderError(f"ارسال پیامک ناموفق بود: {exc}") from exc

        data = response.json()
        status = (data.get("return") or {}).get("status")
        if status != 200:
            message = (data.get("return") or {}).get("message", "خطای نامشخص از سرویس پیامک")
            raise SMSProviderError(message)
        return data


def get_sms_client():
    from .models import SocialAuthSettings

    settings_obj = SocialAuthSettings.load()
    if settings_obj.sms_provider == "kavenegar":
        return KavenegarSMSClient(settings_obj.sms_api_key, settings_obj.sms_sender_line)
    raise SMSProviderError(f"سرویس پیامک «{settings_obj.sms_provider}» پیاده‌سازی نشده است.")


def generate_and_send_otp(phone_number):
    code = f"{random.randint(0, 999999):06d}"
    PhoneOTP.objects.create(
        phone_number=phone_number, code=code,
        expires_at=timezone.now() + timezone.timedelta(minutes=2),
    )
    client = get_sms_client()
    client.send(phone_number, f"کد ورود شما به یاشیل آرت: {code}\nاین کد ۲ دقیقه اعتبار دارد.")


def verify_otp(phone_number, code):
    otp = (
        PhoneOTP.objects.filter(phone_number=phone_number, is_used=False)
        .order_by("-created_at")
        .first()
    )
    if not otp:
        raise SocialAuthError("کدی برای این شماره ارسال نشده یا قبلاً استفاده شده است.")
    if otp.expires_at < timezone.now():
        raise SocialAuthError("کد منقضی شده است؛ دوباره درخواست دهید.")
    if otp.attempts >= 5:
        raise SocialAuthError("تعداد تلاش‌های مجاز تمام شد؛ دوباره درخواست دهید.")
    if otp.code != code:
        otp.attempts += 1
        otp.save(update_fields=["attempts"])
        raise SocialAuthError("کد وارد‌شده نادرست است.")

    otp.is_used = True
    otp.save(update_fields=["is_used"])


# --------------------------------------------------------------------------
# پیدا کردن یا ساختن کاربر - مشترک بین گوگل/تلگرام/پیامک
# --------------------------------------------------------------------------
def get_or_create_social_user(provider, provider_user_id, email=None, first_name="", last_name="",
                               phone_number=None, extra_data=None):
    identity = (
        SocialIdentity.objects.filter(provider=provider, provider_user_id=str(provider_user_id))
        .select_related("user")
        .first()
    )
    if identity:
        return identity.user

    user = None
    if email:
        user = User.objects.filter(email__iexact=email).first()
    if not user and phone_number:
        user = User.objects.filter(phone_number=phone_number).exclude(phone_number="").first()

    if not user:
        base_username = (email.split("@")[0] if email else f"{provider}_{provider_user_id}").lower()
        base_username = "".join(ch for ch in base_username if ch.isalnum() or ch in "._-") or provider
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            counter += 1
            username = f"{base_username}{counter}"

        user = User(
            username=username,
            email=email or f"{username}@social.local",
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number or "",
        )
        user.set_unusable_password()
        user.save()

    SocialIdentity.objects.get_or_create(
        provider=provider, provider_user_id=str(provider_user_id),
        defaults={"user": user, "extra_data": extra_data or {}},
    )
    return user