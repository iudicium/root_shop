from django.contrib.auth import get_user_model
from django.db import models
from taggit.managers import TaggableManager
from django.db.models import Avg


# Create your models here.
def product_directory(instance, filename) -> str:
    return f"product/{str(instance)}/{filename}"


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    src = models.ImageField(upload_to="category_images/", verbose_name="Image Source")
    alt = models.CharField(max_length=255, verbose_name="Alternative Text")
    IsActive = models.BooleanField(default=False, verbose_name="Is Category Active?")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Subcategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Category",
    )
    title = models.CharField(max_length=255, verbose_name="Title")
    src = models.ImageField(
        upload_to="subcategory_images/", verbose_name="Image Source"
    )
    alt = models.CharField(max_length=255, verbose_name="Alternative Text")
    IsActive = models.BooleanField(default=False, verbose_name="Is SubCategory Active?")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Category"
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Price")
    count = models.IntegerField(verbose_name="Count")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.CharField(max_length=255, verbose_name="Description")
    fullDescription = models.TextField(verbose_name="Full Description")
    freeDelivery = models.BooleanField(verbose_name="Free Delivery")
    rating = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Rating")
    tags = TaggableManager(blank=True)
    limited = models.BooleanField(verbose_name="Limtied Item?", default=False)
    banner = models.BooleanField(verbose_name="Show on Banner?", default=False)
    sale = models.BooleanField(verbose_name="Is item on sale?", default=False)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self) -> str:
        return self.title

    def reviews_count(self) -> int:
        return self.reviews.count()

    def average_rating(self) -> float:
        return self.reviews.aggregate(Avg("rate"))["rate__avg"]


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Product", related_name="images"
    )
    src = models.ImageField(upload_to=product_directory, verbose_name="Source")
    alt = models.CharField(max_length=255, verbose_name="Alt")

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return str(self.src)


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Product",
        related_name="reviews",
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author")
    email = models.EmailField(verbose_name="Email")
    text = models.TextField(verbose_name="Text")
    rate = models.IntegerField(verbose_name="Rate")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"{self.author}"


class ProductSpecification(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Product",
        related_name="specifications",
    )
    name = models.CharField(max_length=255, verbose_name="Name")
    value = models.CharField(max_length=255, verbose_name="Value")

    class Meta:
        verbose_name = "Specification"
        verbose_name_plural = "Specifications"

    def __str__(self):
        return self.name
