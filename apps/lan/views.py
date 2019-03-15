from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from fearlessFred.permissions import IsStaffOrReadOnly
from apps.news.serializers import ArticleSerializer

from .models import LAN
from .serializers import LANSerializer


class LANViewSet(viewsets.ModelViewSet):
    queryset = LAN.objects.all()
    serializer_class = LANSerializer
    permission_classes = [IsStaffOrReadOnly]

    @action(detail=True)
    def news(self, request, *args, **kwargs):
        queryset = self.get_object().article_set.all()
        serializer = ArticleSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
