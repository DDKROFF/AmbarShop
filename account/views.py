from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from delivery.models import DeliveryAddress
from delivery.forms import DeliveryAddressForm, CheckoutAddressForm
from .forms import UserRegistrationForm, ReviewForm, UserProfileForm, ChangePasswordForm, ChangeEmailForm, ChangePhoneForm
from .models import Cart, CartItem, Order, OrderItem
from shop.models import Product


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('account:profile')
        else:
            messages.error(request, 'Неверный email или пароль')
            return render(request, 'account/login.html')
    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    return redirect('shop:home')


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('account:login')
        else:
            messages.error(request, 'Ошибка при регистрации')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


@login_required
def profile_view(request):
    # Получаем адрес пользователя
    user_address = None
    try:
        user_profile = request.user.profile
        user_address = user_profile.address
    except:
        pass
    
    return render(request, 'account/profile.html', {
        'user_address': user_address,
    })


@login_required
def edit_profile_view(request):
    """Редактирование профиля"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('account:profile')
        else:
            messages.error(request, 'Ошибка при обновлении профиля')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'account/edit_profile.html', {
        'form': form,
    })


@login_required
def addresses_view(request):
    from delivery.forms import DeliveryAddressForm
    
    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.created_by = request.user
            address.save()
            messages.success(request, 'Адрес успешно добавлен!')
            return redirect('account:addresses')
        else:
            messages.error(request, 'Ошибка при добавлении адреса')
    
    addresses = DeliveryAddress.objects.filter(created_by=request.user, is_active=True)
    form = DeliveryAddressForm()
    
    return render(request, 'account/addresses.html', {
        'addresses': addresses,
        'form': form,
    })


@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'account/orders.html', {'orders': orders})


@login_required
def active_orders_view(request):
    orders = Order.objects.filter(user=request.user, status__in=['pending', 'confirmed', 'preparing', 'shipping']).order_by('-created_at')
    return render(request, 'account/active_orders.html', {'orders': orders})


@login_required
def saved_view(request):
    return render(request, 'account/saved.html')


@login_required
def settings_view(request):
    password_form = ChangePasswordForm(request.user)
    email_form = ChangeEmailForm(request.user)
    phone_form = ChangePhoneForm(request.user)
    
    if request.method == 'POST':
        if 'change_password' in request.POST:
            password_form = ChangePasswordForm(request.user, request.POST)
            if password_form.is_valid():
                user = request.user
                user.set_password(password_form.cleaned_data['new_password'])
                user.save()
                logout(request)
                messages.success(request, 'Пароль успешно изменен. Пожалуйста, войдите снова.')
                return redirect('account:login')
            else:
                messages.error(request, 'Ошибка при изменении пароля')
        elif 'change_email' in request.POST:
            email_form = ChangeEmailForm(request.user, request.POST)
            if email_form.is_valid():
                request.user.email = email_form.cleaned_data['new_email']
                request.user.save()
                messages.success(request, 'Email успешно изменен')
                return redirect('account:settings')
            else:
                messages.error(request, 'Ошибка при изменении email')
        elif 'change_phone' in request.POST:
            phone_form = ChangePhoneForm(request.user, request.POST)
            if phone_form.is_valid():
                request.user.phone = phone_form.cleaned_data['new_phone']
                request.user.save()
                messages.success(request, 'Телефон успешно изменен')
                return redirect('account:settings')
            else:
                messages.error(request, 'Ошибка при изменении телефона')

    context = {
        'password_form': password_form,
        'email_form': email_form,
        'phone_form': phone_form,
    }
    return render(request, 'account/settings.html', context)


@login_required
def delete_account_view(request):
    """Удаление аккаунта"""
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Ваш аккаунт успешно удален')
        return redirect('shop:home')
    return redirect('account:settings')


@login_required
def map_view(request):
    return render(request, 'account/map.html')


@login_required
def save_address_view(request):
    """Сохранение адреса доставки"""
    if request.method == 'POST':
        city = request.POST.get('city', '').strip()
        street = request.POST.get('street', '').strip()
        house = request.POST.get('house', '').strip()
        
        if city and street and house:
            apartment = request.POST.get('apartment', '').strip()
            entrance = request.POST.get('entrance', '').strip()
            floor = request.POST.get('floor', '').strip()
            intercom = request.POST.get('intercom', '').strip()
            
            full_address = f"{city}, {street}, д. {house}"
            if apartment:
                full_address += f", кв. {apartment}"
            
            DeliveryAddress.objects.create(
                created_by=request.user,
                city=city,
                street=street,
                house=house,
                apartment=apartment,
                entrance=entrance,
                floor=floor,
                intercom=intercom,
                full_address=full_address,
                coordinates='',
                is_active=True
            )
            
            # Возвращаем JSON ответ для AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Адрес "{full_address}" успешно добавлен!'
                })
            
            messages.success(request, f'Адрес "{full_address}" успешно добавлен!')
            return redirect('account:addresses')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Пожалуйста, заполните город, улицу и номер дома!'
                })
            messages.error(request, 'Пожалуйста, заполните город, улицу и номер дома!')
            return redirect('account:addresses')
    
    return redirect('account:addresses')


@login_required
def delete_address_view(request, address_id):
    """Удаление адреса доставки"""
    from delivery.models import DeliveryAddress
    address = get_object_or_404(DeliveryAddress, id=address_id, created_by=request.user)
    
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Адрес успешно удален')
        return redirect('account:addresses')
    
    return redirect('account:addresses')


@login_required
def edit_address_view(request, address_id):
    """Редактирование адреса доставки"""
    from delivery.models import DeliveryAddress
    from delivery.forms import DeliveryAddressForm
    
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
    from delivery.models import DeliveryAddress
    address = get_object_or_404(DeliveryAddress, id=address_id, created_by=request.user)
    
    # Сначала сбрасываем все адреса как не по умолчанию
    DeliveryAddress.objects.filter(created_by=request.user).update(is_default=False)
    
    # Устанавливаем текущий адрес как по умолчанию
    address.is_default = True
    address.save()
    
    messages.success(request, 'Адрес успешно установлен как адрес по умолчанию')
    return redirect('account:addresses')


@login_required
def add_review_view(request):
    """Добавление отзыва"""
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.is_moderated = False
            review.save()
            messages.success(request, 'Отзыв успешно добавлен! После модерации он будет опубликован.')
            return redirect('shop:home')
        else:
            messages.error(request, 'Ошибка при добавлении отзыва')
    else:
        form = ReviewForm()
    
    return render(request, 'account/review_form.html', {'form': form})


def get_cart(request):
    """Получение корзины пользователя"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
        return cart


