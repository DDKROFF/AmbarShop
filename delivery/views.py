from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import DeliveryMethod, DeliveryAddress
from .serializers import DeliveryMethodSerializer, DeliveryAddressSerializer
from .forms import DeliveryAddressForm, CheckoutAddressForm
from account.models import Cart


class DeliveryMethodViewSet(viewsets.ModelViewSet):
    queryset = DeliveryMethod.objects.filter(is_active=True).order_by('cost')
    serializer_class = DeliveryMethodSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DeliveryAddressViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = DeliveryAddress.objects.all()
    
    def get_queryset(self):
        return DeliveryAddress.objects.filter(created_by=self.request.user, is_active=True)


def basket_view(request):
    """Корзина"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    
    return render(request, 'delivery/basket.html', {
        'cart': cart,
        'cart_items': cart.items.select_related('product').all() if not created else [],
    })


@login_required
def delete_address_view(request, address_id):
    """Удаление адреса доставки"""
    address = get_object_or_404(DeliveryAddress, id=address_id, created_by=request.user)
    
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Адрес успешно удален')
        return redirect('account:addresses')
    
    return redirect('account:addresses')


@login_required
def edit_address_view(request, address_id):
    """Редактирование адреса доставки"""
    address = get_object_or_404(DeliveryAddress, id=address_id, created_by=request.user)
    
    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Адрес успешно обновлен')
            return redirect('account:addresses')
        else:
            messages.error(request, 'Ошибка при обновлении адреса')
    else:
        form = DeliveryAddressForm(instance=address)
    
    addresses = DeliveryAddress.objects.filter(created_by=request.user, is_active=True)
    
    return render(request, 'account/addresses.html', {
        'addresses': addresses,
        'form': form,
        'edit_mode': True,
        'edit_address': address,
    })


@login_required
def set_default_address_view(request, address_id):
    """Установка адреса по умолчанию"""
    address = get_object_or_404(DeliveryAddress, id=address_id, created_by=request.user)
    
    # Сначала сбрасываем все адреса как не по умолчанию
    DeliveryAddress.objects.filter(created_by=request.user).update(is_default=False)
    
    # Устанавливаем текущий адрес как по умолчанию
    address.is_default = True
    address.save()
    
    messages.success(request, 'Адрес успешно установлен как адрес по умолчанию')
    return redirect('account:addresses')
