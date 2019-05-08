# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")

    class Meta:
        model = Article
        fields = "__all__"
