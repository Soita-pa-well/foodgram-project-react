from django.contrib import admin
from .models import CustomUser, Subscription
from constants import EMPTY_VALUE


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    """Модель CustomUser в админке."""

    list_display = ('id', 'username', 'first_name',
                    'last_name', 'email', 'password',)
    list_filter = ('email', 'username',)
    empty_value_display = EMPTY_VALUE


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Модель подписки на автора в админке."""

    list_display = ('user', 'author')
    list_filter = ('user', 'author',)
    empty_value_display = EMPTY_VALUE
