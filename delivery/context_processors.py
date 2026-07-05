from .cities import MAIN_CITIES


def delivery_cities(request):
    """Контекстный процессор для городов доставки"""
    return {
        'delivery_cities': MAIN_CITIES
    }
