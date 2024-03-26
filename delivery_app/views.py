from decimal import Decimal
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Order, OrderItem
from .serializers import OrderSerializer
from .utils import get_dish_details
from .permissions import IsCourier


class OrderView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-updated_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        if Order.objects.filter(user=request.user, status__in=['active', 'in_progress', 'on_delivery']).exists():
            return Response({"error": "You already have an active order"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            address = request.data.get('delivery_address') or user.profile.address
            payment_method = request.data.get('payment_method')

            order = Order.objects.create(user=user, status='active', delivery_address=address,
                                         payment_method=payment_method)

            total_price = Decimal('2')

            dishes = request.data.get('dishes', [])
            for dish in dishes:
                dish_id = dish['dish_id']
                quantity = dish['quantity']

                dish_price = Decimal(get_dish_details(dish_id)[1])
                total_price += dish_price * quantity
                OrderItem.objects.create(order=order, dish_id=dish_id, quantity=quantity)

            order.total_price = total_price
            order.save()

            response_data = OrderSerializer(order).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(RetrieveAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'order_id'


class ActiveOrdersView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsCourier)

    def get(self, request):
        active_orders = Order.objects.filter(status='active')
        serializer = OrderSerializer(active_orders, many=True)
        return Response(serializer.data)


class AcceptOrderView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsCourier)

    def put(self, request, order_id):
        if Order.objects.filter(courier=request.user.courier).exclude(status='delivered').exclude(
                status='cancelled').exists():
            return Response({"error": "You already have an active order"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(pk=order_id, status='active')
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        order.courier = request.user.courier
        order.status = 'in_progress'
        order.save(update_fields=['courier', 'status'])

        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id, courier=request.user.courier)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')

        if order.status in ['delivered', 'cancelled']:
            return Response({"error": "Cannot update status of this order"}, status=status.HTTP_400_BAD_REQUEST)

        if new_status in ['on_delivery', 'delivered', 'cancelled']:
            order.status = new_status
            order.save(update_fields=['status'])
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            return Response({"error": "Invalid status update"}, status=status.HTTP_400_BAD_REQUEST)
