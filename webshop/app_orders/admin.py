from django.contrib import admin
from .models import Order, OrderProduct, Payment

# Register your models here.


class OrderProductAdmin(admin.TabularInline):
    model = OrderProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user_profile", "created_at_formatted", "totalCost", "status"]
    list_filter = ["status", "deliveryType", "paymentType"]
    search_fields = ["user_profile__user__username", "fullName", "email"]
    inlines = [OrderProductAdmin]

    def created_at_formatted(self, obj):
        return obj.createdAt.strftime("%d-%b-%Y %H:%M:%S")

    created_at_formatted.short_description = "Created At"


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product", "price", "quantity"]
    list_filter = ["order"]
    search_fields = ["order__id", "product__title"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "number", "name", "month", "year", "code")
    list_filter = ("month", "year")
    search_fields = ("number", "name", "order__order_number")
