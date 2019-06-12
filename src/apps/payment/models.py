# -*- coding: utf-8 -*-

from django.db import models

from apps.event.models import Event
from apps.user.models import User


class Payment(models.Model):
    lan = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    payed_date = models.DateField()

    valid = models.BooleanField(default=True)
    invalid_date = models.DateField(null=True, blank=True)
