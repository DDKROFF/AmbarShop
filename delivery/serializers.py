from rest_framework import serializers
from .models import DeliveryMethod, DeliveryAddress
from shop.models import Product


class DeliveryMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMethod
        fields = ['id', 'name', 'description', 'cost', 'min_order_amount', 'is_active']


class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = [
            'id', 'city', 'street', 'house',
            'apartment', 'entrance', 'floor', 'full_address', 'is_default'
        ]
        read_only_fields = ['is_default']
