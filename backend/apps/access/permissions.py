from rest_framework import permissions


class StrictDjangoModelPermissions(permissions.DjangoModelPermissions):
    """
    نسخه‌ای از DjangoModelPermissions که GET را هم permission-gate می‌کند.
    نسخه پیش‌فرض DRF فقط متدهای POST/PUT/PATCH/DELETE را چک می‌کند و GET را
    برای هر کاربر لاگین‌کرده باز می‌گذارد؛ برای ماژول‌های کاملاً داخلی/حساس
    (حسابداری، انبار، مدیریت کاربران) این رفتار کافی نیست.

    استفاده: این کلاس را روی ViewSet هایی بگذارید که هیچ بخش عمومی (public) ندارند.
    برای ViewSet هایی که بخشی از داده‌شان عمومی است (مثل محصولات)، از این کلاس
    مستقیم استفاده نکنید - باید منطق دستی بنویسید (نمونه در apps/products/permissions.py).
    """

    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }


class IsSuperUser(permissions.BasePermission):
    """فقط ادمین اصلی (superuser) - برای مدیریت نقش‌ها و تنظیمات حساس پلتفرم."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


def model_perm_codename(method, app_label, model_name):
    """کدنیم پرمیشن جنگو متناظر با یک متد HTTP را برمی‌گرداند."""
    mapping = {
        "GET": "view", "OPTIONS": None, "HEAD": None,
        "POST": "add", "PUT": "change", "PATCH": "change", "DELETE": "delete",
    }
    action = mapping.get(method)
    if not action:
        return None
    return f"{app_label}.{action}_{model_name}"


class IsEducationAdmin(permissions.BasePermission):
    """
    برای ماژول‌های آموزشگاه (دوره‌ها، اساتید، گالری، کارگاه‌ها):

    خواندن برای عموم آزاد است؛ نوشتن (ساخت/ویرایش/حذف) فقط برای staff که
    نقش «مدیر آموزشگاه» یا «مدیرکل» دارد (یا superuser). پرمیشن جنگویی اعمال
    نمی‌شود چون اپ‌های آموزشگاه در دیتابیس جداگانه‌اند و دسترسی به آن‌ها از
    طریق نقش‌ها و فلگ‌های کاربر مدیریت می‌شود - نه از طریق Group+Permission.
    این یعنی حسابدار/انباردار/مدیر فروشگاه (که staff هستند ولی نقش آموزشگاهی
    ندارند) نمی‌توانند محتوای آموزشی بسازند یا تغییر دهند.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not (user and user.is_authenticated and user.is_staff):
            return False
        if user.is_superuser:
            return True
        try:
            from apps.access.roles import ROLE_ACADEMY_MANAGER, ROLE_GENERAL_MANAGER
        except ImportError:
            # اگر فایل roles.py وجود نداشته باشد، هر staff مجاز است
            return True
        names = set(user.groups.values_list("name", flat=True))
        return ROLE_ACADEMY_MANAGER in names or ROLE_GENERAL_MANAGER in names


class IsAdminWithModelPerm(permissions.BasePermission):
    """
    برای ViewSet هایی که کلاً بخش عمومی ندارند (فقط پنل ادمین/نقش‌های داخلی):
    کاربر باید is_staff باشد و پرمیشن جنگوی متناظر با مدل و متد HTTP را داشته باشد.
    superuser به‌طور خودکار (توسط خود جنگو در has_perm) از این چک عبور می‌کند.
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated and user.is_staff):
            return False
        queryset = getattr(view, "queryset", None)
        if queryset is None:
            return True
        model = queryset.model
        codename = model_perm_codename(request.method, model._meta.app_label, model._meta.model_name)
        if codename is None:
            return True
        return user.has_perm(codename)