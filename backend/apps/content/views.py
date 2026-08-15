from rest_framework import viewsets

from apps.products.permissions import IsAdminOrReadOnly

from .models import HeroSlide
from .serializers import HeroSlideSerializer


class HeroSlideViewSet(viewsets.ModelViewSet):
    """
    عمومی: فقط اسلایدهای فعال، به ترتیب. پنل ادمین: همه اسلایدها (شامل غیرفعال)
    برای مدیریت کامل - با همان الگوی دسترسی محصولات (IsAdminOrReadOnly).
    """

    serializer_class = HeroSlideSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = HeroSlide.objects.all()

    def get_queryset(self):
        qs = HeroSlide.objects.all()
        user = self.request.user
        if user and user.is_authenticated and user.is_staff:
            return qs
        return qs.filter(is_active=True)