from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.article.serializers import ArticleSerializer
from apps.sponsor.serializers import SponsorRelationSerializer

# from auth.permissions import IsStaffOrReadOnly

from .models import Event
from .permissions import EventPermission
from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [EventPermission]

    @action(url_path="articles", methods=["get"], detail=True, permission_classes=[])
    def get_articles(self, request, *args, **kwargs):
        queryset = self.get_object().article_set.all()
        serializer = ArticleSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    @action(url_path="articles", methods=["get"], detail=True, permission_classes=[])
    def get_sponsors(self, request, *args, **kwargs):
        queryset = self.get_object().sponsorrelation_set.all()
        serializer = SponsorRelationSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)
