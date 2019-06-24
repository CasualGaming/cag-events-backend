from rest_framework.viewsets import ReadOnlyModelViewSet

from authentication.models import User
from authentication.permissions import DenyAll, ModelPermission

from .serializers import UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    def get_permissions(self):
        if self.action == "list":
            return [ModelPermission("authentication.user.list")]
        elif self.action == "retrieve":
            # All users are somewhat visible
            return []
        elif self.action == "delete":
            return [ModelPermission("authentication.user.delete")]
        else:
            return [DenyAll()]

    def get_queryset(self):
        if self.action == "list":
            return self.get_list_queryset()
        else:
            return self.queryset

    def get_list_queryset(self):
        queryset = self.queryset

        username = self.request.query_params.get("username", None)
        if username is not None:
            username = username.lower()
            queryset = queryset.filter(username=username)

        partial_username = self.request.query_params.get("partial_username", None)
        if partial_username is not None:
            queryset = queryset.filter(username__icontains=partial_username)

        is_member_str = self.request.query_params.get("member", None)
        if is_member_str is not None and (is_member_str == "true" or is_member_str == "false"):
            is_member = is_member_str == "true"
            queryset = queryset.filter(profile__is_member=is_member)

        groups_str = self.request.query_params.get("groups", None)
        if groups_str is not None:
            for group in groups_str.split(","):
                queryset = queryset.filter(groups__name=group)

        return queryset
