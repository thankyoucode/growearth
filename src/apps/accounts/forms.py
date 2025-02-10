import re

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .._services.verify_email import EmailVerificationService

User = get_user_model()


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


class UserRegistrationForm(
    GrowEarthFormMixin, PasswordValidationMixin, forms.ModelForm
):
    password1 = forms.CharField(
        label=_("Create Password"),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Create a strong password",
                "class": "grow-earth-input",
            }
        ),
        help_text=_(
            "Password must:\n"
            "- Be at least 8 characters\n"
            "- Contain uppercase & lowercase\n"
            "- Include a number and symbol"
        ),
    )

    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm your password", "class": "grow-earth-input"}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Choose a unique username",
                    "class": "grow-earth-input",
                }
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Your email address", "class": "grow-earth-input"}
            ),
            "first_name": forms.TextInput(
                attrs={"placeholder": "Your first name", "class": "grow-earth-input"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Your last name", "class": "grow-earth-input"}
            ),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError(_("Username is already taken"))
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")

        # Email Validation Service Integration
        validation_result = EmailVerificationService.validate_email(email)

        # Check email validity
        if not validation_result["is_valid"]:
            raise ValidationError(_("Invalid email address"))

        # Check for disposable email
        if validation_result.get("is_disposable"):
            raise ValidationError(_("Disposable emails are not allowed"))

        # Check email uniqueness
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Email is already registered"))

        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords do not match"))

        if password1:
            self.validate_password(password1)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True

        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "you@example.com",
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter your password",
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md",
            }
        )
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        # Authentication
        if email and password:
            user = authenticate(email=email, password=password)

            if not user:
                raise forms.ValidationError(_("Invalid login credentials"))

            if not user.is_active:
                raise forms.ValidationError(_("This account is not active"))

        return self.cleaned_data
