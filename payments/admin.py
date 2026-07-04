from django.contrib import admin
from .models import PaymentMethod, Payment, Receipt


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'payment_method', 'amount', 'status', 'provider', 'created_at']
    list_filter = ['status', 'provider', 'created_at']
    search_fields = ['order__id', 'payment_id']
    list_editable = ['status']


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['number', 'order', 'payment', 'total_amount', 'issue_date', 'created_at']
    list_filter = ['issue_date', 'created_at']
    search_fields = ['number', 'order__id', 'payment__id']
