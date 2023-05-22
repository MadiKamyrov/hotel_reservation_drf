from datetime import timedelta

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Category, Room, Pricing, Reservation, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        return user


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh_token = self.get_token(self.user)
        user_serializer = UserSerializer(self.user)
        data['user'] = user_serializer.data
        data['refresh_token'] = str(refresh_token)
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['category', 'number', 'floor']


class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = ['day_of_week', 'category', 'price']


class ReservationSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Reservation
        fields = (
            'id',
            'user',
            'arrival_date', 'departure_date', 'room', 'price')

    @staticmethod
    def get_price(obj):
        room = obj.room.category
        pricing = Pricing.objects.filter(category=room).values('day_of_week', 'price')

        arrival_date = obj.arrival_date
        departure_date = obj.departure_date

        total_price = 0

        current_date = arrival_date
        while current_date <= departure_date:
            current_day_of_week = current_date.weekday()

            matching_prices = [price['price'] for price in pricing if price['day_of_week'] == current_day_of_week]
            if matching_prices:
                total_price += max(matching_prices)

            current_date += timedelta(days=1)

        return total_price
