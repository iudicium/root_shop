from logging import getLogger
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Sum, F
from .models import BasketItem
from rest_framework.request import Request
from app_catalog.models import Product
from typing import Tuple, Dict, Union
from .serializers import BasketSerializer
from django.db.transaction import atomic

logger = getLogger(__name__)


class Cart(object):
    """
    Represents a shopping cart for a user.

    Attributes:
        db (bool): Indicates if the cart is being saved to the database (True) or using session data (False).
        cart (dict): Dictionary representing the cart items with product IDs as keys and their details as values.
        session (django.contrib.sessions.backends.base.SessionBase): The session object to store cart data.
        request (rest_framework.request.Request): The HTTP request object representing the current request.
        user (django.contrib.auth.models.User): The authenticated user associated with the cart.
        queryset (django.db.models.query.QuerySet): The queryset representing the cart items in the database.

    Methods:
        __init__(request: Request): Initializes the Cart instance based on the given request.
        save_to_db(cart: Dict, user: User): Saves the cart data to the database for the authenticated user.
        get_cart_from_db(queryset: django.db.models.query.QuerySet) -> dict: Retrieves cart data from the database
            and returns a dictionary with product IDs as keys and their details as values.
        __iter__(): Iterates through the cart items and yields each item with additional details like product_id,
            price, and total_price.
        get_cart_items() -> List[dict]: Retrieves a list of cart items with serialized product information.
        add(product_id: int, count: int = 1) -> Tuple[bool, str]: Adds a product to the cart or updates its quantity
            if it already exists. Returns a tuple representing the success status and a message string.
        delete(product_id: int, count: int = 1) -> bool: Removes a product from the cart or decreases its quantity
            if it exists. Returns True if the product was removed or updated successfully, False otherwise.
        clear(): Clears the cart by removing all cart items from the session.
        save(): Saves the current cart data to the session.

    Note: Please provide specific implementation for methods marked with "IMPLEMENTATION NEEDED".
    """

    def __init__(self, request: Request) -> None:
        """
        Initialize the Cart instance based on the given request.

        If the user is authenticated, the cart data will be retrieved from the database.
        Otherwise, it will be retrieved from the session.

        :param request: The HTTP request object representing the current request.
        :type request: rest_framework.request.Request
        """
        self.session = request.session
        self.request = request
        self.user = request.user
        self.db = False
        self.cart = None
        self.queryset = None
        cart = self.session.get(settings.CART_SESSION_ID)
        if self.user.is_authenticated:
            self.db = True
            if cart:
                self.save_to_db(cart=cart, user=self.user)
                self.clear(True)
            self.queryset = BasketItem.objects.filter(user=self.user)
            cart = self.get_cart_from_db(self.queryset)
        else:
            if not cart:
                cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save_to_db(self, cart: Dict, user: User) -> None:
        """
        Save the cart data to the database for the authenticated user.

        This method will create or update cart items in the database based on the cart data.

        :param cart: The cart data with product IDs as keys and their details as values.
        :type cart: dict

        :param user: The authenticated user associated with the cart.
        :type user: django.contrib.auth.models.User
        """
        with atomic():
            for key, value in cart.items():
                if BasketItem.objects.filter(user=user, product=key).exists():
                    product = BasketItem.objects.select_for_update().get(
                        user=user, product=key
                    )
                    product.quantity += cart[key]["quantity"]
                    product.price = cart[key]["price"]
                    product.save()
                else:
                    product = Product.objects.get(id=key)
                    BasketItem.objects.create(
                        user=user,
                        product=product,
                        quantity=value["quantity"],
                        price=value["price"],
                    )

    def get_cart_from_db(self, queryset) -> Dict:
        cart = dict()
        for basket_item in queryset:
            cart[str(basket_item.id)] = {
                "product": basket_item.product,
                "quantity": basket_item.quantity,
                "price": basket_item.price,
            }
        return cart

    def get_cart_items(self):
        """
        Get the cart items as a list of serialized data.

        :return: A list of serialized cart items.
        :rtype: list
        """
        cart_items = list()
        if self.db:
            serializer = BasketSerializer(self.queryset, many=True)
            return serializer.data

        else:
            for product_id, item_data in self.cart.items():
                try:
                    product = Product.objects.get(id=int(product_id))
                    serializer = BasketSerializer(
                        BasketItem(
                            product=product,
                            quantity=item_data["quantity"],
                            price=float(product.price),
                        )
                    )
                    cart_items.append(serializer.data)
                except Product.DoesNotExist:
                    logger.warning("Id doesnt exist.")

        return cart_items

    def get_total_price(self) -> Union[float, int]:
        """
        Calculate the total price of items in the cart.

        If `self.db` is True, the calculation is performed using database aggregation.
        Otherwise, the calculation is done on in-memory data.

        :return: The total price as a Float if calculated using database,
            or as an int if calculated using in-memory data. Returns 0 if no items in cart.
        :rtype: Union[Float, int]
        """
        if self.db:
            total = self.queryset.only("quantity", "price").aggregate(
                total=Sum(F("quantity") * F("price"))
            )["total"]
            if total is None:
                total = float(0.00)
            return total
        else:
            cart_values = self.cart.values()
            total = sum(float(item["price"]) * item["quantity"] for item in cart_values)
            return total

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        if self.db:
            for item in self.cart.values():
                item["total_price"] = item["price"] * item["quantity"]
                yield item
        else:
            product_ids = self.cart.keys()
            # get the product objects and add them to the cart
            products = Product.objects.filter(id__in=product_ids)
            for product in products:
                self.cart[str(product.id)]["product"] = product

            for item in self.cart.values():
                item["price"] = float(item["price"])
                item["total_price"] = item["price"] * item["quantity"]
                yield item

    def __len__(self) -> int:
        return sum(item["quantity"] for item in self.cart.values())

    def add(
        self, product_id: int, quantity: int = 1, override_quantity: bool = False
    ) -> Tuple[bool, str]:
        """
        Add a product to the cart or update its quantity if it already exists.

        :param product_id: The ID of the product to be added to the cart.
        :type product_id: int

        :param quantity: The quantity of the product to be added to the cart. Default is 1.
        :type quantity: int

        :param override_quantity: A boolean flag to indicate whether to override the existing quantity with the
                                  given quantity. If set to True, the cart will be updated with the given quantity;
                                  otherwise, the given quantity will be added to the existing quantity. Default is False.
        :type override_quantity: bool

        :return: A tuple representing the success status and a message string.
                 The success status is True if the product was added or updated successfully, False otherwise.
        :rtype: Tuple[bool, str]
        """
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return False, f"Product with ID {product_id} does not exist."

        if self.db:
            if self.queryset.filter(product=product).exists():
                cart = self.queryset.get(product=product)

            else:
                cart = BasketItem(
                    user=self.user,
                    product=product,
                    quantity=0,
                    price=product.price,
                )

            if override_quantity:
                cart.quantity = quantity
            else:
                cart.quantity += quantity
            cart.save()
        else:
            # If the cart is using the session, update the product quantity or add a new item to the cart
            product_id = str(product.id)
            if product_id not in self.cart:
                self.cart[product_id] = {"quantity": 0, "price": float(product.price)}

            if override_quantity:
                self.cart[product_id]["quantity"] = quantity
            else:
                self.cart[product_id]["quantity"] += quantity

            self.save()
        return True, f"Added {quantity} units of '{product.title}' to the cart."

    def delete(self, product_id: int, count: int = 1) -> bool:
        """
        Remove a product from the cart or decrease its quantity if it exists.

        :param product_id: The ID of the product to be removed from the cart.
        :type product_id: int

        :param count: The quantity of the product to be removed from the cart. Default is 1.
        :type count: int

        :return: True if the product was removed or updated successfully, False otherwise.
        :rtype: bool
        """
        logger.warning(
            f"Delete method called for product ID: {product_id}, count: {count}"
        )

        if self.db:
            try:
                cart_item_qs = self.queryset.filter(product_id=product_id)
                if cart_item_qs.exists():
                    cart_item = cart_item_qs.first()
                    if count >= cart_item.quantity:
                        # If count is greater than or equal to the quantity, delete the cart item
                        cart_item.delete()
                    else:
                        cart_item.quantity -= count
                        cart_item.save()
                    logger.info(f"Updated product quantity: {cart_item.quantity}")
                    logger.info(f"Updated in instance: {cart_item}")
                    return True
                return False
            except BasketItem.DoesNotExist:
                return False
        else:
            product_id = str(product_id)
            if product_id in self.cart:
                if count >= self.cart[product_id]["quantity"]:
                    del self.cart[product_id]
                else:
                    self.cart[product_id]["quantity"] -= count
                self.save()
                return True
        return False

    def clear(self, only_session=False):
        """
        remove cart from session or from db if user authorized
        :return:
        """
        if only_session:
            del self.session[settings.CART_SESSION_ID]
            self.session.modified = True
        else:
            if self.queryset:
                self.queryset.delete()

    def save(self):
        """
        Save the current cart data to the session.
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
