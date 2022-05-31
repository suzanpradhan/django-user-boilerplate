from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from safedelete.models import SafeDeleteModel


class GenderChoices(models.TextChoices):
    MALE = "MALE", _("Male")
    FEMALE = "FEMALE", _("Female")
    OTHER = "OTHER", _("Other")
    UNKNOWN = "UNKNOWN", _("Unknown")


class BaseUser(AbstractBaseUser, SafeDeleteModel):

    class Meta:
        abstract = True
    USERNAME_FIELD = 'email_address'
    EMAIL_FIELD = 'email_address'
    REQUIRED_FIELDS = []
    email = models.EmailField(_("Email Address"), unique=True, blank=False, null=False, error_messages={
        'unique': _("A user with that email already exists."),
    })
    first_name = models.CharField(max_length=64, null=True, blank=True)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    is_staff = models.BooleanField(default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_superuser = models.BooleanField(default=False,
                                       help_text=_('Designates whether this user has all permissions without explicitly assigning them.'))
    gender = models.CharField(
        max_length=7, choices=GenderChoices.choices, null=True
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        blank=False,
        null=False,
    )
    deactivated_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class UserStatusChoice(models.TextChoices):
        PENDING = _("Pending")
        ACTIVE = _("Active")
        INACTIVE = _("Inactive")
        REMOVED = _("Removed")

    status = models.CharField(
        max_length=8,
        choices=UserStatusChoice.choices,
        default=UserStatusChoice.INACTIVE,
    )

    def delete(self, *args, **kwargs):
        self.status = BaseUser.UserStatusChoice.REMOVED
        super().delete(*args, **kwargs)

    def undelete(self, *args, **kwargs):
        self.status = BaseUser.UserStatusChoice.ACTIVE
        super().undelete(*args, **kwargs)

    def __str__(self) -> str:
        return self.email
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"