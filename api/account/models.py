import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import crypto
from django.utils.translation import ugettext_lazy as _

from account import managers


def random_token():
    """
    Get a random token with 32 characters.

    Returns:
        A cryptographically secure random string of 32 characters.
    """
    return crypto.get_random_string(32)


class Email(models.Model):
    """
    An email address owned by a user.
    """
    address = models.EmailField(
        help_text=_('The addr-spec of the email as defined in RFC 5322.'),
        unique=True,
        verbose_name=_('address'),
    )
    id = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        help_text=_('A unique identifier for the email.'),
        primary_key=True,
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=_('A boolean indicating if the ownership of the email has '
                    'been verified.'),
        verbose_name=_('is verified'),
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
    user = models.ForeignKey(
        'account.User',
        help_text=_('The user who owns the email address.'),
        on_delete=models.CASCADE,
        related_name='emails',
        related_query_name='email',
        verbose_name=_('user'),
    )

    class Meta:
        ordering = ('time_created',)
        verbose_name = _('email address')
        verbose_name_plural = _('email addresses')

    @staticmethod
    def normalize_address(address: str):
        """
        Normalize the email address as specified in RFC 5322.

        Specifically, the domain portion of the email address is
        lower-cased as it is case insensitive. This method modifies the
        email address it is called on in place.

        Args:
            address:
                The email address to normalize.

        Returns:
            The normalized address.
        """
        local_part, domain = address.split('@')

        return f'{local_part}@{domain.lower()}'

    def __str__(self):
        """
        Get a string representation of the object.

        Returns:
            The email's address and ID.
        """
        return f'{self.address} ({self.id})'

    def save(self, *args, **kwargs):
        """
        Save the email address.

        Before inserting into the database, the email is normalized.
        """
        self.address = self.normalize_address(self.address)

        super().save(*args, **kwargs)


class EmailVerification(models.Model):
    """
    A token used to verify an email address.
    """
    email = models.ForeignKey(
        'account.Email',
        help_text=_('The email instance the verification is tied to.'),
        on_delete=models.CASCADE,
        related_name='verifications',
        related_query_name='verification',
        verbose_name=_('email address'),
    )
    time_created = models.DateTimeField(
        auto_now_add=True,
        help_text=_('The time the instance was created at.'),
        verbose_name=_('time created'),
    )
    token = models.CharField(
        default=random_token,
        editable=False,
        help_text=_('The token used to verify the associated email.'),
        max_length=32,
        verbose_name=_('token'),
    )

    class Meta:
        ordering = ('time_created',)
        verbose_name = _('email verification')
        verbose_name_plural = _('email verifications')

    def __repr__(self):
        """
        Get a string representation of the instance.

        Returns:
            A string containing the instance's ID and the email address
            it is associated with.
        """
        return (f'EmailVerification(id={self.id}, '
                f'email_address="{self.email.address}")')

    def __str__(self):
        """
        Get a string describing the instance.

        Returns:
            A string indicating which email address the verification is
            associated with.
        """
        return f'Email Verification for {self.email.address}'

    def verify(self):
        """
        Verify the associated email address.
        """
        self.email.is_verified = True
        self.email.save()

        self.delete()


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
    primary_email = models.ForeignKey(
        'account.Email',
        blank=True,
        help_text=_("The user's primary email address."),
        null=True,
        on_delete=models.SET_NULL,
        # No backwards relationship
        related_name='+',
        verbose_name=_('primary email address'),
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

    # Use our custom manager
    objects = managers.UserManager()

    class Meta:
        ordering = ('time_created',)
        verbose_name = _('user')
        verbose_name_plural = _('users')
