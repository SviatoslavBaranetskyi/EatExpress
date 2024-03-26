from rest_framework import serializers

from .models import OrderItem, Order
from .utils import get_dish_details


class OrderItemSerializer(serializers.ModelSerializer):
    dish_name = serializers.SerializerMethodField(read_only=True)
    dish_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['dish_name', 'dish_price', 'quantity']

    def get_dish_name(self, obj):
        return get_dish_details(obj.dish_id)[0]

    def get_dish_price(self, obj):
        return get_dish_details(obj.dish_id)[1]


class OrderSerializer(serializers.ModelSerializer):
    dishes = OrderItemSerializer(many=True, read_only=True)
    delivery_address = serializers.CharField(max_length=255, required=False)
    courier = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'dishes', 'status', 'created_at', 'updated_at', 'total_price', 'delivery_address',
                  'payment_method', 'courier']
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_price', 'courier']

    def get_courier(self, obj):
        if obj.courier:
            courier_data = {
                'first_name': obj.courier.user.first_name,
                'contact_info': obj.courier.phone_number,
            }
            return courier_data
        return 'Search for a courier'
