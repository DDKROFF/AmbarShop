from django.urls import path
from .views import catalog_view, product_detail_view, home_view, contacts_view

app_name = 'shop'

urlpatterns = [
    path('', catalog_view, name='catalog'),
    path('home/', home_view, name='home'),
    path('product/<slug:slug>/', product_detail_view, name='product_detail'),
    path('contacts/', contacts_view, name='contacts'),
]
