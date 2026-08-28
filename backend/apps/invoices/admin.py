from django.contrib import admin

from .models import Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0
    readonly_fields = [
        "product", "product_name", "variant_label",
        "unit_price", "quantity", "discount_amount", "tax_amount",
    ]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "invoice_number", "order", "user", "status",
        "grand_total", "is_archived", "email_sent", "created_at",
    ]
    list_filter = ["status", "is_archived", "email_sent"]
    search_fields = ["invoice_number", "buyer_full_name", "buyer_email"]
    readonly_fields = [
        "invoice_number", "issued_at", "email_sent", "email_sent_at",
        "archived_at", "created_at", "updated_at",
    ]
    inlines = [InvoiceItemInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # ویرایش رکورد موجود
            return self.readonly_fields + ["order", "user"]
        return self.readonly_fields