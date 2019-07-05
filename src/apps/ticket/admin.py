from django.contrib.admin import register
from django.contrib.admin.options import ModelAdmin

from .models import Ticket, TicketType


@register(TicketType)
class TicketTypeAdmin(ModelAdmin):
    list_display = [
        "unique_title",
        "event",
        "is_enabled",
        "visual_priority",
        "grants_entrance",
        "is_for_seating",
        "required_ticket_type",
        "is_valid_all_event",
        "total_count",
        "total_available_count",
    ]
    list_filter = ["event", "is_enabled"]


@register(Ticket)
class TicketAdmin(ModelAdmin):
    # Creating and deleting tickets should not be allowed
    list_display = ["id", "ticket_type", "owner", "assignee", "is_activated"]
    list_filter = ["ticket_type"]

    def is_activated(self, obj):
        return obj.is_activated()
    is_activated.short_description = "Activated"
    # Is-activated == if there is an assignee
    is_activated.admin_order_field = "assignee"
    is_activated.boolean = True
