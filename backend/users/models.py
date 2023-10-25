from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from .validators import validate_username
from constants import (EMAIL_MAX_LENGTH, FIRST_NAME_MAX_LENGTH,
                       LAST_NAME_MAX_LENGTH, USERNAME_MAX_LENGTH)


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField('Почта пользователя',
                              max_length=EMAIL_MAX_LENGTH,
                              unique=True)
    first_name = models.CharField('Имя пользователя',
                                  max_length=FIRST_NAME_MAX_LENGTH,
                                  blank=False)
    last_name = models.CharField('Фамилия пользователя',
                                 max_length=LAST_NAME_MAX_LENGTH,
                                 blank=False)
    username = models.CharField('Псевдоним пользователя',
                                max_length=USERNAME_MAX_LENGTH,
                                validators=[validate_username])
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель создания подписки на автора"""

    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             verbose_name='Подписчик',
                             related_name='subscriber')
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               verbose_name='Автор, на которого подписались',
                               related_name='subscribed_author')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            UniqueConstraint(
                    fields=('user', 'author'),
                    name='subscription_user_to_author'
            )
        ]
