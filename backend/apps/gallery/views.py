from django.contrib.auth import get_user_model

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.access.permissions import IsEducationAdmin

from .models import GalleryArtwork, GalleryCategory, GalleryComment, GalleryExhibition, GalleryLike
from .serializers import (
    GalleryArtworkDetailSerializer,
    GalleryArtworkListSerializer,
    GalleryArtworkWriteSerializer,
    GalleryCategorySerializer,
    GalleryCommentSerializer,
    GalleryExhibitionSerializer,
)


class GalleryCategoryViewSet(viewsets.ModelViewSet):
    queryset = GalleryCategory.objects.all()
    serializer_class = GalleryCategorySerializer
    permission_classes = [IsEducationAdmin]
    pagination_class = None

    def get_queryset(self):
        qs = GalleryCategory.objects.all()
        user = self.request.user
        if user and user.is_authenticated and user.is_staff:
            return qs
        return qs.filter(is_active=True)


class GalleryExhibitionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsEducationAdmin]
    filterset_fields = ["is_active", "is_virtual"]
    serializer_class = GalleryExhibitionSerializer

    def get_queryset(self):
        qs = GalleryExhibition.objects.all()
        user = self.request.user
        if user and user.is_authenticated and user.is_staff:
            return qs
        return qs.filter(is_active=True)


class GalleryArtworkViewSet(viewsets.ModelViewSet):
    """آثار هنری: خواندن عمومی، نوشتن فقط مدیر آموزشگاه/مدیرکل."""

    permission_classes = [IsEducationAdmin]
    filterset_fields = ["category", "medium", "is_featured", "is_for_sale", "is_sold", "artist"]
    search_fields = ["title", "description", "artist__first_name", "artist__last_name"]
    ordering_fields = ["created_at", "likes_count", "views_count"]

    def get_queryset(self):
        qs = GalleryArtwork.objects.all()
        user = self.request.user
        # پنل مدیریت همه آثار (از جمله منتشرنشده‌ها) را می‌بیند
        if user and user.is_authenticated and user.is_staff:
            return qs
        return qs.filter(is_published=True)

    def get_serializer_class(self):
        if self.action == "list":
            return GalleryArtworkListSerializer
        if self.action == "retrieve":
            return GalleryArtworkDetailSerializer
        return GalleryArtworkWriteSerializer

    def perform_create(self, serializer):
        if "artist" not in serializer.validated_data:
            serializer.save(artist=self.request.user)
        else:
            serializer.save()

    @action(detail=False, methods=["get"])
    def artist_options(self, request):
        """لیست کاربران فعال برای انتخاب «هنرمند» اثر در فرم گالری (فقط staff)."""
        user = request.user
        if not (user and user.is_authenticated and user.is_staff):
            return Response({"detail": "دسترسی مجاز نیست."}, status=status.HTTP_403_FORBIDDEN)
        users = (
            get_user_model().objects.filter(is_active=True)
            .order_by("first_name", "last_name", "username")
            .values("id", "first_name", "last_name", "username")[:300]
        )
        return Response([
            {
                "id": u["id"],
                "name": " ".join(filter(None, [u["first_name"], u["last_name"]])) or u["username"],
            }
            for u in users
        ])

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=["views_count"])
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        artwork = self.get_object()
        like, created = GalleryLike.objects.get_or_create(artwork=artwork, user=request.user)
        if not created:
            like.delete()
            artwork.likes_count = max(0, artwork.likes_count - 1)
            artwork.save(update_fields=["likes_count"])
            return Response({"liked": False, "likes_count": artwork.likes_count})
        artwork.likes_count += 1
        artwork.save(update_fields=["likes_count"])
        return Response({"liked": True, "likes_count": artwork.likes_count})

    @action(detail=True, methods=["get", "post"], permission_classes=[AllowAny])
    def comments(self, request, pk=None):
        artwork = self.get_object()
        if request.method == "GET":
            comments = artwork.comments.filter(is_approved=True)
            serializer = GalleryCommentSerializer(comments, many=True)
            return Response(serializer.data)

        if not request.user.is_authenticated:
            return Response({"error": "برای ارسال نظر باید وارد شوید."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = GalleryCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, artwork=artwork)
        return Response(serializer.data, status=status.HTTP_201_CREATED)