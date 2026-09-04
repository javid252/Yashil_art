"""
نقش‌های سیستمی سامانه و دسته‌بندی نقش‌ها.

سامانه سه دسته نقش کاملاً مجزا دارد:

1. نقش‌های «مستقل» (category=independent)
   - «مدیرکل» سامانه؛ نه زیرمجموعه آموزشگاه است و نه فروشگاه و در بالای صفحه‌های
     نقش‌ها/دسترسی‌ها نمایش داده می‌شود. دسترسی کامل به همه ماژول‌های پنل مدیریت
     دارد و is_staff او به‌صورت خودکار فعال می‌شود.

2. نقش‌های «فروشگاه / بک‌آفیس» (category=shop)
   - بر پایه Group های جنگو + پرمیشن‌های ماژول‌ها (محصولات، سفارش، انبار، حسابداری، ...).
   - ادمین می‌تواند از صفحه «نقش‌ها و دسترسی‌ها» نقش جدید بسازد یا نقش موجود را ویرایش کند.
   - کاربر چنین نقشی برای ورود به پنل مدیریت باید is_staff باشد (به‌صورت خودکار تنظیم می‌شود).

3. نقش‌های «آموزشگاه» (category=academy)
   - نقش‌های ازپیش‌تعریف‌شده با پنل/بخش اختصاصی؛ قابل ساخت یا حذف از UI نیستند و فقط از
     صفحه «کاربران» به کاربر تخصیص داده می‌شوند:
       - هنرآموز      -> پنل /student (فلگ is_student)
       - استاد        -> پنل /instructor (فلگ is_instructor)
       - مدیر آموزشگاه -> دسترسی به بخش «آموزشگاه» در پنل مدیریت (is_staff خودکار)
   - تغییر گروه این نقش‌ها با فلگ‌های کاربر از طریق سیگنال‌ها همگام می‌شود (apps/accounts/signals.py).

4. «کاربر عادی» نقشی ندارد؛ فقط خرید/مشاهده/نظر و فعالیت‌های عمومی سایت.
"""

from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist

# ── نام نقش‌های سیستمی ──────────────────────────────────────────────
ROLE_GENERAL_MANAGER = "مدیرکل"
ROLE_SHOP_MANAGER = "مدیر فروشگاه"
ROLE_STUDENT = "هنرآموز"
ROLE_INSTRUCTOR = "استاد"
ROLE_ACADEMY_MANAGER = "مدیر آموزشگاه"
ROLE_ACCOUNTANT = "حسابدار"
ROLE_WAREHOUSE = "انباردار"

# ── دسته‌ها ──────────────────────────────────────────────────────────
CATEGORY_INDEPENDENT = "independent"
CATEGORY_ACADEMY = "academy"
CATEGORY_SHOP = "shop"

# اپ‌های قابل‌مدیریت از پنل ادمین (نویز پرمیشن‌های داخلی جنگو حذف می‌شود؛
# اپ‌های آموزشگاه در دیتابیس جداگانه‌اند و پرمیشن‌شان با Group قابل ترکیب نیست؛
# دسترسی به آن‌ها از طریق نقش‌های آموزشگاه و فلگ‌های کاربر مدیریت می‌شود)
MANAGEABLE_APPS = [
    "accounts", "products", "cart", "orders", "dashboard",
    "vendors", "access", "inventory", "accounting",
    "content", "invoices", "payments",
]

# کدنیم پرمیشن‌های پیشنهادی برای نقش‌های فروشگاه (فقط به‌عنوان نقطه شروع؛
# ادمین بعداً می‌تواند آن‌ها را از صفحه «نقش‌ها» دقیق‌تر کند).
ACCOUNTANT_PERMISSIONS = [
    "orders.view_order",
    "orders.change_order",
    "invoices.view_invoice",
    "invoices.change_invoice",
    "payments.view_payment",
    "payments.change_payment",
    "accounting.view_transactioncategory",
    "accounting.view_transaction",
    "accounting.add_transaction",
    "accounting.change_transaction",
]

WAREHOUSE_PERMISSIONS = [
    "products.view_category",
    "products.view_product",
    "products.change_product",
    "inventory.view_warehouse",
    "inventory.change_warehouse",
    "inventory.view_stockmovement",
    "inventory.add_stockmovement",
    "inventory.change_stockmovement",
]

