from django.contrib import admin
from .models import Post, Category


@admin.register(Post)
class WriteitAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'photo', 'cat']
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    
