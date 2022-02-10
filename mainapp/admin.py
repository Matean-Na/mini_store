from django.contrib import admin
from .models import Product, Category
from django.utils.safestring import mark_safe


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'descriptions', 'is_published', 'get_image', 'numbers')
    ordering = ['id']
    list_display_links = ('id', 'category', 'name')
    search_fields = ('name', 'category', 'is_published')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    prepopulated_fields = {'url': ('name',), }

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="80">')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ['id']
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'url': ('name',), }
