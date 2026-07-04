from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentMethodViewSet, PaymentViewSet, ReceiptViewSet, payment_view

app_name = 'payments'

router = DefaultRouter()
router.register(r'payment-methods', PaymentMethodViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'receipts', ReceiptViewSet)

urlpatterns = [
    path('', payment_view, name='payment'),
    path('', include(router.urls)),
]
