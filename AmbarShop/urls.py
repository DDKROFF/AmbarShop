from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import SiteInfoViewSet
from shop.views import CategoryViewSet, ProductViewSet, home_view
from guides.views import GuideViewSet, GuideImageViewSet
from delivery.views import DeliveryMethodViewSet, DeliveryAddressViewSet
from payments.views import PaymentMethodViewSet, PaymentViewSet, ReceiptViewSet
from account.views import login_view, logout_view, register_view, profile_view

router = DefaultRouter()
router.register(r'site-info', SiteInfoViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'guides', GuideViewSet)
router.register(r'guide-images', GuideImageViewSet)
router.register(r'delivery-methods', DeliveryMethodViewSet)
router.register(r'delivery-addresses', DeliveryAddressViewSet)
router.register(r'payment-methods', PaymentMethodViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'receipts', ReceiptViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('shop/', include('shop.urls')),
    path('guides/', include('guides.urls')),
    path('delivery/', include('delivery.urls')),
    path('payments/', include('payments.urls')),
    path('account/', include('account.urls')),
    path('api/', include(router.urls)),
]
