import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(PermissionsMixin, AbstractBaseUser):
    """
    Model representing a single user.
    """
    USERNAME_FIELD = 'name'

    id = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        help_text=_('A unique identifier for the user.'),
        primary_key=True,
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_('A boolean indicating if the user should be allowed to '
                    'perform actions on the site.'),
        verbose_name=_('is active'),
    )
    is_staff = models.BooleanField(
        default=False,
        help_text=_('A boolean indicating if the user is allowed to access '
                    'the admin interface.'),
        verbose_name=_('is staff'),
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text=_('A boolean indicating if the user should have all '
                    'permissions without them being explicitly granted.'),
        verbose_name=_('is superuser'),
    )
    name = models.CharField(
        help_text=_('A name to publicly identify the user.'),
        max_length=127,
        verbose_name=_('name'),
    )
    time_created = models.DateTimeField(
        auto_now_add=True,
        help_text=_('The time the user was created.'),
        verbose_name=_('time created'),
    )
    time_updated = models.DateTimeField(
        auto_now=True,
        help_text=_('The last time the user was edited.'),
        verbose_name=_('time updated'),
    )

    class Meta:
        ordering = ('time_created',)
        verbose_name = _('user')
        verbose_name_plural = _('users')
