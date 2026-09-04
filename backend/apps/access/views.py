from django.contrib.auth.models import Group, Permission
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsSuperUser
from .roles import SYSTEM_ROLE_NAMES, ensure_default_roles, is_system_role
from .serializers import MANAGEABLE_APPS, GroupSerializer, PermissionSerializer


class PermissionCatalogueView(APIView):
    """
    فهرست همه پرمیشن‌های قابل‌واگذاری، دسته‌بندی‌شده بر اساس اپ - برای ساخت
    چک‌باکس‌های صفحه «ساخت/ویرایش نقش» در پنل ادمین استفاده می‌شود.
    """

    permission_classes = [IsSuperUser]

    def get(self, request):
        qs = (
            Permission.objects.filter(content_type__app_label__in=MANAGEABLE_APPS)
            .select_related("content_type")
            .order_by("content_type__app_label", "content_type__model", "codename")
        )
        grouped = {}
        for perm in qs:
            app = perm.content_type.app_label
            grouped.setdefault(app, []).append(PermissionSerializer(perm).data)
        return Response(grouped)


class RoleViewSet(viewsets.ModelViewSet):
    """
    CRUD نقش‌ها (Group های جنگو) - فقط ادمین اصلی (superuser).

    نقش‌های سیستمی (حسابدار، انباردار، هنرآموز، استاد، مدیر آموزشگاه) از اینجا
    قابل حذف/تغییرنام نیستند تا دسته‌بندی نقش‌ها ثابت بماند؛ ادمین برای نیازهای
    خاص، نقش جدید می‌سازد.
    """

    queryset = Group.objects.all().prefetch_related("permissions__content_type")
    serializer_class = GroupSerializer
    permission_classes = [IsSuperUser]
    # تعداد نقش‌ها محدود است؛ همه را یکجا برمی‌گردانیم تا صفحه «کاربران» و «نقش‌ها»
    # بدون دغدغه صفحه‌بندی از آن استفاده کنند.
    pagination_class = None

    def get_queryset(self):
        # نقش‌های سیستمی پیش‌فرض در صورت نبودن ساخته می‌شوند
        ensure_default_roles()
        return super().get_queryset()

    def perform_create(self, serializer):
        name = serializer.validated_data.get("name", "")
        if name in SYSTEM_ROLE_NAMES:
            raise ValidationError({"name": "این نام یک نقش سیستمی است و قابل ساخت مجدد نیست."})
        serializer.save()

    def perform_update(self, serializer):
        if is_system_role(self.get_object().name):
            raise ValidationError("نقش‌های سیستمی قابل ویرایش نیستند؛ برای نیاز خاص یک نقش جدید بسازید.")
        serializer.save()

    def perform_destroy(self, instance):
        if is_system_role(instance.name):
            raise ValidationError("نقش‌های سیستمی قابل حذف نیستند.")

        # قبل از حذف، کاربرانی که این نقش را داشتند مشخص کن تا دسترسی‌شان
        # (فلگ‌های is_staff/is_student/is_instructor) پس از حذف نقش اصلاح شود
        # (حذف cascade گروه سیگنال m2m را اجرا نمی‌کند).
        from django.contrib.auth import get_user_model

        from apps.accounts.signals import recompute_role_flags

        affected_ids = list(instance.user_set.values_list("id", flat=True))
        instance.delete()
        if affected_ids:
            User = get_user_model()
            for user in User.objects.filter(id__in=affected_ids):
                recompute_role_flags(user)