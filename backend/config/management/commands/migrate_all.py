"""
Management command to migrate both databases:
- default: Shop/products/orders/invoices
- education: Courses/instructors/enrollments/grades/gallery

Usage:
    python manage.py migrate_all
    python manage.py migrate_all --education-only
    python manage.py migrate_all --default-only
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Migrate both default and education databases"

    def add_arguments(self, parser):
        parser.add_argument(
            "--education-only",
            action="store_true",
            help="Only migrate the education database",
        )
        parser.add_argument(
            "--default-only",
            action="store_true",
            help="Only migrate the default (shop) database",
        )

    def handle(self, *args, **options):
        education_only = options["education_only"]
        default_only = options["default_only"]

        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS("Database Migration Tool"))
        self.stdout.write(self.style.SUCCESS("=" * 60))

        # Migrate default database (shop)
        if not education_only:
            self.stdout.write("\n" + self.style.WARNING("Migrating DEFAULT database (shop)..."))
            try:
                call_command("migrate", "default", verbosity=1)
                self.stdout.write(self.style.SUCCESS("✓ Default database migrated successfully"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Default database migration failed: {e}"))

        # Migrate education database
        if not default_only:
            self.stdout.write("\n" + self.style.WARNING("Migrating EDUCATION database..."))
            try:
                call_command("migrate", "education", verbosity=1)
                self.stdout.write(self.style.SUCCESS("✓ Education database migrated successfully"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Education database migration failed: {e}"))

        self.stdout.write("\n" + self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS("Migration complete!"))
        self.stdout.write(self.style.SUCCESS("=" * 60))

        # Show database status
        self.stdout.write("\n" + self.style.WARNING("Database Status:"))
        self.stdout.write("  Default database: Shop, Users, Orders, Invoices, etc.")
        self.stdout.write("  Education database: Courses, Enrollments, Gallery, etc.")
        self.stdout.write("  User authentication: Shared (default database)")
