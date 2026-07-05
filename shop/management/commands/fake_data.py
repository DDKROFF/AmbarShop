from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shop.models import Category, Product, ProductImage
from account.models import Review
import os
import random
from django.conf import settings

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет базу данных фейковыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Очищаем старые данные...'))
        Review.objects.all().delete()
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(is_staff=False).delete()
        self.stdout.write(self.style.SUCCESS('Старые данные удалены'))
        
        categories_data = [
            {'name': 'Корм для домашних животных', 'slug': 'korm-dlya-domashnih-zhivotnyh', 'description': 'Вкусный и полезный корм для ваших домашних питомцев'},
            {'name': 'Корм для с/х животных', 'slug': 'korm-dlya-selkhoz-zhivotnyh', 'description': 'Комбикорм и гранулы для скота и поголовья'},
            {'name': 'Аксессуары для животных', 'slug': 'aksessuary-dlya-zhivotnyh', 'description': 'Все необходимое для содержания и ухода за животными'},
            {'name': 'Птица', 'slug': 'ptitsa', 'description': 'Суточные цыплята, утята и гусята от проверенного инкубатора'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'], defaults={'name': cat_data['name'], 'description': cat_data['description']}
            )
            self.stdout.write(self.style.SUCCESS(f'Категория "{category.name}" готова'))

        categories = Category.objects.all()

        products_data = [
            {'name': 'Премиум корм для кошек', 'slug': 'premium-korm-dlya-koshek', 'description': 'Высококачественный премиум корм для взрослых кошек. Содержит все необходимые витамины и минералы для поддержания здорового состояния шерсти и пищеварения. Производится по европейским стандартам.', 'price': 850.00, 'stock': 50, 'category': categories[0]},
            {'name': 'Корм для собак всех пород', 'slug': 'korm-dlya-sobak-vseh-porod', 'description': 'Сбалансированный корм для собак всех пород и возрастов. Формула разработана ветеринарами с учетом всех потребностей собак. Содержит мясо, злаки и натуральные добавки.', 'price': 720.00, 'stock': 30, 'category': categories[0]},
            {'name': 'Корм для хомяков и грызунов', 'slug': 'korm-dlya-khomyakov-i-gryzunov', 'description': 'Специализированный корм для хомяков, морских свинок и других грызунов. Содержит семена, злаки и натуральные добавки для здоровой зубной эмали.', 'price': 350.00, 'stock': 100, 'category': categories[0]},
            {'name': 'Корм для попугаев', 'slug': 'korm-dlya-popugaei', 'description': 'Смесь семян и орехов для экзотических птиц. Богата витаминами A, D, E и другими полезными веществами для яркости оперения и здоровья.', 'price': 420.00, 'stock': 45, 'category': categories[0]},
            {'name': 'Комбикорм для коров', 'slug': 'kombikorm-dlya-korov', 'description': 'Сбалансированный комбикорм для дойных и сухостойных коров. Содержит белки, углеводы, витамины и минералы для максимальной продуктивности.', 'price': 1500.00, 'stock': 200, 'category': categories[1]},
            {'name': 'Гранулы для прудовых рыб', 'slug': 'granuly-dlya-prudovyh-ryb', 'description': 'Питательные гранулы для прудовых рыб. Плавающие гранулы сбалансированным составом для быстрого роста и здорового развития.', 'price': 680.00, 'stock': 80, 'category': categories[1]},
            {'name': 'Корм для свиней', 'slug': 'korm-dlya-svinei', 'description': 'Полноценный рацион для свиней на откорме. Содержит все необходимые питательные вещества для интенсивного роста и набора массы.', 'price': 1250.00, 'stock': 150, 'category': categories[1]},
            {'name': 'Отруби пшеничные', 'slug': 'otrubi-pshenichnye', 'description': 'Качественные пшеничные отруби для кормления скота. Богаты клетчаткой и благоприятно влияют на пищеварение животных.', 'price': 450.00, 'stock': 300, 'category': categories[1]},
            {'name': 'Кормушка для кур', 'slug': 'kormushka-dlya-kur', 'description': 'Надежная пластиковая кормушка для кур несушек. Объем 5 литров, легко крепится к клетке. Удобная система подачи корма.', 'price': 1200.00, 'stock': 25, 'category': categories[2]},
            {'name': 'Автопоилка для птицы', 'slug': 'avtopoilka-dlya-ptitsy', 'description': 'Система автопоения для кур и уток. Объем 3 литра, герметичная конструкция. Обеспечивает постоянный доступ к свежей воде.', 'price': 1800.00, 'stock': 20, 'category': categories[2]},
            {'name': 'Клетка для хомяков', 'slug': 'kletka-dlya-khomyakov', 'description': 'Просторная клетка для хомяков и мелких грызунов. Две уровня, лестницы и домик. Пластиковое дно для легкой уборки.', 'price': 2500.00, 'stock': 15, 'category': categories[2]},
            {'name': 'Лоток для котов', 'slug': 'lotok-dlya-kotov', 'description': 'Угловой лоток для котов с высокими бортиками. Пластиковый материал с антицарапинным покрытием. Удобная ручка для переноски.', 'price': 800.00, 'stock': 40, 'category': categories[2]},
            {'name': 'Суточные цыплята куры', 'slug': 'sutochnye-tsiplyata-kury', 'description': 'Суточные цыплята куры-несушки. Привиты от основных заболеваний. Здоровые и активные птенцы от проверенного инкубатора. Готовы к выращиванию.', 'price': 150.00, 'stock': 100, 'category': categories[3]},
            {'name': 'Суточные утята', 'slug': 'sutochnye-utyata', 'description': 'Суточные утята породы мускусные. Привиты и готовы к выращиванию. Здоровые птенцы от проверенного производителя.', 'price': 200.00, 'stock': 50, 'category': categories[3]},
            {'name': 'Суточные гусята', 'slug': 'sutochnye-gusyata', 'description': 'Суточные гусята. Привиты от гепатита и сальмонеллеза. Сильные и активные птенцы, готовые к выращиванию на пастбище.', 'price': 250.00, 'stock': 30, 'category': categories[3]},
            {'name': 'Цыплята бройлеры', 'slug': 'tsyplyata-broyler', 'description': 'Суточные цыплята бройлеры для откорма. Быстрорастущая порода, отличная мясная продуктивность. Привиты от всех стандартных заболеваний.', 'price': 180.00, 'stock': 80, 'category': categories[3]},
        ]

        for product_data in products_data:
            product = Product.objects.create(**product_data)
            self.add_product_image(product, product_data['name'])
            # Создаем пользователя с email как идентификатором
            first_names = ['Иван', 'Мария', 'Петр', 'Анна', 'Сергей', 'Елена', 'Алексей', 'Ольга', 'Дмитрий', 'Татьяна']
            last_names = ['Иванов', 'Петрова', 'Сидоров', 'Кузнецова', 'Смирнов', 'Попова', 'Васильев', 'Михайлова', 'Макаров', 'Николаева']
            middle_names = ['Иванович', 'Петровна', 'Сидорович', 'Андреевна', 'Сергеевич', 'Владимировна', 'Алексеевич', 'Сергеевна', 'Дмитриевич', 'Фёдоровна']
            
            user, _ = User.objects.get_or_create(
                email=f'user{product.id}@example.com',
                defaults={
                    'first_name': first_names[product.id % len(first_names)],
                    'last_name': last_names[product.id % len(last_names)],
                    'middle_name': middle_names[product.id % len(middle_names)],
                    'phone': f'+7 (900) 000-00-{str(product.id).zfill(2)}',
                }
            )
            self.create_review(user, product)
            self.stdout.write(self.style.SUCCESS(f'Товар "{product.name}" готов'))

        products = Product.objects.all().order_by('id')
        popular_count = 0
        for product in products:
            if popular_count < 6:
                product.popular = True
                product.is_active = True
                product.save()
                popular_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Помечено {popular_count} товаров как популярные'))
        self.stdout.write(self.style.SUCCESS(f'\nСоздано {Product.objects.count()} товаров'))
        self.stdout.write(self.style.SUCCESS(f'Создано {Category.objects.count()} категорий'))
        self.stdout.write(self.style.SUCCESS(f'Создано {Review.objects.count()} отзывов'))

    def add_product_image(self, product, name):
        image_mappings = {
            'кошки': 'Karmy_cat.png', 'собак': 'All_dogs.png', 'хомяков': 'Karmy_cat.png',
            'попугаев': 'Karmy_cat.png', 'комбикорм': 'All_dogs.png', 'гранулы': 'All_dogs.png',
            'свиней': 'All_dogs.png', 'отруби': 'All_dogs.png', 'кормушка': 'Bag.png',
            'автопоилка': 'Bag.png', 'клетка': 'Bag.png', 'лоток': 'Bag.png',
            'цыплята': 'Ug_korona.png', 'утята': 'Ug_korona.png', 'гусята': 'Ug_korona.png',
            'бройлеры': 'Ug_korona.png',
        }
        for key, image_file in image_mappings.items():
            if key.lower() in name.lower():
                static_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', image_file)
                if os.path.exists(static_image_path):
                    from django.core.files.base import ContentFile
                    with open(static_image_path, 'rb') as f:
                        content_file = ContentFile(f.read())
                        product_image = ProductImage(product=product, is_main=True)
                        product_image.image.save(image_file, content_file, save=True)
                    self.stdout.write(f'  Изображение {image_file} добавлено')
                    break
        else:
            self.stdout.write(f'  Внимание: для товара {product.name} не найдено изображение')

    def create_review(self, user, product):
        Review.objects.create(user=user, title='Отличный товар!', comment='Качество на высоте', rating=5, is_moderated=True)
