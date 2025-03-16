from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Use absolute import for custom_404_view
from apps.core.views import custom_404_view

# Define the custom 404 handler globally
handler404 = custom_404_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),  # Core app URLs
    path("store/", include("apps.store.urls")),  # Store app URLs
    path("accounts/", include("apps.accounts.urls")),  # Accounts app URLs
    path("__reload__/", include("django_browser_reload.urls")),  # Browser reload URLs
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.BASE_DIR / "static"
    )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
