from constants import DEJAVUSANS_PATH
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipies.models import (Favorite, Ingredient, IngridientInRecipe, Recipe,
                             ShoppingCart, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from users.models import CustomUser, Subscription

from api.serializers import (CustomUserSerializer, HelpCreateSerializer,
                             IngridientsSerializer, PasswordSerializer,
                             RecipeCreateSerializer, RecipeShowSerializer,
                             TagSerializer, UserSubscriptionSerializer)

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsOwnerOrAdminOrReadOnly

pdfmetrics.registerFont(TTFont('DejaVuSans', DEJAVUSANS_PATH))


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = CustomUser.objects.get(username=request.user.username)
        serializer = CustomUserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = CustomUser.objects.filter(
            subscribed_author__user=request.user)
        if queryset:
            pages = self.paginate_queryset(queryset)
            serializer = UserSubscriptionSerializer(pages, many=True,
                                                    context={'request':
                                                             request})
            return self.get_paginated_response(serializer.data)
        return Response('У вас нет подписок',
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, pk):
        user = self.request.user
        author = get_object_or_404(CustomUser, id=pk)
        subscription = Subscription.objects.filter(user=user.id,
                                                   author=author.id)
        if request.method == 'POST':
            if user == author:
                return Response('Невозможно подписаться на самого себя',
                                status=status.HTTP_400_BAD_REQUEST)
            if subscription:
                return Response(f'Вы уже подписаны на {author}',
                                status=status.HTTP_400_BAD_REQUEST)
            subscribe = Subscription.objects.create(
                user=user,
                author=author
            )
            subscribe.save()
            return Response(f'Вы подписались на {author}',
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if subscription:
                subscription.delete()
                return Response(f'Вы отменили подписку на {author}',
                                status=status.HTTP_204_NO_CONTENT)
            return Response(f'Вы не можете отменить подписку на {author},'
                            f'потому что не подписаны на него',
                            status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=(IsAuthenticated,)
    )
    def set_password(self, request, pk=None):
        user = self.request.user
        serializer = PasswordSerializer(data=request.data,
                                        context={'request': request})
        if serializer.is_valid(raise_exception=True):
            new_password = serializer.data['new_password']
            if user.check_password(new_password):
                return Response(data='Новый пароль не должен совпадать с '
                                'предыдущим',
                                status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response(data='Пароль изменен',
                            status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngridientsSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = IngredientFilter
    search_fields = ('name',)
    pagination_class = None


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('author')
    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = PageNumberPagination

    def get_queryset(self):
        qs = super().get_queryset()
        if 'is_favorited' in self.request.query_params:
            qs = qs.filter(favorites__user=self.request.user)
        if 'is_in_shopping_cart' in self.request.query_params:
            qs = qs.filter(shopping_cart__user=self.request.user)
        return qs

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return RecipeCreateSerializer
        return RecipeShowSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            favorite, created = Favorite.objects.get_or_create(
                user=user, recipe=recipe)
            if created:
                serializer = HelpCreateSerializer(favorite.recipe)
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            favorites = Favorite.objects.filter(user=user, recipe=recipe)
            if favorites:
                favorites.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                data = {'errors': 'Такого рецепта нет в избранных.'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            shopping_cart, created = ShoppingCart.objects.get_or_create(
                user=user, recipe=recipe)
            if created:
                serializer = HelpCreateSerializer(shopping_cart.recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(data='Рецепт уже добавлен в корзину',
                                status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            shopping_cart = ShoppingCart.objects.filter(user=user,
                                                        recipe=recipe)
            if shopping_cart.exists():
                shopping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(data='Этого рецепта нет в списке покупок',
                                status=status.HTTP_404_NOT_FOUND)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        self.response = HttpResponse(content_type='application/pdf')
        self.response[
            'Content-Disposition'] = 'attachment; filename="my_recipes.pdf"'
        queryset = IngridientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user)
        ingredients_dict = {}
        for item in queryset:
            if item.ingredient not in ingredients_dict:
                ingredients_dict[item.ingredient] = (
                    item.ingredient.measurement_unit, item.amount)
            else:
                current_unit, current_amount = ingredients_dict[
                    item.ingredient]
                ingredients_dict[item.ingredient] = (
                    current_unit, current_amount + item.amount)

        ingredients_list = []
        ingredients_list.append(['Ингредиент',
                                 'Единицы изменения',
                                 'Количество'])

        for ing, (unit, amount) in ingredients_dict.items():
            ingredients_list.append([ing, unit, amount])
        style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans')
        ])
        table = Table(ingredients_list, style=style)
        doc = SimpleDocTemplate(self.response)
        doc.build([table])
        return self.response
