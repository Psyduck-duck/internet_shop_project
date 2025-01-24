from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'is_published', 'views')
    search_fields = ('title', 'content')
