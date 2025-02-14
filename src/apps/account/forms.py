import re

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .._services.email_verify import EmailVerificationService
from .models import CustomUser


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Create Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Create a strong password",
                "class": "grow-earth-input",
            }
        ),
        help_text="Password must be at least 8 characters, contain uppercase & lowercase letters, and include a number and symbol.",
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm your password", "class": "grow-earth-input"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": "Your first name", "class": "grow-earth-input"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Your last name", "class": "grow-earth-input"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Your email address", "class": "grow-earth-input"}
            ),
            "phone_number": forms.TextInput(
                attrs={"placeholder": "Your phone number", "class": "grow-earth-input"}
            ),
            "address": forms.Textarea(
                attrs={"placeholder": "Your address", "class": "grow-earth-input"}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if not self.is_valid_password(password):
            raise ValidationError(
                "Password must be at least 8 characters long, contain both uppercase and lowercase letters, include at least one number, and one special character."
            )
        return password

    def is_valid_password(self, password):
        """
        Check if the password is strong enough.
        """
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):  # Check for uppercase letters
            return False
        if not re.search(r"[a-z]", password):  # Check for lowercase letters
            return False
        if not re.search(r"[0-9]", password):  # Check for numbers
            return False
        if not re.search(
            r"[!@#$%^&*(),.?\":{}|<>]", password
        ):  # Check for special chars
            return False
        return True

    def clean(self):
        self.cleaned_data = super().clean()
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")

        # Email verification after form is cleaned
        if password1 and password2:
            email_verification_service = EmailVerificationService()
            verification_code = email_verification_service.generate_verification_code(
                self.instance.id
            )
            email_verification_service.send_verification_email(
                self.instance, verification_code
            )

        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
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

    class Meta:
        model = CustomUser
        fields = [
            "email",
        ]
        widgets = {
            "email": forms.EmailInput(
                attrs={"placeholder": "Your email address", "class": "grow-earth-input"}
            ),
        }
