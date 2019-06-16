from django.conf import settings
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from . import views

schema_view = get_schema_view(title=settings.SITE_NAME)

urlpatterns = [
    path(r"schema/", schema_view),
]

router = DefaultRouter()
router.register(r"articles", views.ArticleViewSet)
urlpatterns += router.urls
