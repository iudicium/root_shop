from django.contrib import admin
from .models import BasketItem

# Register your models here.


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "quantity",
        "price",
    )
    list_filter = ("user", "price")
    search_fields = ("user__username", "product__name")
    list_per_page = 20
