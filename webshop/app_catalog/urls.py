from django.urls import path
from .views import (
    CategoryReadOnlyViewSet,
    TagReadOnlyViewSet,
    ProductReviewViewSet,
    ProductItemViewSet,
    CatalogViewSet,
    PopularProductViewSet,
    LimitedProductsViewSet,
    BannerProductsViewSet,
    SalesProductsViewSet,
)


urlpatterns = [
    path(
        "categories",
        CategoryReadOnlyViewSet.as_view({"get": "list"}),
        name="categories",
    ),
    path("tags", TagReadOnlyViewSet.as_view({"get": "list"}), name="tags"),
    path("catalog", CatalogViewSet.as_view({"get": "list"}), name="catalog"),
    path(
        "catalog/<int:pk>",
        CatalogViewSet.as_view({"get": "retrieve"}),
        name="get_catalog_pk",
    ),
    path(
        "product/<int:pk>",
        ProductItemViewSet.as_view({"get": "retrieve"}),
        name="product-detail",
    ),
    path(
        "product/<int:pk>/reviews",
        ProductReviewViewSet.as_view({"post": "create"}),
        name="create-review",
    ),
    path(
        "products/popular",
        PopularProductViewSet.as_view({"get": "list"}),
        name="popular-products",
    ),
    path(
        "products/limited",
        LimitedProductsViewSet.as_view({"get": "list"}),
        name="limited-products",
    ),
    path(
        "banners",
        BannerProductsViewSet.as_view({"get": "list"}),
        name="banner-products",
    ),
    path("sales", SalesProductsViewSet.as_view({"get": "list"}), name="sales-products"),
]
