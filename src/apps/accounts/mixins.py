import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class GrowEarthFormMixin:
    """
    Custom form styling mixin for Grow Earth platform
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary transition duration-300",
                    "placeholder": field.label,
                }
            )


class PasswordValidationMixin:
    """
    Advanced password validation with Grow Earth specific rules
    """

    def validate_password(self, password):
        """
        Comprehensive password validation
        """
        validation_rules = [
            (lambda p: len(p) >= 8, "Password must be at least 8 characters"),
            (lambda p: re.search(r"[A-Z]", p), "Must contain uppercase letter"),
            (lambda p: re.search(r"[a-z]", p), "Must contain lowercase letter"),
            (lambda p: re.search(r"\d", p), "Must contain a number"),
            (
                lambda p: re.search(r'[!@#$%^&*(),.?":{}|<>]', p),
                "Must contain special character",
            ),
        ]

        for validator, message in validation_rules:
            if not validator(password):
                raise ValidationError(_(message))

        return password
