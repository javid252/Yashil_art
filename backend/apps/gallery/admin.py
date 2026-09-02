from django.contrib import admin

from .models import GalleryArtwork, GalleryCategory, GalleryComment, GalleryExhibition, GalleryLike


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_active", "order"]
    list_editable = ["is_active", "order"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(GalleryExhibition)
class GalleryExhibitionAdmin(admin.ModelAdmin):
    list_display = ["title", "start_date", "end_date", "location", "is_active", "is_virtual"]
    list_filter = ["is_active", "is_virtual"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(GalleryArtwork)
class GalleryArtworkAdmin(admin.ModelAdmin):
    list_display = ["title", "artist", "category", "medium", "likes_count", "views_count", "is_featured", "is_for_sale"]
    list_filter = ["medium", "is_featured", "is_for_sale", "is_sold", "category"]
    search_fields = ["title", "description", "artist__first_name", "artist__last_name"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["artist", "instructor", "category", "exhibition"]
    list_editable = ["is_featured", "is_for_sale"]


@admin.register(GalleryComment)
class GalleryCommentAdmin(admin.ModelAdmin):
    list_display = ["user", "artwork", "is_approved", "created_at"]
    list_filter = ["is_approved"]
    raw_id_fields = ["user", "artwork"]


@admin.register(GalleryLike)
class GalleryLikeAdmin(admin.ModelAdmin):
    list_display = ["user", "artwork", "created_at"]
    raw_id_fields = ["user", "artwork"]
