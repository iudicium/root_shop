from django.contrib.auth import get_user_model
from django.db import models
from app_catalog.models import Product, Category

User = get_user_model()


# Create your models here.
class BasketItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User's cart")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Product ID"
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Price")
    quantity = models.PositiveIntegerField(verbose_name="Quantity")

    class Meta:
        verbose_name = "Basket Item"
        verbose_name_plural = "Basket Items"

    def __str__(self):
        return f"{self.user}:{self.product}"
