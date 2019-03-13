from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth.models import Group


class FredOIDCAB(OIDCAuthenticationBackend):

    def create_user(self, claims):
        user = super(FredOIDCAB, self).create_user(claims)

        user.first_name = claims.get('first_name', '')
        user.last_name = claims.get('last_name', '')
        user.username = claims.get('preferred_username', '')

        groups = claims.get('groups', [])

        if 'supermen' in groups:
            user.is_superuser = True

        for group in groups:
            g, created = Group.objects.get_or_create(name=group)
            user.groups.add(g)

        user.save()

        return user

    def update_user(self, user, claims):
        return user
