from rest_framework import viewsets

from .models import Article
from .serializers import ArticleSerializer
from fearlessFred.permissions import IsStaffOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsStaffOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
