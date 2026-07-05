from django.db import models
from shop.models import Product
from django.conf import settings


class DeliveryMethod(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Стоимость')
    min_order_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Минимальная сумма заказа для бесплатной доставки')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Способ доставки'
        verbose_name_plural = 'Способы доставки'

    def __str__(self):
        return self.name


class DeliveryAddress(models.Model):
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=200, verbose_name='Улица')
    house = models.CharField(max_length=20, verbose_name='Дом')
    apartment = models.CharField(max_length=20, blank=True, verbose_name='Квартира')
    entrance = models.CharField(max_length=20, blank=True, verbose_name='Подъезд')
    floor = models.CharField(max_length=20, blank=True, verbose_name='Этаж')
    full_address = models.TextField(blank=True, verbose_name='Полный адрес')
    is_default = models.BooleanField(default=False, verbose_name='Адрес по умолчанию')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='addresses', verbose_name='Создано пользователем')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'

    def __str__(self):
        return f"{self.city}, {self.street}, д. {self.house}"

