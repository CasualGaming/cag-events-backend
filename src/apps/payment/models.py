# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

from apps.lan.models import Lan


class Payment(models.Model):
    lan = models.ForeignKey(Lan)
    user = models.ForeignKey(User)
    payed_date = models.DateField()

    valid = models.BooleanField(default=True)
    invalid_date = models.DateField(null=True, blank=True)