SHOP_MANAGER_PERMISSIONS = [
    "products.view_category",
    "products.change_category",
    "products.add_category",
    "products.view_product",
    "products.change_product",
    "products.add_product",
    "orders.view_order",
    "orders.change_order",
    "orders.add_order",
    "invoices.view_invoice",
    "invoices.change_invoice",
    "payments.view_payment",
    "payments.change_payment",
    "accounting.view_transactioncategory",
    "accounting.view_transaction",
    "accounting.add_transaction",
    "accounting.change_transaction",
    "inventory.view_warehouse",
    "inventory.change_warehouse",
    "inventory.view_stockmovement",
    "inventory.add_stockmovement",
    "inventory.change_stockmovement",
    "vendors.view_vendor",
    "vendors.change_vendor",
    "content.view_heroslide",
    "content.change_heroslide",
]

# ── کاتالوگ نقش‌های سیستمی ──────────────────────────────────────────
SYSTEM_ROLES = [
    {
        "name": ROLE_GENERAL_MANAGER,
        "category": CATEGORY_INDEPENDENT,
        # دسترسی کامل به همه ماژول‌های پنل مدیریت
        "grant_all": True,
        "description": "مدیرکل سامانه - نقش مستقل و بالاتر از آموزشگاه/فروشگاه با دسترسی کامل به پنل مدیریت",
    },
    {
        "name": ROLE_SHOP_MANAGER,
        "category": CATEGORY_SHOP,
        "description": "مدیر فروشگاه - نظارت کامل بر محصولات، سفارش‌ها، انبار، فاکتورها و مالی",
        "permissions": SHOP_MANAGER_PERMISSIONS,
    },
    {
        "name": ROLE_ACCOUNTANT,
        "category": CATEGORY_SHOP,
        "description": "امور مالی: سفارش‌ها، فاکتورها، پرداخت‌ها و حسابداری",
        "permissions": ACCOUNTANT_PERMISSIONS,
    },
    {
        "name": ROLE_WAREHOUSE,
        "category": CATEGORY_SHOP,
        "description": "انبارداری و مدیریت محصولات و موجودی",
        "permissions": WAREHOUSE_PERMISSIONS,
    },
    {
        "name": ROLE_STUDENT,
        "category": CATEGORY_ACADEMY,
        "flag": "is_student",
        "description": "هنرآموز آموزشگاه - دسترسی به پنل هنرجو (/student)",
        "permissions": [],
    },
    {
        "name": ROLE_INSTRUCTOR,
        "category": CATEGORY_ACADEMY,
        "flag": "is_instructor",
        "description": "استاد آموزشگاه - دسترسی به پنل استاد (/instructor)",
        "permissions": [],
    },
    {
        "name": ROLE_ACADEMY_MANAGER,
        "category": CATEGORY_ACADEMY,
        "description": "مدیر آموزشگاه - دسترسی به بخش آموزشگاه در پنل مدیریت",
        "permissions": [],
    },
]

# هر نقش سیستمی (جز نقش‌های پنل هنرجو/استاد) یعنی کاربرِ دارای آن نقش،
# کاربرِ داخلیِ پنل مدیریت است -> is_staff خودکار فعال می‌شود.
INTERNAL_ROLE_NAMES = {
    ROLE_GENERAL_MANAGER,
    ROLE_SHOP_MANAGER,
    ROLE_ACCOUNTANT,
    ROLE_WAREHOUSE,
    ROLE_ACADEMY_MANAGER,
}

ACADEMY_ROLE_NAMES = {ROLE_STUDENT, ROLE_INSTRUCTOR, ROLE_ACADEMY_MANAGER}
# فقط نقش‌هایی که پنل کاربری جداگانه (غیر از پنل مدیریت) دارند
ACADEMY_PANEL_ROLE_NAMES = {ROLE_STUDENT, ROLE_INSTRUCTOR}
SYSTEM_ROLE_NAMES = {role["name"] for role in SYSTEM_ROLES}


