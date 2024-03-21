from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Courier


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=15)
    address = serializers.CharField(max_length=255, required=False)
    status = serializers.ChoiceField(choices=Courier.STATUS_CHOICES, default='Available', required=False)

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        phone_number = validated_data['phone_number']
        address = validated_data.get('address')
        status = validated_data.get('status')

        # Create and save a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Decide whether to create a profile or courier based on the presence of 'address' or 'status' field
        if address:
            # Create and save a user profile
            profile = Profile.objects.create(user=user, phone_number=phone_number, address=address)
        elif status:
            # Create and save a courier profile
            courier = Courier.objects.create(user=user, phone_number=phone_number, status=status)

        return user


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'email']

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        # Обновляем соответствующие поля пользователя
        user_data = validated_data.get('user', {})
        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)  # Изменено
        user.last_name = user_data.get('last_name', user.last_name)  # Изменено
        user.save()
        return instance


class CourierSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Courier
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'status']

    def update(self, instance, validated_data):
        # Обновляем поля курьера
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Обновляем соответствующие поля пользователя
        user_data = validated_data.get('user', {})
        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)  # Изменено
        user.last_name = user_data.get('last_name', user.last_name)  # Изменено
        user.save()

        return instance
