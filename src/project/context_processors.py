from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# from django.utils.translation import gettext as _


def navigation_links(request):
    return {
        "auth_links": {
            "login": {
                "url": "accounts:login",
                "label": _("Log In"),
                "icon": "fa-sign-in",
                "style": "secondary",
            },
            "register": {
                "url": "accounts:register",
                "label": _("Sign Up"),
                "icon": "fa-user-plus",
                "style": "outline",
            },
            "logout": {
                "url": "accounts:logout",
                "label": _("Logout"),
                "icon": "fa-sign-out",
                "style": "danger",
            },
            "profile": {
                "url": "accounts:profile",
                "label": _("My Profile"),
                "icon": "fa-user",
                "style": "primary",
            },
        },
        "navigation_links": [
            {
                "name": _("Home"),
                "url": "core:home",  # Use the URL pattern name here
                "type": "single",
                "active": request.path == reverse("core:home"),
            },
            {
                "name": _("Plants Category"),
                "url": "store:categoryes",
                "type": "single",
                "active": request.path == reverse("store:categoryes"),
            },
            {
                "name": _("Care Guide"),
                "url": "core:care_guide",
                "type": "single",
                "active": request.path == reverse("core:care_guide"),
            },
            {
                "name": _("About Us"),
                "url": "core:about",
                "type": "single",
                "active": request.path == reverse("core:about"),
            },
        ],
    }


def footer_context(request):
    """
    Provides global context for footer links and social media information
    """
    return {
        "footer_sections": {
            "quick_links": [
                {"name": _("Home"), "url": "core:home", "icon": "home-outline"},
                {
                    "name": _("Plant Categoryes"),
                    "url": "store:categoryes",
                    "icon": "leaf-outline",
                },
                {
                    "name": _("Terms of Service"),
                    "url": "core:termsofservice",
                    "icon": "fa-file-contract",
                },
                {"name": _("About Us"), "url": "core:about", "icon": "info-outline"},
                {"name": _("Reviews"), "url": "accounts:review_list", "icon": "star"},
                {
                    "name": _("Your Opinion"),
                    "url": "accounts:submit_opinion",
                    "icon": "comment",
                },
            ],
            "support_links": [
                {"name": _("FAQ"), "url": "core:faq", "icon": "help-circle-outline"},
                {"name": _("Contact"), "url": "core:contact", "icon": "mail-outline"},
                {
                    "name": _("Shipping"),
                    "url": "core:shipping",
                    "icon": "truck-outline",
                },
                {
                    "name": _("Returns"),
                    "url": "core:returns",
                    "icon": "refresh-outline",
                },
            ],
        },
        "social_links": [
            {
                "name": "Facebook",
                "icon": "fa-facebook-f",
                "color": "text-[#3b5998]",
                "url": "https://facebook.com/growearth",
                "aria_label": "Follow us on Facebook",
            },
            {
                "name": "Twitter",
                "icon": "fa-twitter",
                "color": "text-[#1da1f2]",
                "url": "https://twitter.com/growearth",
                "aria_label": "Follow us on Twitter",
            },
            {
                "name": "Instagram",
                "icon": "fa-instagram",
                "color": "text-[#c13584]",
                "url": "https://instagram.com/growearth",
                "aria_label": "Follow us on Instagram",
            },
            {
                "name": "LinkedIn",
                "icon": "fa-linkedin-in",
                "color": "text-[#0077b5]",
                "url": "https://linkedin.com/company/growearth",
                "aria_label": "Connect with us on LinkedIn",
            },
        ],
        "company_details": {
            "name": "Grow Earth",
            "founded": 2023,
            "tagline": _("Cultivating Sustainable Ecosystems"),
            "mission": _("Transforming urban spaces into thriving green environments"),
            "contact_email": "support@growearth.com",
            "contact_phone": "+1 (555) 123-4567",
        },
    }


def global_settings(request):
    """
    Provides global settings and configuration for templates
    """
    return {
        "site_name": "Grow Earth",
        "site_description": "Innovative Plant Solutions for Sustainable Living",
        "contact_email": "support@growearth.com",
        "contact_phone": "+1 (555) 123-4567",
    }
