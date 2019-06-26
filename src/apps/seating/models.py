
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import BooleanField, CASCADE, CharField, CheckConstraint, FloatField, ForeignKey, Index, IntegerField, Model, OneToOneField, PROTECT, Q, SET_NULL, URLField, UniqueConstraint

from apps.event.models import Event
from apps.ticket.models import Ticket, TicketType


class AreaLayout(Model):
    """
    An area layout used for seatings. Contains attributes for rendering it as an image.
    """
    short_title = CharField("short title", max_length=20, help_text="A short, non-unique title to show to users.")
    long_title = CharField("long title", unique=True, max_length=50, help_text="A long, unique title to show behind the scenes.")
    background_url = URLField("background URL", blank=True, help_text="URL for the area background image containing walls, exits, etc.")
    background_offset_right = FloatField("background offset right", default=0, help_text="Offset in meters of the background image from the left. May be negative.")
    background_offset_down = FloatField("background offset down", default=0, help_text="Offset in meters of the background image from the top. May be negative.")
    background_width = FloatField("background width", help_text="Width in meters of the background image.")
    is_active = BooleanField("is active", default=False, help_text="If this layout is currently available to users.")

    def __str__(self):
        return self.long_title

    class Meta:
        permissions = [
            ("area_layout.list", "Can list layouts"),
            ("area_layout.view_inactive", "Can view inactive layouts"),
        ]


class RowLayout(Model):
    """
    A row in an area layout. Contains attributes for rendering the row in the area image.
    """
    area_layout = ForeignKey(AreaLayout, verbose_name="area layout", related_name="row_layouts", on_delete=CASCADE)
    row_number = IntegerField("row number", validators=[MinValueValidator(1)], help_text="Unique, positive row number within the area.")
    seat_count_horizontal = IntegerField("horizontal seat count", help_text="Number of seats in the horizontal dimension (stacked on the non-wide sides of seats).")
    seat_count_vertical = IntegerField("vertical seat count", help_text="Number of seats in the vertical dimension (stacked on the wide sides of seats).")
    offset_right = FloatField("offset right", default=0, help_text="Offset in meters from the left wrt. the area.")
    offset_down = FloatField("offset down", default=0, help_text="Offset in meters from the top wrt. the area.")
    rotation = IntegerField("rotation", default=0, validators=[MinValueValidator(0), MaxValueValidator(359)], help_text="Counter-clockwise rotation in degrees wrt. the area. Must be in range [0, 360).")
    seat_width = FloatField("seat width", help_text="Width in meters of a seat in this row.")
    seat_height = FloatField("seat height", help_text="Height in meters of a seat in this row.")
    seat_spacing_horizontal = FloatField("horizontal seat spacing", default=0, help_text="Spacing in meters between seats, horizontally.")
    seat_spacing_vertical = FloatField("vertical seat spacing", default=0, help_text="Spacing in meters between seats, vertically.")

    def __str__(self):
        return "{0} – Row {1}".format(self.area_layout, self.row_number)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["area_layout", "row_number"], name="unique_layout_area_row_number"),
            CheckConstraint(check=Q(row_number__gte=1), name="row_number_gte_1"),
        ]
        indexes = [Index(fields=["area_layout", "row_number"])]


class Seating(Model):
    """
    A seating for an event. Contains areas of rows of seats.
    """
    event = OneToOneField(Event, verbose_name="event", primary_key=True, related_name="seating", on_delete=PROTECT)
    is_active = BooleanField("is active", default=False, help_text="If this seating is currently available to users.")

    def __str__(self):
        return str(self.event)

    class Meta:
        permissions = [
            ("seating.list", "Can list seatings"),
            ("seating.view_inactive", "Can view inactive seatings"),
        ]


class Area(Model):
    """
    For adding areas to a seating. Roughly the same as a many-to-many relation between Seating and AreaLayout with some extra attributes.
    """
    seating = ForeignKey(Seating, verbose_name="seating", related_name="areas", on_delete=PROTECT)
    area_layout = ForeignKey(AreaLayout, verbose_name="area layout", related_name="areas", on_delete=PROTECT)
    area_code = CharField("area code", max_length=4, help_text="Unique, non-empty area code for an area within a seating. Max 4 characters.")

    def __str__(self):
        return "{0} – {1}".format(self.seating, self.area_code)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["seating", "area_code"], name="unique_seating_area_code"),
        ]
        indexes = [Index(fields=["seating", "area_code"])]


class RowTicketTypes(Model):
    """
    For specifying which ticket types are available for individual rows in a seating.
    """
    area = ForeignKey(Area, verbose_name="area", related_name="rows", on_delete=PROTECT)
    row_number = IntegerField("row number", help_text="Row number in the area layout.")
    ticket_type = ForeignKey(TicketType, verbose_name="ticket types", related_name="seating_rows", on_delete=PROTECT,
                             help_text="A ticket type available for this seating row.")

    def __str__(self):
        return "{0} – {1} – {2}".format(self.area, self.row_number, self.ticket_type)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["area", "row_number", "ticket_type"], name="unique_area_row_ticket_type"),
        ]


class Seat(Model):
    """
    A seat in a row in an area in a seating. Should be generated automatically when a seating area is created.
    """
    seating = ForeignKey(Seating, verbose_name="seating", related_name="seats", on_delete=PROTECT)
    area = ForeignKey(Area, verbose_name="area", related_name="seats", on_delete=PROTECT, help_text="Area in the seating.")
    row_number = IntegerField("row number", help_text="Row number in the area.")
    seat_number = IntegerField("seat number", help_text="Seat number in the row.")
    is_reserved = BooleanField("is reserved", default=False, help_text="If this seat can not be tied to a ticket.")
    assigned_ticket = ForeignKey(Ticket, verbose_name="assigned ticket", related_name="seats", on_delete=SET_NULL, null=True, blank=True,
                                 help_text="Ticket tied to this seat if it is assigned.")

    def clean(self):
        if self.assigned_ticket is not None and self.is_reserved:
            raise ValidationError("The seat cannot be both reserved and assigned a ticket")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Seat, self).save(*args, **kwargs)

    def __str__(self):
        return "{0} – {1}/{2}/{3}".format(self.seating, self.area.area_code, self.row_number, self.seat_number)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["area", "row_number", "seat_number"], name="unique_area_row_seat"),
            # Make sure a reserved seat is not assigned and vice versa
            CheckConstraint(check=(Q(assigned_ticket__exact=None) | Q(is_reserved__exact=False)), name="seat_not_reserved_and_assigned"),
        ]
        default_permissions = ()
