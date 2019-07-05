from drf_dynamic_fields import DynamicFieldsMixin

from rest_framework.serializers import BaseSerializer, BooleanField, CharField, DateField, HyperlinkedModelSerializer, IntegerField, StringRelatedField

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
    is_age_public = BooleanField(source="profile.is_age_public")
    is_gender_public = BooleanField(source="profile.is_gender_public")
    public_age = IntegerField(source="profile.public_age")
    public_gender = CharField(source="profile.public_gender")

    class Meta:
        model = User
        _public_fields = [
            "url",
            "username",
            "pretty_username",
            "public_name",
            "public_age",
            "public_gender",
        ]
        _basic_fields = [
            "id",
            "subject_id",
            "first_name",
            "last_name",
            "email",
            "groups",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_deleted",
            "join_date",
            "delete_date",
            "last_login",
            "birth_date",
            "gender",
            "phone_number",
            "membership_years",
            "is_member",
            "is_name_public",
            "is_age_public",
            "is_gender_public",
        ]
        _address_fields = [
            "country",
            "postal_code",
            "street_address",
        ]
        fields = _public_fields + _basic_fields + _address_fields
        extra_kwargs = {
            "url": {
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

        allowed_fields += self.Meta._public_fields

        if request.user.has_perm("authentication.user.view_basic") or is_self:
            allowed_fields += self.Meta._basic_fields

        if request.user.has_perm("authentication.user.view_address") or is_self:
            allowed_fields += self.Meta._address_fields

        return allowed_fields
