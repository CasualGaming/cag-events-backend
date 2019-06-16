from django.conf import settings
from django.contrib import admin
from django.urls import include, re_path, path

# Set admin panel header
admin.site.site_header = settings.SITE_NAME

resource_urlpatterns = [
    re_path(r"^article/", include("apps.article.urls")),
    re_path(r"^event/", include("apps.event.urls")),
    re_path(r"^user/", include("apps.user.urls")),
]

urlpatterns = [
    # Home
    # TODO

    # Admin panel
    path(r"admin/", admin.site.urls),
    path(r"grappelli/", include("grappelli.urls")),

    # Auth
    path(r"auth/", include("rest_framework.urls")),
    path(r"oidc/", include("mozilla_django_oidc.urls")),

    # Resources
    re_path(r"^(?P<version>(v0))/", include(resource_urlpatterns)),
]
