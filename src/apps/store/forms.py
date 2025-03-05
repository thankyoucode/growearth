from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Category, Plant


class ManageCategoryForm(UserCreationForm):
    class Meta:
        model = Category
        # Set all fields that define in model
        # fields = "__all__"
        # Specify fields from model
        fields = ["image", "title", "description", "slug"]
