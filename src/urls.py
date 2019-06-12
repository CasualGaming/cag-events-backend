from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from rest_framework_swagger.views import get_swagger_view

from apps.article.views import ArticleViewSet
from apps.event.views import EventViewSet
from apps.sponsor.views import SponsorViewSet
from apps.user.views import UserViewSet

schema_view = get_schema_view(title="CaG Events API")
swagger_schema_view = get_swagger_view(title="CaG Events API")

urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(r"schema/", schema_view),
    path(r"swagger/", swagger_schema_view),
    path(r"auth/", include("rest_framework.urls")),
    path(r"oidc/", include("mozilla_django_oidc.urls")),
]

router = DefaultRouter()
router.register(r"event", EventViewSet)
router.register(r"article", ArticleViewSet)
router.register(r"user", UserViewSet)
router.register(r"sponsor", SponsorViewSet)
urlpatterns += router.urls
