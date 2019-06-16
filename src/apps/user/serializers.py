from rest_framework import serializers

from .models import User


class UserListSerializer(serializers.BaseSerializer):
    """Serializes user to a username string."""

    def to_representation(self, instance):
        return instance.username


class UserSerializer(serializers.ModelSerializer):
    """Serializes user."""

    birth_date = serializers.DateField(source="profile.birth_date")
    gender = serializers.CharField(source="profile.gender")
    country = serializers.CharField(source="profile.country")
    postal_code = serializers.CharField(source="profile.postal_code")
    street_address = serializers.CharField(source="profile.street_address")
    phone_number = serializers.CharField(source="profile.phone_number")
    membership_years = serializers.CharField(source="profile.membership_years")
    is_member = serializers.BooleanField(source="profile.is_member")

    class Meta:
        model = User
        fields = ("username",
                  "pretty_username",
                  "first_name",
                  "last_name",
                  "email",
                  "birth_date",
                  "gender",
                  "country",
                  "postal_code",
                  "street_address",
                  "phone_number",
                  "membership_years",
                  "is_member")


class PublicUserSerializer(serializers.ModelSerializer):
    """Serializes public user info."""

    class Meta:
        model = User
        fields = ("username", "pretty_username")
