from django.db import models
from django.conf import settings


class Guide(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    content = models.TextField(verbose_name='Содержание')
    category = models.CharField(max_length=100, verbose_name='Категория')
    is_active = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    
    class Meta:
        verbose_name = 'Гайд'
        verbose_name_plural = 'Гайды'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/guides/{self.slug}/'


class GuideImage(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='images', verbose_name='Гайд')
    image = models.ImageField(upload_to='guides/', verbose_name='Изображение')
    caption = models.CharField(max_length=200, blank=True, verbose_name='Подпись')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    
    class Meta:
        verbose_name = 'Изображение гида'
        verbose_name_plural = 'Изображения гидов'
    
    def __str__(self):
        return f'{self.guide.title} - {self.caption or "Изображение"}'


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст статьи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def like_count(self):
        return self.likes.filter(is_like=True).count()
    
    @property
    def dislike_count(self):
        return self.likes.filter(is_like=False).count()
    
    @property
    def net_rating(self):
        return self.like_count - self.dislike_count


class ArticleInteraction(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes', verbose_name='Статья')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    is_like = models.BooleanField(default=True, verbose_name='Лайк')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    
    class Meta:
        verbose_name = 'Взаимодействие со статьей'
        verbose_name_plural = 'Взаимодействия со статьями'
        unique_together = ['article', 'user']
    
    def __str__(self):
        return f"{'Лайк' if self.is_like else 'Дизлайк'} на статью '{self.article.title}' от {self.user.username}"
