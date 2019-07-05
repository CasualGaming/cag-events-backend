from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import BooleanField, CASCADE, CharField, CheckConstraint, F, FloatField, ForeignKey, Index, IntegerField, Model, OneToOneField, PROTECT, Q, URLField, UniqueConstraint

from apps.event.models import Event
from apps.ticket.models import Ticket, TicketType


class AreaLayout(Model):
    """
    An area layout used for seatings. Contains attributes for rendering it as an image.
    """
    title = CharField("title", unique=True, max_length=50, help_text="A unique title.")
    is_enabled = BooleanField("is enabled", default=False, help_text="If this layout is currently available to users.")
    width = FloatField("width", validators=[MinValueValidator(0)], help_text="Width in meters of the area.")
    height = FloatField("height", validators=[MinValueValidator(0)], help_text="Height in meters of the area.")
    background_url = URLField("background URL", blank=True, help_text="URL for the area background image containing walls, exits, etc.")

    def __str__(self):
        return self.title

    @property
    def seat_count(self):
        # TODO test
        # return self.row_layouts.annotate(seat_count=(F("seat_count_horizontal") * F("seat_count_vertical"))).aggregate(Sum("seat_count"))
        return self.row_layouts.annotate(seat_count=(F("seat_count_horizontal") * F("seat_count_vertical"))).get("seat_count__sum")


class RowLayout(Model):
    """
    A row in an area layout. Contains attributes for rendering the row in the area image.
    """
    # TODO prevent changing area layout and row number
    # Gets deleted if the area layout is deleted
    area_layout = ForeignKey(AreaLayout, verbose_name="area layout", related_name="row_layouts", on_delete=CASCADE)
    row_number = IntegerField("row number", validators=[MinValueValidator(1)], help_text="Unique, positive row number within the area.")
    description = CharField("description", blank=True, max_length=100, help_text="A short row description for users.")
    seat_count_horizontal = IntegerField("horizontal seat count", validators=[MinValueValidator(1)], help_text="Number of seats in the horizontal dimension (stacked on the non-wide sides of seats).")
    seat_count_vertical = IntegerField("vertical seat count", validators=[MinValueValidator(1)], help_text="Number of seats in the vertical dimension (stacked on the wide sides of seats).")
    offset_horizontal = FloatField("horizontal offset", default=0, help_text="Offset in meters from the left wrt. the area.")
    offset_vertical = FloatField("vertical offset", default=0, help_text="Offset in meters from the top wrt. the area.")
    rotation = IntegerField("rotation", default=0, validators=[MinValueValidator(0), MaxValueValidator(359)], help_text="Counter-clockwise rotation in degrees wrt. the area. Must be in range [0, 360).")
    seat_width = FloatField("seat width", validators=[MinValueValidator(0)], help_text="Width in meters of a seat in this row.")
    seat_height = FloatField("seat height", validators=[MinValueValidator(0)], help_text="Height in meters of a seat in this row.")
    seat_spacing_horizontal = FloatField("horizontal seat spacing", validators=[MinValueValidator(0)], default=0, help_text="Spacing in meters between seats, horizontally.")
    seat_spacing_vertical = FloatField("vertical seat spacing", validators=[MinValueValidator(0)], default=0, help_text="Spacing in meters between seats, vertically.")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["area_layout", "row_number"], name="seating_row_layout_unique_layout_area_row_number"),
            CheckConstraint(check=Q(row_number__gte=1), name="seating_row_layout_row_number_gte_1"),
        ]
        indexes = [Index(fields=["area_layout", "row_number"])]

    def __str__(self):
        return "{0} - Row {1}".format(self.area_layout, self.row_number)

    @property
    def seat_count(self):
        return self.seat_count_horizontal * self.seat_count_vertical


class Seating(Model):
    """
    A seating for an event. Contains areas of rows of seats.
    """
    # TODO prevent changing event
    # Prevents deleting the event
    event = OneToOneField(Event, verbose_name="event", primary_key=True, related_name="seating", on_delete=PROTECT)
    is_enabled = BooleanField("is enabled", default=False, help_text="If this seating is currently available to users.")

    def __str__(self):
        return str(self.event)

    @property
    def seat_count(self):
        # TODO replace with query
        return sum(map(lambda x: x.seat_count, self.areas.select_related("area_layout").all()))


class Area(Model):
    """
    For adding areas to a seating. Roughly the same as a many-to-many relation between Seating and AreaLayout with some extra attributes.
    """
    # TODO prevent changing seating and layout
    # Prevents deleting the seating
    seating = ForeignKey(Seating, verbose_name="seating", related_name="areas", on_delete=PROTECT)
    # Prevents deleting the area layout
    area_layout = ForeignKey(AreaLayout, verbose_name="area layout", related_name="areas", on_delete=PROTECT)
    title = CharField("title", max_length=50, help_text="A non-unique title visible to users.")
    area_code = CharField("area code", max_length=4, help_text="Unique, non-empty area code for an area within a seating. Max 4 characters.")
    description = CharField("description", blank=True, max_length=100, help_text="A short area description for users.")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["seating", "area_code"], name="seating_area_unique_area_code"),
        ]
        indexes = [Index(fields=["seating", "area_code"])]

    def __str__(self):
        return "{0} - Area {1}".format(self.seating, self.area_code)


