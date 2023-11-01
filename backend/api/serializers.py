from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from recipies.models import (Ingredient, Tag, Recipe, ShoppingCart, Favorite,
                             IngridientInRecipe, RecipeTag)
from users.models import CustomUser, Subscription
from djoser.serializers import UserCreateSerializer, UserSerializer


class CustomUserSerializer(UserSerializer):
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


class CustomUserCreateSerializer(UserCreateSerializer):
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

    class Meta:
        model = IngridientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeShowSerializer(serializers.ModelSerializer):
    """Cериализатор просмотора рецепта"""

    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(required=False)
    ingredients = IngredientInRecipeSerializer(many=True,
                                               source='ingredient_in_recipe')
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


class IngredientInRecipeCreateSerializer(serializers.ModelSerializer):
    """Cериализатор игредиентов при создании рецепта"""

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Cериализатор создания рецепта"""

    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeCreateSerializer(
        many=True,
        source='ingredient_in_recipe')
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all(),
                                              required=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'ingredients', 'tags', 'image', 'name',
                  'text', 'cooking_time')

    # def create_ingredients(self, ingredients, recipe):
    #     for i in ingredients:
    #         ingredient = Ingredient.objects.get(id=i['id'])
    #         IngridientInRecipe.objects.create(
    #             ingredient=ingredient, recipe=recipe, amount=i['amount']
    #         )

    # def create_tags(self, tags, recipe):
    #     for tag in tags:
    #         RecipeTag.objects.create(recipe=recipe, tag=tag)

    # def create(self, validated_data):
    #     keys = validated_data.keys()
    #     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', keys)
    #     author = self.context.get('request').user
    #     print(author)
    #     ingredients = validated_data.pop('ingredients')
    #     tags = validated_data.pop('tags')
    #     recipe = Recipe.objects.create(author=author, **validated_data)
    #     self.create_ingredients(ingredients, recipe)
    #     self.create_tags(tags, recipe)
    #     return recipe

    def create_ingredients(self, ingredients, recipe):
        for i in ingredients:
            ingredient = Ingredient.objects.get(id=i['id'])
            IngridientInRecipe.objects.create(
                ingredient=ingredient, recipe=recipe, amount=i['amount']
            )

    def create_tags(self, tags, recipe):
        for tag in tags:
            RecipeTag.objects.create(recipe=recipe, tag=tag)

    def create(self, validated_data):
        """
        Создание рецепта.
        Доступно только авторизированному пользователю.
        """

        ingredients = validated_data.pop('ingredient_in_recipe')
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_ingredients(ingredients, recipe)
        self.create_tags(tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        RecipeTag.objects.filter(recipe=instance).delete()
        IngridientInRecipe.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        self.create_ingredients(ingredients, instance)
        self.create_tags(tags, instance)
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        if validated_data.get('image'):
            instance.image = validated_data.pop('image')
        instance.cooking_time = validated_data.pop('cooking_time')
        instance.save()
        return instance


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
