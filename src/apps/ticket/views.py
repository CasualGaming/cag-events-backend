from django.db.models import Q

from rest_framework.viewsets import ModelViewSet

from common.permissions import DenyAll, DisjunctionPermission, IsEnabled, StringPermission
from common.request_utils import get_query_param_bool, get_query_param_int, get_query_param_str

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
            "retrieve": [DisjunctionPermission(IsEnabled(), StringPermission("ticket.ticket_type.view_disabled"))],
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

        # Hide all disabled if the user is not allowed to see disabled
        if not self.request.user.has_perm("ticket.ticket_type.view_disabled"):
            queryset = queryset.filter(is_enabled=True)

        is_enabled = get_query_param_bool(self.request, "enabled")
        if is_enabled is not None:
            queryset = queryset.filter(is_enabled=is_enabled)

        return queryset


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_permissions(self):
        permissions = {
            # List items are filtered
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

        ticket_type = get_query_param_int(self.request, "ticket_type")
        if ticket_type is not None:
            queryset = queryset.filter(ticket_type=ticket_type)

        owner = get_query_param_str(self.request, "owner")
        if owner is not None:
            queryset = queryset.filter(owner__username=owner)

        assignee = get_query_param_str(self.request, "assignee")
        if assignee is not None:
            queryset = queryset.filter(assignee__username=assignee)

        is_activated = get_query_param_bool(self.request, "activated")
        if is_activated is not None:
            if is_activated:
                queryset = queryset.filter(~Q(assignee=None))
            else:
                queryset = queryset.filter(assignee=None)

        # Filter out tickets the user is not allowed to see
        if not user.has_perm("ticket.ticket.list_all"):
            queryset = queryset.filter(Q(owner=user) | Q(assignee=user))

        return queryset
