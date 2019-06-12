from rest_framework import permissions


class EventPermission(permissions.BasePermission):
    """For events."""

    def has_permission(self, request, view):
        # TMP
        return True
