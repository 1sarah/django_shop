from rest_framework import serializers
from send_sms import send_sms, send
from django.shortcuts import get_object_or_404
from .models import Customer, Order


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