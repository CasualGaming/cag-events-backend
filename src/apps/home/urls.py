from django.urls import path

from .views import Home

urlpatterns = [
    path(r"", Home.as_view()),
]
