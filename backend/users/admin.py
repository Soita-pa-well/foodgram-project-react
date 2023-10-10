from django.contrib import admin
from .models import CustomUser
from constants import EMPTY_VALUE


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    """Модель CustomUser в админке."""
    list_display = ('id', 'username', 'first_name',
                    'last_name', 'email', 'password')
    list_filter = ('email', 'username', )
    empty_value_display = EMPTY_VALUE
