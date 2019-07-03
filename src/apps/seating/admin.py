from django.contrib.admin import StackedInline, register
from django.contrib.admin.options import ModelAdmin

from .models import Area, AreaLayout, RowLayout, RowTicketType, Seat, Seating


class RowLayoutInline(StackedInline):
    model = RowLayout


@register(AreaLayout)
class AreaLayoutAdmin(ModelAdmin):
    inlines = [RowLayoutInline]
    list_display = ["long_title", "is_active"]
    list_filter = ["is_active"]


class AreaInline(StackedInline):
    model = Area


@register(Seating)
class SeatingAdmin(ModelAdmin):
    inlines = [AreaInline]
    list_display = ["event", "is_active"]
    list_filter = ["is_active"]


@register(RowTicketType)
class RowTicketTypeAdmin(ModelAdmin):
    list_display = ["id", "area", "row_number", "ticket_type"]
    list_filter = ["area", "row_number", "ticket_type"]


@register(Seat)
class SeatAdmin(ModelAdmin):
    # Creating and deleting seats should not be allowed
    list_display = ["id", "area", "row_number", "seat_number", "assigned_ticket", "is_reserved"]
    list_filter = ["seating", "area"]

    def is_reserved(self, obj):
        return obj.is_reserved()
    is_reserved.short_description = "Reserved"
    is_reserved.admin_order_field = "assigned_ticket"
    is_reserved.boolean = True
