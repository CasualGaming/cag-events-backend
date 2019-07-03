from threading import Lock

from django.contrib.auth.models import Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Group


_has_run_migration_listener = False
_sync_group_lock = Lock()


@receiver(post_migrate)
def migration_listener(*args, **kwargs):
    """Make sure permissions are recalculated and reapplied if any migrations were performed."""
    global _has_run_migration_listener
    if _has_run_migration_listener:
        return
    _has_run_migration_listener = True

    sync_groups()


def sync_groups():
    """Update all groups and their users."""
    for group in Group.objects.all():
        sync_group(group)


def sync_group(group):
    """
    Update a group and it's users.
    Does nothing if it detects recursion, like when updating perms triggers it recursively.
    Not thread safe.
    """
    if _sync_group_lock.acquire(blocking=False):
        try:
            sync_group_permissions(group)
            sync_group_users(group)
        finally:
            _sync_group_lock.release()


def sync_group_permissions(group):
    """
    Process permissions.
    Includes resolving wildcard permissions to specific ones within the same content type/model.
    """
    new_perms = set()
    for perm in group.permissions.all():
        codename = perm.codename
        parts = codename.rsplit(".", 1)
        last_part = parts[-1]

        # Ignore non-wildcard perms
        if last_part != "*":
            continue

        has_prefix = len(parts) > 1
        if has_prefix:
            prefix = parts[0] + "."
        else:
            prefix = ""

        for ct_perm in Permission.objects.filter(content_type=perm.content_type):
            if not has_prefix or ct_perm.codename.startswith(prefix):
                new_perms.add(ct_perm)

    group.permissions.add(*new_perms)


def sync_group_users(group):
    """Reapply group permissions and statuses to all users in a modified group."""
    for user in group.user_set.all():
        sync_user_groups(user)


def sync_user_groups(user, save=True):
    """
    Reapply group permissions and statuses to user using all its groups.
    """
    is_superuser = False
    is_staff = False
    is_active = False
    for group in user.groups.all():
        group_ext = group.extension
        is_active = is_active or group_ext.is_active
        is_staff = is_staff or group_ext.is_staff
        is_superuser = is_superuser or group_ext.is_superuser
    user.is_superuser = is_superuser
    user.is_staff = is_staff
    user.is_active = is_active

    if save:
        user.save()
