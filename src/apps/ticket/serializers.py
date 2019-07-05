from drf_dynamic_fields import DynamicFieldsMixin

from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Ticket, TicketType


class TicketTypeSerializer(DynamicFieldsMixin, HyperlinkedModelSerializer):

    class Meta:
        model = TicketType
        fields = [
            "url",
            "simple_title",
            "unique_title",
            "event",
            "is_enabled",
            "visual_priority",
            "max_count",
            "max_user_purchase_count",
            "max_user_assignment_count",
            "grants_entrance",
            "is_for_seating",
            "required_ticket_type",
            "valid_start_time",
            "valid_end_time",
            "is_valid_all_event",
            "description",
            "total_count",
            "total_available_count",
        ]


class TicketSerializer(DynamicFieldsMixin, HyperlinkedModelSerializer):

    class Meta:
        model = Ticket
        fields = [
            "url",
            "ticket_type",
            "owner",
            "assignee",
            "is_activated",
            "transfer_code",
            "seat",
        ]
        extra_kwargs = {
            "owner": {
                "lookup_field": "username",
            },
            "assignee": {
                "lookup_field": "username",
            },
        }
