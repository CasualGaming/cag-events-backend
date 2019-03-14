from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Article
        fields = ('created', 'creator', 'title', 'body',)
