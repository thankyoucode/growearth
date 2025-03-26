# apps/core/urls.py
from django.urls import path

from . import views

app_name = "core"

handler404 = views.custom_404_view


urlpatterns = [
    path("", views.home_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
    path("care-guide/", views.care_guide_view, name="care_guide"),
    path("admin-contact/", views.contact_messages_view, name="contact_messages"),
    path("impact/", views.impact_view, name="impact"),
    path("mission/", views.mission_view, name="mission"),
    path("shipping/", views.shipping_view, name="shipping"),
    path("returns/", views.returns_view, name="returns"),
    path("terms-of-service/", views.termsofservice_view, name="termsofservice"),
    path("faq/", views.faq_view, name="faq"),
]
