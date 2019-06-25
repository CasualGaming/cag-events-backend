from django.db.models import BooleanField, CASCADE, CharField, CheckConstraint, FloatField, ForeignKey, Index, IntegerField, ManyToManyField, Model, OneToOneField, PROTECT, Q, SET_NULL, URLField, UniqueConstraint

from apps.event.models import Event
from apps.ticket.models import Ticket, TicketType


class AreaLayout(Model):
    short_title = CharField("short title", max_length=20, help_text="A short, non-unique title to show to users.")
    long_title = CharField("long title", unique=True, max_length=50, help_text="A longer, unique title.")
    background_url = URLField("background URL", blank=True, help_text="URL for the area background image containing walls, exits, etc.")
    background_offset = FloatField("background offset", default=0, help_text="Offset in meters of the background image from the top, left corner. May be negative.")
    background_width = FloatField("background width", help_text="Width in meters of the background image.")

    def __str__(self):
        return self.long_title


class RowLayout(Model):
    area_layout = ForeignKey(AreaLayout, verbose_name="area layout", related_name="row_layouts", on_delete=CASCADE)
    row_number = IntegerField("row number", help_text="Unique, positive row number within the area.")
    offset = FloatField("offset", default=0, help_text="Offset in meters wrt. the area.")
    rotation = FloatField("rotation", default=0, help_text="Rotation in radians wrt. the area.")
    seat_width = FloatField("seat width", help_text="Width in meters of a seat in this row.")
    seat_height = FloatField("seat height", help_text="Height in meters of a seat in this row.")

    def __str__(self):
        return self.long_title

    class Meta:
        constraints = [
            UniqueConstraint(fields=["area_layout", "row_number"], name="unique_layout_area_row_number"),
            CheckConstraint(check=Q(row_number__gte=1), name="row_number_gte_1"),
        ]
        indexes = [Index(fields=["area_layout", "row_number"])]


class Seating(Model):
    event = OneToOneField(Event, verbose_name="event", primary_key=True, related_name="seating", on_delete=PROTECT)
    areas = ManyToManyField(AreaLayout, verbose_name="areas", related_name="seatings", through="SeatingArea")
    is_active = BooleanField("is active", default=False, help_text="If this seating is currently available to users.")

    def __str__(self):
        return str(self.event)


class SeatingArea(Model):
    seating = ForeignKey(Seating, verbose_name="seating", on_delete=PROTECT)
    area_layouts = ForeignKey(AreaLayout, verbose_name="area", on_delete=PROTECT)
    area_code = CharField("area code", max_length=4, help_text="Unique, non-empty area code for an area within a seating.")

    def __str__(self):
        return "{0} – {1}".format(self.seating, self.area_code)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["seating", "area_code"], name="unique_seating_area_code"),
        ]
        indexes = [Index(fields=["seating", "area_code"])]


class SeatingRowTicketTypes(Model):
    seating_area = ForeignKey(SeatingArea, verbose_name="seating area", related_name="seating_rows", on_delete=PROTECT)
    row_number = IntegerField("row number", help_text="Row number in the area layout.")
    ticket_type = ForeignKey(TicketType, verbose_name="ticket types", related_name="seating_rows", on_delete=PROTECT,
                             help_text="A ticket type available for this seating row.")

    def __str__(self):
        return "{0} – {1} – {2}".format(self.seating_area, self.row_number, self.ticket_type)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["seating_area", "row_number", "ticket_type"], name="unique_seating_area_row_ticket_type"),
        ]


class Seat(Model):
    seating = ForeignKey(Seating, verbose_name="seating", related_name="seats", on_delete=PROTECT)
    seating_area = ForeignKey(SeatingArea, verbose_name="seating area", related_name="seats", on_delete=PROTECT, help_text="Area in the seating.")
    row_number = IntegerField("row number", help_text="Row number in the area.")
    seat_number = IntegerField("seat number", help_text="Seat number in the row.")
    is_reserved = BooleanField("is reserved", default=False, help_text="If this seat can not be tied to a ticket.")
    assigned_ticket = ForeignKey(Ticket, verbose_name="assigned ticket", related_name="seats", on_delete=SET_NULL, null=True, blank=True,
                                 help_text="Ticket tied to this seat if it is assigned.")

    def __str__(self):
        return "{0} – {1}/{2}/{3}".format(self.seating, self.area.area_code, self.row_number, self.seat_number)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["seating_area", "row_number", "seat_number"], name="unique_seating_area_row_seat"),
            # Make sure a reserved seat is not assigned and vice versa
            CheckConstraint(check=(Q(assigned_ticket__exact=None) | Q(is_reserved__exact=False)), name="seat_not_reserved_and_assigned"),
        ]
