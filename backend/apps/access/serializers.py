from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from .roles import MANAGEABLE_APPS, is_system_role, role_category, role_description


class PermissionSerializer(serializers.ModelSerializer):
    app_label = serializers.CharField(source="content_type.app_label", read_only=True)
    model = serializers.CharField(source="content_type.model", read_only=True)
    full_codename = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = ["id", "name", "codename", "app_label", "model", "full_codename"]

    def get_full_codename(self, obj):
        return f"{obj.content_type.app_label}.{obj.codename}"


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(
        source="permissions", queryset=Permission.objects.all(), many=True, write_only=True, required=False,
    )
    user_count = serializers.IntegerField(source="user_set.count", read_only=True)
    # دسته نقش: academy = آموزشگاه | shop = فروشگاه/بک‌آفیس | independent = مستقل (مدیرکل)
    category = serializers.SerializerMethodField()
    is_system = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            "id", "name", "permissions", "permission_ids", "user_count",
            "category", "is_system", "description",
        ]

    def get_category(self, obj):
        return role_category(obj.name)

    def get_is_system(self, obj):
        return is_system_role(obj.name)

    def get_description(self, obj):
        return role_description(obj.name)