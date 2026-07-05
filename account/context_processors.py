from .models import Cart, CartItem


def cart_count(request):
    """Контекстный процессор для количества товаров в корзине"""
    cart_count = 0
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.items.count()
    else:
        session_id = request.session.session_key
        if session_id:
            cart, created = Cart.objects.get_or_create(session_id=session_id)
            cart_count = cart.items.count()
    
    return {
        'cart_count': cart_count
    }
