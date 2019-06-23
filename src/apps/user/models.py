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
