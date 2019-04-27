from rest_framework import viewsets
from core.permissions import IsStaffOrReadOnly

from .models import Sponsor, SponsorRelation
from .serializers import SponsorSerializer, SponsorRelationSerializer


class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [IsStaffOrReadOnly]


class SponsorRelationViewSet(viewsets.ModelViewSet):
    queryset = SponsorRelation.objects.all()
    serializer_class = SponsorRelationSerializer
    permission_classes = [IsStaffOrReadOnly]
