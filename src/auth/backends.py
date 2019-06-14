import re
from datetime import datetime

from django.contrib.auth.models import Group
from django.core.exceptions import SuspiciousOperation

from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from apps.user.models import GroupExtension, User, UserProfile


class OidcAuthBackend(OIDCAuthenticationBackend):

    username_regex = re.compile(r"^[a-z0-9_]+$")
    membership_years_regex = re.compile(r"^([0-9]{4},)*([0-9]{4})?$")

    def filter_users_by_claims(self, claims):
        subject_id = self.get_claim(claims, "sub")
        try:
            return User.objects.filter(subject_id=subject_id)
        except User.DoesNotExist:
            return User.objects.none()

    def create_user(self, claims):
        subject_id = self.get_claim(claims, "sub")
        username = self.get_claim(claims, "username")
        email_address = self.get_claim(claims, "email")
        user = User.objects.create_user(subject_id=subject_id, username=username, email=email_address)
        UserProfile.objects.create(user=user)
        return self.update_user(user, claims)

    def update_user(self, user, claims):
        # Update user
        lower_username = self.get_claim(claims, "username").lower()
        user.username = lower_username
        user.pretty_username = self.get_claim(claims, "pretty_username")
        user.first_name = self.get_claim(claims, "given_name")
        user.last_name = self.get_claim(claims, "family_name")
        user.email = self.get_claim(claims, "email")

        # Update user profile
        user.profile.birth_date = self.get_claim(claims, "birth_date")
        user.profile.gender = self.get_claim(claims, "gender")
        user.profile.phone_number = self.get_claim(claims, "phone_number")
        address_claims = self.get_claim(claims, "address")
        user.profile.country = self.get_claim(address_claims, "country")
        user.profile.postal_code = self.get_claim(address_claims, "postal_code")
        user.profile.street_address = self.get_claim(address_claims, "street_address")

        # Update groups and statuses
        user.groups.clear()
        is_staff = False
        is_superuser = False
        is_active = False
        group_names = self.get_claim(claims, "groups")
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

        # Update membership years and status
        (membership_years, is_member) = self.get_membership_years(claims, "membership_years")
        user.profile.membership_years = membership_years
        user.profile.is_member = is_member

        # Validate
        if not self.username_regex.match(user.username):
            raise SuspiciousOperation("Invalid username")
        if user.username.lower() != user.username:
            raise SuspiciousOperation("Invalid pretty username")

        user.save()
        user.profile.save()

        return user

    @classmethod
    def get_membership_years(cls, claims, key, year=datetime.today().strftime("%Y")):
        membership_years = cls.get_claim(claims, key)
        if not cls.membership_years_regex.match(membership_years):
            raise SuspiciousOperation("Invalid membership years: " + membership_years)
        is_member = False
        if len(membership_years) > 0:
            fragments = membership_years.split(",")
            is_member = year in fragments
        return membership_years, is_member

    @staticmethod
    def get_claim(claims, key):
        value = claims.get(key)
        if value is None:
            raise SuspiciousOperation("Missing claim: " + key)
        return value
