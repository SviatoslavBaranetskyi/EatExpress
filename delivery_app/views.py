from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Courier, Cart, CartItem
from .serializers import CourierSignUpSerializer, CourierSerializer, CartSerializer
from .utils import get_dish_details


class CourierSignUpView(APIView):
    def post(self, request):
        serializer = CourierSignUpSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save()  # Saving a new user and courier profile
            courier_group = Group.objects.get(name='CouriersGroup')
            user.groups.add(courier_group)
            return Response({"message": "Courier registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourierSignInView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            response['Access-Token'] = access_token
            response['Refresh-Token'] = str(refresh)
            return response  # or HttpResponseRedirect('/')
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CourierSignOutView(APIView):
    def post(self, request):
        response = Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class CourierProfileView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, slug):
        profile = get_object_or_404(Courier, user__username=slug)
        if request.user != profile.user:
            return Response({'error': 'You do not have permission to view this profile'},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = CourierSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        profile = get_object_or_404(Courier, user__username=slug)
        if request.user != profile.user:
            return Response({'error': 'You do not have permission to update this profile'},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = CourierSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        profile = get_object_or_404(Courier, user__username=slug)
        # Перевіряємо, чи поточний користувач має доступ до цього профілю
        if request.user != profile.user:
            return Response({'error': 'You do not have permission to delete this profile'},
                            status=status.HTTP_403_FORBIDDEN)
        profile.user.delete()
        return Response({'message': 'Profile deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class CartView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        carts = Cart.objects.filter(user=request.user)  # Фільтрація кошиків за поточним користувачем
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            address = user.profile.address

            # Перевірити, чи існує активна корзина для поточного користувача
            active_cart = Cart.objects.filter(user=user, status='active').first()

            if active_cart:
                # Якщо корзина існує, використовуємо її
                cart = active_cart
            else:
                # Якщо корзина не існує, створюємо нову корзину зі статусом "active"
                cart = Cart.objects.create(user=user, status='active', address=address)

            new_address = request.data.get('address')
            if new_address:
                # Оновлення адреси у кошику
                cart.address = new_address

            # Отримати всі предмети у поточній корзині
            existing_items = CartItem.objects.filter(cart=cart)
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
                    CartItem.objects.create(cart=cart, dish_id=dish_id, quantity=quantity)

            # Оновити загальну суму в кошику
            cart.total_price = Decimal('2')  # Обнулити загальну суму
            for item in CartItem.objects.filter(cart=cart):
                dish_price = Decimal(get_dish_details(item.dish_id)[1])
                cart.total_price += dish_price * item.quantity
            cart.save()

            # Повернути відповідь
            response_data = CartSerializer(cart).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(RetrieveAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'id'
