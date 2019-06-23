from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.forms import ValidationError, models

from .models import GroupExtension, User, UserProfile


class NoDeleteInline(models.BaseInlineFormSet):
    """
    Custom formset to prevent deletion.
    Used by the inline for userprofiles to prevent the possibility
    of deleting the profile object.
    """
    def __init__(self, *args, **kwargs):
        super(NoDeleteInline, self).__init__(*args, **kwargs)
        self.can_delete = False


class UserProfileInline(admin.StackedInline):
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


@admin.register(User)
class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_superuser", "is_active", "date_joined", "last_login")
    list_filter = ("groups", "is_staff", "is_superuser", "is_active")
    filter_horizontal = ("groups",)
    form = ImmutableUserChangeForm
    add_form = ImmutableUserCreationForm
    change_password_form = ImmutableAdminPasswordChangeForm


class GroupExtensionInline(admin.StackedInline):
    model = GroupExtension
    formset = NoDeleteInline


admin.site.unregister(Group)


@admin.register(Group)
class GroupExtensionAdmin(GroupAdmin):
    inlines = (GroupExtensionInline,)
    search_fields = ("name",)
    ordering = ("name",)
    filter_horizontal = ("permissions",)
