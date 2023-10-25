from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from recipies.models import (Ingredient, Tag, Recipe, ShoppingCart, Favorite,
                             IngridientInRecipe)
from users.models import CustomUser, Subscription


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели  пользователя"""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated and request is not None:
            item = Subscription.objects.filter(user=request.user,
                                               author=obj).exists()
            return item
        return False


class IngridientsSerializer(serializers.ModelSerializer):
    """Сериализатор модели ингредиента"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели тега"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели рецепта"""
    
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngridientsSerializer(many=True, read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            item = Favorite.objects.filter(user=user, recipe=obj).exists()
            return item
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(
            shopping_cart__user=user,
            id=obj.id
        ).exists()


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор модели корзины покупок"""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели избранного"""

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели связи ингредиента в рецепте"""

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngridientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
