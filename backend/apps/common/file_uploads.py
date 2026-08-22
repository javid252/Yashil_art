from pathlib import Path
from uuid import uuid4


def safe_image_filename(filename):
    """
    نام امن و یکتای فایل تصویر.
    نام اصلی کاربر، فارسی یا انگلیسی بودن آن، در نام ذخیره‌شده اثری ندارد.
    """
    extension = Path(filename or "").suffix.lower()

    if not extension:
        extension = ".bin"

    return f"{uuid4().hex}{extension}"


def product_image_upload_to(instance, filename):
    return f"products/{safe_image_filename(filename)}"


def category_image_upload_to(instance, filename):
    return f"categories/{safe_image_filename(filename)}"


def hero_slide_image_upload_to(instance, filename):
    return f"hero-slides/{safe_image_filename(filename)}"


def vendor_logo_upload_to(instance, filename):
    return f"vendors/logos/{safe_image_filename(filename)}"