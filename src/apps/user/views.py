from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet


from auth.permissions import AllowAll, IsSuperuser

from .models import User
from .permissions import UserPermissions
from .serializers import PublicProfileUserSerializer, UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsSuperuser | UserPermissions]

    def get_queryset(self):
        queryset = User.objects.all()

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

        return queryset

    @action(url_path="public_profile", methods=["get"], detail=True, permission_classes=[AllowAll])
    def get_public_profile(self, request, username):
        instance = self.get_object()
        serializer = PublicProfileUserSerializer(instance)
        return Response(serializer.data)
