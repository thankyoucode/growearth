# apps/account/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "account"


urlpatterns = [
    # path("register/", views.register_view, name="register"),
    # path("login/", views.login_view, name="login"),
    path("register/", views.direct_register_view, name="register"),
    path("login/", views.direct_login_view, name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("logout/", views.logout_view, name="logout"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
]
