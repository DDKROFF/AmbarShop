from django.contrib import admin
from .models import DeliveryMethod, DeliveryAddress


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost', 'min_order_amount', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at']
    list_filter = ['city', 'created_at']
    search_fields = ['city', 'street', 'house']

