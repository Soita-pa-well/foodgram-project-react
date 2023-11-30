import re

from constants import INVALID_SYMBOLS
from django.core.exceptions import ValidationError


def get_banned_chars(chars, value):
    return ", ".join(set(re.sub(chars, '', value)))


def validate_username(value):
    banned_chars = get_banned_chars(INVALID_SYMBOLS, value)
    if banned_chars:
        raise ValidationError(
            f'Нельзя использовать символы: {banned_chars} в имени')
    if value.lower() == 'me':
        raise ValidationError(
            'Нельзя использовать значение me в имени'
        )
    return value


def email_validator(value):
    banned_chars = get_banned_chars(INVALID_SYMBOLS, value)
    if banned_chars:
        raise ValidationError(
            f'Нельзя использовать символы: {banned_chars} в адресе почты')
    return value
