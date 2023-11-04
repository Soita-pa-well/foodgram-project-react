from rest_framework import viewsets, status
from recipies.models import Ingredient, Tag, Recipe
from users.models import CustomUser, Subscription
from api.serializers import (IngridientsSerializer, TagSerializer,
                             RecipeCreateSerializer, CustomUserSerializer,
                             RecipeShowSerializer, UserSubscriptionSerializer)
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.decorators import action
from django.http import HttpResponse
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

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


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngridientsSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
