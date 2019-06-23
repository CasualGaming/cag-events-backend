import datetime

from django.db import models
from django.db.models import Q

from apps.event.models import Event, TicketType

from authentication.models import User


class Layout(models.Model):
    title = models.CharField("title", max_length=50)
    description = models.CharField("description", max_length=250)
    seat_count = models.IntegerField("number of seats")
    template = models.TextField("svg layout for seating", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Layout, self).save(*args, **kwargs)
        else:
            super(Layout, self).save(*args, **kwargs)
            dependant_seatings = Seating.objects.filter(layout=self)
            for seating in dependant_seatings:
                seating.seat_count = self.seat_count
                seating.save()

    def __str__(self):
        return self.title


class Seating(models.Model):
    event = models.ForeignKey(Event)
    title = models.CharField("title", max_length=50)
    description = models.CharField("description", max_length=250)
    # This field is automatically updated to match the chosen layout. Change the chosen layout to alter this field.
    seat_count = models.IntegerField("number of seats", default=0)
    closing_date = models.DateTimeField("closing date")
    layout = models.ForeignKey(Layout)
    ticket_types = models.ManyToManyField(TicketType, blank=True, related_name="seatings")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.seat_count = self.layout.seat_count
            super(Seating, self).save(*args, **kwargs)
            self.populate_seats()
        else:
            self.seat_count = self.layout.seat_count
            super(Seating, self).save(*args, **kwargs)

    def get_user_registered(self):
        return map(lambda x: getattr(x, "user"), Seat.objects.filter(~Q(user=None), Q(seating=self)))

    def get_total_seats(self):
        return Seat.objects.filter(Q(seating=self)).order_by("placement")

    def get_seat_count(self):
        return Seat.objects.filter(Q(seating=self)).count()

    def is_open(self):
        return datetime.datetime.now() < self.closing_date

    def get_free_seats(self):
        return Seat.objects.filter(Q(user=None), Q(seating=self)).count()

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return "seating_details", (), {"event_id": self.event.id, "seating_id": self.id}

    def populate_seats(self):
        for k in range(0, self.seat_count):
            seat = Seat(seating=self, placement=(k + 1))
            seat.save()


class Seat(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    seating = models.ForeignKey(Seating)
    placement = models.IntegerField("placement id")

    def __str__(self):
        return str(self.id)
