# -*- coding: utf-8 -*-
import uuid
from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
from django.dispatch import receiver


class UserProfile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    nick = models.CharField(_(u'nick'), max_length=20, help_text='Specify a nick name (display name).', db_index=True)
    date_of_birth = models.DateField(_(u'Date of birth'), default=date.today)
    address = models.CharField(_(u'Street address'), max_length=100)
    zip_code = models.CharField(_(u'Zip code'), max_length=4)
    phone = models.CharField(_(u'Phone number'), max_length=20)

    def __unicode__(self):
        return self.user.username

    def get_month(self):
        return '%02d' % self.date_of_birth.month

    def get_day(self):
        return '%02d' % self.date_of_birth.day

    def has_address(self):
        if self.address and self.zip_code:
            if not self.address.strip() or not self.zip_code.strip():
                return False
            return True
        return False

    @receiver(models.signals.post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(models.signals.post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


# class AliasType(models.Model):
#     description = models.CharField('Description', max_length=100, help_text='Short description')
#     profile_url = models.URLField('Profile url', blank=True, null=True, help_text='Url where profile info can be '
#                                   'retrieved. E.g. https://steamcommunity.com/id/')
#     activity = models.ManyToManyField('competition.Activity', related_name='alias_type')
#
#     def __unicode__(self):
#         return self.description
#
#
# class Alias(models.Model):
#     alias_type = models.ForeignKey(AliasType, on_delete=models.CASCADE)
#     nick = models.CharField('nick', max_length=40)
#     userprofile = models.ForeignKey(User, related_name='alias', on_delete=models.CASCADE)
#
#     def __unicode__(self):
#         return self.nick
#
#     class Meta:
#         unique_together = ("userprofile", "alias_type")
