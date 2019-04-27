# -*- coding: utf-8 -*-

from rest_framework import viewsets

from core.permissions import IsStaffOrReadOnly

from .models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsStaffOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
