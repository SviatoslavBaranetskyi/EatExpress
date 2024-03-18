from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Courier, CartItem, Cart
from .utils import get_dish_details


class CourierSignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=15)
    status = serializers.ChoiceField(choices=Courier.STATUS_CHOICES, default='Available')

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        phone_number = validated_data['phone_number']
        status = validated_data.get('status')

        # Create and save a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Create and save a courier profile
        courier = Courier.objects.create(user=user, first_name=first_name, last_name=last_name,
                                         phone_number=phone_number, status=status)
        return user


class CourierSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Courier
        fields = ['first_name', 'last_name', 'phone_number', 'status', 'email']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class CartItemSerializer(serializers.ModelSerializer):
    dish_name = serializers.SerializerMethodField(read_only=True)
    dish_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart_id', 'dish_name', 'dish_price', 'quantity']

    def get_dish_name(self, obj):
        return get_dish_details(obj.dish_id)[0]

    def get_dish_price(self, obj):
        return get_dish_details(obj.dish_id)[1]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'status', 'created_at', 'updated_at', 'total_price']
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_price']
