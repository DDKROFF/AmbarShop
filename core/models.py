from django.db import models


class SiteInfo(models.Model):
    key = models.CharField(max_length=100, unique=True, verbose_name='Ключ')
    value = models.TextField(verbose_name='Значение')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Информация сайта'
        verbose_name_plural = 'Информация сайта'

    def __str__(self):
        return self.key
