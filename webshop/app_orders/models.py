from django.contrib.auth import get_user_model
from django.db import models
from app_catalog.models import Product
from app_users.models import Profile
from app_basket.cart import Cart


User = get_user_model()
# Create your models here.


def get_user_default():
    # Replace 'default_username' with the username you want to use as the default value.
    # You can change this to the username of an existing user or create a new default user.
    default_username = "admin"
    user, _ = User.objects.get_or_create(username=default_username)
    return user.id


class Order(models.Model):
    DELIVERY_CHOICES = (
        ("normal", "Normal Delivery"),
        ("express", "Express Delivery"),
    )

    PAYMENT_CHOICES = (
        ("card", "Payment with Card"),
        ("different_card", "Payment with Somebody Else's Card"),
    )

    user_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name="User"
    )
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    fullName = models.CharField(max_length=255, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    deliveryType = models.CharField(
        max_length=50,
        verbose_name="Delivery Type",
        choices=DELIVERY_CHOICES,
        default="normal",
    )
    delivery_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Delivery Cost", default=0
    )
    paymentType = models.CharField(
        max_length=50,
        verbose_name="Payment Type",
        choices=PAYMENT_CHOICES,
        default="card",
    )
    totalCost = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Total Cost"
    )
    status = models.CharField(
        max_length=50, verbose_name="Status", blank=True, null=True
    )
    city = models.CharField(max_length=100, verbose_name="City")
    address = models.CharField(max_length=255, verbose_name="Address")

    class Meta:
        ordering = ("-createdAt",)
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all()) + self.delivery_price


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_products", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Price", default=0
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Quantity",
    )

    class Meta:
        verbose_name = "Order Product"
        verbose_name_plural = "Order Products"

    def __str__(self) -> str:
        return f"{self.product.title} (Order {self.order.id})"

    def get_total_cost(self):
        return self.price * self.quantity


class Payment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="User", default=get_user_default
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    number = models.CharField(max_length=16, verbose_name="Payment Number")
    name = models.CharField(max_length=255, verbose_name="Cardholder Name")
    month = models.CharField(max_length=2, verbose_name="Expiration Month")
    year = models.CharField(max_length=4, verbose_name="Expiration Year")
    code = models.CharField(max_length=8, verbose_name="Security Code")

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Payment for Order: {self.order.id}"
