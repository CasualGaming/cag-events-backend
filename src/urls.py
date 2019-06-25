from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from apps.article.views import ArticleViewSet
from apps.event.views import EventViewSet
from apps.user.views import UserViewSet

from common.permissions import AllowAll


schema_view = get_schema_view(title=settings.APP_NAME, permission_classes=[AllowAll])
router = DefaultRouter()

admin.site.site_header = settings.SITE_NAME

router.register(r"articles", ArticleViewSet)
router.register(r"events", EventViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(r"grappelli/", include("grappelli.urls")),
    path(r"schema/", schema_view, name="schema"),
    path(r"auth/", include("rest_framework.urls")),
    path(r"oidc/", include("mozilla_django_oidc.urls")),
    path(r"v0/", include(router.urls)),
    # path(r"favicon.ico", RedirectView.as_view(url="/static/images/favicon.ico", permanent=True)),
    path(r"", RedirectView.as_view(url="/v0", permanent=False)),
]
