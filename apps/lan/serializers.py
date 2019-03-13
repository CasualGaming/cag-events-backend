from rest_framework import serializers

from .models import LAN


class LANSerializer(serializers.ModelSerializer):
    class Meta:
        model = LAN
        fields = '__all__'
