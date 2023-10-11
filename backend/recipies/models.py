from django.db import models
from users.models import CustomUser
from django.db.models import UniqueConstraint
from constants import (INGRIDIENT_MAX_LENHTH, MEAS_UNIT_MAX_LENHTH,
                       TAG_NAME_MAX_LENGTH, COLOR_MAX_LENGTH, SLUG_MAX_LENGTH,
                       RECIPE_MAX_LENGTH)
from validators import validate_cooking_time, validate_minimum_amount


class Ingredient(models.Model):
    """Модель ингредиента"""

    name = models.CharField('Название ингредиента',
                            max_length=INGRIDIENT_MAX_LENHTH)
    measurement_unit = models.CharField('Единицы измерения',
                                        max_length=MEAS_UNIT_MAX_LENHTH)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='ingredient_name_measurement_unit'
            )
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тега"""

    name = models.CharField('Название тега',
                            max_length=TAG_NAME_MAX_LENGTH,
                            unique=True,)
    color = models.CharField('Цвет',
                             max_length=COLOR_MAX_LENGTH,
                             unique=True,)
    slug = models.SlugField('Cлаг',
                            max_length=SLUG_MAX_LENGTH,
                            unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта"""
    tags = models.ManyToManyField(Tag,
                                  through='RecipeTag',
                                  related_name='tags',
                                  verbose_name='Теги',)
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор рецепта')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngridientInRecipe',
                                         verbose_name='Ингредиенты')
    image = models.ImageField('Изображение рецепта',
                              upload_to='recipies/images/')
    name = models.CharField('Название рецепта',
                            max_length=RECIPE_MAX_LENGTH)
    text = models.TextField('Описание рецепта')
    cooking_time = models.IntegerField(blank=False,
                                       validators=[validate_cooking_time])
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class IngridientInRecipe(models.Model):
    """Модель для связи ингредиента и рецепта."""

    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   verbose_name='Ингредиент')
    amount = models.IntegerField('Количество',
                                 validators=[validate_minimum_amount])

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_ingredient'
            )
        ]


class RecipeTag(models.Model):
    """Модель для связи тега и рецепта."""

    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт')
    tag = models.ForeignKey(Tag,
                            on_delete=models.CASCADE,
                            verbose_name='Тег')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'tag'],
                name='recipe_tag'
            )
        ]


class ShoppingCart(models.Model):
    """Модель корзины."""

    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='shopping_cart',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='shopping_cart',
                               verbose_name='Рецепт')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='user_recipe_cart'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил в корзину {self.recipe}'


class Favorite(models.Model):
    """Модель добавления рецепта в избранное."""

    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='favorites',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favorites',
                               verbose_name='Рецепт')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='user_recipe_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в избранное'
