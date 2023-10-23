from django.contrib import admin
from .models import (Ingredient, Tag, Recipe, ShoppingCart,
                     Favorite, IngridientInRecipe, RecipeTag)
from constants import EMPTY_VALUE


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

    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name', 'slug')
    empty_value_display = EMPTY_VALUE


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Модель Recipe в админке."""

    list_display = ('name', 'author',
                    'text', 'cooking_time', 'pub_date')
    search_fields = ('name', 'author', 'tags', 'ingridients')
    list_filter = ('author', 'name', 'tags')
    inlines = (IngredientInRecipeInline, RecipeTagInLine)
    empty_value_display = EMPTY_VALUE

    def count_favorites(self, obj):
        return obj.favorites.count()


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
