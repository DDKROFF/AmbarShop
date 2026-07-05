"""Context processors для AmbarShop."""


def cart_count(request):
    """Добавляет количество товаров в корзине в контекст."""
    from account.models import Cart
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    
    return {
        'cart_count': cart.items.count() if not created else 0
    }
