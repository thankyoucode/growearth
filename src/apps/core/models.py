from django.conf import settings

# models.py
from django.db import models
from django_countries.fields import CountryField


class Contact(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    country = CountryField()  # Store selected country code
    phone = models.CharField(max_length=15, blank=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.email})"
