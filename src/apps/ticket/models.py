from django.core.validators import MinValueValidator
from django.db.models import BooleanField, CharField, ForeignKey, IntegerField, Model, PROTECT, SET_NULL

from apps.event.models import Event

from authentication.models import User


class TicketType(Model):
    short_title = CharField("short title", max_length=20, help_text="A short, non-unique title to show to users.")
    long_title = CharField("long title", unique=True, max_length=50, help_text="A longer, unique title.")
    event = ForeignKey(Event, verbose_name="event", related_name="ticket_types", on_delete=PROTECT)
    is_active = BooleanField("is active", default=False, help_text="If this ticket type is currently available to users.")
    priority = IntegerField("priority", validators=[MinValueValidator(0)], default=10, help_text="Lower priority shows it higher on the list among other ticket types.")

    def __str__(self):
        return self.long_title


class Ticket(Model):
    ticket_type = ForeignKey(TicketType, verbose_name="type", related_name="tickets", on_delete=PROTECT)
    owner = ForeignKey(User, verbose_name="owner", related_name="owned_tickets", null=True, default=None, on_delete=SET_NULL)
    assignee = ForeignKey(User, verbose_name="assignee", related_name="assigned_tickets", null=True, blank=True, on_delete=SET_NULL)

    class Meta:
        default_permissions = ["view", "change"]

    def __str__(self):
        return "{0} #{1}".format(self.ticket_type, self.id)

    def is_activated(self):
        return self.assignee is not None


class Permissions(Model):
    class Meta:
        managed = False
        default_permissions = []
        permissions = [
            ("*", "Ticket app admin"),
            ("ticket_type.*", "Ticket type admin"),
            ("ticket_type.list", "List ticket types"),
            ("ticket_type.create", "Create ticket types"),
            ("ticket_type.change", "Change ticket types"),
            ("ticket_type.delete", "Delete ticket types"),
            ("ticket_type.view_inactive", "View inactive ticket types"),
            ("ticket.*", "Ticket admin"),
            ("ticket.list_all", "List all tickets"),
            ("ticket.view_all", "View all tickets"),
            ("ticket.create", "Manually create tickets"),
            ("ticket.change", "Manually change tickets"),
            ("ticket.delete", "Manually delete tickets"),
        ]
