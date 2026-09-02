from django.contrib import admin

from .models import Enrollment, SubscriptionPlan


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["user", "course", "status", "payment_type", "enrolled_at", "subscription_expires"]
    list_filter = ["status", "payment_type"]
    search_fields = ["user__username", "user__first_name", "course__title"]
    raw_id_fields = ["user", "course"]


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "is_active"]
    list_editable = ["is_active"]
