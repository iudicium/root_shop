from logging import getLogger
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import OrderSerializer, PaymentSerializer
from .models import Order, Payment
from app_users.models import Profile
from app_basket.cart import Cart
from .order_manager import create_or_return_order, update_order


# Create your views here.

logger = getLogger(__name__)


class OrderViewSet(ViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def get_queryset(self):
        return Order.objects.select_related("user_profile").prefetch_related(
            "order_products"
        )

    def list(self, request: Request) -> Response:
        try:
            user = request.user
            user_profile = Profile.objects.get(user=user)
            orders = self.get_queryset().filter(user_profile=user_profile)
            serializer = self.serializer_class(orders, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(
                f"Error occurred while retrieving orders for user {request.user}: {e}"
            )
            return Response(
                data={"detail": "An error occurred while processing your request."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request: Request) -> Response:
        try:
            user_profile = Profile.objects.get(user=request.user)
            cart = Cart(request)
            order = create_or_return_order(user_profile, cart)
            cart.clear()

            # Log the successful creation of the order
            logger.info(
                f"Order created successfully. Order ID: {order.id}, User Profile: {user_profile}"
            )

            return Response(data={"orderId": order.id}, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            # Handle the case if the user profile does not exist
            logger.error(f"Profile not found for user {request.user}.")
            return Response(
                data={"detail": "User profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            # Log the exception
            logger.exception(f"Error occurred while creating the order: {e}")
            return Response(
                data={"detail": "An error occurred while processing your request."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None) -> Response:
        try:
            order = self.get_queryset().get(id=pk)
            print(order.totalCost)
            if not order:
                return Response(
                    data={"detail": "Order not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Http404:
            return Response(
                data={"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            # Log the exception
            logger.exception(f"Error occurred while retrieving the order: {e}")
            return Response(
                data={"detail": "An error occurred while processing your request."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request: Request, pk=None) -> Response:
        try:
            # Retrieve the order
            order = get_object_or_404(
                Order, id=pk, user_profile=self.request.user.profile
            )
            update_order(request, order)

            return Response({"orderId": order.id}, status=status.HTTP_200_OK)

        except Http404:
            return Response(
                data={"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            # Log the exception
            logger.exception(f"Error occurred while updating the order: {e}")
            return Response(
                data={"detail": "An error occurred while processing your request."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PaymentView(APIView):
    def post(self, request: Request, pk: int = None) -> Response:
        # Check if the request data is valid
        serializer = PaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Process the payment data and perform any required operations
        # In this example, we are just returning a success response

        payment_data = serializer.validated_data
        order_id = pk
        payment = Payment(order_id=order_id, **payment_data, user=request.user)
        payment.save()

        response_data = {
            "message": "Payment successful",
            "order_id": pk,
            "payment_data": serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