def add_to_cart_view(request):
    """Добавление товара в корзину"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        cart = get_cart(request)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'cart_count': cart.items.count(),
            'cart_total': cart.get_total_price()
        })
    
    return JsonResponse({'success': False})


def remove_from_cart_view(request):
    """Удаление товара из корзины"""
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=get_cart(request))
        cart_item.delete()
        
        cart = get_cart(request)
        
        return JsonResponse({
            'success': True,
            'cart_count': cart.items.count(),
            'cart_total': cart.get_total_price()
        })
    
    return JsonResponse({'success': False})


def update_cart_view(request):
    """Обновление количества товара в корзине"""
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=get_cart(request))
        cart_item.quantity = quantity
        cart_item.save()
        
        cart = get_cart(request)
        
        return JsonResponse({
            'success': True,
            'cart_count': cart.items.count(),
            'cart_total': cart.get_total_price(),
            'item_total': cart_item.get_total_price()
        })
    
    return JsonResponse({'success': False})


def cart_view(request):
    """Просмотр корзины"""
    cart = get_cart(request)
    cart_items = cart.items.select_related('product').all()
    
    return render(request, 'account/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
    })


def checkout_view(request):
    """Оформление заказа"""
    from delivery.forms import CheckoutAddressForm
    
    if request.method == 'POST':
        cart = get_cart(request)
        
        if not cart.items.exists():
            messages.error(request, 'Корзина пуста')
            return redirect('account:cart')
        
        form = CheckoutAddressForm(request.POST)
        
        if form.is_valid():
            # Получаем данные заказа
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            comment = form.cleaned_data.get('comment', '')
            
            # Создаем заказ
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                address='',  # Будет заполнено в DeliveryAddress
                delivery_method=request.POST.get('delivery_method', 'courier'),
                payment_method='sbp',
                status='pending',
                total_amount=cart.get_total_price(),
                comment=comment
            )
            
            # Добавляем товары в заказ
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            # Очищаем корзину
            cart.items.all().delete()
            
            # Если пользователь авторизован и выбрал сохранение адреса, сохраняем его
            if request.user.is_authenticated:
                city = form.cleaned_data.get('city', '').strip()
                street = form.cleaned_data.get('street', '').strip()
                house = form.cleaned_data.get('house', '').strip()
                save_to_profile = form.cleaned_data.get('save_to_profile', False)
                
                if city and street and house and save_to_profile:
                    apartment = form.cleaned_data.get('apartment', '').strip()
                    entrance = form.cleaned_data.get('entrance', '').strip()
                    floor = form.cleaned_data.get('floor', '').strip()
                    intercom = form.cleaned_data.get('intercom', '').strip()
                    
                    full_address = f"{city}, {street}, д. {house}"
                    if apartment:
                        full_address += f", кв. {apartment}"
                    
                    DeliveryAddress.objects.create(
                        created_by=request.user,
                        city=city,
                        street=street,
                        house=house,
                        apartment=apartment,
                        entrance=entrance,
                        floor=floor,
                        intercom=intercom,
                        full_address=full_address,
                        coordinates='',
                        is_active=True
                    )
            
            # Генерируем ссылку для оплаты через СБП (Система быстрых платежей)
            # Ссылка формируется по формату sbp.nspk.ru
            # Телефон получателя: 89898080839
            sbp_phone = "79898080839"  # Мобильный формат для СБП
            payment_url = f"https://sbp.nspk.ru/pay?tid=100000000001&sum={order.total_amount}&bankid=200000000001&phone={sbp_phone}&name=AmbarShop&comment=Заказ%20{order.id}"
            
            # Альтернативный вариант: QR-код для оплаты
            qr_payment_url = f"https://api.qrserver.com/v1/create-qr-code/?data=sbp%3A%2F%2F{sbp_phone}%3Fsum={order.total_amount}&size=300x300"
            
            return render(request, 'account/payment_choice.html', {
                'order': order,
                'payment_url': payment_url,
                'qr_payment_url': qr_payment_url,
                'sbp_phone': sbp_phone,
            })
    
    cart = get_cart(request)
    
    # Инициализация формы
    form = CheckoutAddressForm()
    
    # Автоматически заполняем данные из аккаунта пользователя
    initial_data = {}
    
    if request.user.is_authenticated:
        # Заполняем данные пользователя
        if request.user.first_name:
            initial_data['first_name'] = request.user.first_name
        if request.user.last_name:
            initial_data['last_name'] = request.user.last_name
        if request.user.email:
            initial_data['email'] = request.user.email
        if request.user.phone:
            initial_data['phone'] = request.user.phone
        
        # Получаем последний использованный адрес
        last_address = DeliveryAddress.objects.filter(created_by=request.user, is_active=True).first()
        if last_address:
            # Заполняем форму начальными данными
            form = CheckoutAddressForm(initial={
                'first_name': request.user.first_name or '',
                'last_name': request.user.last_name or '',
                'email': request.user.email or '',
                'phone': request.user.phone or '',
                'city': last_address.city,
                'street': last_address.street,
                'house': last_address.house,
                'apartment': last_address.apartment or '',
                'entrance': last_address.entrance or '',
                'floor': last_address.floor or '',
                'intercom': last_address.intercom or '',
            })
    
    return render(request, 'account/checkout.html', {
        'cart': cart,
        'form': form,
        'initial_data': initial_data,
    })


def payment_success_view(request, order_id):
    """Страница успешной оплаты"""
    order = get_object_or_404(Order, id=order_id)
    order.payment_status = 'paid'
    order.status = 'confirmed'
    order.save()
    
    return render(request, 'account/payment_success.html', {'order': order})
