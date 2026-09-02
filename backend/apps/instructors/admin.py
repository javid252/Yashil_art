from django.contrib import admin

from .models import Instructor, InstructorPortfolio


class InstructorPortfolioInline(admin.TabularInline):
    model = InstructorPortfolio
    extra = 3


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ["display_name", "years_experience", "students_count", "rating", "is_featured", "is_active"]
    list_filter = ["is_featured", "is_active"]
    search_fields = ["display_name", "bio"]
    prepopulated_fields = {"slug": ("display_name",)}
    inlines = [InstructorPortfolioInline]
    list_editable = ["is_featured", "is_active"]
