from django.contrib.admin import StackedInline, register, site
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.forms import ValidationError

from common.admin import NoDeleteInline

from .models import GroupExtension, User, UserProfile


class UserProfileInline(StackedInline):
    model = UserProfile
    formset = NoDeleteInline


class ImmutableUserChangeForm(UserChangeForm):
    def clean(self):
        raise ValidationError("Users can not be changed locally.")


class ImmutableUserCreationForm(UserCreationForm):
    def clean(self):
        raise ValidationError("Users can not be created locally.")


class ImmutableAdminPasswordChangeForm(AdminPasswordChangeForm):
    def clean(self):
        raise ValidationError("Users can not be changed locally.")


@register(User)
class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ["username", "email", "first_name", "last_name", "is_staff", "is_superuser", "is_active", "date_joined", "last_login"]
    list_filter = ["groups", "is_staff", "is_superuser", "is_active"]
    form = ImmutableUserChangeForm
    add_form = ImmutableUserCreationForm
    change_password_form = ImmutableAdminPasswordChangeForm


class GroupExtensionInline(StackedInline):
    model = GroupExtension
    formset = NoDeleteInline


site.unregister(Group)


@register(Group)
class GroupExtensionAdmin(GroupAdmin):
    inlines = (GroupExtensionInline,)
    list_display = ["name", "description", "is_staff", "is_superuser", "is_active"]
    list_filter = ["extension__is_staff", "extension__is_superuser", "extension__is_active"]
    ordering = ["name"]

    def description(self, obj):
        return obj.extension.description
    description.short_description = "Description"
    description.admin_order_field = "extension__description"

    def is_staff(self, obj):
        return obj.extension.is_staff
    is_staff.short_description = "Is staff"
    is_staff.admin_order_field = "extension__is_staff"
    is_staff.boolean = True

    def is_superuser(self, obj):
        return obj.extension.is_superuser
    is_superuser.short_description = "Is superuser"
    is_superuser.admin_order_field = "extension__is_superuser"
    is_superuser.boolean = True

    def is_active(self, obj):
        return obj.extension.is_active
    is_active.short_description = "Is active"
    is_active.admin_order_field = "extension__is_active"
    is_active.boolean = True
