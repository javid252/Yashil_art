from rest_framework import serializers

from .models import Payment, PaymentSettings


class PaymentSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSettings
        fields = [
            "card_transfer_enabled", "card_number", "card_holder_name", "bank_name",
            "card_transfer_instructions", "online_gateway_enabled",
            "zarinpal_merchant_id", "zarinpal_sandbox",
        ]


class PublicPaymentSettingsSerializer(serializers.ModelSerializer):
    """
    نسخه عمومی - فقط چیزی که مشتری در صفحه انتخاب روش پرداخت باید ببیند.
    merchant_id هرگز به فرانت‌اند فاش نمی‌شود.
    """

    class Meta:
        model = PaymentSettings
        fields = [
            "card_transfer_enabled", "card_number", "card_holder_name", "bank_name",
            "card_transfer_instructions", "online_gateway_enabled",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    method_display = serializers.CharField(source="get_method_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    order_id = serializers.IntegerField(source="order.id", read_only=True)
    customer_username = serializers.CharField(source="order.user.username", read_only=True, default=None)
    reviewed_by_username = serializers.CharField(source="reviewed_by.username", read_only=True, default=None)

    class Meta:
        model = Payment
        fields = [
            "id", "order_id", "customer_username", "method", "method_display", "status", "status_display",
            "amount", "receipt_image", "gateway_authority", "gateway_ref_id", "admin_note",
            "reviewed_by_username", "reviewed_at", "created_at",
        ]
        read_only_fields = [
            "id", "order_id", "customer_username", "method", "amount", "gateway_authority",
            "gateway_ref_id", "reviewed_by_username", "reviewed_at", "created_at",
        ]


class CardTransferSubmitSerializer(serializers.Serializer):
    order = serializers.IntegerField()
    receipt_image = serializers.ImageField()


class OnlinePaymentInitiateSerializer(serializers.Serializer):
    order = serializers.IntegerField()