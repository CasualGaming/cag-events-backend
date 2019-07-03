from drf_dynamic_fields import DynamicFieldsMixin

from rest_framework.serializers import BaseSerializer, BooleanField, CharField, DateField, HyperlinkedModelSerializer, StringRelatedField

from authentication.models import User


class UsernameUserSerializer(BaseSerializer):
    """Serializes user to a username string."""

    def to_representation(self, instance):
        return instance.username


class UserSerializer(DynamicFieldsMixin, HyperlinkedModelSerializer):
    """Serializes users based on which fields the current user has permission to view."""

    groups = StringRelatedField(many=True)
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
        fields = [
            "url",
            "id",
            "subject_id",
            "username",
            "pretty_username",
            "first_name",
            "last_name",
            "email",
            "groups",
            "birth_date",
            "gender",
            "country",
            "postal_code",
            "street_address",
            "phone_number",
            "membership_years",
            "is_member",
        ]
        extra_kwargs = {
            "url": {
                "view_name": "user-detail",
                "lookup_field": "username",
            },
        }

    @property
    def fields(self):
        fields = super(UserSerializer, self).fields
        allowed_fields = self.get_allowed_fields()
        for field in set(fields.keys()):
            if field not in allowed_fields:
                fields.pop(field, None)
        return fields

    def get_allowed_fields(self):
        allowed_fields = []
        request = self.context["request"]
        is_detail = isinstance(self.instance, User)
        is_self = is_detail and self.instance == request.user

        # Public fields
        allowed_fields += [
            "url",
            "username",
            "pretty_username",
        ]

        # Basic fields
        if request.user.has_perm("authentication.user.view_basic") or is_self:
            allowed_fields += [
                "id",
                "subject_id",
                "first_name",
                "last_name",
                "email",
                "groups",
                "birth_date",
                "gender",
                "phone_number",
                "membership_years",
                "is_member",
            ]

        # Address fields
        if request.user.has_perm("authentication.user.view_address") or is_self:
            allowed_fields += [
                "country",
                "postal_code",
                "street_address",
            ]

        return allowed_fields
