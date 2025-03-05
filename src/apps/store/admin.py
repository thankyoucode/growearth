from django.contrib import admin

# Register your models here.
from .models import Category, Plant, Tag

# Register your models here.
admin.site.register((Category, Plant, Tag))
