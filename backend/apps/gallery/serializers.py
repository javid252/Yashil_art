from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.instructors.models import Instructor

from .models import GalleryArtwork, GalleryCategory, GalleryComment, GalleryExhibition, GalleryLike

User = get_user_model()


class GalleryCategorySerializer(serializers.ModelSerializer):
    artworks_count = serializers.SerializerMethodField()

    class Meta:
        model = GalleryCategory
        fields = ["id", "name", "slug", "description", "icon", "is_active", "order", "artworks_count"]

    def get_artworks_count(self, obj):
        return obj.artworks.filter(is_published=True).count()


class GalleryExhibitionSerializer(serializers.ModelSerializer):
    artworks_count = serializers.SerializerMethodField()

    class Meta:
        model = GalleryExhibition
        fields = [
            "id", "title", "slug", "description", "cover_image",
            "start_date", "end_date", "location", "is_active", "is_virtual",
            "artworks_count",
        ]

    def get_artworks_count(self, obj):
        return obj.artworks.filter(is_published=True).count()


class GalleryCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = GalleryComment
        fields = ["id", "user", "user_name", "text", "is_approved", "created_at"]
        read_only_fields = ["user", "is_approved"]


class GalleryArtworkListSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source="artist.get_full_name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True, default="")
    medium_display = serializers.CharField(source="get_medium_display", read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = GalleryArtwork
        fields = [
            "id", "title", "slug", "artist", "artist_name", "category", "category_name",
            "medium", "medium_display", "image", "thumbnail", "dimensions",
            "year_created", "likes_count", "views_count",
            "is_featured", "is_for_sale", "sale_price", "is_sold",
            "is_liked", "created_at",
        ]

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class GalleryArtworkWriteSerializer(serializers.ModelSerializer):
    """سریالایزر ساخت/ویرایش اثر هنری از پنل مدیریت آموزشگاه.

    «هنرمند» اختیاری است؛ اگر ارسال نشود، کاربرِ لاگین‌شده (مدیر) به‌عنوان
    سازنده اثر ثبت می‌شود تا بتواند بعداً با انتخاب از لیست هنرجویان آن را اصلاح کند.
    """

    artist = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True,
    )
    instructor = serializers.PrimaryKeyRelatedField(
        queryset=Instructor.objects.all(), required=False, allow_null=True,
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=GalleryCategory.objects.all(), required=False, allow_null=True,
    )
    exhibition = serializers.PrimaryKeyRelatedField(
        queryset=GalleryExhibition.objects.all(), required=False, allow_null=True,
    )
    image = serializers.ImageField(required=False, allow_null=True)
    thumbnail = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = GalleryArtwork
        fields = [
            "id", "artist", "instructor", "category", "exhibition",
            "title", "description", "medium", "dimensions", "year_created",
            "image", "thumbnail",
            "is_featured", "is_published", "is_for_sale", "sale_price",
        ]

    def validate(self, attrs):
        if not self.instance and "image" not in attrs:
            raise serializers.ValidationError({"image": "تصویر اثر الزامی است."})
        return attrs


class GalleryArtworkDetailSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source="artist.get_full_name", read_only=True)
    instructor_name = serializers.CharField(source="instructor.display_name", read_only=True, default="")
    category_name = serializers.CharField(source="category.name", read_only=True, default="")
    exhibition_title = serializers.CharField(source="exhibition.title", read_only=True, default="")
    medium_display = serializers.CharField(source="get_medium_display", read_only=True)
    comments = GalleryCommentSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = GalleryArtwork
        fields = "__all__"

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()
