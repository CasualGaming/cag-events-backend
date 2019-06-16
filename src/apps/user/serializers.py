from drf_dynamic_fields import DynamicFieldsMixin

from rest_framework.serializers import BaseSerializer, BooleanField, CharField, DateField, ModelSerializer

from .models import User


class UsernameUserSerializer(BaseSerializer):
    """Serializes user to a username string."""

    def to_representation(self, instance):
        return instance.username


class UserSerializer(DynamicFieldsMixin, ModelSerializer):
    """Serializes users."""

    birth_date = DateField(source="profile.birth_date")
    gender = CharField(source="profile.gender")
    country = CharField(source="profile.country")
    postal_code = CharField(source="profile.postal_code")
    street_address = CharField(source="profile.street_address")
    phone_number = CharField(source="profile.phone_number")
    membership_years = CharField(source="profile.membership_years")
    is_member = BooleanField(source="profile.is_member")

    class Meta:
        model = User
        fields = ("id",
                  "subject_id",
                  "username",
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


class PublicProfileUserSerializer(ModelSerializer):
    """Serializes public user info."""

    class Meta:
        model = User
        fields = ("username", "pretty_username")
