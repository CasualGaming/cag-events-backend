from django.db import models

# from translatable.models import TranslatableModel, get_translation_model

from apps.event.models import Event


class Sponsor(models.Model):
    title = models.CharField("title", max_length=50)
    banner_url = models.CharField("banner", max_length=100, blank=True)
    logo_url = models.URLField("logo", max_length=100, blank=True)
    website = models.URLField("website", max_length=200, blank=True)
    events = models.ManyToManyField(Event, related_name="sponsors", through="SponsorRelation")

    def __str__(self):
        return self.title


# class SponsorTranslation(get_translation_model(Sponsor, "Sponsor")):
#     description = models.TextField("description")


class SponsorRelation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    # Higher priority means closer to the top of the sponsor list
    priority = models.IntegerField("priority", default=10)

    def __str__(self):
        return self.event.title + " + " + self.sponsor.title

    class Meta:
        ordering = ["-priority"]
