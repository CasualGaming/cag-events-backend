from rest_framework import permissions


class DenyAll(permissions.BasePermission):
    """Deny everything."""
    def has_permission(self, request, view):
        return False


class AllowAll(permissions.BasePermission):
    """Allow everything. Same as empty permission set."""
    def has_permission(self, request, view):
        return True


class IsSuperuser(permissions.BasePermission):
    """Allow if user is superuser."""
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsStaff(permissions.BasePermission):
    """Allow if user is staff."""
    def has_permission(self, request, view):
        return request.user.is_staff


class IsOwner(permissions.BasePermission):
    """Allow if user is owner of resource."""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsReadOnly(permissions.BasePermission):
    """Allow if request is using a safe (read-only) HTTP method."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsStaffOrReadOnly(permissions.BasePermission):
    """DEPRECATED: Use [IsSuperuser | IsReadOnly] instead"""
    def has_permission(self, request, view):
        return request.user.is_staff or request.method in permissions.SAFE_METHODS
