from rest_framework import serializers
from .models import PaymentMethod, Payment, Receipt
from account.models import Order


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name', 'description', 'is_active']


class PaymentSerializer(serializers.ModelSerializer):
    payment_method = PaymentMethodSerializer(read_only=True)
    payment_method_id = serializers.PrimaryKeyRelatedField(
        queryset=PaymentMethod.objects.all(),
        source='payment_method',
        write_only=True,
        required=False
    )
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        source='order',
        write_only=True
    )

    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'order_id', 'payment_method', 'payment_method_id',
            'amount', 'status', 'payment_id', 'provider', 'created_at', 'updated_at'
        ]


class ReceiptSerializer(serializers.ModelSerializer):
    payment_id = serializers.PrimaryKeyRelatedField(
        queryset=Payment.objects.all(),
        source='payment',
        write_only=True,
        required=False
    )

    class Meta:
        model = Receipt
        fields = [
            'id', 'order', 'payment', 'payment_id', 'number',
            'issue_date', 'total_amount', 'json_data', 'created_at'
        ]
