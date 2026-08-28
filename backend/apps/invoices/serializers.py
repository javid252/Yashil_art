from rest_framework import serializers

from .models import Invoice, InvoiceItem


class InvoiceItemSerializer(serializers.ModelSerializer):
    """سریالایزر آیتم فاکتور"""

    line_total = serializers.DecimalField(
        max_digits=14, decimal_places=0, read_only=True,
    )
    line_total_after_discount = serializers.DecimalField(
        max_digits=14, decimal_places=0, read_only=True,
    )
    formatted_unit_price = serializers.CharField(read_only=True)
    formatted_line_total = serializers.CharField(read_only=True)
    formatted_line_total_after_discount = serializers.CharField(read_only=True)

    class Meta:
        model = InvoiceItem
        fields = [
            "id", "product", "product_name", "variant_label",
            "unit_price", "quantity", "discount_amount", "tax_amount",
            "line_total", "line_total_after_discount",
            "formatted_unit_price", "formatted_line_total",
            "formatted_line_total_after_discount",
        ]


class InvoiceSerializer(serializers.ModelSerializer):
    """سریالایزر اصلی فاکتور (برای لیست و جزئیات)"""

    items = InvoiceItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    status_display_fa = serializers.CharField(read_only=True)
    formatted_grand_total = serializers.CharField(read_only=True)
    order_id_display = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            "id", "invoice_number", "status", "status_display", "status_display_fa",
            "order", "order_id_display", "user",
            "buyer_full_name", "buyer_phone", "buyer_email",
            "buyer_address", "buyer_postal_code",
            "subtotal", "discount_total", "tax_total", "grand_total",
            "formatted_grand_total",
            "notes", "is_archived", "archived_at",
            "email_sent", "email_sent_at",
            "issued_at", "created_at", "updated_at",
            "items",
        ]
        read_only_fields = [
            "invoice_number", "user", "subtotal", "grand_total",
            "is_archived", "archived_at", "email_sent", "email_sent_at",
            "issued_at", "created_at", "updated_at",
        ]

    def get_order_id_display(self, obj):
        return f"#{obj.order_id}"


class InvoiceListSerializer(serializers.ModelSerializer):
    """سریالایزر سبک برای لیست فاکتورها"""

    status_display = serializers.CharField(source="get_status_display", read_only=True)
    status_display_fa = serializers.CharField(read_only=True)
    formatted_grand_total = serializers.CharField(read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            "id", "invoice_number", "status", "status_display", "status_display_fa",
            "order", "grand_total", "formatted_grand_total",
            "is_archived", "issued_at", "created_at", "items_count",
        ]

    def get_items_count(self, obj):
        return obj.items.count()


class InvoiceStatusUpdateSerializer(serializers.ModelSerializer):
    """سریالایزر تغییر وضعیت فاکتور"""

    class Meta:
        model = Invoice
        fields = ["status"]


class InvoiceNoteUpdateSerializer(serializers.ModelSerializer):
    """سریالایزر بروزرسانی یادداشت فاکتور"""

    class Meta:
        model = Invoice
        fields = ["notes"]


class InvoiceArchiveSerializer(serializers.Serializer):
    """سریالایزر عملیات بایگانی"""

    archive = serializers.BooleanField(required=True)