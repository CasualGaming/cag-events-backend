from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import BooleanField, CharField, CheckConstraint, DateTimeField, F, ForeignKey, IntegerField, Model, PROTECT, Q, SET_NULL, TextField, UniqueConstraint

from apps.event.models import Attendance, Event

from authentication.models import User


class TicketType(Model):
    # TODO prevent changing type, event, grants-entrance, for-seating, requires-ticket
    simple_title = CharField("simple title", max_length=20, help_text="A short title for use within the context of an event. Must be unique within the event.")
    unique_title = CharField("unique title", unique=True, max_length=50, help_text="A unique version of the short title, for use outside the context of an event.")
    # Prevents deleting the event
    event = ForeignKey(Event, verbose_name="event", related_name="ticket_types", on_delete=PROTECT)
    is_enabled = BooleanField("is enabled", default=False, help_text="If this ticket type is not disabled.")
    visual_priority = IntegerField("visual priority", validators=[MinValueValidator(0)], default=10,
                                   help_text="Lower priority value shows it higher on the list among other ticket types.")
    max_count = IntegerField("max count", validators=[MinValueValidator(0)], default=0,
                             help_text="The max number of tickets of this type. If this is a seating ticke type, the actual max number is the minimum of this and the number of available seats for this type. 0 means unlimited.")
    max_user_purchase_count = IntegerField("max user purchase count", validators=[MinValueValidator(0)], default=0,
                                           help_text="The max number of tickets a user may purchase. 0 means unlimited.")
    max_user_assignment_count = IntegerField("max user assignment count", validators=[MinValueValidator(0)], default=1,
                                             help_text="The max number of tickets a user may be assigned. 0 means unlimited. Should be 1 for normal seating tickets.")
    grants_entrance = BooleanField("grants entrance", default=True, help_text="If being assigned a ticket of this type grants entrance to the event.")
    is_for_seating = BooleanField("for seating", default=True, help_text="If this is a seating ticket.")
    required_ticket_type = ForeignKey("self", verbose_name="required ticket type", related_name="requiring_ticket_types", null=True, blank=True, on_delete=PROTECT,
                                      help_text="If set, tickets of this type can't be assigned to a user before the user has a ticket of the other type assigned it first.")
    valid_start_time = DateTimeField("validity start time", null=True, blank=True, help_text="Start of the period this ticket type is valid for the event.")
    valid_end_time = DateTimeField("validity end time", null=True, blank=True, help_text="End of the period this ticket type is valid for the event.")
    is_valid_all_event = BooleanField("valid all event", default=True, help_text="If this ticket type is valid the entire event. Enabling this removes validity start and end time.")
    description = TextField("description")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["simple_title", "event"], name="ticket_ticket_type_unique_simple_title_event"),
            CheckConstraint(check=(Q(is_valid_all_event=True) | Q(valid_end_time__gt=F("valid_start_time"))), name="ticket_tickettype_validity_ends_after_start"),
        ]

    def __str__(self):
        return self.long_title

    def clean(self):
        if self.required_ticket_type is not None:
            if self.required_ticket_type.event_id != self.event_id:
                raise ValidationError("The required ticket type is for another event.")

        if self.is_valid_all_event:
            self.valid_start_time = None
            self.valid_end_time = None
        elif self.valid_start_time is None or self.valid_end_time is None:
            raise ValidationError("Missing validity start and/or end time.")
        elif self.valid_start_time >= self.valid_end_time:
            raise ValidationError("The validity must start before it ends.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(TicketType, self).save(*args, **kwargs)

    @property
    def total_count(self):
        count = self.max_count
        if self.is_for_seating:
            seat_count = 0
            for area_layout in self.applicable_rows.select_related("area__area_layout").all():
                seat_count += area_layout.seat_count
            count = min(count, seat_count)
        return count

    @property
    def total_available_count(self):
        existing_count = self.tickets.count()
        if self.is_for_seating:
            existing_seat_count = self.applicable_rows.get("area__seats__count")
            existing_count = max(existing_count, existing_seat_count)
        return self.total_count - existing_count


class Ticket(Model):
    # TODO prevent changing ticket type
    # Prevents deleting the ticket type
    ticket_type = ForeignKey(TicketType, verbose_name="type", related_name="tickets", on_delete=PROTECT)
    # Set to NULL if the owner is deleted
    owner = ForeignKey(User, verbose_name="owner", related_name="owned_tickets", null=True, default=None, on_delete=SET_NULL,
                       help_text="The person owning and managing this ticket.")
    # Set to NULL if the assignee is deleted
    assignee = ForeignKey(User, verbose_name="assignee", related_name="assigned_tickets", null=True, blank=True, on_delete=SET_NULL,
                          help_text="The person using this ticket. If this is set, the ticket is activated.")
    # Prevents deleting attendance as long as any ticket exists
    attendance = ForeignKey(Attendance, verbose_name="attendance", related_name="tickets", null=True, blank=True, on_delete=PROTECT, editable=False)
    # TODO actions for disable, regen and transfer
    transfer_code = CharField("transfer code", max_length=50, db_index=True, blank=True, editable=False,
                              help_text="A code used for transferring the ticket to another user by giving the other user the code. Can be regenerated.")

    class Meta:
        default_permissions = ["view", "change"]

    def __str__(self):
        return "{0} #{1}".format(self.ticket_type, self.id)

    def clean(self):
        if self.assignee is not None:
            self.attendance = Attendance.objects.get_or_create(event=self.ticket_type.event, user=self.assignee)[0]
        else:
            self.attendance = None

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Ticket, self).save(*args, **kwargs)

    @property
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
            ("ticket_type.view_disabled", "View disabled ticket types"),
            ("ticket.*", "Ticket admin"),
            ("ticket.list_all", "List all tickets"),
            ("ticket.view_all", "View all tickets"),
            ("ticket.create", "Manually create tickets"),
            ("ticket.change", "Manually change tickets"),
            ("ticket.delete", "Manually delete tickets"),
        ]
