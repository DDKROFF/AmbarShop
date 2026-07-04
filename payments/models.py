from django.db import models
from account.models import Order


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'

    def __str__(self):
        return self.name


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачено'),
        ('refunded', 'Возврат'),
        ('failed', 'Ошибка'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment', verbose_name='Заказ')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, verbose_name='Способ оплаты')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    payment_id = models.CharField(max_length=255, blank=True, verbose_name='ID платежа')
    provider = models.CharField(max_length=50, blank=True, verbose_name='Провайдер')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-created_at']

    def __str__(self):
        return f"Платеж #{self.id} для заказа #{self.order.id}"

    def process_quick_payment(self, phone_number):
        """Метод для быстрого платежа по номеру телефона"""
        if self.status == 'pending':
            self.status = 'paid'
            self.save()
            return True
        return False


class Receipt(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='receipt', verbose_name='Заказ')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, verbose_name='Платеж')
    number = models.CharField(max_length=100, unique=True, verbose_name='Номер чека')
    issue_date = models.DateTimeField(verbose_name='Дата выдачи')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    json_data = models.JSONField(verbose_name='Данные чека (JSON)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    def __str__(self):
        return f"Чек #{self.number}"
