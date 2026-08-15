from rest_framework import serializers

from .models import HeroSlide


class HeroSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSlide
        fields = [
            "id", "image", "label", "title", "description",
            "primary_button_text", "primary_button_link",
            "secondary_button_text", "secondary_button_link",
            "order", "is_active",
        ]