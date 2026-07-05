import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AmbarShop.settings')
django.setup()

from shop.models import Product, ProductImage

products = Product.objects.all()
print(f"Всего товаров: {products.count()}")

for product in products:
    images = product.images.all()
    print(f"{product.name}: {images.count()} изображений")
    if images.count() == 0:
        print(f"  -> НЕТ ИЗОБРАЖЕНИЙ!")
