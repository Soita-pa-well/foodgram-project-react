from constants import EMPTY_VALUE
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import (Favorite, Ingredient, IngridientInRecipe, Recipe,
                     RecipeTag, ShoppingCart, Tag)


class IngredientInRecipeInline(admin.TabularInline):
    """Модель для добавления ингридиентов в рецепт в админке"""
    model = IngridientInRecipe


class RecipeTagInLine(admin.TabularInline):
    """Модель для добавления тегов в рецепт в админке"""
    model = RecipeTag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Модель Ingredient в админке."""

    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    inlines = (IngredientInRecipeInline,)
    empty_value_display = EMPTY_VALUE


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Модель Tag в админке."""

    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name', 'slug')
    empty_value_display = EMPTY_VALUE


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Модель Recipe в админке."""

    list_display = ('name', 'author', 'text', 'cooking_time',
                    'pub_date', 'count_favorites')
    search_fields = ('name', 'author', 'tags', 'ingridients')
    list_filter = ('author', 'name', 'tags')
    inlines = (IngredientInRecipeInline, RecipeTagInLine)
    empty_value_display = EMPTY_VALUE

    @admin.display(description='Favorites Count')
    def count_favorites(self, obj):
        favorites_count = obj.favorites.count()
        url = reverse('admin:foodgram_recipe', args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, favorites_count)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Модель ShoppindCart в админке."""

    list_display = ('user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = EMPTY_VALUE


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Модель Favorite в админке."""

    list_display = ('user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = EMPTY_VALUE
