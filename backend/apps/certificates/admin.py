from django.contrib import admin

from .models import Certificate, CertificateTemplate


@admin.register(CertificateTemplate)
class CertificateTemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "course", "is_active"]
    list_editable = ["is_active"]


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ["certificate_number", "student_name", "course_name", "status", "issued_date", "grade"]
    list_filter = ["status", "issued_date"]
    search_fields = ["certificate_number", "student_name", "course_name", "unique_code"]
    readonly_fields = ["unique_code", "certificate_number"]
    raw_id_fields = ["student", "course", "enrollment"]
