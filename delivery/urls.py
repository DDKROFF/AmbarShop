from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeliveryMethodViewSet, DeliveryAddressViewSet, basket_view, delete_address_view, edit_address_view, set_default_address_view

app_name = 'delivery'

router = DefaultRouter()
router.register(r'delivery-methods', DeliveryMethodViewSet)
router.register(r'delivery-addresses', DeliveryAddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('basket/', basket_view, name='basket'),
    # Управление адресами пользователя
    path('addresses/delete/<int:address_id>/', delete_address_view, name='delete_address'),
    path('addresses/edit/<int:address_id>/', edit_address_view, name='edit_address'),
    path('addresses/set-default/<int:address_id>/', set_default_address_view, name='set_default_address'),
]
