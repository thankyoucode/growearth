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
    path("__reload__/", include("django_browser_reload.urls")),
    # path("two_factor/", include(("two_factor.urls", "two_factor"))), # not using two_factor authentication
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.BASE_DIR / "static"
    )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
