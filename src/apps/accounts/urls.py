# apps/accounts/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"


urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # django login and logout for use
    # path("login/", auth_views.LoginView.as_view(), name="login"),
    # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
