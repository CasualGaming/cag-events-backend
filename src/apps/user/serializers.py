from rest_framework.serializers import BaseSerializer, ModelSerializer

from .models import User, UserProfile


class UserListSerializer(BaseSerializer):
    """Serializes user to a username string."""

    def to_representation(self, instance):
        return instance.username


class UserProfileSerializer(ModelSerializer):
    """Serializes user profile part of user."""

    class Meta:
        model = UserProfile
        fields = ("birth_date", "gender", "country", "postal_code", "street_address", "phone_number", "membership_years", "is_member")


class UserSerializer(ModelSerializer):
    """Serializes all user attributes."""

    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "profile")


class UserPublicSerializer(ModelSerializer):
    """Serializes public user attributes."""

    class Meta:
        model = User
        fields = ("username", "first_name")
