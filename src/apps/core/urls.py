# apps/core/urls.py
from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
    path("impact/", views.impact_view, name="impact"),
    path("mission/", views.mission_view, name="mission"),
    path("shipping/", views.shipping_view, name="shipping"),
    path("returns/", views.returns_view, name="returns"),
    path("consultation/", views.consultation_view, name="consultation"),
    path("faq/", views.faq_view, name="faq"),
]
