from drf_dynamic_fields import DynamicFieldsMixin

from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Ticket, TicketType


class TicketTypeSerializer(DynamicFieldsMixin, HyperlinkedModelSerializer):
    """Serializes a ticket type."""

    class Meta:
        model = TicketType
        fields = [
            "url",
            "short_title",
            "long_title",
            "event",
            "priority",
        ]


class TicketSerializer(DynamicFieldsMixin, HyperlinkedModelSerializer):
    """Serializes a ticket."""

    class Meta:
        model = Ticket
        fields = [
            "url",
            "ticket_type",
            "owner",
            "assignee",
            "is_activated",
            "seat",
        ]
        extra_kwargs = {
            "owner": {
                "view_name": "user-detail",
                "lookup_field": "username",
            },
            "assignee": {
                "view_name": "user-detail",
                "lookup_field": "username",
            },
        }
