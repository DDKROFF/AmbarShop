from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Category, Product
from account.models import Review
from .serializers import CategorySerializer, ProductSerializer
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.db import models


def home_view(request):
    reviews = Review.objects.filter(is_moderated=True).order_by('?')[:3]
    
    # Получаем популярные товары (ограничиваем 3 штуками)
    popular_products = Product.objects.filter(popular=True, is_active=True)[:3]
    
    # Если популярных товаров меньше 3, добавляем случайные
    if popular_products.count() < 3:
        additional_count = 3 - popular_products.count()
        additional_products = Product.objects.filter(is_active=True).exclude(id__in=popular_products.values_list('id', flat=True)).order_by('?')[:additional_count]
        popular_products = list(popular_products) + list(additional_products)
    
    # Получаем категории для отображения на главной
    categories = Category.objects.filter(is_active=True).order_by('name')
    
    return render(request, 'home.html', {
        'reviews': reviews,
        'popular_products': popular_products,
        'categories': categories,
    })


def catalog_view(request):
    # Получаем все категории
    categories = Category.objects.filter(is_active=True).order_by('name')
    
    # Получаем выбранные категории из GET-параметра
    selected_categories = request.GET.getlist('category')
    
    # Получаем все товары или фильтруем по категориям
    products = Product.objects.filter(is_active=True)
    
    if selected_categories:
        products = products.filter(category__slug__in=selected_categories).distinct()
    
    # Поиск по названию
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)
    
    # Сортировка
    sort = request.GET.get('sort')
    if sort == 'price-asc':
        products = products.order_by('price')
    elif sort == 'price-desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')
    
    # Пагинация (9 товаров на страницу)
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'shop/catalog.html', {
        'categories': categories,
        'products': page_obj,
        'selected_categories': selected_categories,
        'query': query,
        'sort': sort,
    })


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
    })


def contacts_view(request):
    """Контакты и форма обратной связи"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if name and email and message:
            try:
                # Отправляем email
                send_mail(
                    f'Сообщение от {name}',
                    f'Имя: {name}\nEmail: {email}\nСообщение: {message}',
                    email,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
                return render(request, 'contacts.html', {'success': True})
            except Exception as e:
                return render(request, 'contacts.html', {'error': 'Ошибка при отправке сообщения'})
        else:
            return render(request, 'contacts.html', {'error': 'Заполните все поля'})
    
    return render(request, 'contacts.html')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'
