from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = "حساب‌های کاربری"

    def ready(self):
        # همگام‌سازی خودکار نقش‌ها (Group) با فلگ‌های کاربر
        from . import signals  # noqa: F401
