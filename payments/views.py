from django.shortcuts import render
from rest_framework import viewsets
from .models import PaymentMethod, Payment, Receipt
from .serializers import PaymentMethodSerializer, PaymentSerializer, ReceiptSerializer


def payment_view(request):
    return render(request, 'payments/payment.html')


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.all()
        return queryset


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
