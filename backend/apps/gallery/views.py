from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import GalleryArtwork, GalleryCategory, GalleryComment, GalleryExhibition, GalleryLike
from .serializers import (
    GalleryArtworkDetailSerializer,
    GalleryArtworkListSerializer,
    GalleryCategorySerializer,
    GalleryCommentSerializer,
    GalleryExhibitionSerializer,
)


class GalleryCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GalleryCategory.objects.filter(is_active=True)
    serializer_class = GalleryCategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None


class GalleryExhibitionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filterset_fields = ["is_active", "is_virtual"]
    serializer_class = GalleryExhibitionSerializer

    def get_queryset(self):
        return GalleryExhibition.objects.filter(is_active=True)


class GalleryArtworkViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    filterset_fields = ["category", "medium", "is_featured", "is_for_sale", "is_sold", "artist"]
    search_fields = ["title", "description", "artist__first_name", "artist__last_name"]
    ordering_fields = ["created_at", "likes_count", "views_count"]

    def get_queryset(self):
        return GalleryArtwork.objects.filter(is_published=True)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GalleryArtworkDetailSerializer
        return GalleryArtworkListSerializer

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
