from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuideViewSet, GuideImageViewSet, guides_view, articles_list_view, article_detail_view, like_article_view, unlike_article_view

app_name = 'guides'

router = DefaultRouter()
router.register(r'guides', GuideViewSet)
router.register(r'guide-images', GuideImageViewSet)

urlpatterns = [
    path('', guides_view, name='guides'),
    path('', include(router.urls)),
    # Статьи
    path('articles/', articles_list_view, name='articles_list'),
    path('articles/<int:article_id>/', article_detail_view, name='article_detail'),
    path('articles/<int:article_id>/like/', like_article_view, name='like_article'),
    path('articles/<int:article_id>/unlike/', unlike_article_view, name='unlike_article'),
]
