from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from logging import getLogger
from .cart import Cart
from app_catalog.models import Product

# Create a logger
logger = getLogger(__name__)


class CartViewSet(ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request: Request) -> Response:
        logger.info("Listing carts for the authenticated user.")
        logger.warning(request.session.get("cart"))
        cart = Cart(request)
        cart_items = cart.get_cart_items()
        return Response(cart_items, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        # Assuming you have the necessary data from the request data
        product_id = request.data.get("id")
        count = int(request.data.get("count", 1))
        # Instantiate the Cart class with the request object

        cart = Cart(request)

        success, message = cart.add(product_id, count)
        logger.info(cart.cart)
        if success:
            cart_items = cart.get_cart_items()
            # Log successful cart creation
            logger.info(f"Cart created successfully: {message}")

            return Response(
                cart_items, status=status.HTTP_201_CREATED, headers={"message": message}
            )
        else:
            # Log cart creation failure
            logger.error(f"Failed to create cart: {message}")
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request) -> Response:
        # Get the product_id and count from request.data

        # Get the product_id and count from request.data
        product_id = request.data.get("id")
        count = int(request.data.get("count", 1))
        logger.warning(count)
        cart = Cart(request)
        success = cart.delete(product_id, count)
        logger.info(f"Deletion status: {success}")
        if success:
            cart_items = cart.get_cart_items()
            # Get the updated cart items after the deletion
            logger.debug(f"Updated cart items: {cart_items}")
            return Response(cart_items, status=status.HTTP_200_OK)
        else:
            logger.warning("Product not found in cart.")
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                headers={"message": "Product was not found in the cart"},
            )
