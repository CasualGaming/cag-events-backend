# -*- coding: utf-8 -*-

from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or \
            (request.user and (request.user.is_staff or request.user.is_superuser))


class IsAuthOrPost(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in 'POST':
            return True
        return request.user.is_authenticated
