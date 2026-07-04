from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker
from shop.models import Category, Product, ProductImage
from account.models import Order, OrderItem, User as CustomUser
from delivery.models import DeliveryAddress, DeliveryMethod
from payments.models import PaymentMethod
import requests
from django.core.files.base import ContentFile

fake = Faker('ru_RU')

# Ссылки на картинки корма для животных (альтернативные источники)
PRODUCT_IMAGES = [
    "https://loremflickr.com/600/400/dog,carnivore?random=1",
    "https://loremflickr.com/600/400/cat,pet?random=2",
    "https://loremflickr.com/600/400/pet,food?random=3",
    "https://loremflickr.com/600/400/dog?random=4",
    "https://loremflickr.com/600/400/cat?random=5",
    "https://loremflickr.com/600/400/bird?random=6",
    "https://loremflickr.com/600/400/fish?random=7",
]

User = settings.AUTH_USER_MODEL


class Command(BaseCommand):
    help = 'Create test data for AmbarShop'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data creation...')

        # Создаем суперпользователя
        if not CustomUser.objects.filter(email='admin@example.com').exists():
            CustomUser.objects.create_superuser(
                email='admin@example.com',
                password='admin123',
                username='admin',
                phone='+79990000000'
            )
            self.stdout.write('Created superuser: admin@example.com')

        # Создаем обычных пользователей
        for i in range(2):
            email = f'user{i+1}@example.com'
            if not CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.create_user(
                    email=email,
                    password='password123',
                    username=f'user{i+1}',
                    phone=f'+7999123456{i}',
                    first_name=fake.first_name(),
                    last_name=fake.last_name()
                )
                self.stdout.write(f'Created user: {email}')

        # Создаем категорию
        category, _ = Category.objects.get_or_create(
            name='Корм для животных',
            slug='korm-dlya-zhivotnyh',
            defaults={
                'description': 'Разнообразные корма для домашних животных'
            }
        )
        self.stdout.write('Created category: Корм для животных')

        # Создаем способы оплаты
        payment_methods_data = [
            ('Картой при получении', 'Оплата банковской картой курьеру'),
            ('Наличными при получении', 'Оплата наличными курьеру'),
            ('Онлайн оплата', 'Оплата через сайт'),
        ]
        for name, description in payment_methods_data:
            PaymentMethod.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
        self.stdout.write('Created payment methods')

        # Создаем способы доставки
        delivery_methods_data = [
            ('Курьерская доставка', 'Доставка курьером по городу', '500.00', '1500.00'),
            ('Самовывоз', 'Забрать заказ из пункта выдачи', '0.00', '0.00'),
            ('Почта России', 'Доставка почтой по России', '300.00', '2000.00'),
        ]
        for name, description, cost, min_amount in delivery_methods_data:
            DeliveryMethod.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                    'cost': cost,
                    'min_order_amount': min_amount
                }
            )
        self.stdout.write('Created delivery methods')

        # Создаем продукты
        product_names = [
            ('Корм для собак премиум', 'Вкусный и полезный корм для взрослых собак', '2500.00'),
            ('Корм для кошек деликатес', 'Корм с рыбой для избирательных кошек', '1800.00'),
            ('Сухой корм для щенков', 'Полноценное питание для растущих собак', '2200.00'),
            ('Консервы для кошек', 'Нежная консерва с курицей', '450.00'),
            ('Корм для хомяков', 'Смесь зерновая для хомяков и декоративных крыс', '350.00'),
            ('Корм для попугаев', 'Питательная смесь для экзотических птиц', '600.00'),
            ('Корм для рыб', 'Хрустящие гранулы для аквариумных рыб', '280.00'),
        ]

        for i, (name, description, price) in enumerate(product_names):
            product, created = Product.objects.get_or_create(
                name=name,
                slug=f'korm-dlya-zhivotnyh-{i+1}',
                defaults={
                    'category': category,
                    'description': description,
                    'price': price,
                    'stock': fake.random_int(10, 100),
                }
            )
            if created:
                # Скачиваем и сохраняем изображение
                image_url = PRODUCT_IMAGES[i]
                try:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        image_name = f'product_{i+1}.jpg'
                        # Создаем ProductImage
                        ProductImage.objects.create(
                            product=product,
                            image=ContentFile(response.content, name=image_name),
                            is_main=True
                        )
                        self.stdout.write(f'Created product: {name} with image')
                    else:
                        self.stdout.write(f'Could not download image for {name}')
                except Exception as e:
                    self.stdout.write(f'Error downloading image for {name}: {e}')
            else:
                self.stdout.write(f'Product already exists: {name}')

        # Создаем пару заказов
        user1 = CustomUser.objects.get(email='user1@example.com')
        user2 = CustomUser.objects.get(email='user2@example.com')

        # Заказ 1
        address1 = DeliveryAddress.objects.create(
            city='Белореченск',
            street='Лесная',
            house='15',
            apartment='45',
            created_by=user1
        )
        order1 = Order.objects.create(
            first_name='Иван',
            last_name='Иванов',
            phone='+79991234567',
            email='ivan@example.com',
            user=user1,
            address='Белореченск, Лесная, д. 15, кв. 45',
            delivery_method='Курьерская доставка',
            payment_method='Картой при получении',
            payment_status='pending',
            status='pending',
            total_amount='2950.00'
        )
        product1 = Product.objects.get(name='Корм для собак премиум')
        OrderItem.objects.create(
            order=order1,
            product=product1,
            quantity=1,
            price=product1.price
        )
        product2 = Product.objects.get(name='Консервы для кошек')
        OrderItem.objects.create(
            order=order1,
            product=product2,
            quantity=2,
            price=product2.price
        )

        # Заказ 2
        address2 = DeliveryAddress.objects.create(
            city='Приморско-Ахтарский',
            street='Морская',
            house='80',
            apartment='100',
            created_by=user2
        )
        order2 = Order.objects.create(
            first_name='Мария',
            last_name='Петрова',
            phone='+79997654321',
            email='maria@example.com',
            user=user2,
            address='Приморско-Ахтарский, Морская, д. 80, кв. 100',
            delivery_method='Почта России',
            payment_method='Наличными при получении',
            payment_status='paid',
            status='confirmed',
            total_amount='2780.00'
        )
        product3 = Product.objects.get(name='Корм для хомяков')
        OrderItem.objects.create(
            order=order2,
            product=product3,
            quantity=3,
            price=product3.price
        )
        product4 = Product.objects.get(name='Корм для попугаев')
        OrderItem.objects.create(
            order=order2,
            product=product4,
            quantity=1,
            price=product4.price
        )

        self.stdout.write('Created test orders')

        self.stdout.write(self.style.SUCCESS('Data creation completed successfully!'))
