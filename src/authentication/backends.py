import re
from datetime import datetime

from django.contrib.auth.models import Group
from django.core.exceptions import SuspiciousOperation

from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from .models import GroupExtension, User, UserProfile


class OidcAuthBackend(OIDCAuthenticationBackend):

    username_regex = re.compile(r"^[a-z0-9_]+$")
    username_min_length = 3
    username_max_length = 25
    membership_years_regex = re.compile(r"^([0-9]{4},)*([0-9]{4})?$")

    def filter_users_by_claims(self, claims):
        subject_id = self.get_claim(claims, "sub")
        try:
            return User.objects.filter(subject_id=subject_id)
        except User.DoesNotExist:
            return User.objects.none()

    def create_user(self, claims):
        # Check if provided user attributes are okay first
        attributes = self.decode_attributes(claims)
        self.validate_attributes(attributes)

        user = User.objects.create(subject_id=attributes["subject_id"],
                                   username=attributes["username"],
                                   email=attributes["email"])
        UserProfile.objects.create(user=user)

        return self.update_user(user, claims, attributes)

    def update_user(self, user, claims, attributes=None):
        # Check if provided user attributes are okay first, if not already checked
        if attributes is None:
            attributes = self.decode_attributes(claims)
            self.validate_attributes(attributes)

        # Update user and userprofile
        user.username = attributes["username"]
        user.pretty_username = attributes["pretty_username"]
        user.first_name = attributes["first_name"]
        user.last_name = attributes["last_name"]
        user.email = attributes["email"]
        user.profile.birth_date = attributes["birth_date"]
        user.profile.gender = attributes["gender"]
        user.profile.phone_number = attributes["phone_number"]
        user.profile.country = attributes["country"]
        user.profile.postal_code = attributes["postal_code"]
        user.profile.street_address = attributes["street_address"]
        user.profile.membership_years = attributes["membership_years"]
        user.profile.is_member = attributes["is_member"]

        # Update groups and statuses
        user.groups.clear()
        is_staff = False
        is_superuser = False
        is_active = False
        group_names = attributes["groups"]
        for group_name in group_names:
            try:
                group = Group.objects.get(name=group_name)
                group_ext = GroupExtension.objects.get(group=group)
                user.groups.add(group)
                is_superuser = is_superuser or group_ext.is_superuser
                is_staff = is_staff or group_ext.is_staff
                is_active = is_active or group_ext.is_active
            except Group.DoesNotExist:
                continue
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = is_active

        # All okay, save
        user.save()
        user.profile.save()

        return user

    @classmethod
    def decode_attributes(cls, claims):
        attributes = {}

        attributes["subject_id"] = cls.get_claim(claims, "sub")
        attributes["username"] = cls.get_claim(claims, "username").lower()
        attributes["pretty_username"] = cls.get_claim(claims, "pretty_username")
        attributes["first_name"] = cls.get_claim(claims, "given_name")
        attributes["last_name"] = cls.get_claim(claims, "family_name")
        attributes["email"] = cls.get_claim(claims, "email")
        attributes["birth_date"] = cls.get_claim(claims, "birth_date")
        attributes["gender"] = cls.get_claim(claims, "gender")
        attributes["phone_number"] = cls.get_claim(claims, "phone_number")

        address_claims = cls.get_claim(claims, "address", expected_type=dict)
        attributes["country"] = cls.get_claim(address_claims, "country")
        attributes["postal_code"] = cls.get_claim(address_claims, "postal_code")
        attributes["street_address"] = cls.get_claim(address_claims, "street_address")

        (membership_years, is_member) = cls.decode_membership_years(claims, "membership_years")
        attributes["membership_years"] = membership_years
        attributes["is_member"] = is_member

        groups = cls.get_claim(claims, "groups", expected_type=list)
        attributes["groups"] = groups

        return attributes

    @classmethod
    def validate_attributes(cls, attributes):
        # Verify username and pretty_username
        if not cls.username_regex.match(attributes["username"]):
            raise SuspiciousOperation("Invalid username format")
        if len(attributes["username"]) < cls.username_min_length:
            raise SuspiciousOperation("Username too short")
        if len(attributes["username"]) > cls.username_max_length:
            raise SuspiciousOperation("Username too long")
        if attributes["pretty_username"].lower() != attributes["username"]:
            raise SuspiciousOperation("Pretty username doesn't match username")

    @classmethod
    def decode_membership_years(cls, claims, key, year=datetime.today().strftime("%Y")):
        membership_years = cls.get_claim(claims, key, allow_empty=True)
        if not cls.membership_years_regex.match(membership_years):
            raise SuspiciousOperation("Invalid membership years format: " + membership_years)
        is_member = False
        if len(membership_years) > 0:
            fragments = membership_years.split(",")
            is_member = year in fragments
        return membership_years, is_member

    @staticmethod
    def get_claim(claims, key, allow_empty=False, expected_type=str):
        value = claims.get(key)
        if value is None:
            raise SuspiciousOperation("Claim '" + key + "' is missing")
        if value == "" and not allow_empty:
            raise SuspiciousOperation("Claim '" + key + "' is empty")
        if value != "" and not isinstance(value, expected_type):
            raise SuspiciousOperation("Claim '" + key + "' is not a " + str(expected_type) + " but a " + str(type(value)))
        return value
