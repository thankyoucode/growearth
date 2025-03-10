from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Category, Plant


class ManageCategoryForm(UserCreationForm):
    class Meta:
        model = Category
        # Set all fields that define in model
        # fields = "__all__"
        # Specify fields from model
        fields = ["image", "title", "description", "slug"]


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-primary focus:border-primary placeholder-gray-400",
                "rows": 3,
                "placeholder": "Enter your shipping address",
            }
        )
    )
    billing_address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-primary focus:border-primary placeholder-gray-400",
                "rows": 3,
                "placeholder": "Enter your billing address",
            }
        )
    )
    payment_method = forms.ChoiceField(
        choices=[
            ("COD", "Cash on Delivery"),
            ("CREDIT_CARD", "Credit Card"),
            ("DEBIT_CARD", "Debit Card"),
            ("UPI", "UPI"),
            ("NET_BANKING", "Net Banking"),
        ],
        widget=forms.RadioSelect(attrs={"class": "space-y-2"}),
    )
