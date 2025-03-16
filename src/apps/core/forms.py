from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        error_messages={"required": "Please enter your name."},
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-green-500"
            }
        ),
    )

    email = forms.EmailField(
        required=True,
        error_messages={"required": "Please enter your email address."},
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-green-500"
            }
        ),
    )

    # Dropdown for selecting country code
    country = CountryField(blank_label="(Select Country)").formfield(
        widget=CountrySelectWidget(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-green-500"
            }
        )
    )

    phone = forms.CharField(
        max_length=15,
        required=False,
        error_messages={"max_length": "Phone number cannot exceed 15 digits."},
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-green-500",
                "placeholder": "+91 XXXXXXXXXX (Optional)",
            }
        ),
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-green-500",
                "rows": 5,
                "placeholder": "Tell us how we can help you",
            }
        ),
        required=True,
        error_messages={"required": "Please enter your message."},
    )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone
