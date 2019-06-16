# from django.http import Http404

# from rest_framework import mixins
# from rest_framework import generics, status
# from rest_framework.views import APIView
# from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet


from auth.permissions import AllowAll, IsSuperuser

from .models import User
# from .permissions import IsAuthOrPost
# from .permissions import UserPermission, PublicUserSerializer
from .serializers import PublicUserSerializer, UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    lookup_field = "username"
    serializer_class = UserSerializer
    # TODO fix permissions
    permission_classes = [IsSuperuser]

    # def get_serializer_class(self):
    #     if self.action == "list":
    #         return UserListSerializer
    #     return super(ReadOnlyModelViewSet, self).get_serializer_class()

    @action(url_path="public", methods=["get"], detail=True, permission_classes=[AllowAll])
    def get_public(self, request, username):
        instance = self.get_object()
        serializer = PublicUserSerializer(instance)
        return Response(serializer.data)


# class UserViewSet(mixins.RetrieveModelMixin,
#                  mixins.UpdateModelMixin,
#                  mixins.DestroyModelMixin,
#                  mixins.ListModelMixin,
#                  GenericViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializerPublic
#    permission_classes = [IsAuthOrPost, IsOwnerOrAdmin]
#    lookup_field = "username"
#
#    def retrieve(self, request, *args, **kwargs):
#        instance = self.get_object()
#        serializer = UserSerializerPrivate(instance)
#        return Response(serializer.data)

# class UserView(generics.ListCreateAPIView):
#     """
#     Returns a list of all users
#     """
#     queryset = User.objects.all()
#     permission_classes = [IsAuthOrPost]
#
#     def get_serializer_class(self):
#         if self.request.user.is_staff or self.request.user.is_superuser or (self.request.method == "POST"):
#             return UserSerializerPrivate
#         return UserSerializerPublic

#
# class UserDetailViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializerPrivate
#     permission_classes = [IsOwnerOrAdmin]


# class UserDetail(APIView):
#     """
#     GET, POST and PUT userinfo, resticted if request.userprofile is not admin or self
#     """
#
#     permission_classes = [IsOwnerOrAdmin]
#
#     def get_object(self, pk):
#         try:
#             return User.objects.get(pk=pk)
#         except User.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         user = self.get_object(pk)
#         serializer = UserSerializerPrivate(user)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         user = self.get_object(pk)
#         serializer = UserSerializerPrivate(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         user = self.get_object(pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
