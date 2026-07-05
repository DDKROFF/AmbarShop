from django.core.management.base import BaseCommand
from shop.models import Product, ProductImage
from django.core.files.base import ContentFile
import os
import shutil


class Command(BaseCommand):
    help = 'Создает фейковые изображения для товаров'

    def handle(self, *args, **kwargs):
        # Список изображений для каждого товара
        image_mapping = {
            # Корм для домашних животных
            'premium-korm-dlya-koshek': 'Karmy_cat.png',
            'korm-dlya-sobak-vseh-porod': 'All_dogs.png',
            'korm-dlya-khomyakov-i-gryzunov': 'Karmy_cat.png',
            'korm-dlya-popugaei': 'Karmy_cat.png',
            # Корм для сельскохозяйственных животных
            'kombikorm-dlya-korov': 'All_dogs.png',
            'granuly-dlya-prudovyh-ryb': 'All_dogs.png',
            'korm-dlya-svinei': 'All_dogs.png',
            'otrubi-pshenichnye': 'All_dogs.png',
            # Аксессуары
            'kormushka-dlya-kur': 'Bag.png',
            'avtopoilka-dlya-ptitsy': 'Bag.png',
            'клетка-для-хомяков': 'Bag.png',
            'lotok-dlya-kotov': 'Bag.png',
            # Птица
            'sutochnye-tsiplyata-kury': 'Ug_korona.png',
            'sutochnye-utyata': 'Ug_korona.png',
            'sutochnye-gusyata': 'Ug_korona.png',
            'tsyplyata-broyjlerы': 'Ug_korona.png',
        }
        
        base_path = 'C:/Users/DDKROFF/Documents/Сайт проекты/AmbarShop'
        
        for slug, image_name in image_mapping.items():
            try:
                product = Product.objects.get(slug=slug)
                
                # Путь к исходному изображению
                src_path = os.path.join(base_path, 'static/images', image_name)
                
                if not os.path.exists(src_path):
                    self.stdout.write(self.style.WARNING(f'Изображение "{image_name}" не найдено по пути "{src_path}"'))
                    # Создаем пустое изображение
                    product_image = ProductImage(product=product, is_main=True)
                    product_image.save()
                    continue
                
                # Копируем изображение
                with open(src_path, 'rb') as f:
                    image_content = ContentFile(f.read())
                
                # Создаем запись изображения
                product_image = ProductImage(product=product, is_main=True)
                product_image.image.save(image_name, image_content, save=True)
                
                self.stdout.write(self.style.SUCCESS(f'Изображение добавлено для "{product.name}"'))
            except Product.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Товар с slug "{slug}" не найден'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка для "{slug}": {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('\nВсе изображения успешно созданы!'))
