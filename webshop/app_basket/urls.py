from django.urls import path
from .views import CartViewSet

urlpatterns = [
    path(
        "basket",
        CartViewSet.as_view({"get": "list", "post": "create", "delete": "destroy"}),
        name="basket",
    ),
]