class RowTicketType(Model):
    """
    For specifying which ticket types are available for individual rows in a seating.
    """
    # TODO prevent changing anything
    # Gets deleted if the area is deleted
    area = ForeignKey(Area, verbose_name="area", related_name="row_ticket_types", on_delete=CASCADE)
    row_number = IntegerField("row number", validators=[MinValueValidator(1)], help_text="Row number in the area layout.")
    # Gets deleted if the ticket type is deleted
    ticket_type = ForeignKey(TicketType, verbose_name="ticket types", related_name="applicable_rows", on_delete=CASCADE,
                             help_text="A ticket type available for this seating row.")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["area", "row_number", "ticket_type"], name="seating_row_ticket_type_unique_area_row_ticket_type"),
        ]

    def __str__(self):
        return "{0} - {1} - {2}".format(self.area, self.row_number, self.ticket_type)

    def clean(self):
        if self.area.seating.event != self.ticket_type.event:
            raise ValidationError("The seating and ticket type are for different events.")
        if not RowLayout.objects.filter(area_layout=self.area.area_layout_id, row_number=self.row_number).exists():
            raise ValidationError("Row number {0} does not exist in the area layout.".format(self.row_number))

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(RowTicketType, self).save(*args, **kwargs)


class Seat(Model):
    """
    A seat in a row in an area in a seating. If a seat exists without an assigned ticket, it means it's reserved.
    """
    # TODO prevent changing area/row_num/seat/num
    # Prevents deleting the area
    area = ForeignKey(Area, verbose_name="area", related_name="seats", on_delete=PROTECT, help_text="Seating area.")
    row_number = IntegerField("row number", validators=[MinValueValidator(1)], help_text="Row number within area.")
    seat_number = IntegerField("seat number", validators=[MinValueValidator(1)], help_text="Seat number within row. Horizontal-major seat numbering.")
    # Gets deleted if the ticket is deleted, if there is a ticket assigned
    assigned_ticket = OneToOneField(Ticket, verbose_name="assigned ticket", related_name="seat", on_delete=CASCADE, null=True, blank=True,
                                    help_text="Ticket assigned to this seat.")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["area", "row_number", "seat_number"], name="seating_seat_unique_area_row_seat"),
            CheckConstraint(check=Q(row_number__gte=1), name="seating_seat_row_number_gte_1"),
            CheckConstraint(check=Q(seat_number__gte=1), name="seating_seat_seat_number_gte_1"),
        ]
        default_permissions = ["view", "change"]

    def __str__(self):
        return "{0} - {1}/{2}/{3}".format(self.area.seating, self.area.area_code, self.row_number, self.seat_number)

    def clean(self):
        if self.assigned_ticket is not None:
            if self.assigned_ticket.ticket_type.event_id != self.area.seating_id:
                raise ValidationError("The assigned ticket is for the wrong event.")

        row_layout_qs = RowLayout.objects.filter(area_layout=self.area.area_layout_id, row_number=self.row_number)
        if not row_layout_qs.exists():
            raise ValidationError("Row number does not exist in the area layout.")

        row_layout = row_layout_qs[0]
        if self.seat_number > row_layout.seat_count:
            raise ValidationError("Seat number higher than seat count in row layout.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Seat, self).save(*args, **kwargs)

    @property
    def is_taken(self):
        return self.assigned_ticket is not None

    @property
    def is_reserved(self):
        return self.assigned_ticket is None


class Permissions(Model):
    class Meta:
        managed = False
        default_permissions = []
        permissions = [
            ("*", "Seating app admin"),
            ("layout.*", "Seating layout admin"),
            ("layout.list", "List seating layouts"),
            ("layout.create", "Create seating layouts"),
            ("layout.change", "Change seating layouts"),
            ("layout.delete", "Delete seating layouts"),
            ("layout.view_disabled", "View disabled seating layouts"),
            ("layout.generate_image", "Generate seating layout images"),
            ("seating.*", "Seating admin"),
            ("seating.list", "List seatings"),
            ("seat.*", "Seat admin"),
            ("seat.create", "Manually create seats"),
            ("seat.change", "Manually change seats"),
            ("seat.delete", "Manually delete seats"),
            ("seat.view_ticket", "View tickets assigned to seats"),
            ("seat.view_hidden_user", "View hidden users assigned to seats"),
        ]
