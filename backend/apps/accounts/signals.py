"""
همگام‌سازی خودکار بین نقش‌ها (Group) و فلگ‌های کاربر.

«نقش‌ها» (عضویت در Group های جنگو) تنها منبع تعیین نقش کاربر است و فلگ‌های
کاربر (is_student / is_instructor / is_staff) صرفاً «بازتاب» همان عضویت‌ها هستند:

- عضویت در گروه «هنرآموز»     -> is_student=True
- عضویت در گروه «استاد»       -> is_instructor=True
- عضویت در هر نقش داخلیِ پنل مدیریت (حسابدار، انباردار، مدیر آموزشگاه و هر نقش
  سفارشی ساخته‌شده در صفحه «نقش‌ها و دسترسی‌ها») -> is_staff=True

نتیجه: جای تعیین نقش یکتا و یکپارچه است و دیگر دو مسیر موازی (فلگ جدا + گروه
جدا) که باعث تداخل می‌شد وجود ندارد. این تابع در سه جا صدا زده می‌شود تا در
همه مسیرهای تغییر نقش (پنل ادمین، جنگو-ادمین، اسکریپت‌ها و حذف نقش) سازگار بماند:
1. سیگنال m2m_changed (هر تغییری در گروه‌های کاربر)
2. serializer مدیریت کاربران (پس از هر PATCH)
3. حذف یک نقش سفارشی (برای کاربرانی که آن نقش را داشتند)

کاربر «عادی» هیچ نقشی ندارد؛ بنابراین هر سه فلگ او False می‌ماند و فقط امکانات
عمومی سایت (خرید، مشاهده، نظر و ...) را دارد.
"""

from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from apps.access.roles import ROLE_INSTRUCTOR, ROLE_STUDENT, is_internal_role

User = get_user_model()


def recompute_role_flags(user):
    """
    فلگ‌های مرتبط با نقشِ یک کاربر را بر اساس عضویت فعلی او در گروه‌ها
    بازمحاسبه و (فقط در صورت تغییر) ذخیره می‌کند. کاربر ابرمدیر (superuser)
    همیشه staff باقی می‌ماند حتی اگر هیچ گروهی نداشته باشد.
    """
    names = set(user.groups.values_list("name", flat=True))

    expected = {
        "is_student": ROLE_STUDENT in names,
        "is_instructor": ROLE_INSTRUCTOR in names,
        "is_staff": bool(
            user.is_superuser or any(is_internal_role(name) for name in names)
        ),
    }

    changed_fields = [
        field for field, value in expected.items() if getattr(user, field, None) != value
    ]
    if not changed_fields:
        return

    for field in changed_fields:
        setattr(user, field, expected[field])
    user.save(update_fields=changed_fields)


@receiver(m2m_changed, sender=User.groups.through)
def sync_role_flags(sender, instance, action, **kwargs):
    """پس از هر تغییر در گروه‌های کاربر، فلگ‌های مرتبط با نقش را به‌روز کن."""
    if action not in ("post_add", "post_remove", "post_clear"):
        return
    recompute_role_flags(instance)
