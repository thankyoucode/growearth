# apps/accounts/urls.py
from django.urls import path

from . import views

app_name = "accounts"


urlpatterns = [
    # path("register/", views.register_view, name="register"),
    # path("login/", views.login_view, name="login"),
    path("register/", views.direct_register_view, name="register"),
    path("login/", views.direct_login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile_view, name="edit_profile"),
    path("profile/delete_account/", views.delete_account_view, name="delete_account"),
    path("reviews/", views.review_list, name="review_list"),
    path("submit_opinion/", views.submit_opinion, name="submit_opinion"),
]
