from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import BooleanField, CASCADE, CharField, DateTimeField, F, ForeignKey, Index, IntegerField, Model, Q, SlugField, TextField
from django.db.models.constraints import CheckConstraint, UniqueConstraint

from authentication.models import User


class Event(Model):
    """An event, such as a LAN party or game night."""
    title = CharField("title", unique=True, max_length=50)
    slug = SlugField("slug", unique=True, db_index=True, max_length=20,
                     help_text="Short, unique text for this event, used in URLs and such. Changing this may break existing links.")
    start_time = DateTimeField("start date and time")
    end_time = DateTimeField("end date and time")
    location = CharField("location", blank=True, max_length=100)
    require_ticket = BooleanField("require ticket", default=True, help_text="If a ticket with the grants-entrance flag is required to enter.")
    age_requirement = IntegerField("age requirement", validators=[MinValueValidator(0)], default=0,
                                   help_text="The lower age requirement for attending this event. 0 means no requirement.")
    map_url = CharField("map URL", blank=True, max_length=300, help_text="URL for an embedded map.")
    banner_url = CharField("banner URL", blank=True, max_length=300, help_text="URL for the banner image.")
    description = TextField("description")

    class Meta:
        ordering = ["start_time"]
        constraints = [
            CheckConstraint(check=Q(end_time__gt=F("start_time")), name="event_event_ends_after_start"),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("The event must start before it ends.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Event, self).save(*args, **kwargs)


class Attendance(Model):
    """
    An attendance for a user at an event.
    The existance of an attendance means the user intend to attend the event.
    Users do not need a ticket to register intent to attend,
    but all users with a ticket should automatically attend and should no longer have an option to not attend.
    Arrivals are registered by setting the arrival time.
    """
    # TODO prevent changing event and user
    # Gets deleted if the event is deleted
    event = ForeignKey(Event, verbose_name="event", related_name="attendances", on_delete=CASCADE)
    # Gets deleted if the user is deleted
    user = ForeignKey(User, verbose_name="user", related_name="attendances", on_delete=CASCADE)
    arrival_time = DateTimeField("arrival time", null=True, blank=True, help_text="When the user arrived at the event.")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["event", "user"], name="event_attendance_unique_event_user"),
        ]
        indexes = [Index(fields=["event", "user"])]

    def __str__(self):
        return self.title

    @property
    def has_arrived(self):
        return self.arrival_time is not None

    @property
    def has_ticket(self):
        return self.tickets.exists()


class Permissions(Model):
    class Meta:
        managed = False
        default_permissions = []
        permissions = [
            ("*", "Event app admin"),
            ("event.*", "Event admin"),
            ("event.create", "Create events"),
            ("event.change", "Change events"),
            ("event.delete", "Delete events"),
            ("attendance.*", "Arrival admin"),
            ("attendance.view", "Show attendances"),
            ("attendance.create", "Manually create attendances"),
            ("attendance.change", "Manually change attendances"),
            ("attendance.delete", "Manually delete attendances"),
            ("attendance.register_arrival", "Register arrivals for attendances"),
            ("attendance.attend", "Add attendances for one self"),
            ("attendance.unattend", "Remove attendances for one self"),
        ]
