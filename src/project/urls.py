from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("store/", include("apps.store.urls")),
    path("accounts/", include("apps.accounts.urls")),
    # path("tags/", include("apps.tags.urls")),
    # not using two_factor authentication
    # path("two_factor/", include(("two_factor.urls", "two_factor"))),
    path("__reload__/", include("django_browser_reload.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
