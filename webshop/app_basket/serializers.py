from typing import List, Dict
from rest_framework import serializers
from .models import BasketItem
from app_catalog.models import Product


class BasketSerializer(serializers.ModelSerializer):
    """
    Serializer for the BasketItem model.
    """

    id = serializers.IntegerField(source="product.id")
    date = serializers.DateTimeField(
        source="product.date", format="%a %b %d %Y %H:%M:%S GMT%z (%Z)"
    )
    reviews = serializers.IntegerField(source="product.reviews_count")
    rating = serializers.DecimalField(
        source="product.average_rating", max_digits=3, decimal_places=1
    )
    title = serializers.CharField(source="product.title")
    description = serializers.CharField(source="product.description")
    fullDescription = serializers.CharField(source="product.fullDescription")
    freeDelivery = serializers.BooleanField(source="product.freeDelivery")
    count = serializers.IntegerField(source="quantity")
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = BasketItem
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
            "rating",
        ]

    def get_images(self, basket_item: BasketItem) -> List[Dict[str, str]]:
        """
        Get a list of dictionaries containing 'src' and 'alt' for each image in the product.

        :param basket_item: The BasketItem instance.
        :type basket_item: BasketItem

        :return: A list of dictionaries containing 'src' and 'alt' for each image.
        :rtype: List[Dict[str, str]]
        """
        return [
            {"src": image.src.url, "alt": image.alt}
            for image in basket_item.product.images.all()
        ]

    def get_tags(self, basket_item: BasketItem) -> List[Dict[str, str]]:
        """
        Get a list of dictionaries containing 'id' and 'name' for each tag in the product.

        :param basket_item: The BasketItem instance.
        :type basket_item: BasketItem

        :return: A list of dictionaries containing 'id' and 'name' for each tag.
        :rtype: List[Dict[str, str]]
        """
        return list(basket_item.product.tags.all().values("id", "name"))

    def get_category(self, basket_item: BasketItem) -> int:
        """
        Get the ID of the category to which the product belongs.

        :param basket_item: The BasketItem instance.
        :type basket_item: BasketItem

        :return: The ID of the category.
        :rtype: int
        """
        return basket_item.product.category.id
