from rest_framework import serializers


class RestaurantMenuSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    categories = serializers.ListField(child=serializers.CharField())
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
