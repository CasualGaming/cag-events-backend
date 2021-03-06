# import datetime
from django.db import models
# from translatable.models import TranslatableModel, get_translation_model

from apps.event.models import Event

from authentication.models import User


class Article(models.Model):
    title = models.CharField(max_length=100, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    relevant_to = models.ManyToManyField(Event, blank=True)
    creator = models.ForeignKey(User, blank=False, on_delete=models.PROTECT)
    body = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("created",)


# class Article():
#     pub_date = models.DateTimeField("published", default=datetime.datetime.now)
#     relevant_to = models.ManyToManyField(Event, blank=True)
#     pinned = models.BooleanField(default=False)
#
#     def count(self):
#         return len(Article.objects.all())
#
#     @models.permalink
#     def get_absolute_url(self):
#         return ("news_single", (), {"article_id": self.id})
#
#     class Meta:
#         ordering = ["-pub_date"]

# class ArticleTranslation(get_translation_model(Article, "Article")):
#     translated_title = models.CharField("title", max_length=50)
#     translated_body = models.TextField("body")
#
#     def __unicode__(self):
#         return self.translated_title
