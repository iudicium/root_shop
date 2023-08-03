from rest_framework import serializers
from taggit.models import Tag
from taggit.serializers import TaggitSerializer
from .models import Subcategory, Category
from typing import Dict, Any


class SubcategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Subcategory
        fields = ("id", "title", "image")

    def get_image(self, subcategory) -> Dict[str, Any]:
        return {"src": subcategory.src.url, "alt": subcategory.alt}


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ("id", "title", "image", "subcategories")

    def get_image(self, category) -> Dict[str, Any]:
        return {"src": category.src.url, "alt": category.alt}


class CatalogItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    free_delivery = serializers.BooleanField()
    available = serializers.BooleanField()


class TagSerializer(TaggitSerializer):
    id = serializers.CharField(source="name", read_only=True)
    name = serializers.CharField(source="slug", read_only=True)

    class Meta:
        model = Tag
        fields = ["id", "name"]
