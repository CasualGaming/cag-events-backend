# -*- coding: utf-8 -*-

from rest_framework import permissions


class IsAuthOrPost(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in "POST":
            return True
        return request.user.is_authenticated
