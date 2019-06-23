from django.conf import settings
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from authentication.permissions import AllowAll

from . import views

schema_view = get_schema_view(title=settings.APP_NAME, urlconf="apps.event.urls", permission_classes=[AllowAll])

urlpatterns = [
    path(r"", schema_view),
]

router = DefaultRouter()
router.register(r"events", views.EventViewSet)
urlpatterns += router.urls
