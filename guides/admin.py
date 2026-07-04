from django.contrib import admin
from .models import Article, ArticleInteraction


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'like_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'content']
    ordering = ['-created_at']
    
    @admin.display(description='Лайки')
    def like_count(self, obj):
        return obj.like_count


@admin.register(ArticleInteraction)
class ArticleInteractionAdmin(admin.ModelAdmin):
    list_display = ['article', 'user', 'is_like', 'created_at']
    list_filter = ['is_like', 'created_at', 'article', 'user']
    search_fields = ['article__title', 'user__username']
    list_select_related = ['article', 'user']
