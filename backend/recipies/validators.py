from django.core.exceptions import ValidationError
from constants import MINIMUM_COOKING_TIME


def validate_cooking_time(value):
    if value < MINIMUM_COOKING_TIME:
        raise ValidationError(
            'Время приготовления не может быть меньше минуты'
        )


def validate_minimum_amount(value):
    if value < MINIMUM_AMOUNT:
        raise ValidationError(
            'Количество не может быть меньше единицы'
        )