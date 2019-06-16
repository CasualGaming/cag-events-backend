# from rest_framework import permissions


# class IsAuthOrPost(permissions.BasePermission):
#    def has_permission(self, request, view):
#        return request.method in "POST" or request.user.is_authenticated


# class UserPermission(permissions.BasePermission):
#     """Full user details are restricted."""
#
#     def has_permission(self, request, view):
#         # WIP
#         return True
