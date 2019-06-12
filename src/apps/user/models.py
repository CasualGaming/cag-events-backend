# -*- coding: utf-8 -*-

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _
# from django.dispatch import receiver


class User(AbstractUser):
    uuid = models.UUIDField("uuid", primary_key=True, db_index=True, default=uuid.uuid4)
    username = models.CharField("Username", unique=True, db_index=True, max_length=20)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    birth_date = models.DateField(_(u"date of birth"), null=True, blank=True)
    gender = models.CharField(_(u"gender"), null=True, blank=True, max_length=50)
    country = models.CharField(_(u"country"), null=True, blank=True, max_length=50)
    postal_code = models.CharField(_(u"postal code"), null=True, blank=True, max_length=10)
    street_address = models.CharField(_(u"street address"), null=True, blank=True, max_length=100)
    phone_number = models.CharField(_(u"phone number"), null=True, blank=True, max_length=20)

    def __str__(self):
        return self.user.username

    def get_month(self):
        return "{0:02d}".format(self.birth_date.month)

    def get_day(self):
        return "{0:02d}".format(self.birth_date.day)

    def has_address(self):
        return self.street_address and self.postal_code


# class AliasType(models.Model):
#     description = models.CharField("Description", max_length=100, help_text="Short description")
#     profile_url = models.URLField("Profile url", blank=True, null=True, help_text="Url where profile info can be "
#                                   "retrieved. E.g. https://steamcommunity.com/id/")
#     activity = models.ManyToManyField("competition.Activity", related_name="alias_type")
#
#     def __unicode__(self):
#         return self.description
#
#
# class Alias(models.Model):
#     alias_type = models.ForeignKey(AliasType, on_delete=models.CASCADE)
#     nick = models.CharField("nick", max_length=40)
#     userprofile = models.ForeignKey(User, related_name="alias", on_delete=models.CASCADE)
#
#     def __unicode__(self):
#         return self.nick
#
#     class Meta:
#         unique_together = ("userprofile", "alias_type")
