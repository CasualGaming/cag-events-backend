# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import include, path

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from rest_framework_swagger.views import get_swagger_view

from lan.views import LANViewSet

from news.views import ArticleViewSet

# from userprofile import urls as userprofile_urls
from sponsor.views import SponsorViewSet

from userprofile.views import UserViewSet

router = DefaultRouter()
router.register(r"lan", LANViewSet)
router.register(r"news", ArticleViewSet)
router.register(r"users", UserViewSet)
router.register(r"sponsor", SponsorViewSet)

swagger_schema_view = get_swagger_view(title="CaG Events API")
schema_view = get_schema_view(title="CaG Events API", permission_classes=[IsAuthenticatedOrReadOnly])

urlpatterns = [
    path("", include(router.urls)),
    path("schema/", schema_view),
    path("swagger/", swagger_schema_view),
    path("admin/", admin.site.urls),
    # path("users/", include(userprofile_urls)),
    path("auth/", include("rest_framework.urls")),
    path("oidc/", include("mozilla_django_oidc.urls")),
]
