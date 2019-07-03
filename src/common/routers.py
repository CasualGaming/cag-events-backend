from rest_framework.routers import APIRootView, DefaultRouter

from .permissions import AllowAll


class PublicAPIRootView(APIRootView):
    permission_classes = [AllowAll]


class PublicDefaultRouter(DefaultRouter):
    APIRootView = PublicAPIRootView
