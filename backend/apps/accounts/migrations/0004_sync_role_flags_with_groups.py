from django.db import migrations

# نقش‌هایی که پنل جداگانه (غیر از پنل مدیریت) دارند
ACADEMY_PANEL_ROLES = {"هنرآموز", "استاد"}


def sync_role_flags(apps, schema_editor):
    """
    یکپارچه‌سازی داده‌های قدیمی با قانون جدید «نقش = عضویت در گروه»:

    - is_student فقط از عضویت در گروه «هنرآموز» محاسبه می‌شود.
    - is_instructor فقط از عضویت در گروه «استاد» محاسبه می‌شود.
    - داشتن هر گروه دیگری (نقش‌های فروشگاه/بک‌آفیس یا «مدیر آموزشگاه») به معنای
      کاربرِ داخلی پنل مدیریت است -> is_staff=True (و superuser همیشه staff است).

    is_staff کاربرانی که هیچ گروه داخلی ندارند دست‌کاری نمی‌شود (محافظه‌کارانه،
    تا دسترسیِ قبلاً داده‌شده ناگهان حذف نشود؛ مدیر می‌تواند از صفحه «کاربران»
    نقش‌ها را بازتنظیم کند).
    """

    User = apps.get_model("accounts", "User")
    Group = apps.get_model("auth", "Group")

    group_names = set(Group.objects.values_list("name", flat=True))
    student_group = "هنرآموز" if "هنرآموز" in group_names else None
    instructor_group = "استاد" if "استاد" in group_names else None
    internal_group_names = group_names - ACADEMY_PANEL_ROLES

    for user in User.objects.all():
        names = set(user.groups.values_list("name", flat=True))

        updates = {}
        if student_group is not None:
            updates["is_student"] = student_group in names
        if instructor_group is not None:
            updates["is_instructor"] = instructor_group in names

        has_internal_role = bool(names & internal_group_names)
        if user.is_superuser or has_internal_role:
            if not user.is_staff:
                updates["is_staff"] = True

        changed = {f: v for f, v in updates.items() if getattr(user, f, None) != v}
        if not changed:
            continue
        for field, value in changed.items():
            setattr(user, field, value)
        user.save(update_fields=list(changed))


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_user_is_instructor_user_is_student"),
    ]

    operations = [
        migrations.RunPython(sync_role_flags, noop),
    ]
