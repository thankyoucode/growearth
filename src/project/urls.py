from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Admin URLs
    path("admin/", admin.site.urls),
    # App-specific URLs
    path("", include("apps.core.urls")),  # Home/Landing page
    path("store/", include("apps.store.urls")),  # Store-related pages
    path(
        "accounts/", include("apps.accounts.urls")
    ),  # Authentication & User management
    # path("tags/", include("apps.tags.urls")),  # Optional: Tag-related URLs
    # Development & Debug URLs
    path("__reload__/", include("django_browser_reload.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
