from rest_framework.permissions import BasePermission


class IsTicketOwnerOrAssignee(BasePermission):
    """
    Allow if user is the ornwe or assignee of the ticket.
    """

    def has_object_permission(self, request, view, obj):
        return obj.assignee_id == request.user.id or obj.owner_id == request.user.id
