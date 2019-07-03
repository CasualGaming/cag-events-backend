from rest_framework.viewsets import ReadOnlyModelViewSet

from authentication.models import User

from common.permissions import DenyAll, StringPermission
from common.request_utils import get_query_param_bool, get_query_param_list, get_query_param_str

from .serializers import UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    def get_permissions(self):
        permissions = {
            "list": [StringPermission("authentication.user.list")],
            "retrieve": [],
            "destroy": [StringPermission("authentication.user.delete")],
        }
        return permissions.get(self.action, [DenyAll()])

    def get_queryset(self):
        queryset = self.queryset
        if self.action != "list":
            return queryset

        username = get_query_param_str(self.request, "username")
        if username is not None:
            username = username.lower()
            queryset = queryset.filter(username=username)

        partial_username = get_query_param_str(self.request, "partial_username")
        if partial_username is not None:
            queryset = queryset.filter(username__icontains=partial_username)

        is_member = get_query_param_bool(self.request, "member")
        if is_member is not None:
            queryset = queryset.filter(profile__is_member=is_member)

        groups = get_query_param_list(self.request, "groups")
        if groups is not None:
            queryset = queryset.filter(groups__name__in=groups)

        return queryset
