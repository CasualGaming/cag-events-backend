from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import UserView, UserDetail

urlpatterns = [
    path('', UserView.as_view(), name='userprofile-list'),
    path('<int:pk>', UserDetail.as_view(), name='userprofile-detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
