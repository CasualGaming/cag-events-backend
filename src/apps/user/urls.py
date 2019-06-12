# -*- coding: utf-8 -*-

# from django.urls import path

# from rest_framework.urlpatterns import format_suffix_patterns

# from .views import UserView, UserDetailViewSet

# urlpatterns = [
#     path("", UserView.as_view(), name="userprofile-list"),
#     path("<int:pk>", UserDetailViewSet, name="userprofile-detail"),
# ]
#
#
# urlpatterns = format_suffix_patterns(urlpatterns, allowed=["json", "html"])

from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = []

router = DefaultRouter()
router.register(r"", views.UserViewSet)
urlpatterns += router.urls
