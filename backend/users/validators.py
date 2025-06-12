from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_username(value):
    """Validate username format."""
    if value.lower() == 'me':
        raise ValidationError(
            _('Username "me" is not allowed.'),
            params={'value': value},
        )
    if not value.isalnum():
        raise ValidationError(
            _('Username must contain only letters and numbers.'),
            params={'value': value},
        )
    return value


def validate_first_name(value):
    """Validate first name format."""
    if not value.isalpha():
        raise ValidationError(
            _('First name must contain only letters.'),
            params={'value': value},
        )
    return value


def validate_last_name(value):
    """Validate last name format."""
    if not value.isalpha():
        raise ValidationError(
            _('Last name must contain only letters.'),
            params={'value': value},
        )
    return value 