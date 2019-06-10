# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.news.serializers import ArticleSerializer
from apps.sponsor.serializers import SponsorRelationSerializer

from auth.permissions import IsStaffOrReadOnly

from .models import Lan
from .serializers import LanSerializer


class LanViewSet(viewsets.ModelViewSet):
    queryset = Lan.objects.all()
    serializer_class = LanSerializer
    permission_classes = [IsStaffOrReadOnly]

    @action(detail=True)
    def news(self, request, *args, **kwargs):
        queryset = self.get_object().article_set.all()
        serializer = ArticleSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True)
    def sponsor(self, request, *args, **kwargs):
        queryset = self.get_object().sponsorrelation_set.all()
        serializer = SponsorRelationSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)
