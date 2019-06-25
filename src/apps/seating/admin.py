from django.contrib.admin import StackedInline, register
from django.contrib.admin.options import ModelAdmin

from .models import Area, AreaLayout, RowLayout, Seating


class RowLayoutInline(StackedInline):
    model = RowLayout


@register(AreaLayout)
class AreaLayoutAdmin(ModelAdmin):
    inlines = [RowLayoutInline]
    # list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_superuser", "is_active", "date_joined", "last_login")
    # list_filter = ("groups", "is_staff", "is_superuser", "is_active")


class AreaInline(StackedInline):
    model = Area


@register(Seating)
class SeatingAdmin(ModelAdmin):
    inlines = [AreaInline]
    # list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_superuser", "is_active", "date_joined", "last_login")
    # list_filter = ("groups", "is_staff", "is_superuser", "is_active")
