# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Lan


class LanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lan
        fields = "__all__"
