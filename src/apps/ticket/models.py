from django.db.models import CharField, DateField, ForeignKey, IntegerField, Model, PROTECT, SET_NULL

from apps.event.models import Event

from authentication.models import User


class TicketType(Model):
    short_title = CharField(max_length=20, verbose_name="short title", help_text="A short, non-unique title to show to users.")
    long_title = CharField(unique=True, max_length=50, verbose_name="long title", help_text="A longer, unique title.")
    event = ForeignKey(Event, related_name="ticket_types", on_delete=PROTECT, verbose_name="event", help_text="Which event this is for.")
    priority = IntegerField(default=10, verbose_name="priority", help_text="Lower priority shows it higher on the list among other ticket types.")

    def __str__(self):
        return self.long_title


class Ticket(Model):
    ticket_type = ForeignKey(TicketType, related_name="tickets", on_delete=PROTECT, editable=False, verbose_name="type", help_text="Ticket type.")
    owner = ForeignKey(User, related_name="tickets", null=True, on_delete=SET_NULL, editable=False, verbose_name="owner", help_text="The user owning the ticket.")
    purchase_date = DateField(editable=False, verbose_name="purchase date", help_text="When it was bought.")

    def __str__(self):
        return str(self.id)
