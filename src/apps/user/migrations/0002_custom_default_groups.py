# DO NOT DELETE
# Custom data migration for adding default groups

from django.db import migrations


def add_default_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")  # noqa: N806 (var not lower-case)
    GroupExtension = apps.get_model("user", "GroupExtension")  # noqa: N806 (var not lower-case)

    user_group = Group.objects.create(name="user")
    user_group_extension = GroupExtension.objects.create(
        group=user_group, is_superuser=False, is_staff=False, is_active=True)
    user_group.save()
    user_group_extension.save()

    admin_group = Group.objects.create(name="admin")
    admin_group_extension = GroupExtension.objects.create(
        group=admin_group, is_superuser=True, is_staff=True, is_active=True)
    admin_group.save()
    admin_group_extension.save()


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_default_groups),
    ]
