from colorfield.fields import ColorField
from django.db import models
from django.db.models import UniqueConstraint
from users.models import CustomUser

from .validators import validate_cooking_time, validate_minimum_amount


class Ingredient(models.Model):
    """Модель ингредиента"""

    name = models.CharField('Название ингредиента',
                            max_length=200)
    measurement_unit = models.CharField('Единицы измерения',
                                        max_length=20)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['id']
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
                            max_length=200,
                            unique=True,)
    color = ColorField(unique=True,
                       verbose_name='Цвет тега')
    slug = models.SlugField('Cлаг',
                            max_length=200,
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
                                  verbose_name='Теги')
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               verbose_name='Автор рецепта')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngridientInRecipe',
                                         verbose_name='Ингредиенты')
    image = models.ImageField('Изображение рецепта',
                              upload_to='recipies/images/',
                              null=True)
    name = models.CharField('Название рецепта',
                            max_length=200)
    text = models.TextField('Описание рецепта')
    cooking_time = models.IntegerField('Время приготовления рецепта',
                                       blank=False,
                                       validators=[validate_cooking_time])
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']
        default_related_name = 'recipes'

    def __str__(self):
        return self.name


class IngridientInRecipe(models.Model):
    """Модель для связи ингредиента и рецепта."""

    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='ingredients_in_recipe')
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   verbose_name='Ингредиент',
                                   related_name='ingredients_in_recipe')
    amount = models.IntegerField('Количество',
                                 validators=[validate_minimum_amount])

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='ingredient_in_recipe'
            )]


class RecipeTag(models.Model):
    """Модель для связи тега и рецепта."""

    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe_tags',
                               verbose_name='Рецепт')
    tag = models.ForeignKey(Tag,
                            on_delete=models.CASCADE,
                            related_name='recipe_tags',
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
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
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
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='user_recipe_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в избранное'
