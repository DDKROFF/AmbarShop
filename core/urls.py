from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SiteInfoViewSet

router = DefaultRouter()
router.register(r'site-info', SiteInfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
