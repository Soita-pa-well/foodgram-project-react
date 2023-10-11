from django.contrib import admin
from models import Ingredient, Tag, Recipe, ShoppingCart, Favorite
from constants import EMPTY_VALUE


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Модель Ingredient в админке."""

    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    # inlines = (IngredientRecipeInline,)
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

    list_display = ('name', 'tags', 'author', 'ingridients',
                    'text', 'cooking_time', 'pub_date')
    search_fields = ('name', 'author', 'tags', 'ingridients')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = EMPTY_VALUE


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
