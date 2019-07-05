from django.contrib.admin import register
from django.contrib.admin.options import ModelAdmin

from .models import Attendance, Event


@register(Event)
class EventAdmin(ModelAdmin):
    list_display = [
        "title",
        "slug",
        "start_time",
        "end_time",
        "location",
        "require_ticket",
        "age_requirement",
    ]


@register(Attendance)
class AttendanceAdmin(ModelAdmin):
    list_display = [
        "id",
        "event",
        "user",
        "has_arrived",
        "has_ticket",
    ]
