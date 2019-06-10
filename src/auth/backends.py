# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group

from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from apps.userprofile.models import UserProfile


class OidcAuthBackend(OIDCAuthenticationBackend):

    def create_user(self, claims):
        user = super(OidcAuthBackend, self).create_user(claims)

        return self.update_user(user, claims)

    def update_user(self, user, claims):
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.username = claims.get("preferred_username", "")
        user.email = claims.get("email", "")

        groups = claims.get("groups", [])

        if "supermen" in groups:
            user.is_staff = True
            user.is_superuser = True

        for group in groups:
            g, created = Group.objects.get_or_create(name=group)
            user.groups.add(g)

        user.save()

        address = claims.get("address", {})

        profile_data = {
            "nick": claims.get("preferred_username", ""),
            "date_of_birth": claims.get("birthdate", ""),
            "phone": claims.get("phone_number", ""),
            "address": address["street_address"],
            "zip_code": address["postal_code"],
        }

        UserProfile.objects.update_or_create(user=user, defaults=profile_data)

        return user
