from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint

from .managers import UserManager
from .validators import email_validator, validate_username


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField('Почта пользователя',
                              max_length=254,
                              unique=True,
                              validators=[email_validator])
    first_name = models.CharField('Имя пользователя',
                                  max_length=150,
                                  blank=False)
    last_name = models.CharField('Фамилия пользователя',
                                 max_length=150,
                                 blank=False)
    username = models.CharField('Псевдоним пользователя',
                                max_length=150,
                                unique=True,
                                validators=[validate_username])
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

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
                name='subscription_user_on_author'
            )
        ]

    def __str__(self):
        return f'{self.user} подписался на {self.author}'
