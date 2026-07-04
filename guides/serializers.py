from rest_framework import serializers
from .models import Guide, GuideImage, Article, ArticleInteraction


class GuideImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideImage
        fields = ['id', 'image', 'caption']


class GuideSerializer(serializers.ModelSerializer):
    images = GuideImageSerializer(many=True, read_only=True)

    class Meta:
        model = Guide
        fields = ['id', 'title', 'slug', 'content', 'category', 'is_active', 'images', 'created_at', 'updated_at']


class ArticleSerializer(serializers.ModelSerializer):
    like_count = serializers.ReadOnlyField()
    dislike_count = serializers.ReadOnlyField()
    net_rating = serializers.ReadOnlyField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'is_active', 'like_count', 'dislike_count', 'net_rating']


class ArticleInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleInteraction
        fields = ['id', 'article', 'user', 'is_like', 'created_at']
        read_only_fields = ['user', 'created_at']
