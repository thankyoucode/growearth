from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# from django.utils.translation import gettext as _


# def navigation_links(request):
#     """
#     Dynamically generate navigation links with active state and metadata
#     """
#     current_path = request.path
#     links = [
#         {
#             "name": _("Home"),
#             "url": "core:home",
#             "icon": "home-outline",
#             "active": current_path == reverse("core:home"),
#             "permission": None,
#             "order": 1,
#         },
#         {
#             "name": _("Plants"),
#             "url": "store:plants",
#             "icon": "leaf-outline",
#             "active": current_path == reverse("store:plants"),
#             "permission": "store.view_plant",
#             "order": 2,
#         },
#         {
#             "name": _("Collections"),
#             "url": "store:collections",
#             "icon": "collection-outline",
#             "active": current_path == reverse("store:collections"),
#             "permission": None,
#             "order": 3,
#         },
#         {
#             "name": _("Care Guide"),
#             "url": "store:care_guide",
#             "icon": "book-outline",
#             "active": current_path == reverse("store:care_guide"),
#             "permission": None,
#             "order": 4,
#         },
#         {
#             "name": _("Impact"),
#             "url": "core:impact",
#             "icon": "globe-outline",
#             "active": current_path == reverse("core:impact"),
#             "permission": None,
#             "order": 5,
#         },
#     ]
#     # Optional: Filter links based on user permissions
#     filtered_links = [
#         link
#         for link in links
#         if (not link.get("permission"))
#         or (request.user.is_authenticated and request.user.has_perm(link["permission"]))
#     ]
#     # Optional: Sort links by order
#     sorted_links = sorted(filtered_links, key=lambda x: x.get("order", 999))
#     return {"navigation_links": sorted_links}
# for now not using that dropdown manu
# {
#     "name": _("Plants"),
#     "type": "dropdown",
#     "active": "/store/" in request.path,
#     "categories": [
#         {
#             "name": _("Indoor Plants"),
#             "url": "store:indoor_plants",  # URL pattern name
#             "icon": "fa-home",
#             "description": _("Perfect for home and office spaces"),
#         },
#         {
#             "name": _("Outdoor Plants"),
#             "url": "store:outdoor_plants",  # URL pattern name
#             "icon": "fa-tree",
#             "description": _("Enhance your garden and landscape"),
#         },
#         {
#             "name": _("Rare Collectibles"),
#             "url": "store:rare_plants",  # URL pattern name
#             "icon": "fa-star",
#             "description": _("Unique and exotic plant varieties"),
#         },
#         {
#             "name": _("Succulents"),
#             "url": "store:succulents",  # URL pattern name
#             "icon": "fa-seedling",
#             "description": _("Low maintenance plant collection"),
#         },
#     ],
# },
def navigation_links(request):
    return {
        "auth_links": {
            "login": {
                "url": "account:login",
                "label": _("Log In"),
                "icon": "fa-sign-in",
                "style": "secondary",
            },
            "register": {
                "url": "account:register",
                "label": _("Sign Up"),
                "icon": "fa-user-plus",
                "style": "outline",
            },
            "logout": {
                "url": "account:logout",
                "label": _("Logout"),
                "icon": "fa-sign-out",
                "style": "danger",
            },
            "profile": {
                "url": "account:profile",
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
                "name": _("Plants"),
                "url": "store:plants",
                "type": "single",
                "active": request.path == reverse("store:plants"),
            },
            {
                "name": _("Care Guide"),
                "url": "store:care_guide",
                "type": "single",
                "active": request.path == reverse("store:care_guide"),
            },
            {
                "name": _("Consultation"),
                "url": "core:consultation",
                "type": "single",
                "active": request.path == reverse("core:consultation"),
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
                    "name": _("Plant Catalog"),
                    "url": "store:catalog",
                    "icon": "leaf-outline",
                },
                {
                    "name": _("Consultation"),
                    "url": "core:consultation",
                    "icon": "support-outline",
                },
                {"name": _("About Us"), "url": "core:about", "icon": "info-outline"},
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
