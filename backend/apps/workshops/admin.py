from django.contrib import admin

from .models import Workshop, WorkshopCategory, WorkshopRegistration


@admin.register(WorkshopCategory)
class WorkshopCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_active", "order"]
    list_editable = ["is_active", "order"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "instructor", "duration_type", "status", "start_date", "price", "enrolled_count", "is_featured"]
    list_filter = ["duration_type", "status", "is_featured", "is_online"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["category", "instructor"]
    list_editable = ["status", "is_featured"]


@admin.register(WorkshopRegistration)
class WorkshopRegistrationAdmin(admin.ModelAdmin):
    list_display = ["user", "workshop", "status", "registered_at"]
    list_filter = ["status"]
    search_fields = ["user__username", "workshop__title"]
    raw_id_fields = ["user", "workshop"]
