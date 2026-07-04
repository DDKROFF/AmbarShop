from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Guide, GuideImage, Article, ArticleInteraction
from .serializers import GuideSerializer, GuideImageSerializer, ArticleSerializer, ArticleInteractionSerializer


class GuideViewSet(viewsets.ModelViewSet):
    queryset = Guide.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = GuideSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class GuideImageViewSet(viewsets.ModelViewSet):
    queryset = GuideImage.objects.all()
    serializer_class = GuideImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ArticleInteractionViewSet(viewsets.ModelViewSet):
    queryset = ArticleInteraction.objects.all()
    serializer_class = ArticleInteractionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


def guides_view(request):
    """Страница гайдов - отображает список статей"""
    articles = Article.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'guides/guides.html', {
        'articles': articles,
    })


def articles_list_view(request):
    """Список статей"""
    query = request.GET.get('q', '').strip()
    
    if query:
        articles = Article.objects.filter(
            is_active=True,
            title__icontains=query
        ).order_by('-created_at')
    else:
        articles = Article.objects.filter(is_active=True).order_by('-created_at')
    
    return render(request, 'guides/articles_list.html', {
        'articles': articles,
        'query': query,
    })


def article_detail_view(request, article_id):
    """Детальная страница статьи"""
    article = get_object_or_404(Article, id=article_id, is_active=True)
    
    # Получаем взаимодействие пользователя со статьей
    user_interaction = None
    if request.user.is_authenticated:
        try:
            user_interaction = ArticleInteraction.objects.get(
                article=article,
                user=request.user
            )
        except ArticleInteraction.DoesNotExist:
            user_interaction = None
    
    return render(request, 'guides/article_detail.html', {
        'article': article,
        'user_interaction': user_interaction,
    })


@login_required
def like_article_view(request, article_id):
    """Лайк/дизлайк статьи"""
    if request.method == 'POST':
        article = get_object_or_404(Article, id=article_id, is_active=True)
        
        # Получаем или создаем взаимодействие
        interaction, created = ArticleInteraction.objects.get_or_create(
            article=article,
            user=request.user,
            defaults={'is_like': True}
        )
        
        if not created:
            # Если взаимодействие уже существует, переключаем состояние
            if interaction.is_like:
                # Уже лайкнул - убираем лайк (только дизлайк)
                interaction.delete()
                return JsonResponse({'success': True, 'action': 'unliked'})
            else:
                # Уже дизлайкнул - меняем на лайк
                interaction.is_like = True
                interaction.save()
                return JsonResponse({'success': True, 'action': 'liked'})
        else:
            return JsonResponse({'success': True, 'action': 'liked'})
    
    return JsonResponse({'success': False})


@login_required
def unlike_article_view(request, article_id):
    """Удаление лайка"""
    if request.method == 'POST':
        article = get_object_or_404(Article, id=article_id, is_active=True)
        
        try:
            interaction = ArticleInteraction.objects.get(
                article=article,
                user=request.user
            )
            interaction.delete()
            return JsonResponse({'success': True, 'action': 'unliked'})
        except ArticleInteraction.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Взаимодействие не найдено'})
    
    return JsonResponse({'success': False})

