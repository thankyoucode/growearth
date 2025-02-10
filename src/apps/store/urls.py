# apps/store/urls.py
from django.urls import path

from . import views

app_name = "store"  # Important for namespacing

urlpatterns = [
    path("plants/", views.plants_view, name="plants"),
    path("collections/", views.collections_view, name="collections"),
    path("care-guide/", views.care_guide_view, name="care_guide"),
    path("catalog/", views.catalog_view, name="catalog"),
]
