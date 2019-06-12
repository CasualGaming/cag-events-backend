# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group
from django.core.exceptions import ImproperlyConfigured

from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from apps.user.models import User, UserProfile


class OidcAuthBackend(OIDCAuthenticationBackend):

    def filter_users_by_claims(self, claims):
        uuid = get_claim(claims, "sub")
        if not uuid:
            return User.objects.none()
        try:
            return User.objects.filter(uuid=uuid)
        except User.DoesNotExist:
            return User.objects.none()

    def create_user(self, claims):
        uuid = get_claim(claims, "sub")
        username = get_claim(claims, "username")
        user = User.objects.create_user(uuid=uuid, username=username)
        UserProfile.objects.create(user=user)
        return self.update_user(user, claims)

    def update_user(self, user, claims):
        # Update user
        user.username = get_claim(claims, "username")
        user.first_name = get_claim(claims, "given_name")
        user.last_name = get_claim(claims, "family_name")
        user.email = get_claim(claims, "email")

        # Update user profile
        user.profile.birth_date = get_claim(claims, "birth_date")
        user.profile.gender = get_claim(claims, "gender")
        user.profile.phone_number = get_claim(claims, "phone_number")
        address_claims = get_claim(claims, "address")
        user.profile.country = get_claim(address_claims, "country")
        user.profile.postal_code = get_claim(address_claims, "postal_code")
        user.profile.street_address = get_claim(address_claims, "street_address")

        # Reset statuses and group memberships
        user.is_staff = False
        user.is_superuser = False
        user.groups.clear()

        # Update group memberships and inherited statuses
        groups = get_claim(claims, "groups")
        # TMP set superuser group in config
        if "supermen" in groups:
            user.is_staff = True
            user.is_superuser = True
        # TMP don't add groups automatically
        for group in groups:
            g, created = Group.objects.get_or_create(name=group)
            user.groups.add(g)

        user.save()
        user.profile.save()

        return user


def get_claim(claims, key):
    value = claims.get(key)
    if value is None:
        raise ImproperlyConfigured("Missing claim: " + key)
    return value
