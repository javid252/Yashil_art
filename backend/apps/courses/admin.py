from django.contrib import admin

from .models import Course, CourseCategory, CourseGallery, CourseSchedule


class CourseScheduleInline(admin.TabularInline):
    model = CourseSchedule
    extra = 1


class CourseGalleryInline(admin.TabularInline):
    model = CourseGallery
    extra = 3


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_active", "order"]
    list_editable = ["is_active", "order"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "instructor", "level", "status", "price", "enrolled_count", "is_featured"]
    list_filter = ["level", "status", "pricing_type", "is_featured", "category"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CourseScheduleInline, CourseGalleryInline]
    list_editable = ["status", "is_featured"]


@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ["course", "day_of_week", "start_time", "end_time", "room", "is_active"]
    list_filter = ["day_of_week", "is_active"]
