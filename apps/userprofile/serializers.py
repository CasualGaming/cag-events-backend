from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('nick', 'date_of_birth', 'address', 'zip_code', 'phone')


class UserSerializerPrivate(serializers.ModelSerializer):
    profile = UserProfileSerializer(many=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'profile')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        UserProfile.objects.get_or_create(user=user, **profile_data)
        return user


class UserSerializerPublic(serializers.ModelSerializer):

    nick = serializers.CharField(source='profile.nick')

    class Meta:
        model = User
        fields = ('id', 'nick', 'first_name', 'last_name')
