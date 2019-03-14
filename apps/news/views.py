from rest_framework import viewsets, permissions

from .models import Article
from .serializers import ArticleSerializer
#from .permissions import IsAdminOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
