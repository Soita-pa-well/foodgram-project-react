from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from recipies.models import (Ingredient, Tag, Recipe, ShoppingCart, Favorite,
                             IngridientInRecipe)
from users.models import CustomUser, Subscription


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            item = Subscription.objects.filter(user=request.user,
                                               author=obj).exists()
            return item
        return False


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя."""

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


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
    amount = serializers.ReadOnlyField()

    class Meta:
        model = IngridientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Cериализатор просмотора рецепта"""

    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(required=False)
    ingredients = IngredientInRecipeSerializer(
        many=True,
        source='ingredient_in_recipe'
    )
    # ingredients = IngredientInRecipeSerializer(many=True, required=False)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if (user.is_authenticated and
                Favorite.objects.filter(user=user, recipe=obj).exists()):
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if (user.is_authenticated and
                ShoppingCart.objects.filter(user=user, recipe=obj).exists()):
            return True
        return False


class SubscriptionsRecipeSerializer(serializers.ModelSerializer):
    """Cериализатор рецепта в модели подписки на автора"""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSubscriptionSerializer(serializers.ModelSerializer):
    """"Cериализатор подписки на автора"""

    is_subscribed = serializers.SerializerMethodField()
    recipes = SubscriptionsRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if (user.is_authenticated
                and user.subscribers.filter(author=obj,).exists()):
            return True
        return False

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
