from rest_framework import viewsets, permissions

from .models import LAN
from .serializers import LANSerializer


class LANViewSet(viewsets.ModelViewSet):
    queryset = LAN.objects.all()
    serializer_class = LANSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
