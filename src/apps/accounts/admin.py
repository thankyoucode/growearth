from django.contrib import admin

from .models import CustomUser, UserOpinion

# Register your models here.
admin.site.register((CustomUser, UserOpinion))
