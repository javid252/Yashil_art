"""
Management command to show database status and table information.

Usage:
    python manage.py db_status
"""

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

from config.database_router import EDUCATION_APPS


class Command(BaseCommand):
    help = "Show status of both databases (default and education)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(self.style.SUCCESS("Yashil Art Academy - Database Status"))
        self.stdout.write(self.style.SUCCESS("=" * 70))

        # Database configuration
        self.stdout.write("\n" + self.style.WARNING("Database Configuration:"))
        for db_name, db_config in settings.DATABASES.items():
            engine = db_config.get("ENGINE", "unknown")
            name = db_config.get("NAME", "unknown")
            self.stdout.write(f"  {db_name}: {engine} -> {name}")

        # Apps by database
        self.stdout.write("\n" + self.style.WARNING("Apps by Database:"))

        default_apps = []
        education_apps_list = []

        for app_config in apps.get_app_configs():
            if app_config.label in EDUCATION_APPS:
                education_apps_list.append(app_config.label)
            elif not app_config.label.startswith("django."):
                default_apps.append(app_config.label)

        self.stdout.write(f"\n  Default database ({len(default_apps)} apps):")
        for app in sorted(default_apps):
            self.stdout.write(f"    - {app}")

        self.stdout.write(f"\n  Education database ({len(education_apps_list)} apps):")
        for app in sorted(education_apps_list):
            self.stdout.write(f"    - {app}")

        # Table counts (if databases are accessible)
        self.stdout.write("\n" + self.style.WARNING("Table Counts:"))
        for db_name in ["default", "education"]:
            try:
                from django.db import connection
                cursor = connection.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'django_%' ORDER BY name")
                tables = [row[0] for row in cursor.fetchall()]

                if tables:
                    self.stdout.write(f"\n  {db_name} database ({len(tables)} tables):")
                    for table in tables:
                        try:
                            cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
                            count = cursor.fetchone()[0]
                            self.stdout.write(f"    - {table}: {count} rows")
                        except Exception:
                            self.stdout.write(f"    - {table}: (count unavailable)")
                else:
                    self.stdout.write(f"\n  {db_name} database: No tables found")
            except Exception as e:
                self.stdout.write(f"\n  {db_name} database: Error - {e}")

        self.stdout.write("\n" + self.style.SUCCESS("=" * 70))
