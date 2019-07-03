from django.db.models import Q

from rest_framework.viewsets import ModelViewSet

from common.permissions import DenyAll, DisjunctionPermission, IsActive, StringPermission

from .models import Ticket, TicketType
from .permissions import IsTicketOwnerOrAssignee
from .serializers import TicketSerializer, TicketTypeSerializer


class TicketTypeViewSet(ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer

    def get_permissions(self):
        permissions = {
            # List has more granular permission filtering
            "list": [StringPermission("ticket.ticket_type.list")],
            "retrieve": [DisjunctionPermission(IsActive(), StringPermission("ticket.ticket_type.view_inactive"))],
            "create": [StringPermission("ticket.ticket_type.create")],
            "update": [StringPermission("ticket.ticket_type.change")],
            "partial_update": [StringPermission("ticket.ticket_type.change")],
            "destroy": [StringPermission("ticket.ticket_type.delete")],
        }
        return permissions.get(self.action, [DenyAll()])

    def get_queryset(self):
        queryset = self.queryset
        if self.action != "list":
            return queryset

        # Hide all inactive if the user is not allowed to see inactive
        if not self.request.user.has_perm("ticket.ticket_type.view_inactive"):
            queryset = queryset.filter(is_active=True)

        is_active_str = self.request.query_params.get("active", None)
        if is_active_str is not None and (is_active_str == "true" or is_active_str == "false"):
            is_active = is_active_str == "true"
            queryset = queryset.filter(is_active=is_active)

        return queryset


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_permissions(self):
        permissions = {
            "list": [],
            "retrieve": [DisjunctionPermission(StringPermission("ticket.ticket.view_all"), IsTicketOwnerOrAssignee())],
            "create": [StringPermission("ticket.ticket.create")],
            "update": [StringPermission("ticket.ticket.change")],
            "partial_update": [StringPermission("ticket.ticket.change")],
            "destroy": [StringPermission("ticket.ticket.delete")],
        }
        return permissions.get(self.action, [DenyAll()])

    def get_queryset(self):
        queryset = self.queryset
        if self.action != "list":
            return queryset

        user = self.request.user

        ticket_type_str = self.request.query_params.get("ticket_type", None)
        if ticket_type_str is not None:
            try:
                ticket_type = int(ticket_type_str)
                queryset = queryset.filter(ticket_type=ticket_type)
            except ValueError:
                pass

        owner = self.request.query_params.get("owner", None)
        if owner is not None:
            queryset = queryset.filter(owner__username=owner)

        assignee = self.request.query_params.get("assignee", None)
        if assignee is not None:
            queryset = queryset.filter(assignee__username=assignee)

        is_activated_str = self.request.query_params.get("activated", None)
        if is_activated_str is not None and (is_activated_str == "true" or is_activated_str == "false"):
            is_activated = is_activated_str == "true"
            if is_activated:
                queryset = queryset.filter(~Q(assignee=None))
            else:
                queryset = queryset.filter(assignee=None)

        # Filter out tickets the user is not allowed to see
        if not user.has_perm("ticket.ticket.list_all"):
            queryset = queryset.filter(Q(owner=user) | Q(assignee=user))

        return queryset
