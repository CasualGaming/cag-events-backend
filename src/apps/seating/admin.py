from django.contrib.admin import StackedInline, register
from django.contrib.admin.options import ModelAdmin

from .models import Area, AreaLayout, RowLayout, Seating


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
