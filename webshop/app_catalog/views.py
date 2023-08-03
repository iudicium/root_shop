from logging import getLogger
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet, ModelViewSet
from .serializers import TagSerializer
from .models import Category, Subcategory, Product
from taggit.models import Tag
from .serializers import CategorySerializer
from .product_serializers import ProductSerializer, ProductReviewSerializer
from .paginations import CatalogItemPagination
from django.db.models import Prefetch, Count
from django.db.models.query import QuerySet
from rest_framework.serializers import ListSerializer
from rest_framework.utils.serializer_helpers import ReturnDict
from typing import Union

logger = getLogger(__name__)


class CategoryReadOnlyViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    # Filtering only active categories and prefetching related subcategories
    queryset = Category.objects.filter(IsActive=True).prefetch_related(
        Prefetch("subcategories", queryset=Subcategory.objects.filter(IsActive=True))
    )
    serializer_class = CategorySerializer

    def list(
        self, request: Request, *args, **kwargs
    ) -> Union[Response, Response(status)]:
        try:
            response = super().list(request, *args, **kwargs)
            logger.info("Category list retrieved successfully.")
            return response
        except Exception as e:
            logger.error(f"Error occurred while retrieving category list: {e}")
            return Response(
                {"detail": "An error occurred while retrieving the category list."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TagReadOnlyViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Tag.objects.order_by("name")
    serializer_class = TagSerializer

    def list(
        self, request: Request, *args, **kwargs
    ) -> Union[Response, Response(status)]:
        try:
            response = super().list(request, *args, **kwargs)
            logger.info("Tag list retrieved successfully.")
            return response
        except Exception as e:
            logger.error(f"Error occurred while retrieving tag list: {e}")
            return Response(
                {"detail": "An error occurred while retrieving the tag list."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProductItemViewSet(ViewSet):
    permission_classes = (AllowAny,)

    def retrieve(
        self, request: Request, pk=None
    ) -> Union[Response(ProductSerializer.data), Response(status)]:
        try:
            product = (
                Product.objects.select_related("category")
                .prefetch_related("images", "reviews", "specifications")
                .get(pk=pk)
            )
            serializer = ProductSerializer(product)
            logger.info(f" Successfully accessed product with pk={pk}")
            return Response(serializer.data)
        except Product.DoesNotExist:
            logger.warning(f"Attempted to access non-existent product with pk={pk}")
            return Response({"detail": "Product not found"}, status=404)


class ProductReviewViewSet(ViewSet):
    def create(
        self, request: Request, pk=None
    ) -> Union[Response(ListSerializer), Response(ReturnDict), Response(status)]:
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductReviewSerializer(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                review = serializer.save(product=product)
                logger.info("Product review created successfully.")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.warning("Invalid data for product review.")
                print(type(serializer.errors))
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            logger.warning("Product not found.")
            return Response(
                {"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )


class CatalogViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    pagination_class = CatalogItemPagination
    queryset = Product.objects.select_related().order_by("date")
    ordering_fields = ["rating", "price", "reviews", "date"]

    def list(
        self, request: Request, *args, **kwargs
    ) -> Union[Response(ListSerializer), Response(status)]:
        try:
            response = super().list(request, *args, **kwargs)
            logger.info("Product list retrieved successfully.")
            return response
        except Exception as e:
            logger.error(f"Error occurred while retrieving product list: {e}")
            return Response(
                {"detail": "An error occurred while retrieving the product list."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        queryset = queryset.annotate(num_reviews=Count("reviews"))
        if self.request.query_params:
            name = self.request.query_params.get("filter[name]")
            if name:
                queryset = queryset.filter(description__icontains=name)

            min_price = self.request.query_params.get("filter[minPrice]")
            if min_price:
                queryset = queryset.filter(price__gte=min_price)

            max_price = self.request.query_params.get("filter[maxPrice]")
            if max_price:
                queryset = queryset.filter(price__lte=max_price)

            delivery = self.request.query_params.get("filter[freeDeivery]")
            if delivery:
                queryset = queryset.filter(freeDelivery=delivery)

            sort = self.request.query_params.get("sort")
            sort_type_param = self.request.query_params.get("sortType")

            if sort in self.ordering_fields:
                sort_field = sort
            else:
                sort_field = "date"

            if sort_type_param.lower() == "dec":
                logger.info("Sorting in descending order.")
                sort_field = f"-{sort_field}"

            if sort == "reviews":  # Sort by number of reviews
                sort_field = (
                    f"-num_reviews"
                    if sort_type_param.lower() == "dec"
                    else "num_reviews"
                )

            queryset = queryset.order_by(sort_field)
            return queryset


class PopularProductViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(rating__gte=4.0).order_by("-rating")[:10]

    def list(self, reques: Request, *args, **kwargs) -> Response(ListSerializer):
        logger.info("Accessing popular items view set.")
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        print(type(serializer))
        return Response(serializer.data)


class LimitedProductsViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(limited=True)

    def list(self, request: Request, *args, **kwargs) -> Response(ListSerializer):
        logger.info("Accessing limited items view set.")
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BannerProductsViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Product.objects.filter(banner=True)[:5]
    serializer_class = ProductSerializer


class SalesProductsViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Product.objects.filter(sale=True)
    serializer_class = ProductSerializer
    pagination_class = CatalogItemPagination
