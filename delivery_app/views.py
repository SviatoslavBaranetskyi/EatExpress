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


class OrderView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        orders = Order.objects.filter(user=request.user)  # Фільтрація кошиків за поточним користувачем
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            address = user.profile.address

            new_address = request.data.get('delivery_address')
            if new_address:
                # Оновлення адреси у кошику
                address = new_address

            # Перевірити, чи існує активна корзина для поточного користувача
            active_order = Order.objects.filter(user=user, status='active').first()

            if active_order:
                # Якщо корзина існує, використовуємо її
                order = active_order
            else:
                # Якщо корзина не існує, створюємо нову корзину зі статусом "active"
                order = Order.objects.create(user=user, status='active', delivery_address=address)

            payment_method = request.data.get('payment_method')
            order.payment_method = payment_method

            # Отримати всі предмети у поточній корзині
            existing_items = OrderItem.objects.filter(order=order)
            total_price = Decimal('0')

            # Додати до корзини нові предмети та оновити загальну суму
            dishes = request.data.get('items', [])
            for dish in dishes:
                dish_id = dish['dish_id']
                quantity = dish['quantity']

                # Перевірити, чи блюдо вже є у кошику
                existing_item = existing_items.filter(dish_id=dish_id).first()
                if existing_item:
                    # Якщо блюдо вже є, збільшити його кількість
                    existing_item.quantity += quantity
                    # Оновити вартість існуючого предмета
                    existing_item.save()
                else:
                    # Якщо блюдо ще не додано, створити новий предмет
                    dish_price = Decimal(get_dish_details(dish_id)[1])
                    total_price += dish_price * quantity
                    OrderItem.objects.create(order=order, dish_id=dish_id, quantity=quantity)

            # Оновити загальну суму в кошику
            order.total_price = Decimal('2')  # Обнулити загальну суму
            for item in OrderItem.objects.filter(order=order):
                dish_price = Decimal(get_dish_details(item.dish_id)[1])
                order.total_price += dish_price * item.quantity
            order.save()

            # Повернути відповідь
            response_data = OrderSerializer(order).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(RetrieveAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'
