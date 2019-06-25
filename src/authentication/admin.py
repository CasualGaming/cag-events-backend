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
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_superuser", "is_active", "date_joined", "last_login")
    list_filter = ("groups", "is_staff", "is_superuser", "is_active")
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
    search_fields = ("name",)
    ordering = ("name",)
    filter_horizontal = ("permissions",)
