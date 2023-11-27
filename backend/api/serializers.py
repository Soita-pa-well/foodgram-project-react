from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.models import CustomUser, Subscription
from recipies.models import Ingredient, IngridientInRecipe, Recipe, Tag


class CustomUserSerializer(UserSerializer):
    """Сериализатор для модели пользователя"""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, author=obj.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя."""

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class PasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


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
        user = self.context.get('request').user
        return (user.favorites.filter(recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return (user.shopping_cart.filter(recipe=obj).exists())
        # request = self.context.get('request')
        # if request is None or request.user.is_anonymous:
        #     return False
        # return ShoppingCart.objects.filter(
        #     user=request.user, recipe_id=obj
        # ).exists()


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
        many=True, source='ingredient_in_recipe')
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'ingredients', 'tags', 'image', 'name',
                  'text', 'cooking_time')

    def validate(self, data):
        ingredients = data['ingredient_in_recipe']
        ingredients_set = set()
        if not ingredients:
            raise serializers.ValidationError(
                'Необходимо добавить ингредиенты!')
        for ingredient in ingredients:
            if ingredient['id'] in ingredients_set:
                raise serializers.ValidationError('У вас повторяются '
                                                  'ингредиенты')
            ingredients_set.add(ingredient['id'])
            amount = ingredient['amount']
            if int(amount) < 1:
                raise serializers.ValidationError('Количество ингредиента не '
                                                  'может быть меньше единицы!')

    def get_ingredients(self, obj):
        ingredients = IngridientInRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(ingredients).data

    def add_recipe_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            IngridientInRecipe.objects.update_or_create(
                recipe=recipe, ingredient=ingredient_id,
                defaults={'amount': amount})

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredient_in_recipe')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        ingredients_in_recipe = []
        for ingredient in ingredients_data:
            id = ingredient.get('id')
            amount = ingredient.get('amount')
            ingredient_instance, created = Ingredient.objects.get_or_create(
                id=id)
            ingredients_in_recipe.append(IngridientInRecipe(
                recipe=recipe,
                ingredient=ingredient_instance,
                amount=amount))
        IngridientInRecipe.objects.bulk_create(ingredients_in_recipe)
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredient_in_recipe')
        new_tags = []
        for item in tags_data:
            tag = get_object_or_404(Tag, id=item.id)
            new_tags.append(tag)
        instance.tags.set(new_tags)
        new_ingredients = []
        for item in ingredients_data:
            amount = item.get('amount')
            ingredient = get_object_or_404(Ingredient, id=item.get('id'))
            new_ingredients.append(
                ingredient
            )
        instance.ingredients.set(
            new_ingredients,
            through_defaults={'amount': amount}
        )

        instance.save()
        return instance


class HelpCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор для создания объекта в
    FavoriteSerializer, SubscriptionSerializer, ShoppingCartSerializer """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSubscriptionSerializer(serializers.ModelSerializer):
    """"Cериализатор подписки на автора"""

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count',)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, author=obj.id).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return HelpCreateSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
