from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("accounts/", include("account.urls")),
    path("", include("cinema.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
