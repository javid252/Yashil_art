"""
کلاینت درگاه زرین‌پال - دقیقاً مطابق مستندات رسمی:
https://docs.zarinpal.com/paymentGateway/

نکته مهم: این کلاینت واقعاً به سرور زرین‌پال درخواست HTTP می‌زند. تست کامل آن
(گرفتن Authority واقعی، تکمیل پرداخت، verify) فقط با یک Merchant ID واقعی/آزمایشی
از پنل زرین‌پال شما ممکن است - در محیط توسعه این پروژه، دسترسی شبکه به
zarinpal.com وجود نداشت، پس این بخش فقط بر اساس مستندات نوشته شده، نه تست‌شده
با سرور واقعی.
"""
import requests
from django.conf import settings


class ZarinPalError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.message = message
        self.code = code


class ZarinPalClient:
    def __init__(self, merchant_id, sandbox=True):
        self.merchant_id = merchant_id
        base = "sandbox.zarinpal.com" if sandbox else "payment.zarinpal.com"
        self.request_url = f"https://{base}/pg/v4/payment/request.json"
        self.verify_url = f"https://{base}/pg/v4/payment/verify.json"
        start_pay_host = "sandbox.zarinpal.com" if sandbox else "www.zarinpal.com"
        self.start_pay_url_template = f"https://{start_pay_host}/pg/StartPay/{{authority}}"

    def request_payment(self, amount, callback_url, description, mobile=None, email=None):
        """
        مرحله اول: درخواست پرداخت. amount باید به تومان باشد (زرین‌پال داخلی به ریال
        تبدیل می‌کند طبق نسخه API؛ در v4 مقدار به تومان ارسال می‌شود).
        در صورت موفقیت (authority, redirect_url) برمی‌گرداند.
        """
        payload = {
            "merchant_id": self.merchant_id,
            "amount": int(amount),
            "callback_url": callback_url,
            "description": description,
        }
        if mobile:
            payload["metadata"] = {"mobile": mobile}
        if email:
            payload.setdefault("metadata", {})["email"] = email

        try:
            response = requests.post(self.request_url, json=payload, timeout=15)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise ZarinPalError(f"ارتباط با درگاه زرین‌پال برقرار نشد: {exc}") from exc

        data = response.json()
        result = data.get("data") or {}
        errors = data.get("errors") or {}

        if errors:
            message = errors.get("message", "درخواست پرداخت توسط زرین‌پال رد شد.")
            raise ZarinPalError(message, code=errors.get("code"))

        authority = result.get("authority")
        if not authority:
            raise ZarinPalError("پاسخ نامعتبر از زرین‌پال دریافت شد.")

        return {
            "authority": authority,
            "redirect_url": self.start_pay_url_template.format(authority=authority),
        }

    def verify_payment(self, amount, authority):
        """
        مرحله دوم: بعد از برگشت کاربر از درگاه، این متد پرداخت را نزد زرین‌پال
        تایید می‌کند. در صورت موفقیت ref_id برمی‌گرداند.
        """
        payload = {
            "merchant_id": self.merchant_id,
            "amount": int(amount),
            "authority": authority,
        }
        try:
            response = requests.post(self.verify_url, json=payload, timeout=15)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise ZarinPalError(f"ارتباط با درگاه زرین‌پال برای تایید برقرار نشد: {exc}") from exc

        data = response.json()
        result = data.get("data") or {}
        errors = data.get("errors") or {}

        if errors:
            message = errors.get("message", "تایید پرداخت ناموفق بود.")
            raise ZarinPalError(message, code=errors.get("code"))

        # کد 100 یعنی تایید موفق؛ 101 یعنی قبلاً تایید شده (هم موفق تلقی می‌شود)
        if result.get("code") not in (100, 101):
            raise ZarinPalError("پرداخت تایید نشد.", code=result.get("code"))

        return {"ref_id": result.get("ref_id")}


def get_zarinpal_client():
    from .models import PaymentSettings

    payment_settings = PaymentSettings.load()
    return ZarinPalClient(
        merchant_id=payment_settings.zarinpal_merchant_id,
        sandbox=payment_settings.zarinpal_sandbox,
    )