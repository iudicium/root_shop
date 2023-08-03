from rest_framework.request import Request
from typing import Dict
from .cart import Cart


def cart(request: Request) -> Dict[str, Cart]:
    """
    Context processor to add the cart to the context.

    :param request: The current DRF request.
    :type request: rest_framework.request.Request

    :return: A dictionary containing the cart instance.
    :rtype: dict
    """
    cart_instance = Cart(request)
    return {"cart": cart_instance}
