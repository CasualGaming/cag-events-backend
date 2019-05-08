# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Sponsor, SponsorRelation


class SponsorSerializer(serializers.HyperlinkedModelSerializer):
    uid = serializers.ReadOnlyField()

    class Meta:
        model = Sponsor
        fields = "__all__"


class SponsorRelationSerializer(serializers.HyperlinkedModelSerializer):
    sponsor = SponsorSerializer(read_only=True)

    class Meta:
        model = SponsorRelation
        fields = ["priority", "sponsor"]
