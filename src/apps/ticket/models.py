from django.db.models import CharField, DateField, ForeignKey, IntegerField, Model, PROTECT, SET_NULL

from apps.event.models import Event

from authentication.models import User


class TicketType(Model):
    short_title = CharField("short title", max_length=20, help_text="A short, non-unique title to show to users.")
    long_title = CharField("long title", unique=True, max_length=50, help_text="A longer, unique title.")
    event = ForeignKey(Event, verbose_name="event", related_name="ticket_types", on_delete=PROTECT)
    priority = IntegerField("priority", default=10, help_text="Lower priority shows it higher on the list among other ticket types.")

    def __str__(self):
        return self.long_title


class Ticket(Model):
    ticket_type = ForeignKey(TicketType, verbose_name="type", related_name="tickets", on_delete=PROTECT, editable=False)
    owner = ForeignKey(User, verbose_name="owner", related_name="tickets", null=True, on_delete=SET_NULL, editable=False)
    purchase_date = DateField("purchase date", editable=False)

    def __str__(self):
        return str(self.id)