def _normalize(name: str) -> str:
    """حذف همه فاصله‌ها تا نام‌هایی مثل «هنر آموز» و «هنرآموز» یکی در نظر گرفته شوند."""
    return "".join((name or "").split())


_ROLE_DEFS_BY_NAME = {_normalize(role["name"]): role for role in SYSTEM_ROLES}
_SYSTEM_ROLE_NAMES_NORM = {_normalize(n) for n in SYSTEM_ROLE_NAMES}


def role_category(name: str) -> str:
    """دسته‌بندی یک نقش بر اساس نام. نقش‌های ساخته‌شده توسط ادمین، «فروشگاه» محسوب می‌شوند."""
    role = _ROLE_DEFS_BY_NAME.get(_normalize(name))
    if role:
        return role["category"]
    return CATEGORY_SHOP


def is_academy_role(name: str) -> bool:
    return _normalize(name) in {_normalize(n) for n in ACADEMY_ROLE_NAMES}


def is_independent_role(name: str) -> bool:
    """نقش‌های مستقل (مدیرکل) که نه آموزشگاه‌اند و نه فروشگاه."""
    role = _ROLE_DEFS_BY_NAME.get(_normalize(name))
    return bool(role and role.get("category") == CATEGORY_INDEPENDENT)


def is_system_role(name: str) -> bool:
    return _normalize(name) in _SYSTEM_ROLE_NAMES_NORM


def role_description(name: str) -> str:
    role = _ROLE_DEFS_BY_NAME.get(_normalize(name))
    return role["description"] if role else ""


def academy_flag_for_role(name: str):
    """فلگ کاربری متناظر با نقش آموزشگاه (is_student/is_instructor) یا None."""
    role = _ROLE_DEFS_BY_NAME.get(_normalize(name))
    if role and role.get("category") == CATEGORY_ACADEMY:
        return role.get("flag")
    return None


def is_internal_role(name: str) -> bool:
    """
    آیا داشتن این نقش یعنی کاربرِ داخلی پنل مدیریت است (is_staff لازم دارد)؟
    فقط نقش‌های پنل هنرجو/استاد این‌طور نیستند؛ هر نقش دیگری (مدیرکل، مدیر
    فروشگاه، حسابدار، انباردار، مدیر آموزشگاه یا نقش‌های ساخته‌شده توسط ادمین)
    به پنل مدیریت مربوط است.
    """
    return _normalize(name) not in {_normalize(n) for n in ACADEMY_PANEL_ROLE_NAMES}


def _grant_manageable_permissions(group: Group) -> None:
    """همه پرمیشن‌های اپ‌های قابل‌مدیریت را به نقش می‌دهد (برای مدیرکل)."""
    perms = Permission.objects.filter(content_type__app_label__in=MANAGEABLE_APPS)
    existing = set(group.permissions.values_list("pk", flat=True))
    to_add = [perm for perm in perms if perm.pk not in existing]
    if to_add:
        group.permissions.add(*to_add)


def ensure_default_roles():
    """
    ساخت نقش‌های سیستمی در صورت نبودن (idempotent) + اعطای پرمیشن‌های پیشنهادی
    نقش‌های فروشگاه (فقط اضافه می‌کند و هرگز پرمیشنی را از نقش حذف نمی‌کند تا
    تنظیمات دستی ادمین حفظ شود). این تابع هنگام باز شدن صفحه «نقش‌ها/کاربران» صدا زده می‌شود.
    """
    try:
        for definition in SYSTEM_ROLES:
            group, _ = Group.objects.get_or_create(name=definition["name"])
            if definition.get("grant_all"):
                _grant_manageable_permissions(group)
                continue
            for full_codename in definition.get("permissions", []):
                app_label, _, codename = full_codename.partition(".")
                try:
                    perm = Permission.objects.get(
                        content_type__app_label=app_label, codename=codename
                    )
                except ObjectDoesNotExist:
                    continue
                if not group.permissions.filter(pk=perm.pk).exists():
                    group.permissions.add(perm)
    except Exception:
        # در اولین اجرای migrate (قبل از ساخته‌شدن جداول auth) بی‌صدا نادیده گرفته می‌شود؛
        # تضمین‌شده است که قبل از هر درخواست HTTP واقعی، میگریشن‌ها اجرا شده‌اند.
        pass