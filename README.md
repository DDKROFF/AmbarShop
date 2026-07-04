# AmbarShop

Зоомагазин с онлайн-продажами и доставкой.

## Установка

1. Установите зависимости:
```bash
poetry install
```

2. Выполните миграции:
```bash
poetry run python manage.py migrate
```

3. Создайте суперпользователя:
```bash
poetry run python manage.py createsuperuser
```

4. Запустите сервер:
```bash
poetry run python manage.py runserver
```

## Яндекс.Карты

Для интеграции карт добавьте API ключ:

1. Получите бесплатный API ключ на [Яндекс.Конструктор](https://developer.tech.yandex.ru/)
2. Откройте `templates/account/map.html`
3. Замените `YOUR_API_KEY` на ваш реальный ключ
4. Перезапустите сервер

Бесплатный тариф включает:
- 25 000 запросов геокодирования в день
- 15 000 запросов маршрутизации в день
- 40 000 запросов поиска в день

## API endpoints

Все API доступны по адресу `/api/`:

- `/api/categories/` - категории товаров
- `/api/products/` - товары
- `/api/guides/` - гайды по уходу за животными
- `/api/delivery-methods/` - способы доставки
- `/api/delivery-addresses/` - адреса доставки
- `/api/orders/` - заказы
- `/api/payment-methods/` - способы оплаты
- `/api/payments/` - платежи
- `/api/receipts/` - чеки
- `/api/site-info/` - служебная информация

## Структура проекта

- `core` - основное приложение ( служебная информация)
- `shop` - товары и категории
- `guides` - гайды по уходу за животными
- `delivery` - доставка и заказы
- `payments` - платежи и чеки
