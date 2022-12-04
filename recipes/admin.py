from django.contrib import admin

from .models import Category, Recipe

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'author', 'is_published']
    list_display_links = ['id', 'title', 'created_at']
    search_fields = ['id', 'title', 'slug', 'description', 'preparation_steps']
    list_filter = ['category', 'author',
                   'is_published', 'preparation_steps_is_html']
    list_per_page = 10
    list_editable = ['is_published', 'author']
    ordering = ['-id']


admin.site.register(Category, CategoryAdmin)
