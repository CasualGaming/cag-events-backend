from django.contrib.admin import register
from django.contrib.admin.options import ModelAdmin

from .models import Event


@register(Event)
class EventAdmin(ModelAdmin):
    list_display = ("title", "start_time", "end_time", "location")
