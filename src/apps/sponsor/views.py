from rest_framework import viewsets

from auth.permissions import IsStaffOrReadOnly

from .models import Sponsor, SponsorRelation
from .serializers import SponsorRelationSerializer, SponsorSerializer


class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [IsStaffOrReadOnly]


class SponsorRelationViewSet(viewsets.ModelViewSet):
    queryset = SponsorRelation.objects.all()
    serializer_class = SponsorRelationSerializer
    permission_classes = [IsStaffOrReadOnly]
