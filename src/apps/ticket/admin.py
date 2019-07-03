from django.contrib.admin import register
from django.contrib.admin.options import ModelAdmin

from .models import Ticket, TicketType


@register(TicketType)
class TicketTypeAdmin(ModelAdmin):
    list_display = ["long_title", "event", "is_active", "priority"]
    list_filter = ["event", "is_active"]


@register(Ticket)
class TicketAdmin(ModelAdmin):
    # Creating and deleting tickets should not be allowed
    list_display = ["id", "ticket_type", "owner", "assignee", "is_active"]
    list_filter = ["ticket_type"]

    def is_active(self, obj):
        return obj.is_active()
    is_active.short_description = "Active"
    # Is-active == if there is an assignee
    is_active.admin_order_field = "assignee"
    is_active.boolean = True
