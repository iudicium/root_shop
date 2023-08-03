from rest_framework import serializers
from .models import Product, ProductImage, ProductReview, ProductSpecification
from datetime import datetime
from collections import OrderedDict
from typing import Dict


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["src", "alt"]


class ProductReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = ProductReview
        fields = ["author", "email", "text", "rate", "date"]

    def create(self, validated_data: Dict) -> ProductReview:
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            # Set the authenticated user as the author of the review
            validated_data["author"] = request.user
        return super().create(validated_data)
        # return super().create(validated_data)

    def to_representation(self, instance: ProductReview) -> OrderedDict:
        representation = super().to_representation(instance)
        # Parse the date string from the instance into a datetime object
        dt = datetime.strptime(representation["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
        # Format the date in the desired format ("%a %b %d %Y %H:%M:%S GMT%z")
        formatted_date = dt.strftime("%a %b %d %Y %H:%M:%S GMT%z")
        representation["date"] = formatted_date
        return representation


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ["name", "value"]


class ProductSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(
        format="%a %b %d %Y %H:%M:%S GMT%z (%Z)", input_formats=None
    )
    images = ProductImageSerializer(many=True)
    reviews = ProductReviewSerializer(many=True)
    specifications = ProductSpecificationSerializer(many=True)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        ]

    def get_tags(self, product):
        return list(product.tags.all().values("id", "name"))
