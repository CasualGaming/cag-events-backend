from django.contrib.admin import StackedInline, register
from django.contrib.admin.options import ModelAdmin

from .models import Area, AreaLayout, RowLayout, RowTicketType, Seat, Seating


class RowLayoutInline(StackedInline):
    model = RowLayout


@register(AreaLayout)
class AreaLayoutAdmin(ModelAdmin):
    inlines = [RowLayoutInline]
    list_display = ["title", "is_enabled"]
    list_filter = ["is_enabled"]


class AreaInline(StackedInline):
    model = Area


@register(Seating)
class SeatingAdmin(ModelAdmin):
    inlines = [AreaInline]
    list_display = ["event", "is_enabled", "seat_count"]
    list_filter = ["is_enabled"]


@register(RowTicketType)
class RowTicketTypeAdmin(ModelAdmin):
    list_display = ["id", "area", "row_number", "ticket_type"]
    list_filter = ["area__seating", "ticket_type"]


@register(Seat)
class SeatAdmin(ModelAdmin):
    list_display = [
        "id",
        "seating",
        "area_code",
        "row_number",
        "seat_number",
        "assigned_ticket",
        "is_reserved",
    ]
    # TODO filter is_reserved, is_taken
    list_filter = ["area__seating"]

    def seating(self, obj):
        return obj.area.seating
    seating.short_description = "Seating"
    seating.admin_order_field = "area__seating"

    def area_code(self, obj):
        return obj.area.area_code
    area_code.short_description = "Area code"
    area_code.admin_order_field = "area__area_code"

    def is_reserved(self, obj):
        return obj.is_reserved
    is_reserved.short_description = "Reserved"
    is_reserved.admin_order_field = "assigned_ticket"
    is_reserved.boolean = True
