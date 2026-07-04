from rest_framework import serializers
from .models import SiteInfo


class SiteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteInfo
        fields = ['id', 'key', 'value', 'description']
