from typing import List, Dict
from rest_framework import serializers
from app_catalog.product_serializers import ProductSerializer
from app_users.models import Profile
from app_catalog.models import Product
from .models import OrderProduct, Order, Payment


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = []


class OrderSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(format="%Y-%m-%d %H:%M", input_formats=None)
    fullName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.CharField(source="user_profile.phone")
    totalCost = serializers.FloatField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        ]

    def get_fullName(self, order: Order):
        return order.user_profile.fullName

    def get_email(self, order: Order):
        return order.user_profile.email

    def get_products(self, order: Order) -> List[Dict]:
        products_in_order = list()
        order_products = OrderProduct.objects.select_related("product").filter(
            order=order.id
        )
        for order_product in order_products:
            product = order_product.product
            product.count = order_product.quantity
            product.price = order_product.price
            products_in_order.append(product)
        return ProductSerializer(products_in_order, many=True).data


class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = ("number", "name", "month", "year", "code", "order")

    def validate_number(self, value):
        """
        Custom validation for the 'code' field.
        The code must be even and not end in 0.
        """
        if int(value) % 2 != 0:
            raise serializers.ValidationError(
                "The 'card_number' must be an even number."
            )

        if value.endswith("0"):
            raise serializers.ValidationError("The 'card_number' must not end in 0.")

        return value

    def validate_month(self, value):
        """
        Custom validation for the 'month' field.
        The 'month' must be a number between 1 and 12 (inclusive).
        """
        try:
            month_number = int(value)
            if not 1 <= month_number <= 12:
                raise serializers.ValidationError(
                    "The 'month' must be a number between 1 and 12."
                )
        except ValueError:
            raise serializers.ValidationError("The 'month' must be a valid number.")

        return value

    def validate_year(self, value):
        """
        Custom validation for the 'year' field.
        The 'year' must be a number between 2000 and 2099 (inclusive).
        """
        try:
            year_number = int(value)
            if not 2000 <= year_number <= 2099:
                raise serializers.ValidationError(
                    "The 'year' must be a number between 2000 and 2099."
                )
        except ValueError:
            raise serializers.ValidationError("The 'year' must be a valid number.")

        return value

    def get_order(self, payment) -> Order:
        order_pk = payment.get("order")
        if order_pk is not None:
            try:
                return Order.objects.get(pk=order_pk)
            except Order.DoesNotExist:
                pass
