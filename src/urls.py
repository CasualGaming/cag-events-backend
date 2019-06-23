from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path


admin.site.site_header = settings.SITE_NAME

resource_urlpatterns = [
    path(r"article/", include("apps.article.urls")),
    path(r"event/", include("apps.event.urls")),
    path(r"user/", include("apps.user.urls")),
]

urlpatterns = [
    path(r"", include("apps.home.urls")),
    path(r"admin/", admin.site.urls),
    path(r"grappelli/", include("grappelli.urls")),
    path(r"auth/", include("rest_framework.urls")),
    path(r"oidc/", include("mozilla_django_oidc.urls")),
    # path(r"favicon.ico", RedirectView.as_view(url="/static/images/favicon.ico", permanent=True)),
    re_path(r"^(?P<version>(v0))/", include(resource_urlpatterns)),
]
