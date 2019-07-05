from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import BooleanField, CASCADE, CharField, DateField, DateTimeField, EmailField, Model, OneToOneField, Q, UUIDField
from django.db.models.constraints import CheckConstraint
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.utils import timezone

from authentication.group_sync import sync_group


# TODO mark for deletion admin panel action and view


class UserManager(BaseUserManager):
    """
    Model manager for the surrogate user model.
    """

    def create_user(self, username, email, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Surrogate user model. Does not use password and has extra fields.
    All information is received from the authentication backend (like OpenID Connect),
    or is inherited from the user's groups.
    """

    # Fields from auth backend
    subject_id = UUIDField("subject id", unique=True, db_index=True)
    username = CharField("username", unique=True, db_index=True, max_length=50)
    pretty_username = CharField("pretty username", unique=True, max_length=50, help_text="Same as the username, but allows different letter cases.")
    first_name = CharField("first name", max_length=50, blank=True)
    last_name = CharField("last name", max_length=50, blank=True)
    email = EmailField("email address", blank=True)

    # Fields from groups
    is_staff = BooleanField("staff status", default=False, help_text="If the user can use the admin panel.")
    is_active = BooleanField("active status", default=False, help_text="If the user can log into the site.")
    # is_superuser in PermissionsMixin

    # Special fields
    join_date = DateTimeField("date joined", default=timezone.now, editable=False)
    # Make sure this is not unset or accidentally changed
    delete_date = DateTimeField("date joined", null=True, blank=True, help_text="When the user was marked for deletion.")

    # Privacy fields
    is_name_public = BooleanField("is name public", default=False, help_text="If the user's name is public.")
    is_seat_user_public = BooleanField("is seat user public", default=False, help_text="If the user will show publicly on seats it's assigned to.")

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        constraints = [
            CheckConstraint(check=~(Q(is_active=True) & ~Q(delete_date=None)), name="user_user_not_both_active_and_deleted"),
        ]
        default_permissions = ["view"]

    def clean(self):
        self.email = self.__class__.objects.normalize_email(self.email)
        if self.is_active and self.is_deleted:
            raise ValidationError("Deleted user cannot be activated.")

    # Required
    def get_full_name(self):
        """
        Return the combined full name.
        """
        full_name = "{0} {1}".format(self.first_name, self.last_name)
        return full_name.strip()

    # Required
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    # Required
    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_deleted(self):
        return self.deleted_date

    @property
    def public_name(self):
        """The full name if it's public, else NULL."""
        return self.get_full_name() if self.is_name_public else None

    @property
    def public_seat_user(self):
        """This user if it allows being shown in its seats, else NULL."""
        return self if self.is_seat_user_public else None

    def delete(self):
        self.is_active = False
        self.delete_date = timezone.now


class UserProfile(Model):
    """
    Contains user information not related to authentication.
    It is automatically created for a user when the user is created, and deleted when the user is deleted.
    Like the user, all information is received from the authentication backend (like OpenID Connect),
    or is inherited from the user's groups.
    """
    user = OneToOneField(User, verbose_name="user", primary_key=True, related_name="profile", on_delete=CASCADE)

    # Fields from auth backend
    birth_date = DateField("date of birth", null=True, blank=True)
    gender = CharField("gender", null=True, blank=True, max_length=20)
    phone_number = CharField("phone number", null=True, blank=True, max_length=20)
    country = CharField("country", null=True, blank=True, max_length=50)
    postal_code = CharField("postal code", null=True, blank=True, max_length=10)
    street_address = CharField("street address", null=True, blank=True, max_length=100)
    membership_years = CharField("membership years", null=True, blank=True, max_length=500,
                                 help_text="Comma separated list of years the user has been a member of the organization.")
    is_member = BooleanField("membership status", default=False, help_text="If the user is currently a member of the organization.")

    # Privacy fields
    is_age_public = BooleanField("is age public", default=False, help_text="If the user's age in years is public.")
    is_gender_public = BooleanField("is gender public", default=False, help_text="If the user's gender is public.")

    class Meta:
        default_permissions = ["view", "change"]

    def __str__(self):
        return self.user.username

    @property
    def has_address(self):
        """If a full address (valid or not) is set."""
        return self.country and self.street_address and self.postal_code

    @property
    def public_age(self):
        """The age in years if that is public, otherwise NULL."""
        return (timezone.now() - self.birth_date).years if self.is_age_public else None

    @property
    def public_gender(self):
        """The gender if that is public, otherwise NULL."""
        return self.gender if self.is_gender_public else None


class GroupExtension(Model):
    """
    Contains more group information, since Django groups cannot be (easily) substituted.
    It is automatically created for a group when the group is created, and deleted when the group is deleted.
    """
    group = OneToOneField(Group, verbose_name="group", primary_key=True, related_name="extension", on_delete=CASCADE)
    description = CharField("description", max_length=50, blank=True)
    is_superuser = BooleanField("superuser status", default=False, help_text="If users have every permission.")
    is_staff = BooleanField("staff status", default=False, help_text="If users can log into the admin panel.")
    is_active = BooleanField("active status", default=False, help_text="If users can log into the site.")

    class Meta:
        default_permissions = ["view", "change"]

    def __str__(self):
        return self.group.name


class Permissions(Model):
    class Meta:
        managed = False
        default_permissions = []
        permissions = [
            ("*", "Authentication app admin"),
            ("user.*", "User admin"),
            ("user.list", "List users"),
            ("user.view_basic", "View users' non-address info"),
            ("user.view_address", "View users' address"),
            ("user.delete", "Delete users"),
            ("group.*", "Group admin"),
            ("group.list", "List groups"),
            ("group.create", "Add groups"),
            ("group.change", "Change groups"),
            ("group.delete", "Delete groups"),
        ]


@receiver(m2m_changed, sender=Group.permissions.through)
def sync_group_from_group_permissions_change(sender, instance, action, **kwargs):
    accepted_actions = ["post_add", "post_remove", "post_clear"]
    if action not in accepted_actions:
        return

    sync_group(instance)


@receiver(post_save, sender=GroupExtension)
def sync_group_from_group_extension_save(sender, instance, **kwargs):
    sync_group(instance.group)
