from logging import getLogger
from .models import Order, OrderProduct
from app_basket.cart import Cart
from app_users.models import Profile
from rest_framework.request import Request
from django.conf import settings

logger = getLogger(__name__)


def bulk_create_orders(cart: Cart, existing_order: Order) -> Order:
    order_items = list()
    logger.warning(existing_order)
    for product in cart:
        order_items.append(
            OrderProduct(
                order=existing_order,
                product=product.get("product"),
                price=product.get("price"),
                quantity=product.get("quantity"),
            )
        )
    OrderProduct.objects.bulk_create(order_items)
    return existing_order


def create_or_return_order(user_profile: Profile, cart: Cart) -> Order:
    try:
        total_price = cart.get_total_price()

        logger.debug(
            f"Creating or returning order for user: {user_profile.user.username}"
        )
        logger.debug(f"User Profile ID: {user_profile.id}")
        logger.debug(f"Cart Contents: {cart}")
        # Check if an order with the same products and quantities exists for the user
        existing_order = Order.objects.filter(
            user_profile=user_profile,
            order_products__product__id__in=[
                product.get("product").id for product in cart
            ],
            order_products__quantity__in=[product.get("quantity") for product in cart],
        ).first()

        logger.info(existing_order)
        if existing_order:
            # If an order with the same products and quantities exists, return
            logger.info("Order already exists. Returning same order.")
            return existing_order

        logger.info("Creating a new order.")
        order = Order.objects.create(
            user_profile=user_profile, totalCost=total_price, status="accepted"
        )
        bulk_create_orders(cart=cart, existing_order=order)
        return order
    except Exception as e:
        logger.exception(e)


def update_order(request: Request, order: Order) -> Order:
    data = request.data
    totalCost = data.get("totalCost")
    deliveryType = data.get("deliveryType")
    # if totalCost < settings.FREE_DELIVERY_EDGE and deliveryType == 'normal':
    #     totalCost += 2
    #
    # if deliveryType == 'express':
    #     totalCost += settings.EXPRESS_COST

    order.fullName = data.get("fullName")
    order.email = data.get("email")
    order.phone = data.get("phone")
    order.deliveryType = deliveryType
    order.paymentType = data.get("paymentType")
    order.totalCost = float(totalCost)
    order.status = data.get("status")
    order.city = data.get("city")
    order.address = data.get("address")
    order.save()
