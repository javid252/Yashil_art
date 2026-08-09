from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.access.permissions import IsAdminWithModelPerm, IsSuperUser
from apps.orders.models import Order

from .models import Payment, PaymentSettings
from .serializers import (
    CardTransferSubmitSerializer,
    OnlinePaymentInitiateSerializer,
    PaymentSerializer,
    PaymentSettingsSerializer,
    PublicPaymentSettingsSerializer,
)
from .services import ZarinPalError, get_zarinpal_client


class PublicPaymentSettingsView(APIView):
    """مشتری در صفحه پرداخت با این endpoint می‌فهمد کدام روش‌ها فعال‌اند."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(PublicPaymentSettingsSerializer(PaymentSettings.load()).data)


class AdminPaymentSettingsView(APIView):
    """تنظیمات کامل پرداخت (شامل شماره کارت و Merchant ID) - فقط ادمین اصلی."""

    permission_classes = [IsSuperUser]

    def get(self, request):
        return Response(PaymentSettingsSerializer(PaymentSettings.load()).data)

    def patch(self, request):
        obj = PaymentSettings.load()
        serializer = PaymentSettingsSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


def _get_own_pending_order(user, order_id):
    return Order.objects.filter(pk=order_id, user=user, status=Order.Status.PENDING).first()


class CardTransferSubmitView(APIView):
    """مشتری بعد از واریز کارت‌به‌کارت، تصویر رسید را اینجا آپلود می‌کند."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        settings_obj = PaymentSettings.load()
        if not settings_obj.card_transfer_enabled:
            return Response({"detail": "روش کارت‌به‌کارت در حال حاضر غیرفعال است."}, status=403)

        serializer = CardTransferSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = _get_own_pending_order(request.user, serializer.validated_data["order"])
        if not order:
            return Response({"detail": "سفارش پیدا نشد یا قبلاً پرداخت شده است."}, status=404)

        payment = Payment.objects.create(
            order=order,
            method=Payment.Method.CARD_TRANSFER,
            status=Payment.Status.SUBMITTED,
            amount=order.total_price,
            receipt_image=serializer.validated_data["receipt_image"],
        )
        return Response(PaymentSerializer(payment).data, status=201)


class OnlinePaymentInitiateView(APIView):
    """مرحله اول درگاه آنلاین: از زرین‌پال Authority می‌گیرد و آدرس ریدایرکت را برمی‌گرداند."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        settings_obj = PaymentSettings.load()
        if not settings_obj.online_gateway_enabled:
            return Response({"detail": "درگاه پرداخت آنلاین در حال حاضر غیرفعال است."}, status=403)
        if not settings_obj.zarinpal_merchant_id:
            return Response({"detail": "درگاه پرداخت هنوز توسط ادمین پیکربندی نشده است."}, status=503)

        serializer = OnlinePaymentInitiateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = _get_own_pending_order(request.user, serializer.validated_data["order"])
        if not order:
            return Response({"detail": "سفارش پیدا نشد یا قبلاً پرداخت شده است."}, status=404)

        payment = Payment.objects.create(
            order=order, method=Payment.Method.ZARINPAL,
            status=Payment.Status.PENDING, amount=order.total_price,
        )

        callback_url = request.build_absolute_uri(reverse("payments-online-callback"))
        client = get_zarinpal_client()
        try:
            result = client.request_payment(
                amount=order.total_price,
                callback_url=callback_url,
                description=f"پرداخت سفارش #{order.id}",
                mobile=getattr(order, "phone_number", None),
            )
        except ZarinPalError as exc:
            payment.status = Payment.Status.FAILED
            payment.admin_note = str(exc)
            payment.save(update_fields=["status", "admin_note"])
            return Response({"detail": str(exc)}, status=502)

        payment.gateway_authority = result["authority"]
        payment.save(update_fields=["gateway_authority"])

        return Response({"redirect_url": result["redirect_url"]})


class OnlinePaymentCallbackView(APIView):
    """
    زرین‌پال بعد از پرداخت، مرورگر کاربر را به این آدرس ریدایرکت می‌کند
    (بدون هدر Authorization - چون درخواست از سمت مرورگر/زرین‌پال است، نه فرانت‌اند ما).
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from django.conf import settings

        authority = request.query_params.get("Authority")
        status_param = request.query_params.get("Status")
        result_base = settings.FRONTEND_PAYMENT_RESULT_URL

        payment = Payment.objects.filter(gateway_authority=authority, method=Payment.Method.ZARINPAL).first()
        if not payment:
            return redirect(f"{result_base}?status=error&reason=payment_not_found")

        if status_param != "OK":
            payment.status = Payment.Status.FAILED
            payment.save(update_fields=["status"])
            return redirect(f"{result_base}?status=cancelled&order={payment.order_id}")

        settings_obj = PaymentSettings.load()
        client = get_zarinpal_client()
        try:
            result = client.verify_payment(amount=payment.amount, authority=authority)
        except ZarinPalError as exc:
            payment.status = Payment.Status.FAILED
            payment.admin_note = str(exc)
            payment.save(update_fields=["status", "admin_note"])
            return redirect(f"{result_base}?status=failed&order={payment.order_id}")

        payment.status = Payment.Status.VERIFIED
        payment.gateway_ref_id = result.get("ref_id") or ""
        payment.reviewed_at = None
        payment.save(update_fields=["status", "gateway_ref_id"])

        order = payment.order
        order.status = Order.Status.PAID
        order.save(update_fields=["status"])

        from apps.accounting.services import ensure_income_transaction

        ensure_income_transaction(order)

        return redirect(f"{result_base}?status=success&order={order.id}")


class AdminPaymentViewSet(viewsets.ModelViewSet):
    """پنل ادمین: بررسی رسیدهای کارت‌به‌کارت و لیست کل پرداخت‌ها."""

    queryset = Payment.objects.select_related("order", "order__user", "reviewed_by")
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminWithModelPerm]
    http_method_names = ["get", "patch", "head", "options"]

    def partial_update(self, request, *args, **kwargs):
        payment = self.get_object()
        new_status = request.data.get("status")

        if new_status not in (Payment.Status.VERIFIED, Payment.Status.REJECTED):
            return Response({"detail": "فقط تایید یا رد مجاز است."}, status=400)

        from django.utils import timezone

        payment.status = new_status
        payment.admin_note = request.data.get("admin_note", payment.admin_note)
        payment.reviewed_by = request.user
        payment.reviewed_at = timezone.now()
        payment.save()

        if new_status == Payment.Status.VERIFIED:
            order = payment.order
            order.status = Order.Status.PAID
            order.save(update_fields=["status"])

            from apps.accounting.services import ensure_income_transaction

            ensure_income_transaction(order, request.user)

        return Response(PaymentSerializer(payment).data)