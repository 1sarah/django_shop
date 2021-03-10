from rest_framework import serializers
from send_sms import send_sms, send
from django.shortcuts import get_object_or_404
from .models import Customer, Order, User
# from django.contrib.auth import authenticatefrom shop.models import User
from django.contrib.auth import authenticate


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {'customer': {'write_only': True}}

    def create(self, validated_data):
        customer_pk = validated_data.get('customer')
        customer = get_object_or_404(Customer, pk=customer_pk.id)

        # {'item': 'shirt', 'amount': 20, 'code': 334, 'customer': '3'}
        # Order(item='shirt', amount=20, code=334, customer='3')

        order = Order(
            **validated_data
        )

        order.save()
        if customer.phone_number:
            try:
                send(f'{order.item} order successfully added', customer.phone_number)
            except Exception as e:
                print(f"ERROR SENDING MESSAGE {e}")
        return order


class CustomerSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'


class SocialAuthSerializer(serializers.Serializer):
    provider = serializers.CharField(
        max_length=30,
        allow_blank=True
    )
    access_token = serializers.CharField(
        max_length=255,
        allow_blank=True
    )
    access_token_secret = serializers.CharField(
        max_length=255,
        allow_blank=True,
        default=""
    )

    def validate(self, data):
        """Method to validate provider and access token"""
        provider = data.get('provider', None)
        access_token = data.get('access_token', None)
        access_token_secret = data.get('access_token_secret', None)
        if not provider:
            raise serializers.ValidationError(
                'A provider is required for Social Login'
            )

        if not access_token:
            raise serializers.ValidationError(
                'An access token is required for Social Login'
            )

        if provider == 'twitter' and not access_token_secret:
            raise serializers.ValidationError(
                'An access token secret is required for Twitter Login'
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    class Meta:
        model = User
        fields = ('email', 'username', 'tokenn')


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'token', 'email', 'password')

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
