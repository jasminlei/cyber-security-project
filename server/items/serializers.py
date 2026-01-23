from rest_framework import serializers
from .models import Item, Like


class ItemSerializer(serializers.ModelSerializer):
    seller_username = serializers.CharField(source="seller.username", read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            "id",
            "seller",
            "seller_username",
            "title",
            "description",
            "price",
            "contact",
            "image_url",
            "created_at",
            "updated_at",
            "likes_count",
            "is_liked",
        ]
        read_only_fields = ["id", "seller", "created_at", "updated_at"]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "item", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
