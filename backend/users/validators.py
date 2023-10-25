import re
from django.core.exceptions import ValidationError
from constants import INVALID_SYMBOLS


def validate_username(value):
    banned_chars = ", ".join(set(re.sub(INVALID_SYMBOLS, '', value)))
    if banned_chars:
        raise ValidationError(
            f'Нельзя использовать символы: {banned_chars} в имени')
    if value.lower() == 'me':
        raise ValidationError(
            'Нельзя использовать значение me в имени'
        )
    return value
