from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('addresses/', views.addresses_view, name='addresses'),
    path('map/', views.map_view, name='map'),
    path('save-address/', views.save_address_view, name='save_address'),
    path('addresses/delete/<int:address_id>/', views.delete_address_view, name='delete_address'),
    path('addresses/edit/<int:address_id>/', views.edit_address_view, name='edit_address'),
    path('addresses/set-default/<int:address_id>/', views.set_default_address_view, name='set_default_address'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/active/', views.active_orders_view, name='active_orders'),
    path('saved/', views.saved_view, name='saved'),
    path('settings/', views.settings_view, name='settings'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/success/<int:order_id>/', views.payment_success_view, name='payment_success'),
    path('add-review/', views.add_review_view, name='add_review'),
    path('cart/add/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/remove/', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/update/', views.update_cart_view, name='update_cart'),
]
