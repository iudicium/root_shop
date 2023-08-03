from django.contrib import admin
from .models import (
    Category,
    Subcategory,
    Product,
    ProductImage,
    ProductReview,
    ProductSpecification,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "src", "alt"]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "src", "alt"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "price", "count")
    list_filter = ("category",)
    search_fields = ("title", "description")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "src", "alt")
    list_filter = ("product",)


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "author", "rate", "date")
    list_filter = ("product", "author")
    search_fields = ("author", "text")


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ("product", "name", "value")
    list_filter = ("product",)
