"""
تنظیمات پروژه فروشگاه یاشیل آرت (Yashil Art Shop)
Django 4.2 + DRF + SimpleJWT

Development:
    SQLite

Production:
    MariaDB / MySQL
"""

import os
from datetime import timedelta
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# Environment
# ============================================================

# Load local .env if it exists.
#
# IMPORTANT:
# override=False means that real environment variables
# supplied by the server/cPanel have priority over .env.
#
load_dotenv(BASE_DIR / ".env", override=False)


DJANGO_ENV = os.environ.get("DJANGO_ENV", "development").strip().lower()

if DJANGO_ENV not in ("development", "production"):
    raise RuntimeError(
        "DJANGO_ENV must be either 'development' or 'production'"
    )


IS_PRODUCTION = DJANGO_ENV == "production"


# ============================================================
# Security
# ============================================================

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

if IS_PRODUCTION and not SECRET_KEY:
    raise RuntimeError(
        "DJANGO_SECRET_KEY must be set in production."
    )

if not SECRET_KEY:
    SECRET_KEY = "dev-only-secret-key-change-this"


# ============================================================
# Debug
# ============================================================

DEBUG_DEFAULT = "0" if IS_PRODUCTION else "1"

DEBUG = (
    os.environ.get("DJANGO_DEBUG", DEBUG_DEFAULT).strip() == "1"
)


# ============================================================
# Allowed Hosts
# ============================================================

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS", ""
    ).split(",")
    if host.strip()
]


# Production must have explicit hosts.
if IS_PRODUCTION and not ALLOWED_HOSTS:
    raise RuntimeError(
        "DJANGO_ALLOWED_HOSTS must be set in production."
    )


# ============================================================
# Database
# ============================================================

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

DATABASE_SSL_REQUIRE = (
    os.environ.get(
        "DATABASE_SSL_REQUIRE",
        "0",
    ).strip()
    == "1"
)


if DATABASE_URL:

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=DATABASE_SSL_REQUIRE,
        )
    }

    # Ensure proper Unicode support for Persian text.
    DATABASES["default"].setdefault("OPTIONS", {})
    DATABASES["default"]["OPTIONS"]["charset"] = "utf8mb4"


elif IS_PRODUCTION:

    # Never silently fall back to SQLite in production.
    raise RuntimeError(
        "DATABASE_URL must be set in production."
    )


else:

    # Development only
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --------------------------------------------------------------------------
# Apps
# --------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    # Local apps
    "apps.accounts",
    "apps.products",
    "apps.cart",
    "apps.orders",
    "apps.dashboard",
    "apps.vendors",
    "apps.access",
    "apps.inventory",
    "apps.accounting",
    "apps.payments",
    "apps.content",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 6}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
]

# --------------------------------------------------------------------------
# Localization - فارسی / راست‌به‌چپ
# --------------------------------------------------------------------------
LANGUAGE_CODE = "fa-ir"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------------
# فایل‌های استاتیک - WhiteNoise (بدون نیاز به Nginx/CDN جداگانه روی Render)
# --------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================================================
# CORS / CSRF
# ============================================================

_default_origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

_extra_origins = [
    origin.strip()
    for origin in os.environ.get(
        "FRONTEND_URL",
        "",
    ).split(",")
    if origin.strip()
]

CORS_ALLOWED_ORIGINS = list(
    dict.fromkeys(
        _default_origins + _extra_origins
    )
)

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = list(
    dict.fromkeys(_extra_origins)
)
# --------------------------------------------------------------------------
# Django REST Framework
# --------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 12,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=6),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ایمیل بازیابی رمز عبور: در توسعه فقط در کنسول چاپ می‌شود.
# روی Render در صورت تنظیم متغیرهای SMTP_*، به‌صورت واقعی ایمیل ارسال می‌شود.
if os.environ.get("SMTP_HOST"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ["SMTP_HOST"]
    EMAIL_PORT = int(os.environ.get("SMTP_PORT", "587"))
    EMAIL_HOST_USER = os.environ.get("SMTP_USER", "")
    EMAIL_HOST_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
    EMAIL_USE_TLS = os.environ.get("SMTP_USE_TLS", "1") == "1"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

FRONTEND_PAYMENT_RESULT_URL = os.environ.get(
    "FRONTEND_PAYMENT_RESULT_URL",
    "http://localhost:8080/payment-result",
)

FRONTEND_RESET_PASSWORD_URL = os.environ.get(
    "FRONTEND_RESET_PASSWORD_URL",
    "http://localhost:8080/reset-password",
)


# ============================================================
# Production Security
# ============================================================

if IS_PRODUCTION:

    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    SECURE_SSL_REDIRECT = (
        os.environ.get(
            "DJANGO_SECURE_SSL_REDIRECT",
            "0",
        ).strip()
        == "1"
    )

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
