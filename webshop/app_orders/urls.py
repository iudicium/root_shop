from django.urls import path

from .views import OrderViewSet, PaymentView


app_name = "app_orders"


urlpatterns = [
    path(
        "orders", OrderViewSet.as_view({"get": "list", "post": "create"}), name="orders"
    ),
    path(
        "order/<int:pk>",
        OrderViewSet.as_view({"get": "retrieve", "post": "update"}),
        name="orders",
    ),
    path("payment/<int:pk>", PaymentView.as_view(), name="payment"),
]
