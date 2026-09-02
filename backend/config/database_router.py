"""
Database Router for Yashil Art Academy

This router directs education-related apps to a separate database (`education`),
while keeping the shop/apps on the default database.

Education apps:
    - courses
    - instructors
    - enrollments
    - attendance
    - grades
    - certificates
    - gallery
    - workshops

Important:
    - User model (accounts.User) stays in the default database for shared authentication
    - ForeignKey relationships from education apps to User are handled via cross-database
      references (Django supports this with ForeignKey to a shared model)
    - All other education models use the education database
"""


# Apps that use the separate education database
EDUCATION_APPS = {
    "courses",
    "instructors",
    "enrollments",
    "attendance",
    "grades",
    "certificates",
    "gallery",
    "workshops",
}


class EducationDatabaseRouter:
    """
    Routes education apps to the 'education' database.
    All other apps use the 'default' database.
    """

    def _is_education_app(self, app_label):
        """Check if the app belongs to education apps."""
        return app_label in EDUCATION_APPS

    def db_for_read(self, model, **hints):
        """Send reads for education models to the education database."""
        app_label = model._meta.app_label

        # Education apps go to education database
        if self._is_education_app(app_label):
            return "education"

        # Everything else uses default database
        return "default"

    def db_for_write(self, model, **hints):
        """Send writes for education models to the education database."""
        app_label = model._meta.app_label

        if self._is_education_app(app_label):
            return "education"

        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations between models.

        Cross-database relations are allowed when:
        - Both objects are from education apps (same database)
        - One is from an education app and the other is User (shared auth)
        - Both are from non-education apps (same database)
        """
        db_set = {"default", "education"}

        # Check if both models are in education apps
        obj1_education = self._is_education_app(obj1._meta.app_label)
        obj2_education = self._is_education_app(obj2._meta.app_label)

        # Allow cross-database relations for User model (shared auth)
        if obj1._meta.app_label == "accounts" or obj2._meta.app_label == "accounts":
            return True

        # Allow relations within the same database type
        if obj1_education == obj2_education:
            return True

        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Control which models can be migrated to which database.

        - Education apps only migrate to 'education' database
        - Non-education apps only migrate to 'default' database
        - User model (accounts) always goes to 'default' for shared auth
        """
        if db == "education":
            # Education database should only have education app tables
            return self._is_education_app(app_label)
        elif db == "default":
            # Default database should have everything except education tables
            return not self._is_education_app(app_label)

        # Unknown database - don't allow migration
        return False
