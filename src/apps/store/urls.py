from django.urls import path

from . import views

app_name = "store"  # Important for namespacing


urlpatterns = [
    path("category", views.categoryes_view, name="categoryes"),
    path(
        "category/plant/<str:slug>/",
        views.category_plants_view,
        name="category_plants",
    ),
    path("category/plant/detail/<uuid:id>/", views.plant_view, name="plant"),
    path("care-guide/", views.care_guide_view, name="care_guide"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/update/<uuid:plant_id>/", views.update_cart_view, name="update_cart"),
    path(
        "cart/remove/<uuid:plant_id>/",
        views.remove_from_cart_view,
        name="remove_from_cart",
    ),
    path("add_to_cart/<uuid:plant_id>/", views.add_to_cart_view, name="add_to_cart"),
    path("checkout/", views.checkout_view, name="checkout"),  # Add checkout URL
    path(
        "order_confirmation/<uuid:order_id>/",
        views.order_confirmation_view,
        name="order_confirmation",
    ),  # Add checkout URL
]
