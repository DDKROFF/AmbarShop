from django.contrib import admin
from .models import SiteInfo


@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ['key', 'description']
    search_fields = ['key', 'value', 'description']
