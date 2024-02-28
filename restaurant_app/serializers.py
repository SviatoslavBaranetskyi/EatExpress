from rest_framework import serializers


class RestaurantSerializer(serializers.Serializer):
    name = serializers.CharField()
    distance = serializers.FloatField()
    address = serializers.CharField(source='location.formatted_address')
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        categories = obj.get('categories', [])
        if categories:
            return categories[0]['name']
        return None
