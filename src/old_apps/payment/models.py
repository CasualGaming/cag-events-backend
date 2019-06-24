from django.db import models

from apps.event.models import Event

from authentication.models import User


class Payment(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    payed_date = models.DateField()

    valid = models.BooleanField(default=True)
    invalid_date = models.DateField(null=True, blank=True)
