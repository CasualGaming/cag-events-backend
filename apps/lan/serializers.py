# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import LAN


class LANSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LAN
        fields = "__all__"
