# -*- coding: utf-8 -*-

import re
from datetime import datetime

from django.contrib.auth.models import Group
from django.core.exceptions import ImproperlyConfigured

from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from apps.user.models import User, UserProfile


class OidcAuthBackend(OIDCAuthenticationBackend):

    membership_years_regex = re.compile(r"^([0-9]{4},)*([0-9]{4})?$")

    def filter_users_by_claims(self, claims):
        uuid = self.get_claim(claims, "sub")
        if not uuid:
            return User.objects.none()
        try:
            return User.objects.filter(uuid=uuid)
        except User.DoesNotExist:
            return User.objects.none()

    def create_user(self, claims):
        uuid = self.get_claim(claims, "sub")
        username = self.get_claim(claims, "username")
        user = User.objects.create_user(uuid=uuid, username=username)
        UserProfile.objects.create(user=user)
        return self.update_user(user, claims)

    def update_user(self, user, claims):
        # Update user
        user.username = self.get_claim(claims, "username")
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

        # Reset statuses and group memberships
        user.is_staff = False
        user.is_superuser = False
        user.groups.clear()
        user.profile.membership_years = None
        user.profile.is_member = False

        # Update group memberships and inherited statuses
        groups = self.get_claim(claims, "groups")
        # TMP set superuser group in config
        if "supermen" in groups:
            user.is_staff = True
            user.is_superuser = True

        # TMP don't add groups automatically
        for group in groups:
            g, created = Group.objects.get_or_create(name=group)
            user.groups.add(g)

        (membership_years, is_member) = self.get_membership_years(claims, "membership_years")
        user.profile.membership_years = membership_years
        user.profile.is_member = is_member

        user.save()
        user.profile.save()

        return user

    @classmethod
    def get_membership_years(cls, claims, key, year=datetime.today().strftime("%Y")):
        membership_years = cls.get_claim(claims, key)
        if not cls.membership_years_regex.match(membership_years):
            raise ImproperlyConfigured("Invalid membership years: " + membership_years)
        is_member = False
        if len(membership_years) > 0:
            fragments = membership_years.split(",")
            is_member = year in fragments
        return membership_years, is_member

    @staticmethod
    def get_claim(claims, key):
        value = claims.get(key)
        if value is None:
            raise ImproperlyConfigured("Missing claim: " + key)
        return value
