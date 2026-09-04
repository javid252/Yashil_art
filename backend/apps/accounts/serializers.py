from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    group_names = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "phone_number", "is_staff", "is_superuser", "is_active",
            "is_student", "is_instructor",
            "groups", "group_names",
            "permissions", "date_joined",
        ]
        # نقش‌ها و دسترسی‌ها فقط از سمت پنل مدیریت (superuser) قابل تغییرند؛
        # خود کاربر نمی‌تواند برای خودش نقش/دسترسی بسازد یا حسابش را غیرفعال کند.
        read_only_fields = [
            "id", "is_staff", "is_superuser", "is_active",
            "is_student", "is_instructor",
            "groups", "group_names", "permissions", "date_joined",
        ]

    def get_group_names(self, obj):
        return list(obj.groups.values_list("name", flat=True))

    def get_permissions(self, obj):
        if obj.is_superuser:
            from django.contrib.auth.models import Permission

            from apps.access.serializers import MANAGEABLE_APPS

            perms = Permission.objects.filter(content_type__app_label__in=MANAGEABLE_APPS).select_related("content_type")
            return [f"{p.content_type.app_label}.{p.codename}" for p in perms]
        return sorted(obj.get_all_permissions())


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username", "email", "first_name", "last_name",
            "phone_number", "password", "password_confirm",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError({"password_confirm": "رمزهای عبور یکسان نیستند."})
        if User.objects.filter(email__iexact=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "این ایمیل قبلاً ثبت شده است."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Login با ایمیل یا نام کاربری + بازگرداندن اطلاعات کاربر همراه با توکن."""

    username_field = "username"

    def validate(self, attrs):
        login_value = attrs.get(self.username_field, "")
        if "@" in login_value:
            user = User.objects.filter(email__iexact=login_value).first()
            if user:
                attrs[self.username_field] = user.username
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
