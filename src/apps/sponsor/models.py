# -*- coding: utf-8 -*-

from django.db import models

# from translatable.models import TranslatableModel, get_translation_model

from apps.event.models import Event


class Sponsor(models.Model):
    title = models.CharField("name", max_length=50)
    banner = models.CharField("Banner url", max_length=100, blank=True,
                              help_text="Use a mirrored image of at least a height of 150px.")
    logo = models.CharField("Logo url", max_length=100, blank=True,
                            help_text="Use a mirrored image of at least a height of 150px.")
    website = models.URLField("website", max_length=200)

    def __unicode__(self):
        return self.title


# class SponsorTranslation(get_translation_model(Sponsor, "Sponsor")):
#     description = models.TextField("description")


class SponsorRelation(models.Model):
    lan = models.ForeignKey(Event, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    priority = models.IntegerField("priority", help_text="higher priority means closer to the top of the sponsor list.")

    # def __unicode__(self):
    #     return unicode(self.lan) + " - " + unicode(self.sponsor)

    class Meta:
        ordering = ["-priority"]
